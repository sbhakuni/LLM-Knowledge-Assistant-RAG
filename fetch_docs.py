"""Download the public docs listed in data/sources.json as Markdown files."""
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

from config import DOCS_DIR, SOURCES_FILE


def page_to_markdown(url):
    html = requests.get(url, timeout=30, headers={"User-Agent": "rag-practice-bot"})
    html.raise_for_status()
    soup = BeautifulSoup(html.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
        tag.decompose()
    root = soup.find("main") or soup.find("article") or soup.body
    return markdownify(str(root), heading_style="ATX").strip()


def main():
    sources = json.loads(Path(SOURCES_FILE).read_text())
    for s in sources:
        try:
            text = page_to_markdown(s["url"])
        except requests.RequestException as e:
            print(f"FAILED  {s['url']} ({e})")
            continue
        out = Path(DOCS_DIR) / s["doc_type"] / f"web-{s['name']}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"<!-- source: {s['url']} -->\n\n{text}\n", encoding="utf-8")
        print(f"OK      {out} ({len(text)} chars)")


if __name__ == "__main__":
    main()
