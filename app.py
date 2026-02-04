import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感 CSS (加強置中 + 按鈕顏色調整) ---
st.markdown("""
    <style>
    /* 全域字體縮小 */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
        min-height: 100vh;
    }
    
    /* 隱藏預設元件 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 標題 */
    h1 { color: #38bdf8 !important; font-size: 1.7rem !important; font-weight: 800; }
    .sub-text { color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }
    
    /* 登入容器 - 強制螢幕正中央 */
    .auth-wrapper {
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0;
        padding: 0;
    }
    .auth-container {
        width: 380px;
        max-width: 90%;
        padding: 40px 32px;
        background: rgba(30, 41, 59, 0.75);
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        backdrop-filter: blur(8px);
        text-align: center;
    }
    
    /* 輸入框 */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }
    
    /* 8格輸入排版 */
    div[data-testid="stHorizontalBlock"] { gap: 0.6rem !important; }
    
    /* 報告區塊 */
    .report-container {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 28px;
        margin-top: 24px;
    }
    
    /* 按鈕 - 統一改回藍色科技風 */
    .stButton>button, .stFormSubmitButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px !important;
        width: 100% !important;
        transition: all 0.2s;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background: linear-gradient(90deg, #0369a1 0%, #0ea5e9 100%) !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 密碼驗證（支援 Enter + 螢幕正中間） ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # 使用 wrapper 強制垂直水平置中
        st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
        st.markdown("""
            <div class='auth-container'>
                <h3>🔐 系統登入</h3>
                <p class='sub-text' style='margin: 12px 0 28px;'>請輸入密碼繼續</p>
        """, unsafe_allow_html=True)

        with st.form(key="login_form", clear_on_submit=False):
            password = st.text_input(
                "訪問密碼",
                type="password",
                placeholder="輸入密碼...",
                label_visibility="collapsed"
            )
            submit = st.form_submit_button("確認登入", use_container_width=True)

            if submit:
                if password == "1234":  # ← 請改成你想要的密碼 或使用 st.secrets
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤，請再試一次。")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # 關閉 wrapper
        return False

    return True

# --- 4. 主程式 ---
if check_password():
    # AI 模型設定
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        ai_model = genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"無法連線到 AI 模型：{e}\n請確認 Secrets 中的 GEMINI_API_KEY 是否正確。")
        st.stop()

    st.title("🛡️ AI 智慧比對顧問")
    st.markdown("<p class='sub-text'>HIOKI 專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    st.markdown("#### 📋 待分析型號（至少填入 2 個）")

    with st.form(key="analysis_form"):
        product_names = []
        for r in range(2):
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                with cols[c]:
                    name = st.text_input(
                        "",
                        placeholder=f"型號 {idx+1}",
                        key=f"prod_{idx}",
                        label_visibility="collapsed"
                    )
                    if name.strip():
                        product_names.append(name.strip())

        submitted = st.form_submit_button("✨ 啟動 AI 深度比對分析", use_container_width=True)

        if submitted:
            valid_products = [p for p in product_names if p]
            if len(valid_products) < 2:
                st.warning("請至少輸入兩個有效型號。")
            else:
                with st.spinner("正在進行深度比對分析..."):
                    prompt = (
                        f"你是 HIOKI 專業儀器專家。請針對以下型號進行詳細比較：{', '.join(valid_products)}。\n"
                        "請用繁體中文回覆，並包含：\n"
                        "1. 規格對照表（量程、精度、分辨率、主要功能、尺寸、重量、適用場景等）\n"
                        "2. 各型號技術差異與優缺點分析\n"
                        "3. 針對不同使用情境的選購建議（例如：生產線、實驗室、現場維護）\n"
                        "4. 總結推薦順序（若適用）"
                    )

                    try:
                        response = ai_model.generate_content(prompt)
                        st.markdown('<div class="report-container">', unsafe_allow_html=True)
                        st.subheader("📊 分析報告")
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.success("分析完成")
                    except Exception as e:
                        st.error(f"分析失敗：{str(e)}")

    with st.sidebar:
        st.markdown("### ⚙️ 系統狀態")
        st.success("🔒 已登入")
        if st.button("登出"):
            st.session_state["password_correct"] = False
            st.rerun()
