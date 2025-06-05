import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from cli.chat import main


def test_cli_without_api_key(tmp_path):
    """APIキーが設定されていない場合のテスト"""
    runner = CliRunner()
    
    # 環境変数を一時的に削除
    with patch.dict(os.environ, {}, clear=True):
        result = runner.invoke(main, ['--docs-dir', str(tmp_path)])
        
        assert result.exit_code == 0
        assert "GOOGLE_API_KEY環境変数が設定されていません" in result.output


def test_cli_with_invalid_docs_dir():
    """存在しないディレクトリを指定した場合のテスト"""
    runner = CliRunner()
    
    with patch.dict(os.environ, {'GOOGLE_API_KEY': 'dummy_key'}):
        result = runner.invoke(main, ['--docs-dir', 'nonexistent_dir'])
        
        assert result.exit_code != 0
        assert "does not exist" in result.output


def test_cli_with_empty_docs_dir(tmp_path):
    """空のディレクトリを指定した場合のテスト"""
    runner = CliRunner()
    
    with patch.dict(os.environ, {'GOOGLE_API_KEY': 'dummy_key'}):
        result = runner.invoke(main, ['--docs-dir', str(tmp_path)])
        
        assert result.exit_code == 0
        assert "文書の読み込みが完了しました" in result.output


def test_cli_with_sample_docs(tmp_path):
    """サンプル文書を使用したテスト"""
    # テスト用の文書を作成
    docs_dir = tmp_path / "test_docs"
    docs_dir.mkdir()
    
    md_file = docs_dir / "test.md"
    md_file.write_text("""
    # テスト文書
    
    これはテスト用の文書です。
    """)
    
    runner = CliRunner()
    
    with patch.dict(os.environ, {'GOOGLE_API_KEY': 'dummy_key'}):
        # モックの設定
        with patch('app.pipeline.Pipeline.run') as mock_run:
            mock_run.return_value = {
                "answer": "これはテスト回答です。",
                "sources": "文書 1: test_docs"
            }
            
            # 対話モードのテスト
            result = runner.invoke(
                main,
                ['--docs-dir', str(docs_dir)],
                input='テスト質問\nexit\n'
            )
            
            assert result.exit_code == 0
            assert "文書の読み込みが完了しました" in result.output
            assert "テスト回答" in result.output
            assert "文書 1: test_docs" in result.output 