import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感 CSS (按鍵全面優化版) ---
st.markdown("""
    <style>
    /* 全域設定 */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    .stApp { background: #0f172a; color: #e2e8f0; }

    /* --- 核心：藍色跑馬燈效果按鈕 --- */
    /* 同時針對普通按鈕與 Primary 按鈕 */
    div.stButton > button {
        position: relative !important;
        width: 100% !important;
        /* 漸層背景：深藍 - 亮藍 - 深藍 */
        background: linear-gradient(90deg, #0369a1, #38bdf8, #0ea5e9, #0369a1) !important;
        background-size: 300% 100% !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        transition: all 0.4s ease !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3) !important;
        /* 動畫：持續流動的跑馬燈光 */
        animation: aurora-flow 6s linear infinite !important;
    }

    /* 跑馬燈動畫定義 */
    @keyframes aurora-flow {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    /* 滑鼠懸停：加速流動並上浮 */
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.5) !important;
        animation: aurora-flow 2s linear infinite !important; /* 懸停時流速變快 */
    }

    /* 點選效果：物理縮放回彈 */
    div.stButton > button:active {
        transform: scale(0.96) !important;
    }

    /* 閃光掃描線特效 (橫向劃過) */
    div.stButton > button::before {
        content: "";
        position: absolute;
        top: 0; left: -150%;
        width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transform: skewX(-20deg);
        transition: 0.6s;
    }
    div.stButton > button:hover::before {
        left: 150%;
        transition: 0.6s ease-in-out;
    }

    /* 側邊欄按鈕特殊處理 (確保風格一致) */
    [data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #1e40af, #3b82f6, #1e40af) !important;
        background-size: 200% auto !important;
    }

    /* 登入容器置中優化 */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 10vh;
    }
    .auth-container {
        width: 380px;
        padding: 45px;
        background: rgba(30, 41, 59, 0.7);
        border-radius: 24px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        backdrop-filter: blur(15px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        text-align: center;
    }

    /* 輸入框質感 */
    .stTextInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 登入邏輯 (配合置中 CSS) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#38bdf8; margin-bottom:0;'>HIOKI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:0.8rem; margin-bottom:30px;'>AI 數據分析系統</p>", unsafe_allow_html=True)

        with st.form(key="login_form"):
            password = st.text_input("密碼", type="password", placeholder="請輸入訪問代碼", label_visibility="collapsed")
            submit = st.form_submit_button("進入系統") # 此按鈕會自動套用上面的藍色流動效果

            if submit:
                if password == "1234":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤")
        
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



