from pathlib import Path
from typing import List, Optional

from app.embedders.gemini_embedder import GeminiEmbedder
from app.loaders.document_loader import DocumentLoader
from app.retrievers.vector_store import VectorStore
from app.splitters.text_splitter import TextSplitter


class DocumentStore:
    """文書のベクトル登録と検索を管理するクラス"""

    def __init__(self, collection_name: str = "documents"):
        """
        Args:
            collection_name: コレクション名
        """
        self.embedder = GeminiEmbedder()
        self.vector_store = VectorStore(collection_name)
        self.splitter = TextSplitter()

    def add_documents(
        self,
        directory: Path,
        metadata: Optional[dict] = None
    ) -> None:
        """
        ディレクトリ内の文書を読み込み、ベクトルストアに登録

        Args:
            directory: 文書が格納されているディレクトリ
            metadata: 追加するメタデータ（オプション）
        """
        # 文書の読み込み
        loader = DocumentLoader()
        texts = loader.load_documents(directory)

        # テキストの分割
        chunks = self.splitter.split_texts(texts)

        # メタデータの準備
        if metadata is None:
            metadata = {}
        metadatas = [metadata.copy() for _ in chunks]

        # ベクトルストアへの登録
        self.vector_store.add_texts(
            texts=chunks,
            metadatas=metadatas
        )

    def search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[dict] = None
    ) -> List[dict]:
        """
        クエリに類似した文書を検索

        Args:
            query: 検索クエリ
            k: 取得する結果の数
            filter: 検索フィルター（オプション）

        Returns:
            List[dict]: 検索結果のリスト
        """
        return self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter
        )

    def clear(self) -> None:
        """コレクションを削除"""
        self.vector_store.delete_collection() 