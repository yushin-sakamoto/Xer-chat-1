from typing import List, Dict, Any

from app.config import MAX_RETRIEVAL_DOCS
from app.retrievers.document_store import DocumentStore


class Retriever:
    """質問に対するベクトル検索を実装するクラス"""

    def __init__(self, document_store: DocumentStore):
        """
        Args:
            document_store: 文書ストアのインスタンス
        """
        self.document_store = document_store

    def retrieve(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        クエリに関連する文書を検索

        Args:
            query: 検索クエリ
            n_results: 取得する結果の数

        Returns:
            List[Dict[str, Any]]: 検索結果のリスト
        """
        return self.document_store.vector_store.search(
            query=query,
            n_results=n_results
        )

    def format_context(self, documents: List[dict]) -> str:
        """
        検索結果をコンテキストとして整形

        Args:
            documents: 検索結果のリスト

        Returns:
            str: 整形されたコンテキスト
        """
        context = []
        for i, doc in enumerate(documents, 1):
            context.append(f"文書 {i}:")
            context.append(doc["text"])
            context.append("")  # 空行を追加

        return "\n".join(context) 