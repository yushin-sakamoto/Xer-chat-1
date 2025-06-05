from typing import List

import google.generativeai as genai

from app.config import GOOGLE_API_KEY


class GeminiEmbedder:
    """Google Gemini APIを使用した埋め込み生成クラス"""

    def __init__(self):
        """Gemini APIの初期化"""
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('embedding-001')

    def embed_text(self, text: str) -> List[float]:
        """
        テキストの埋め込みベクトルを生成

        Args:
            text: 埋め込みを生成するテキスト

        Returns:
            List[float]: 埋め込みベクトル
        """
        result = self.model.embed_content(text)
        return result.embedding

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        複数のテキストの埋め込みベクトルを生成

        Args:
            texts: 埋め込みを生成するテキストのリスト

        Returns:
            List[List[float]]: 埋め込みベクトルのリスト
        """
        embeddings = []
        for text in texts:
            embedding = self.embed_text(text)
            embeddings.append(embedding)
        return embeddings 