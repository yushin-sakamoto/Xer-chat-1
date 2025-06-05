from pathlib import Path
from typing import List, Union

import markdown
from pypdf import PdfReader


class DocumentLoader:
    """PDFとMarkdownファイルを読み込むためのローダークラス"""

    @staticmethod
    def load_document(file_path: Union[str, Path]) -> str:
        """
        指定されたファイルを読み込み、テキストとして返す

        Args:
            file_path: 読み込むファイルのパス

        Returns:
            str: 読み込まれたテキスト

        Raises:
            ValueError: サポートされていないファイル形式の場合
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() == '.pdf':
            return DocumentLoader._load_pdf(file_path)
        elif file_path.suffix.lower() in ['.md', '.markdown']:
            return DocumentLoader._load_markdown(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

    @staticmethod
    def _load_pdf(file_path: Path) -> str:
        """PDFファイルを読み込む"""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    @staticmethod
    def _load_markdown(file_path: Path) -> str:
        """Markdownファイルを読み込む"""
        with open(file_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
        # MarkdownをHTMLに変換し、テキストのみを抽出
        html = markdown.markdown(md_text)
        # 簡易的なHTMLタグ除去（実際のプロジェクトではBeautifulSoupなどを使用することを推奨）
        text = html.replace('<p>', '').replace('</p>', '\n')
        text = text.replace('<h1>', '# ').replace('</h1>', '\n')
        text = text.replace('<h2>', '## ').replace('</h2>', '\n')
        text = text.replace('<h3>', '### ').replace('</h3>', '\n')
        return text

    @staticmethod
    def load_documents(directory: Union[str, Path]) -> List[str]:
        """
        指定されたディレクトリ内のPDFとMarkdownファイルを読み込む

        Args:
            directory: 読み込むディレクトリのパス

        Returns:
            List[str]: 読み込まれたテキストのリスト
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        texts = []
        for file_path in directory.glob('**/*'):
            if file_path.suffix.lower() in ['.pdf', '.md', '.markdown']:
                try:
                    text = DocumentLoader.load_document(file_path)
                    texts.append(text)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    continue

        return texts 