# LLM Knowledge Assistant (RAG)

Small RAG assistant that answers developer and production-support questions from technical docs, with citations.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # add your LLM key (OpenAI or local Ollama)

python fetch_docs.py            # download public docs listed in data/sources.json
python ingest.py                # index new/changed/deleted docs only
python ask.py "How do I debug a pod stuck in Pending?"
python ask.py --no-llm "..."    # retrieval only, no LLM key needed
python ask.py --type jenkins    # interactive mode, filtered by doc type
python eval.py                  # retrieval quality: Recall@5 and MRR on eval/questions.json
```

## Updating docs
- Add your own Markdown files under `data/docs/<doc_type>/` (e.g. `runbooks/`, `troubleshooting/`).
- Add more public pages to `data/sources.json` and re-run `fetch_docs.py`.
- Run `ingest.py` again: unchanged files are skipped, edited or deleted files are re-indexed or removed.

## Layout
`fetch_docs.py` (download) -> `ingest.py` (chunk by heading, embed, store in Chroma) -> `rag.py` (retrieve, prompt, LLM) -> `ask.py` (CLI).