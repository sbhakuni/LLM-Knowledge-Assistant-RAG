import argparse

from rag import answer, search


def show_sources(hits):
    print("\nSources:")
    for n, h in enumerate(hits, 1):
        print(f"  [{n}] {h['source']} > {h['section']}  {h['url']}")


def ask(question, doc_type, no_llm):
    if no_llm:
        for n, h in enumerate(search(question, doc_type=doc_type), 1):
            print(f"\n[{n}] {h['source']} > {h['section']} (distance {h['distance']:.3f})")
            print(h["text"][:400])
        return
    text, hits = answer(question, doc_type)
    print(f"\n{text}")
    show_sources(hits)


def main():
    p = argparse.ArgumentParser(description="Ask the knowledge assistant.")
    p.add_argument("question", nargs="?", help="omit for interactive mode")
    p.add_argument("--type", dest="doc_type", help="filter by doc type, e.g. runbooks")
    p.add_argument("--no-llm", action="store_true", help="only show retrieved chunks")
    args = p.parse_args()

    if args.question:
        ask(args.question, args.doc_type, args.no_llm)
        return
    while (q := input("\nQuestion (empty to quit): ").strip()):
        ask(q, args.doc_type, args.no_llm)


if __name__ == "__main__":
    main()
