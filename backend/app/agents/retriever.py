# backend/app/agents/retriever.py
from typing import List, Dict, Optional
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = os.environ.get("EMB_MODEL", "all-MiniLM-L6-v2")
INDEX_PATH = os.environ.get("KB_INDEX", "data/kb.index")
META_PATH  = os.environ.get("KB_META", "data/kb_meta.json")

class KB:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = None
        self.meta: List[Dict] = []
        self._load()

    def _load(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(META_PATH, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
        else:
            # create empty
            self.index = faiss.IndexFlatIP(384)
            self.meta = []
            self._persist()

    def _persist(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def add_many(self, qa_list: List[Dict[str, str]]):
        texts = [f"Q: {q['question']} A: {q['answer']}" for q in qa_list]
        emb = self.model.encode(texts, normalize_embeddings=True)
        xb = np.array(emb, dtype="float32")
        self.index.add(xb)
        self.meta.extend(qa_list)
        self._persist()

    def retrieve(self, query: str, k: int = 3) -> Dict:
        q_emb = self.model.encode([query], normalize_embeddings=True).astype("float32")
        D, I = self.index.search(q_emb, k)
        hits = []
        for idx, score in zip(I[0], D[0]):
            if idx < 0 or idx >= len(self.meta): 
                continue
            m = self.meta[idx]
            hits.append({"score": float(score), "question": m["question"], "answer": m["answer"]})
        return {"hit": len(hits) > 0 and hits[0]["score"] > 0.4, "results": hits}
