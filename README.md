# lesson23_4_product.recommend

## 商品推薦システム

このアプリケーションは、RAG（Retrieval-Augmented Generation）を使用した商品推薦システムです。

## Streamlit Cloudでのデプロイ手順

1. **環境変数の設定**
   - Streamlit Cloudのアプリダッシュボードで「Settings」→「Secrets」に移動
   - 以下の環境変数を設定してください：
     ```
     OPENAI_API_KEY = "your_actual_openai_api_key"
     ```

2. **必要なファイル**
   - `requirements.txt`: 依存関係が記載されています
   - `main.py`: メインアプリケーションファイル
   - `data/products.csv`: 商品データ

3. **ローカル環境での実行**
   ```bash
   pip install -r requirements.txt
   streamlit run main.py
   ```

## 解決済みの問題

- **ModuleNotFoundError: No module named 'dotenv'**: `requirements.txt`ファイルを作成し、`python-dotenv`を含むすべての依存関係を追加しました。