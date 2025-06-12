# ⏱️ Timer & Stopwatch App

高機能なWebベースのタイマー＆ストップウォッチアプリケーションです。

## 🌟 機能

### ⏰ タイマー機能
- 時間・分・秒での時間設定
- 開始・一時停止・リセット機能
- 進捗を示すサークルプログレスバー
- タイマー終了時のアラート表示
- レスポンシブデザイン

### 🕐 ストップウォッチ機能
- 精密な時間計測（ミリ秒表示）
- 開始・停止・リセット機能
- ラップタイム記録機能
- ラップタイムの履歴表示
- リアルタイム更新

## 🚀 使用方法

### Dockerを使用した起動

```bash
# プロジェクトディレクトリに移動
cd timer-stopwatch-app

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

アプリケーションは `http://localhost:5001` でアクセスできます。

## 📁 プロジェクト構造

```
timer-stopwatch-app/
├── src/
│   └── app.py              # Flask バックエンド
├── static/
│   ├── css/
│   │   └── style.css       # スタイルシート
│   └── js/
│       └── app.js          # フロントエンド JavaScript
├── templates/
│   └── index.html          # HTMLテンプレート
├── docker/
│   ├── Dockerfile          # Docker設定
│   ├── docker-compose.yml  # Docker Compose設定
│   └── .dockerignore       # Docker除外設定
├── requirements.txt        # Python依存関係
└── README.md              # このファイル
```

## 🎨 UI特徴

- **モダンデザイン**: ガラスモーフィズム効果
- **レスポンシブ**: デスクトップ・モバイル対応
- **直感的操作**: 分かりやすいボタン配置
- **視覚的フィードバック**: アニメーションとエフェクト

## 🛠️ 技術スタック

- **バックエンド**: Flask (Python)
- **フロントエンド**: HTML5, CSS3, JavaScript
- **デザイン**: CSS Grid, Flexbox, Glassmorphism
- **コンテナ**: Docker, Docker Compose