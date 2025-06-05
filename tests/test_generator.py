import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.generators.generator import Generator
from app.generators.prompt_template import PromptTemplate
from app.retrievers.document_store import DocumentStore
from app.retrievers.retriever import Retriever


def test_prompt_template():
    """PromptTemplateの基本機能をテスト"""
    template = PromptTemplate()
    
    # プロンプト生成のテスト
    query = "テスト質問"
    context = "テストコンテキスト"
    prompt = template.create_prompt(query, context)
    
    assert query in prompt
    assert context in prompt
    assert "回答は以下の形式で提供してください" in prompt
    
    # 参考文書情報の整形テスト
    documents = [
        {"metadata": {"source": "test1"}},
        {"metadata": {"source": "test2"}}
    ]
    sources = template.format_sources(documents)
    
    assert "文書 1: test1" in sources
    assert "文書 2: test2" in sources


@patch('google.generativeai.GenerativeModel')
def test_generator(mock_model, tmp_path):
    """Generatorの基本機能をテスト"""
    # モックの設定
    mock_response = MagicMock()
    mock_response.text = "これはテスト回答です。"
    mock_model.return_value.generate_content.return_value = mock_response
    
    # テスト用の文書を作成
    doc_dir = tmp_path / "test_docs"
    doc_dir.mkdir()
    
    md_file = doc_dir / "test.md"
    md_file.write_text("""
    # テスト文書
    
    これはテスト用の文書です。
    """)
    
    # DocumentStore、Retriever、Generatorの初期化
    store = DocumentStore(collection_name="test_generator")
    retriever = Retriever(store)
    generator = Generator(retriever)
    
    # 文書の追加
    store.add_documents(
        directory=doc_dir,
        metadata={"source": "test_docs"}
    )
    
    # 回答生成のテスト
    query = "テスト質問"
    response = generator.generate_response(query)
    
    # レスポンスの形式を確認
    assert isinstance(response, dict)
    assert "answer" in response
    assert "sources" in response
    assert response["answer"] == "これはテスト回答です。"
    assert "文書 1: test_docs" in response["sources"]
    
    # コレクションの削除
    store.clear()


def test_generator_with_empty_context():
    """空のコンテキストでの回答生成をテスト"""
    # モックのRetrieverを作成
    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = []
    mock_retriever.format_context.return_value = ""
    
    # Generatorの初期化
    generator = Generator(mock_retriever)
    
    # 回答生成のテスト
    query = "テスト質問"
    response = generator.generate_response(query)
    
    # レスポンスの形式を確認
    assert isinstance(response, dict)
    assert "answer" in response
    assert "sources" in response
    assert response["sources"] == "" 