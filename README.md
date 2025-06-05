# RAG Chatbot

Google Gemini APIを使用したRAG（Retrieval-Augmented Generation）ベースのチャットボットです。PDFやMarkdownファイルを読み込み、質問応答システムを構築します。

## 機能

- PDF/Markdownドキュメントの読み込みとチャンク化
- Gemini APIを使用したテキストの埋め込み生成
- ChromaDBを使用したベクトルストアの実装
- 質問応答システムの実装
- CLIインターフェース
- Dockerコンテナ化
- CI/CDパイプライン

## 必要条件

- Python 3.11以上
- Google Gemini APIキー
- Docker（オプション）

## セットアップ

### 1. 環境変数の設定

```bash
cp .env.example .env
# .envファイルを編集して必要なAPIキーを設定
```

### 2. 仮想環境の作成と依存パッケージのインストール

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. アプリケーションの起動

```bash
python cli/chat.py
```

### 4. Dockerを使用する場合

```bash
# イメージのビルドと起動
docker-compose -f docker/docker-compose.yml up --build
```

## プロジェクト構造

```
.
├── app/
│   ├── loaders/      # ドキュメントローダー
│   ├── splitters/    # テキスト分割ロジック
│   ├── embedders/    # 埋め込み生成
│   ├── retrievers/   # ベクトル検索
│   └── generators/   # 回答生成
├── cli/             # コマンドラインインターフェース
├── docs/            # サンプルドキュメント
├── tests/           # テストコード
└── docker/          # Docker関連ファイル
```

## 開発

### テストの実行

```bash
pytest
```

### コードフォーマット

```bash
# コードの整形
black .
isort .

# リンターの実行
flake8
```

### テストカバレッジ

```bash
pytest --cov=app --cov-report=term-missing
```

## CI/CD

GitHub Actionsを使用して以下のCI/CDパイプラインを実装しています：

- コードの品質チェック（flake8, isort, black）
- テストの実行とカバレッジレポートの生成
- Dockerイメージのビルドとプッシュ

## ライセンス

MIT

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add some amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを作成

## 時間見積もり

各フェーズの実装に要した時間：

- フェーズ0: プロジェクト初期化 - 1時間
- フェーズ1: データロードとチャンク化 - 2時間
- フェーズ2: 埋め込み生成と保存 - 2時間
- フェーズ3: 質問→検索→回答 - 2時間
- フェーズ4: 統合とCLI - 1時間
- フェーズ5: コンテナ＆CI - 1時間
- フェーズ6: ドキュメント - 1時間

合計: 10時間 