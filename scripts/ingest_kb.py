import sys, json
from pathlib import Path
from backend.app.agents.retriever import KB

def read_jsonl(p: Path):
    with p.open() as f:
        for line in f:
            line = line.strip()
            if not line: continue
            yield json.loads(line)

def main(path: str):
    kb = KB()
    items = list(read_jsonl(Path(path)))
    kb.ingest(items)
    print(f"Ingested {len(items)} items into KB.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest_kb.py data/sample_gsm8k.jsonl")
        sys.exit(1)
    main(sys.argv[1])
