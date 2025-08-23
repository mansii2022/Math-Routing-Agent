from typing import List, Dict, Any, Optional
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

class KB:
    def __init__(self) -> None:
        # ✅ Use HuggingFace embeddings (no OpenAI key needed)
        self.storage_context = StorageContext.from_defaults()
        self.index: Optional[VectorStoreIndex] = None
        self.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def ensure_index(self):
        if self.index is None:
            self.index = VectorStoreIndex.from_documents(
                [],
                storage_context=self.storage_context,
                embed_model=self.embed_model,
            )

    def ingest(self, items: List[Dict[str, str]]):
        self.ensure_index()
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        docs = []
        for it in items:
            text = f"Question: {it['question']}\nAnswer: {it['answer']}"
            docs.append(Document(text=text, metadata={"source": "kb"}))
        self.index.insert_nodes(splitter.get_nodes_from_documents(docs))

    def retrieve(self, question: str, k: int = 3) -> Dict[str, Any]:
        self.ensure_index()
        query_engine = self.index.as_query_engine(similarity_top_k=k)
        res = query_engine.query(question)
        nodes = getattr(res, "source_nodes", [])
        contexts = [n.node.get_content() for n in nodes]
        hit = len(contexts) > 0 and any("Answer:" in c for c in contexts)
        return {"hit": hit, "contexts": contexts, "raw": res}
