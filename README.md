# 🛠️ Mitsu Web Utility Tools - Flask Applications Collection

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

モダンなFlaskベースのWebアプリケーションコレクション。Docker対応で整理されたプロジェクト構造を採用。

## 🚀 含まれるアプリケーション

### 🎯 Flask Counter App
高機能なWebベースカウンターアプリケーション
- **ポート**: `5000`
- **場所**: `flask-counter-app/`
- **機能**: カウンター操作、メモリ機能、リアルタイム統計、操作履歴

### ⏱️ Timer & Stopwatch App  
精密なタイマー＆ストップウォッチアプリケーション
- **ポート**: `5001`
- **場所**: `timer-stopwatch-app/`
- **機能**: 高精度ストップウォッチ、カウントダウンタイマー、ラップタイム

## 📁 プロジェクト構造

```
mitsu-web-utility-tools/
├── flask-counter-app/          # カウンターアプリ
│   ├── src/
│   │   └── app.py             # メインアプリケーション
│   ├── docker/                # Docker設定
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── .dockerignore
│   ├── docs/                  # ドキュメント
│   ├── assets/                # 静的ファイル
│   └── tests/                 # テストファイル
├── timer-stopwatch-app/        # タイマーアプリ
│   ├── src/
│   │   └── app.py             # メインアプリケーション
│   ├── static/                # CSS/JS
│   ├── templates/             # HTMLテンプレート
│   ├── docker/                # Docker設定
│   └── README.md
├── test_mat/                   # MATLABテストファイル
│   ├── dispatchPrice.mat
│   ├── test.m
│   └── test2.m
└── README.md                   # このファイル
```

## 🚀 クイックスタート

### 🐳 Dockerを使用（推奨）

#### カウンターアプリを起動
```bash
cd flask-counter-app
docker-compose -f docker/docker-compose.yml up --build
```
→ `http://localhost:5000` でアクセス

#### タイマーアプリを起動
```bash
cd timer-stopwatch-app
docker-compose -f docker/docker-compose.yml up --build
```
→ `http://localhost:5001` でアクセス

#### 両方のアプリを同時起動
```bash
# Terminal 1
cd flask-counter-app
docker-compose -f docker/docker-compose.yml up

# Terminal 2  
cd timer-stopwatch-app
docker-compose -f docker/docker-compose.yml up
```

### 💻 直接実行

#### カウンターアプリ
```bash
cd flask-counter-app
pip install -r requirements.txt
python src/app.py
```

#### タイマーアプリ
```bash
cd timer-stopwatch-app
pip install -r requirements.txt
python src/app.py
```

## ✨ 主な機能

### 🎯 カウンターアプリ
- **ガラスモーフィズムUI**: モダンで美しいデザイン
- **多機能カウンター**: 基本操作、ステップ制御、クイックアクション
- **メモリシステム**: 3つのメモリスロット（M1, M2, M3）
- **リアルタイム統計**: 総クリック数、最大/最小値、セッション時間
- **操作履歴**: タイムスタンプ付きの詳細ログ

### ⏱️ タイマーアプリ
- **精密ストップウォッチ**: ミリ秒まで計測
- **カウントダウンタイマー**: 時分秒設定可能
- **ラップタイム機能**: 複数のラップタイム記録
- **進捗視覚化**: サークルプログレスバー
- **アラート機能**: タイマー終了通知

## 🛠️ 技術スタック

- **バックエンド**: Flask (Python 3.11+)
- **フロントエンド**: HTML5, CSS3, JavaScript
- **デザイン**: Glassmorphism, CSS Grid, Flexbox
- **コンテナ**: Docker, Docker Compose
- **セキュリティ**: 非rootユーザー実行、最新セキュリティパッチ

## 🎨 デザイン特徴

- **レスポンシブデザイン**: デスクトップ・モバイル完全対応
- **モダンUI**: ガラスモーフィズム効果
- **一貫性**: 統一されたカラースキームとタイポグラフィ
- **アクセシビリティ**: 直感的な操作とフィードバック

## 🔧 開発・カスタマイズ

### 新機能の追加
1. 対応するアプリディレクトリで開発
2. Flask APIエンドポイントの追加
3. フロントエンド機能の実装
4. Docker設定の更新（必要に応じて）

### ポート設定の変更
- カウンターアプリ: `docker-compose.yml`の`5000:5000`を変更
- タイマーアプリ: `docker-compose.yml`の`5001:5000`を変更

## 📱 モバイル対応

両アプリともフルレスポンシブ対応：
- 📱 スマートフォン（iOS/Android）
- 📟 タブレット
- 💻 デスクトップ
- 🖥️ 大画面ディスプレイ

## 🤝 コントリビューション

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。

## 🙏 謝辞

- ❤️ Flask framework
- 🐳 Docker containerization
- 🎨 Modern web design trends
- 🤖 [Claude Code](https://claude.ai/code) で開発

---

**楽しいWebアプリ体験を！ 🎯⏱️**