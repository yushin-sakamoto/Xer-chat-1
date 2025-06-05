# RAG Chatbot

Google Gemini APIを使用したRetrieval-Augmented Generation (RAG) ベースのチャットボットです。PDFやMarkdownファイルを読み込み、それらの内容に基づいて質問に答えることができます。

## 機能

- ドキュメントの読み込み（PDF、Markdown）
- テキストの埋め込み生成
- ChromaDBを使用したベクトルストアの実装
- 質問応答システム
- CLIインターフェース
- Dockerコンテナ化
- CI/CDパイプライン

## 必要条件

- Python 3.11以上
- Google Gemini APIキー
- Docker（オプション）

## セットアップ

1. 環境変数の設定
   ```sh
   cp .env.example .env
   # .envファイルを編集してGOOGLE_API_KEYを設定
   ```

2. 仮想環境の作成と依存関係のインストール
   ```sh
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. アプリケーションの起動
   ```sh
   python cli/chat.py
   ```

## Dockerを使用する場合

```sh
docker-compose up
```

## プロジェクト構造

```
.
├── app/                    # アプリケーションコード
│   ├── embedders/         # テキスト埋め込み生成
│   ├── generators/        # 回答生成
│   ├── loaders/          # ドキュメント読み込み
│   ├── retrievers/       # 文書検索
│   └── splitters/        # テキスト分割
├── cli/                   # コマンドラインインターフェース
├── docs/                  # ドキュメント
├── tests/                 # テスト
└── docker/               # Docker設定
```

## 開発

### テストの実行

```sh
pytest
```

### コードフォーマット

```sh
black .
isort .
```

### テストカバレッジ

```sh
pytest --cov=app tests/
```

## CI/CD

GitHub Actionsを使用して以下の処理を自動化しています：

- コード品質チェック
- テスト実行
- Dockerイメージのビルドとプッシュ

## ライセンス

MIT

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 実装時間

- 3時間程度
