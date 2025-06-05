import pytest
from pathlib import Path

from app.embedders.gemini_embedder import GeminiEmbedder
from app.retrievers.document_store import DocumentStore
from app.retrievers.vector_store import VectorStore


def test_gemini_embedder():
    """GeminiEmbedderの基本機能をテスト"""
    embedder = GeminiEmbedder()
    
    # 単一テキストの埋め込み
    text = "これはテスト用のテキストです。"
    embedding = embedder.embed_text(text)
    
    # 埋め込みベクトルの形式を確認
    assert isinstance(embedding, list)
    assert all(isinstance(x, float) for x in embedding)
    assert len(embedding) > 0
    
    # 複数テキストの埋め込み
    texts = [
        "1つ目のテキストです。",
        "2つ目のテキストです。"
    ]
    embeddings = embedder.embed_texts(texts)
    
    # 埋め込みベクトルの形式を確認
    assert len(embeddings) == len(texts)
    assert all(isinstance(emb, list) for emb in embeddings)
    assert all(len(emb) == len(embedding) for emb in embeddings)


def test_vector_store():
    """VectorStoreの基本機能をテスト"""
    store = VectorStore(collection_name="test_collection")
    
    # テストデータ
    texts = [
        "これはテスト用のテキストです。",
        "これは別のテストテキストです。"
    ]
    metadatas = [
        {"source": "test1"},
        {"source": "test2"}
    ]
    
    # テキストの追加
    store.add_texts(texts=texts, metadatas=metadatas)
    
    # 類似検索
    results = store.similarity_search("テスト", k=2)
    
    # 検索結果の形式を確認
    assert len(results) == 2
    assert all(isinstance(doc, dict) for doc in results)
    assert all("text" in doc for doc in results)
    assert all("metadata" in doc for doc in results)
    
    # コレクションの削除
    store.delete_collection()


def test_document_store(tmp_path):
    """DocumentStoreの基本機能をテスト"""
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
    
    # DocumentStoreのテスト
    store = DocumentStore(collection_name="test_docs")
    
    # 文書の追加
    store.add_documents(
        directory=doc_dir,
        metadata={"source": "test_docs"}
    )
    
    # 検索テスト
    results = store.search("テスト文書", k=1)
    
    # 検索結果の形式を確認
    assert len(results) > 0
    assert all(isinstance(doc, dict) for doc in results)
    assert all("text" in doc for doc in results)
    assert all("metadata" in doc for doc in results)
    
    # コレクションの削除
    store.clear() 