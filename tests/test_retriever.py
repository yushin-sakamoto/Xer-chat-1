import pytest
from pathlib import Path

from app.retrievers.document_store import DocumentStore
from app.retrievers.retriever import Retriever


def test_retriever(tmp_path):
    """Retrieverの基本機能をテスト"""
    # テスト用の文書を作成
    doc_dir = tmp_path / "test_docs"
    doc_dir.mkdir()
    
    # テスト用のMarkdownファイルを作成
    md_file = doc_dir / "test.md"
    md_file.write_text("""
    # テスト文書
    
    これはテスト用の文書です。
    この文書は複数の段落に分かれています。
    
    ## サブセクション
    
    ここには別の内容が書かれています。
    """)
    
    # DocumentStoreとRetrieverの初期化
    store = DocumentStore(collection_name="test_retriever")
    retriever = Retriever(store)
    
    # 文書の追加
    store.add_documents(
        directory=doc_dir,
        metadata={"source": "test_docs"}
    )
    
    # 検索テスト
    results = retriever.retrieve("テスト文書", k=1)
    
    # 検索結果の形式を確認
    assert len(results) > 0
    assert all(isinstance(doc, dict) for doc in results)
    assert all("text" in doc for doc in results)
    assert all("metadata" in doc for doc in results)
    
    # コンテキストの整形テスト
    context = retriever.format_context(results)
    assert isinstance(context, str)
    assert "文書 1:" in context
    assert "テスト用の文書" in context
    
    # コレクションの削除
    store.clear()


def test_retriever_with_filter(tmp_path):
    """フィルター付きの検索をテスト"""
    # テスト用の文書を作成
    doc_dir = tmp_path / "test_docs"
    doc_dir.mkdir()
    
    # テスト用のMarkdownファイルを作成
    md_file1 = doc_dir / "test1.md"
    md_file1.write_text("""
    # テスト文書1
    
    これは1つ目のテスト文書です。
    """)
    
    md_file2 = doc_dir / "test2.md"
    md_file2.write_text("""
    # テスト文書2
    
    これは2つ目のテスト文書です。
    """)
    
    # DocumentStoreとRetrieverの初期化
    store = DocumentStore(collection_name="test_retriever_filter")
    retriever = Retriever(store)
    
    # 文書の追加（メタデータ付き）
    store.add_documents(
        directory=doc_dir,
        metadata={"source": "test_docs"}
    )
    
    # フィルター付きの検索テスト
    filter_dict = {"source": "test_docs"}
    results = retriever.retrieve("テスト文書", k=2, filter=filter_dict)
    
    # 検索結果の確認
    assert len(results) > 0
    assert all(doc["metadata"]["source"] == "test_docs" for doc in results)
    
    # コレクションの削除
    store.clear() 