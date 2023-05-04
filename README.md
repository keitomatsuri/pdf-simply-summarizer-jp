# 概要
PDFをかんたんな日本語に要約するWebアプリケーションです。  
https://qiita.com/keitomatsuri/items/4c848d58ea5f9b3ebe42  

# 環境構築
- node18系、python3.11系での動作を確認。
## フロントエンド
- cd frontend
- pnpm install
- pnpm run dev
## バックエンド
- cd backend
- .env作成
  - OPENAI_API_KEYを設定
  - MAX_CONTENT_LENGTHの初期値は10MB(10*1024*1024)
- pip install -r requirements.txt
- python app.py