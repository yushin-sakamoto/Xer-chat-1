from typing import List


class PromptTemplate:
    """Geminiへの入力プロンプトテンプレート"""

    @staticmethod
    def create_prompt(query: str, context: str) -> str:
        """
        質問とコンテキストからプロンプトを生成

        Args:
            query: ユーザーの質問
            context: 関連文書のコンテキスト

        Returns:
            str: 生成されたプロンプト
        """
        return f"""以下の文書を参考に、質問に答えてください。

参考文書:
{context}

質問: {query}

回答は以下の形式で提供してください：
1. 回答の要約（1-2文）
2. 詳細な説明
3. 参考にした文書の番号

回答:"""

    @staticmethod
    def format_sources(documents: List[dict]) -> str:
        """
        参考文書の情報を整形

        Args:
            documents: 検索結果のリスト

        Returns:
            str: 整形された参考文書情報
        """
        sources = []
        for i, doc in enumerate(documents, 1):
            source = f"文書 {i}:"
            if "metadata" in doc and "source" in doc["metadata"]:
                source += f" {doc['metadata']['source']}"
            sources.append(source)
        return "\n".join(sources) 