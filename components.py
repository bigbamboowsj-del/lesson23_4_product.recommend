"""
このファイルは、画面表示に特化した関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import logging
import streamlit as st
import constants as ct


############################################################
# 関数定義
############################################################

def display_app_title():
    """
    タイトル表示
    """
    st.markdown(f"## {ct.APP_NAME}")


def display_initial_ai_message():
    """
    AIメッセージの初期表示
    """
    with st.chat_message("assistant", avatar=ct.AI_ICON_FILE_PATH):
        st.markdown("こちらは対話型の商品レコメンド生成AIアプリです。「こんな商品が欲しい」という情報・要望を画面下部のチャット欄から送信いただければ、おすすめの商品をレコメンドいたします。")
        st.markdown("**入力例**")
        st.info("""
        - 「長時間使える、高音質なワイヤレスイヤホン」
        - 「机のライト」
        - 「USBで充電できる加湿器」
        """)


def display_conversation_log():
    """
    会話ログの一覧表示
    """
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar=ct.USER_ICON_FILE_PATH):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar=ct.AI_ICON_FILE_PATH):
                display_product(message["content"])


def display_product(result):
    """
    商品情報の表示

    Args:
        result: LLMからの回答
    """
    logger = logging.getLogger(ct.LOGGER_NAME)

    # 詳細なデバッグ情報をログに出力
    logger.info(f"result type: {type(result)}")
    logger.info(f"result length: {len(result) if hasattr(result, '__len__') else 'N/A'}")
    logger.info(f"result content: {result}")
    
    # デバッグ情報を簡潔に表示（必要に応じてコメントアウト可能）
    # st.write(f"**デバッグ情報:** {len(result)}件の商品が見つかりました")
    
    try:
        # resultが期待される形式かチェック
        if not result or len(result) == 0:
            error_msg = "検索結果が空です"
            logger.error(error_msg)
            st.error(error_msg)
            return
            
        # 最初の要素にpage_contentがあるかチェック
        if not hasattr(result[0], 'page_content'):
            error_msg = f"検索結果にpage_contentが見つかりません。result[0] type: {type(result[0])}, content: {result[0]}"
            logger.error(error_msg)
            st.error(error_msg)
            return
        
        # LLMレスポンスのテキストを辞書に変換
        page_content = result[0].page_content
        # BOM（\ufeff）を除去
        if page_content.startswith('\ufeff'):
            page_content = page_content[1:]
        
        logger.info(f"page_content (after BOM removal): {page_content}")
        product_lines = page_content.split("\n")
        logger.info(f"product_lines: {product_lines}")
        
        product = {}
        for item in product_lines:
            if ": " in item:
                key, value = item.split(": ", 1)
                # キーからもBOMを除去（念のため）
                key = key.strip().lstrip('\ufeff')
                product[key] = value
            else:
                logger.warning(f"Skipping malformed line: {item}")
                
        logger.info(f"parsed product: {product}")
        
    except Exception as e:
        error_msg = f"商品データの解析でエラーが発生: {str(e)}, result: {result}"
        logger.error(error_msg)
        st.error(error_msg)
        return

    st.markdown("以下の商品をご提案いたします。")

    # 「商品名」と「価格」
    st.success(f"""
            商品名：{product['name']}（商品ID: {product['id']}）\n
            価格：{product['price']}
    """)

    # 在庫状況の表示
    stock_status = product.get('stock_status', 'あり')
    if stock_status == ct.STOCK_LOW_STATUS:
        st.warning(ct.STOCK_LOW_MESSAGE, icon=ct.STOCK_ERROR_ICON)
    elif stock_status == ct.STOCK_OUT_STATUS:
        st.error(ct.STOCK_OUT_MESSAGE, icon=ct.ERROR_ICON)

    # 「商品カテゴリ」と「メーカー」と「ユーザー評価」
    st.code(f"""
        商品カテゴリ：{product['category']}\n
        メーカー：{product['maker']}\n
        評価：{product['score']}({product['review_number']}件)
    """, language=None, wrap_lines=True)

    # 商品画像
    st.image(f"images/products/{product['file_name']}", width=400)

    # 商品説明
    st.code(product['description'], language=None, wrap_lines=True)

    # おすすめ対象ユーザー
    st.markdown("**こんな方におすすめ！**")
    st.info(product["recommended_people"])

    # 商品ページのリンク
    st.link_button("商品ページを開く", type="primary", use_container_width=True, url="https://google.com")