import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感 CSS (優化版：含流光按鈕動畫) ---
st.markdown("""
    <style>
    /* 全域縮小至約 80% */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    
    /* 隱藏預設元件 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 標題與文字 */
    h1 { color: #38bdf8 !important; font-size: 1.7rem !important; font-weight: 800; text-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }
    .sub-text { color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }
    
    /* 登入容器 */
    .auth-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        background: rgba(30, 41, 59, 0.7);
        border-radius: 20px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
    }
    
    /* 輸入框優化 */
    .stTextInput input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4) !important;
    }

    /* --- 流光按鈕核心 CSS --- */
    div.stButton > button {
        position: relative;
        overflow: hidden;
        background: linear-gradient(90deg, #0284c7, #38bdf8, #0284c7) !important;
        background-size: 200% auto !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3);
        cursor: pointer;
    }

    /* 跑馬燈光效果 (流動感) */
    div.stButton > button:hover {
        background-position: right center !important; /* 背景滑動 */
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5);
        transform: translateY(-2px);
    }

    /* 點選動畫 (縮小回彈) */
    div.stButton > button:active {
        transform: scale(0.96);
        box-shadow: 0 2px 10px rgba(2, 132, 199, 0.2);
    }

    /* 閃光掃描效果 (偽元素) */
    div.stButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            120deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transition: all 0.6s;
    }

    div.stButton > button:hover::before {
        left: 100%;
    }

    /* 報告區塊 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯（支援 Enter 鍵） ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("""
            <div class='auth-container'>
                <h3>🔐 私密訪問控制</h3>
                <p class='sub-text' style='margin: 10px 0 25px;'>請輸入密碼繼續使用</p>
        """, unsafe_allow_html=True)

        with st.form(key="login_form", clear_on_submit=False):
            password = st.text_input(
                "訪問密碼",
                type="password",
                placeholder="輸入密碼...",
                label_visibility="collapsed"
            )
            submit = st.form_submit_button("確認登入", use_container_width=True)

            if submit or (st.session_state.get("login_attempted", False) and password):
                if password == "1234":  # ← 請在此修改為你的真實密碼，或改用 st.secrets
                    st.session_state["password_correct"] = True
                    st.session_state.pop("login_attempted", None)
                    st.rerun()
                else:
                    st.error("密碼錯誤，請聯繫管理員。")
                    st.session_state["login_attempted"] = True

        st.markdown("</div>", unsafe_allow_html=True)
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
        st.error(f"API 連線失敗：{e}\n請檢查 Secrets 中的 GEMINI_API_KEY 是否正確設定。")
        st.stop()

    # 頁面標題
    st.title("🛡️ AI 智慧比對顧問")
    st.markdown("<p class='sub-text'>HIOKI 專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    st.markdown("#### 📋 待分析型號（至少輸入 2 個）")

    # 使用 form 包裝所有輸入，讓 Enter 鍵可直接觸發分析
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
                        key=f"product_{idx}",
                        label_visibility="collapsed"
                    )
                    product_names.append(name.strip())

        # 提交按鈕
        submitted = st.form_submit_button("✨ 啟動 AI 深度比對分析", use_container_width=True, type="primary")

        if submitted:
            valid_products = [p for p in product_names if p]
            if len(valid_products) < 2:
                st.warning("⚠️ 請至少輸入兩個有效型號。")
            else:
                with st.spinner("🔍 正在檢索全球數據並進行深度分析..."):
                    prompt = (
                        f"你是一位精密儀器專家，專精 HIOKI 產品。請針對以下型號進行詳細比對：{', '.join(valid_products)}。\n"
                        "請用繁體中文回覆，並包含以下內容：\n"
                        "1. 規格對照表（量程、精度、分辨率、功能、尺寸、重量、價格區間等）\n"
                        "2. 各型號主要技術差異與優勢分析\n"
                        "3. 針對不同使用情境（例如：生產線檢測、實驗室校正、現場維護）的選購建議\n"
                        "4. 總結推薦排名（若適用）"
                    )

                    try:
                        response = ai_model.generate_content(prompt)
                        st.markdown('<div class="report-container">', unsafe_allow_html=True)
                        st.subheader("📊 AI 深度分析報告")
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.success("分析完成！")
                    except Exception as e:
                        st.error(f"分析失敗：{str(e)}")

    # 側邊欄
    with st.sidebar:
        st.markdown("### ⚙️ 系統狀態")
        st.success("🔒 已受保護的私密連線")
        if st.button("登出系統"):
            st.session_state["password_correct"] = False
            st.rerun()
