# Flask Counter App

高機能なFlaskカウンターアプリケーションです。

## プロジェクト構成

```
flask-counter-app/
├── src/                    # アプリケーションソースコード
│   └── app.py             # メインのFlaskアプリケーション
├── docker/                # Docker関連ファイル
│   ├── Dockerfile         # Dockerイメージ設定
│   ├── docker-compose.yml # Docker Compose設定
│   └── .dockerignore      # Dockerビルド除外設定
├── docs/                  # ドキュメント
│   ├── README.md          # 元のREADME
│   ├── manual.md          # マニュアル
│   ├── sub_manual.md      # サブマニュアル
│   └── manual1.xlsx       # Excelマニュアル
├── assets/                # 静的ファイル
│   └── img/               # 画像ファイル
├── tests/                 # テストファイル
└── requirements.txt       # Python依存関係
```

## 使用方法

### Dockerを使用した起動

```bash
# プロジェクトディレクトリに移動
cd flask-counter-app

# ビルドして起動
docker-compose -f docker/docker-compose.yml up --build

# バックグラウンドで起動
docker-compose -f docker/docker-compose.yml up -d

# 停止
docker-compose -f docker/docker-compose.yml down
```

### 直接起動

```bash
# 依存関係をインストール
pip install -r requirements.txt

# アプリケーション起動
python src/app.py
```

アプリケーションは `http://localhost:5000` でアクセスできます。