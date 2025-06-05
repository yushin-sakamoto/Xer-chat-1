from pathlib import Path
from typing import List, Optional, Dict, Any

import chromadb

from app.config import CHROMA_PERSIST_DIRECTORY


class VectorStore:
    """ChromaDBを使用したベクトルストアの管理クラス"""

    def __init__(self, collection_name: str = "documents"):
        """
        Args:
            collection_name: コレクション名
        """
        self.persist_directory = Path(".chroma")
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_texts(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]] = None,
        ids: List[str] = None
    ) -> None:
        """
        テキストとその埋め込みをベクトルストアに追加

        Args:
            texts: 追加するテキストのリスト
            metadatas: メタデータのリスト（オプション）
            ids: ドキュメントIDのリスト（オプション）
        """
        if metadatas is None:
            metadatas = [{"source": f"document_{i}", "type": "markdown"} for i in range(len(texts))]
        elif len(metadatas) == 0:
            metadatas = [{"source": f"document_{i}", "type": "markdown"} for i in range(len(texts))]
        else:
            # 空の辞書をデフォルト値で置き換え
            metadatas = [
                {"source": f"document_{i}", "type": "markdown", **meta} if not meta else meta
                for i, meta in enumerate(metadatas)
            ]
        
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def search(
        self,
        query: str,
        n_results: int = 5,
        filter: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        クエリに類似したテキストを検索

        Args:
            query: 検索クエリ
            n_results: 取得する結果の数
            filter: 検索フィルター（オプション）

        Returns:
            List[Dict[str, Any]]: 検索結果のリスト（テキストとメタデータを含む）
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filter
        )
        
        return [
            {
                "text": doc,
                "metadata": meta,
                "id": id_
            }
            for doc, meta, id_ in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["ids"][0]
            )
        ]

    def delete_collection(self) -> None:
        """コレクションを削除"""
        self.client.delete_collection(self.collection.name) 