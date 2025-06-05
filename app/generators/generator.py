import os
from typing import Dict, List, Any

import google.generativeai as genai

from app.config import GOOGLE_API_KEY
from app.generators.prompt_template import PromptTemplate
from app.retrievers.retriever import Retriever


class Generator:
    """Gemini APIを使用した回答生成クラス"""

    def __init__(self, retriever: Retriever):
        """
        Args:
            retriever: 文書検索用のRetrieverインスタンス
        """
        self.retriever = retriever
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        
        # 利用可能なモデルを確認
        for m in genai.list_models():
            print(f"Model: {m.name}")
            print(f"Display name: {m.display_name}")
            print(f"Description: {m.description}")
            print("---")
        
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.prompt_template = PromptTemplate()

    def generate_response(self, query: str) -> str:
        """
        質問に対する回答を生成

        Args:
            query: ユーザーの質問

        Returns:
            str: 生成された回答
        """
        # 関連文書の検索
        docs = self.retriever.retrieve(query)
        
        # プロンプトの作成
        context = "\n".join([doc["text"] for doc in docs])
        prompt = f"""以下の文脈に基づいて質問に答えてください。
文脈が質問に関連していない場合は、その旨を伝えてください。

文脈:
{context}

質問: {query}

回答:"""
        
        # 回答の生成
        response = self.model.generate_content(prompt)
        return response.text 