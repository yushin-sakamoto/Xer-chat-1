from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP


class TextSplitter:
    """テキストをチャンクに分割するクラス"""

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP
    ):
        """
        Args:
            chunk_size: チャンクの最大サイズ（トークン数）
            chunk_overlap: チャンク間のオーバーラップ（トークン数）
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "、", " ", ""]
        )

    def split_text(self, text: str) -> List[str]:
        """
        テキストをチャンクに分割する

        Args:
            text: 分割するテキスト

        Returns:
            List[str]: 分割されたチャンクのリスト
        """
        return self.splitter.split_text(text)

    def split_texts(self, texts: List[str]) -> List[str]:
        """
        複数のテキストをチャンクに分割する

        Args:
            texts: 分割するテキストのリスト

        Returns:
            List[str]: 分割されたチャンクのリスト
        """
        chunks = []
        for text in texts:
            chunks.extend(self.split_text(text))
        return chunks 