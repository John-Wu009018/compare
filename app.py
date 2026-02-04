import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感 CSS (集中對齊與流光按鈕優化) ---
st.markdown("""
    <style>
    /* 全域縮小與字體設定 */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* 隱藏預設元件 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* --- 登入頁面完全置中方案 --- */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 70vh; /* 設定視窗高度比例 */
        width: 100%;
    }
    
    .auth-container {
        width: 400px;
        padding: 40px;
        background: rgba(30, 41, 59, 0.7);
        border-radius: 24px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        text-align: center;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
    }

    /* --- 科技藍按鈕：流光與動畫效果 --- */
    /* 定位所有 Streamlit 按鈕，特別是 Primary 按鈕 */
    div.stButton > button {
        position: relative !important;
        background: linear-gradient(90deg, #0369a1 0%, #0ea5e9 50%, #0369a1 100%) !important;
        background-size: 200% auto !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4) !important;
    }

    /* 1. 跑馬燈光流動效果 */
    div.stButton > button:hover {
        background-position: right center !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.6) !important;
        transform: translateY(-2px) scale(1.02);
    }

    /* 2. 點選縮放動畫 */
    div.stButton > button:active {
        transform: scale(0.95) !important;
        transition: 0.1s !important;
    }

    /* 3. 內切流光掃描線 */
    div.stButton > button::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -60%;
        width: 20%;
        height: 200%;
        background: rgba(255, 255, 255, 0.2);
        transform: rotate(30deg);
        transition: none;
    }

    div.stButton > button:hover::after {
        left: 120%;
        transition: all 0.7s ease-in-out;
    }

    /* 輸入框美化 */
    .stTextInput input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
        text-align: center;
    }
    
    /* 報告區塊 */
    .report-container {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 (結構調整為置中) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # 使用 auth-wrapper 來達成全畫面置中
        st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("<h3>🔐 系統安全驗證</h3>", unsafe_allow_html=True)
        st.markdown("<p class='sub-text'>請輸入訪問代碼以啟動 AI 顧問</p>", unsafe_allow_html=True)

        with st.form(key="login_form"):
            password = st.text_input("Password", type="password", placeholder="請輸入密碼", label_visibility="collapsed")
            submit = st.form_submit_button("進入系統")

            if submit:
                if password == "1234":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤，請重新輸入")
        
        st.markdown("</div>", unsafe_allow_html=True)
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

