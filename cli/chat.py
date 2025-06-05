import os
from pathlib import Path

import click
from rich.console import Console
from rich.markdown import Markdown

from app.pipeline import Pipeline


@click.command()
@click.option(
    '--docs-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default='docs',
    help='文書が格納されているディレクトリ'
)
@click.option(
    '--collection-name',
    default='documents',
    help='コレクション名'
)
def main(docs_dir: str, collection_name: str):
    """RAGチャットボットのCLIインターフェース"""
    console = Console()
    
    # 環境変数の確認
    if not os.getenv('GOOGLE_API_KEY'):
        console.print("[red]エラー: GOOGLE_API_KEY環境変数が設定されていません[/red]")
        return
    
    # パイプラインの初期化
    pipeline = Pipeline(
        docs_dir=Path(docs_dir),
        collection_name=collection_name
    )
    
    try:
        # 文書の読み込み
        console.print("[yellow]文書を読み込んでいます...[/yellow]")
        pipeline.initialize()
        console.print("[green]文書の読み込みが完了しました[/green]")
        
        # 対話ループ
        console.print("\n[bold blue]RAGチャットボット[/bold blue]")
        console.print("終了するには 'exit' または 'quit' と入力してください\n")
        
        while True:
            # 質問の入力
            query = click.prompt("質問")
            
            if query.lower() in ['exit', 'quit']:
                break
            
            try:
                # 回答の生成
                response = pipeline.run(query)
                
                # 回答の表示
                console.print("\n[bold]回答:[/bold]")
                console.print(Markdown(response["answer"]))
                
                # 参考文書の表示
                if response["sources"]:
                    console.print("\n[bold]参考文書:[/bold]")
                    console.print(response["sources"])
                
                console.print()  # 空行
                
            except Exception as e:
                console.print(f"[red]エラー: {str(e)}[/red]")
    
    finally:
        # コレクションの削除
        pipeline.clear()


if __name__ == '__main__':
    main() 