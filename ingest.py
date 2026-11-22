"""Incrementally index data/docs/**/*.md: only new, changed or deleted files are processed."""
import hashlib
import re
from pathlib import Path

from config import DOCS_DIR, MAX_CHUNK_CHARS
from store import get_collection, get_model


def split_markdown(text):
    """Split on #/##/### headings (ignoring '#' inside code fences), keeping the heading path."""
    chunks, path, buf, in_code = [], [], [], False

    def flush():
        body = "\n".join(buf).strip()
        if body:
            chunks.append((" > ".join(path), body))
        buf.clear()

    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^(#{1,3})\s+(.*)", line)
        if m:
            flush()
            path[:] = path[: len(m.group(1)) - 1] + [m.group(2).strip()]
        else:
            buf.append(line)
    flush()
    return chunks


def window(body):
    if len(body) <= MAX_CHUNK_CHARS:
        return [body]
    parts, cur = [], ""
    for para in body.split("\n\n"):
        if cur and len(cur) + len(para) > MAX_CHUNK_CHARS:
            parts.append(cur.strip())
            cur = ""
        cur += para + "\n\n"
    if cur.strip():
        parts.append(cur.strip())
    return parts


def main():
    root = Path(DOCS_DIR)
    current = {}
    for f in sorted(root.rglob("*.md")):
        current[str(f.relative_to(root))] = (f, hashlib.sha256(f.read_bytes()).hexdigest())

    col = get_collection()
    indexed = {m["source"]: m["file_hash"] for m in col.get(include=["metadatas"])["metadatas"]}

    stale = [s for s, h in indexed.items() if s not in current or current[s][1] != h]
    for s in stale:
        col.delete(where={"source": s})
    to_add = [s for s in current if s not in indexed or s in stale]
    print(f"{len(current)} files | {len(to_add)} to index | {len(stale)} removed/updated")
    if not to_add:
        return

    ids, texts, metas = [], [], []
    for source in to_add:
        path, file_hash = current[source]
        text = path.read_text(encoding="utf-8")
        url = (re.match(r"<!-- source: (.*?) -->", text) or [None, ""])[1]
        doc_type = Path(source).parts[0] if len(Path(source).parts) > 1 else "general"
        n = 0
        for section, body in split_markdown(text):
            for part in window(body):
                ids.append(f"{source}::{n}")
                texts.append(part)
                metas.append({"source": source, "section": section or path.stem,
                              "doc_type": doc_type, "url": url, "file_hash": file_hash})
                n += 1

    inputs = [f"{m['source']} | {m['section']}\n{t}" for m, t in zip(metas, texts)]
    embeddings = get_model().encode(inputs, normalize_embeddings=True, batch_size=32).tolist()
    for i in range(0, len(ids), 500):
        col.add(ids=ids[i:i + 500], documents=texts[i:i + 500],
                embeddings=embeddings[i:i + 500], metadatas=metas[i:i + 500])
    print(f"Indexed {len(ids)} chunks")


if __name__ == "__main__":
    main()
