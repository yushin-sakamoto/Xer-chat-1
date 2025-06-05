import pytest

from app.splitters.text_splitter import TextSplitter


def test_split_text():
    """テキスト分割の基本機能をテスト"""
    splitter = TextSplitter(chunk_size=100, chunk_overlap=20)
    
    # テスト用の長いテキスト
    text = """
    これはテスト用のテキストです。
    このテキストは複数の段落に分かれています。
    
    2番目の段落です。
    ここには別の内容が書かれています。
    
    3番目の段落です。
    最後の段落になります。
    """
    
    chunks = splitter.split_text(text)
    
    # チャンクが生成されていることを確認
    assert len(chunks) > 0
    
    # 各チャンクの長さが制限を超えていないことを確認
    for chunk in chunks:
        assert len(chunk) <= 100
    
    # チャンクの内容が元のテキストの一部であることを確認
    for chunk in chunks:
        assert chunk.strip() in text


def test_split_texts():
    """複数テキストの分割をテスト"""
    splitter = TextSplitter(chunk_size=100, chunk_overlap=20)
    
    texts = [
        "1つ目のテキストです。\n複数行に分かれています。",
        "2つ目のテキストです。\nこれも複数行です。"
    ]
    
    chunks = splitter.split_texts(texts)
    
    # チャンクが生成されていることを確認
    assert len(chunks) > 0
    
    # 各チャンクの長さが制限を超えていないことを確認
    for chunk in chunks:
        assert len(chunk) <= 100
    
    # チャンクの内容が元のテキストの一部であることを確認
    for chunk in chunks:
        assert any(chunk.strip() in text for text in texts)


def test_empty_text():
    """空のテキストの処理をテスト"""
    splitter = TextSplitter()
    
    # 空のテキスト
    chunks = splitter.split_text("")
    assert len(chunks) == 0
    
    # 空のテキストリスト
    chunks = splitter.split_texts([])
    assert len(chunks) == 0


def test_custom_chunk_size():
    """カスタムチャンクサイズの設定をテスト"""
    splitter = TextSplitter(chunk_size=50, chunk_overlap=10)
    
    text = "これはテスト用のテキストです。" * 10  # 長いテキスト
    
    chunks = splitter.split_text(text)
    
    # チャンクが生成されていることを確認
    assert len(chunks) > 0
    
    # 各チャンクの長さが制限を超えていないことを確認
    for chunk in chunks:
        assert len(chunk) <= 50 