"""Measure retrieval quality: is the expected doc in the top-k chunks for each question?"""
import json
import sys

from config import TOP_K
from rag import search


def main():
    cases = json.load(open("eval/questions.json"))
    passed, reciprocal = 0, 0.0
    for c in cases:
        sources = [h["source"] for h in search(c["question"])]
        rank = sources.index(c["expected_source"]) + 1 if c["expected_source"] in sources else None
        passed += rank is not None
        reciprocal += 1 / rank if rank else 0
        print(f"{'PASS' if rank else 'FAIL'}  rank={rank}  {c['question']}")
    recall, mrr = passed / len(cases), reciprocal / len(cases)
    print(f"\nRecall@{TOP_K}: {recall:.0%}   MRR: {mrr:.2f}   ({passed}/{len(cases)})")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
