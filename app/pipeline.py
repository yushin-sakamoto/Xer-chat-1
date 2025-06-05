from pathlib import Path
from typing import Dict, Optional

from app.generators.generator import Generator
from app.retrievers.document_store import DocumentStore
from app.retrievers.retriever import Retriever


class Pipeline:
    """チャンク検索→回答生成の一連処理を管理するクラス"""

    def __init__(self, docs_dir: Path, collection_name: str = "documents"):
        """
        Args:
            docs_dir: 文書が格納されているディレクトリ
            collection_name: コレクション名
        """
        self.docs_dir = docs_dir
        self.document_store = DocumentStore(collection_name)
        self.retriever = Retriever(self.document_store)
        self.generator = Generator(self.retriever)

    def initialize(self, metadata: Optional[dict] = None) -> None:
        """
        文書の読み込みとベクトルストアへの登録を実行

        Args:
            metadata: 追加するメタデータ（オプション）
        """
        self.document_store.add_documents(
            directory=self.docs_dir,
            metadata=metadata
        )

    def run(self, query: str) -> Dict:
        """
        質問に対する回答を生成

        Args:
            query: ユーザーの質問

        Returns:
            Dict: 回答と参考文書の情報を含む辞書
        """
        return self.generator.generate_response(query)

    def clear(self) -> None:
        """コレクションを削除"""
        self.document_store.clear() 