# Placeholder JEE Bench runner. Assumes a JSONL with fields: question, answer
import json, sys
import httpx

API = "http://localhost:8000/solve"

def read_jsonl(path):
    with open(path) as f:
        for line in f:
            if not line.strip(): continue
            yield json.loads(line)

def main(path):
    gold, correct, total = [], 0, 0
    with httpx.Client(timeout=120) as client:
        for ex in read_jsonl(path):
            total += 1
            q, a = ex["question"], ex["answer"]
            r = client.post(API, json={"question": q}).json()
            pred = r.get("answer", "")
            # naive exact check (replace with better math equivalence)
            if str(a).strip().lower() in pred.strip().lower():
                correct += 1
    print(f"Total: {total}, Correct (substring match): {correct}, Acc: {correct/total:.2%}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_jeebench.py data/jee_sample.jsonl")
        sys.exit(1)
    main(sys.argv[1])
