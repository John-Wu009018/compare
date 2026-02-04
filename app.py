import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感 CSS (極致質感優化：流光按鈕 + 懸浮登入頁) ---
st.markdown("""
    <style>
    /* 全域字體與背景 */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    
    .stApp {
        background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
        color: #e2e8f0;
    }

    /* 隱藏預設元件 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* --- 1. 高質感登入頁佈局 --- */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 100px; /* 位於螢幕中上方 */
        width: 100%;
    }
    
    .auth-container {
        width: 380px;
        padding: 50px 40px;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 28px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        text-align: center;
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.1), 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(20px);
        position: relative;
    }

    .auth-container::before {
        content: "";
        position: absolute;
        top: -1px; left: -1px; right: -1px; bottom: -1px;
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(56,189,248,0.5) 0%, transparent 40%, transparent 60%, rgba(56,189,248,0.2) 100%);
        z-index: -1;
    }

    /* --- 2. 科技藍流光按鈕 (對應您的紅色按鈕位置) --- */
    /* 強制覆蓋 Streamlit 的 Primary 按鈕顏色 */
    div.stButton > button[kind="primary"], div.stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #0284c7, #38bdf8, #0284c7) !important;
        background-size: 200% auto !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* 滑鼠懸停：流光與上浮 */
    div.stButton > button:hover {
        background-position: right center !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.7) !important;
        transform: translateY(-3px);
    }

    /* 點擊：縮小回彈動畫 */
    div.stButton > button:active {
        transform: scale(0.96) !important;
        box-shadow: 0 0 5px rgba(56, 189, 248, 0.2) !important;
    }

    /* 內部閃光特效 */
    div.stButton > button::after {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: 0.7s;
    }
    div.stButton > button:hover::after {
        left: 100%;
    }

    /* 輸入框質感 */
    .stTextInput input {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: #fff !important;
        border-radius: 12px !important;
        height: 45px;
        text-align: center;
        transition: 0.3s;
    }
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
    }

    /* 報告容器 */
    .report-container {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 24px;
        padding: 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 登入邏輯 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        
        # 標誌性設計
        st.markdown("<h2 style='color:#38bdf8; margin-bottom:5px;'>HIOKI</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-weight:300; color:#94a3b8; margin-bottom:30px;'>AI INTELLIGENCE SYSTEM</h4>", unsafe_allow_html=True)

        with st.form(key="login_form"):
            password = st.text_input("ACCESS CODE", type="password", placeholder="••••••••", label_visibility="collapsed")
            # 這裡的按鈕會自動套用 CSS 中的流光藍色效果
            submit = st.form_submit_button("進入系統")

            if submit:
                if password == "1234":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("認證失敗，請檢查存取代碼。")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
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


