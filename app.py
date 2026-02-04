import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感 CSS (按鍵全面優化版 + 登入頁面頂部置中強化) ---
st.markdown("""
    <style>
    /* 全域設定 - 縮小字體80% + 深藍科技背景 */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #e2e8f0;
        background-attachment: fixed;
    }
    
    /* 隱藏Streamlit預設元件 */
    #MainMenu, footer { visibility: hidden !important; }
    .stToolbar { visibility: hidden !important; }

    /* ===========================================
       登入頁面 - 頂部置中 + 極致科技質感 
       =========================================== */
.auth-wrapper {
    ...
    justify-content: flex-start;
    min-height: auto;              /* 移除固定高度 */
    padding-bottom: 10vh;
}

    /* 登入頁面科技網格背景 + 微粒子效果 */
    .auth-wrapper::before {
        content: "";
        position: absolute;
        inset: 0;
        background: 
            /* 科技網格 */
            radial-gradient(circle at 20% 30%, rgba(56,189,248,0.06) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(14,165,233,0.05) 0%, transparent 35%),
            radial-gradient(circle at 50% 10%, rgba(59,130,246,0.04) 0%, transparent 30%),
            /* 微粒子 */
            radial-gradient(circle at 10% 90%, rgba(255,255,255,0.02) 0%, transparent 20%);
        pointer-events: none;
        z-index: 0;
        animation: particles 20s linear infinite;
    }

    @keyframes particles {
        0%, 100% { transform: rotate(0deg) scale(1); opacity: 0.6; }
        50% { transform: rotate(180deg) scale(1.1); opacity: 0.8; }
    }

    .auth-container {
        width: 420px;
        max-width: 95%;
        padding: 55px 45px;
        background: linear-gradient(145deg, 
            rgba(30,41,59,0.85) 0%, 
            rgba(15,23,42,0.95) 50%, 
            rgba(30,41,59,0.8) 100%);
        border-radius: 28px;
        border: 1px solid rgba(56,189,248,0.3);
        backdrop-filter: blur(20px) saturate(160%);
        box-shadow: 
            0 30px 80px -20px rgba(0,0,0,0.7),
            0 0 0 1px rgba(56,189,248,0.2) inset,
            0 0 60px rgba(56,189,248,0.15),
            inset 0 1px 0 rgba(255,255,255,0.1);
        position: relative;
        z-index: 2;
        overflow: hidden;
    }

    /* 容器頂部掃描光條 */
    .auth-container::before {
        content: "";
        position: absolute;
        top: 0; left: -120%;
        width: 120%; height: 4px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(56,189,248,0.8), 
            rgba(14,165,233,1), 
            rgba(56,189,248,0.8), 
            transparent);
        border-radius: 0 0 10px 10px;
        animation: scanline-top 7s linear infinite;
    }

    @keyframes scanline-top {
        0% { left: -120%; opacity: 0.7; }
        50% { left: 0%; opacity: 1; }
        100% { left: 100%; opacity: 0.7; }
    }

    /* HIOKI標題 - 呼吸燈 + 3D文字 */
    .auth-container h2 {
        color: #7dd3fc;
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: 4px;
        margin: 0 0 12px 0;
        text-shadow: 
            0 0 25px rgba(56,189,248,0.7),
            0 2px 10px rgba(0,0,0,0.5);
        animation: title-breathe 5s ease-in-out infinite;
        position: relative;
    }

    .auth-container h2::after {
        content: "AI 儀器智慧比對顧問";
        position: absolute;
        top: 2px; left: 2px;
        color: rgba(14,165,233,0.3);
        z-index: -1;
    }

    @keyframes title-breathe {
        0%, 100% { 
            opacity: 0.95; 
            text-shadow: 0 0 25px rgba(56,189,248,0.6), 0 2px 10px rgba(0,0,0,0.5);
            transform: scale(1);
        }
        50% { 
            opacity: 1; 
            text-shadow: 0 0 45px rgba(56,189,248,1), 0 0 60px rgba(14,165,233,0.6), 0 2px 15px rgba(0,0,0,0.6);
            transform: scale(1.03);
        }
    }

    /* 副標題 */
    .auth-container p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 2.5rem;
        letter-spacing: 1px;
        font-weight: 500;
    }

    /* 輸入框 - 科技光暈 + 掃描邊框 */
    .stTextInput input {
        background: linear-gradient(145deg, rgba(15,23,42,0.8), rgba(30,41,59,0.6)) !important;
        border: 1.5px solid rgba(56,189,248,0.25) !important;
        border-radius: 16px !important;
        color: #e0f2fe !important;
        padding: 18px 20px !important;
        font-size: 1.1rem !important;
        text-align: center;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 0 0 4px rgba(56,189,248,0.1) inset,
            0 4px 20px rgba(0,0,0,0.3);
        position: relative;
    }

    .stTextInput input::placeholder {
        color: rgba(148,163,184,0.6) !important;
        font-style: italic;
    }

    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 
            0 0 0 4px rgba(56,189,248,0.4),
            0 0 0 8px rgba(56,189,248,0.15),
            0 8px 35px rgba(56,189,248,0.3),
            0 0 0 4px rgba(56,189,248,0.1) inset !important;
        background: linear-gradient(145deg, rgba(15,23,42,0.95), rgba(30,41,59,0.75)) !important;
        transform: translateY(-1px);
    }

    /* 登入按鈕 - 藍色能量核心版 */
    div.stButton > button:has(form[key="login_form"]) {
        position: relative !important;
        width: 100% !important;
        background: linear-gradient(90deg, #0369a1, #0ea5e9, #38bdf8, #0ea5e9, #0369a1) !important;
        background-size: 400% 100% !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 18px 32px !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        letter-spacing: 2px !important;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        overflow: hidden !important;
        box-shadow: 
            0 8px 35px rgba(14,165,233,0.4),
            inset 0 1px 0 rgba(255,255,255,0.3) !important;
        animation: login-flow 8s linear infinite !important;
    }

    @keyframes login-flow {
        0% { background-position: 0% 50%; }
        100% { background-position: 400% 50%; }
    }

    div.stButton > button:has(form[key="login_form"]):hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 
            0 20px 50px rgba(56,189,248,0.6),
            0 0 60px rgba(14,165,233,0.4),
            inset 0 1px 0 rgba(255,255,255,0.4) !important;
        animation-duration: 2.5s !important;
    }

    div.stButton > button:has(form[key="login_form"]):active {
        transform: scale(0.96) !important;
        animation-play-state: paused !important;
    }

    /* 登入按鈕掃描光效 */
    div.stButton > button:has(form[key="login_form"])::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,255,255,0.3), 
            transparent);
        transition: left 0.7s;
    }

    div.stButton > button:has(form[key="login_form"]):hover::before {
        left: 100%;
    }

    /* 錯誤訊息優化 */
    .st-emotion-cache-1axtus3 {
        background: rgba(239,68,68,0.15) !important;
        border: 1px solid rgba(239,68,68,0.4) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }

    /* ===========================================
       主頁面 AI分析按鈕 - 頂級藍色燈光脈衝
       =========================================== */
    div.stButton > button[kind="primary"],
    div.stButton > button[type="primary"] {
        position: relative !important;
        width: 100% !important;
        max-width: 480px !important;
        margin: 2rem auto !important;
        display: block !important;
        background: linear-gradient(90deg, 
            #0369a1 0%, 
            #0ea5e9 20%, 
            #38bdf8 40%, 
            #60a5fa 60%, 
            #38bdf8 80%, 
            #0369a1 100%) !important;
        background-size: 400% 100% !important;
        animation: ai-gradient-flow 6s ease infinite !important;
        color: white !important;
        font-size: 1.25rem !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        padding: 22px 40px !important;
        border: none !important;
        border-radius: 24px !important;
        box-shadow: 
            0 12px 45px rgba(56,189,248,0.5),
            0 0 0 1px rgba(255,255,255,0.1) inset,
            0 0 80px rgba(14,165,233,0.2);
        transition: all 0.45s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        overflow: hidden !important;
        text-transform: uppercase;
        position: relative;
    }

    @keyframes ai-gradient-flow {
        0% { background-position: 0% 50%; }
        100% { background-position: 400% 50%; }
    }

    /* AI按鈕懸停 - 能量脈衝 */
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[type="primary"]:hover {
        transform: translateY(-5px) scale(1.04) !important;
        box-shadow: 
            0 25px 70px rgba(56,189,248,0.7),
            0 0 100px rgba(14,165,233,0.5),
            inset 0 0 20px rgba(255,255,255,0.3) !important;
        animation-duration: 2s !important;
    }

    /* AI按鈕核心脈衝光環 */
    div.stButton > button[kind="primary"]::before,
    div.stButton > button[type="primary"]::before {
        content: "";
        position: absolute;
        inset: 0;
        background: conic-gradient(from 0deg, transparent, rgba(56,189,248,0.3), transparent 60%);
        padding: 2px;
        border-radius: 24px;
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude;
        opacity: 0;
        animation: pulse-ring 3s linear infinite;
        z-index: -1;
    }

    div.stButton > button[kind="primary"]:hover::before,
    div.stButton > button[type="primary"]:hover::before {
        opacity: 1;
        animation-duration: 1.5s;
    }

    @keyframes pulse-ring {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* 按下效果 */
    div.stButton > button[kind="primary"]:active,
    div.stButton > button[type="primary"]:active {
        transform: translateY(-2px) scale(0.98) !important;
        box-shadow: 0 8px 30px rgba(56,189,248,0.5) !important;
    }

    /* 一般按鈕（登出等） */
    div.stButton > button:not([kind="primary"]):not([type="primary"]) {
        background: linear-gradient(90deg, #1e40af, #3b82f6, #1e40af) !important;
        background-size: 200% 100% !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        animation: sidebar-flow 5s linear infinite !important;
    }

    @keyframes sidebar-flow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    /* 輸入框通用優化 */
    .stTextInput input, .stTextArea textarea {
        background: rgba(15,23,42,0.7) !important;
        border: 1px solid rgba(56,189,248,0.2) !important;
        color: #e0f2fe !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56,189,248,0.25) !important;
    }

    /* 表格輸入格子優化 */
    div[style*="grid"] input {
        background: rgba(30,41,59,0.8) !important;
        border-radius: 8px !important;
        text-align: center !important;
        height: 45px !important;
    }

    /* 回報容器 */
    .report-container {
        background: rgba(15,23,42,0.6);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(56,189,248,0.3);
        backdrop-filter: blur(15px);
        margin-top: 2rem;
    }

    /* 側邊欄優化 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%);
        border-right: 1px solid rgba(56,189,248,0.2);
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
        st.markdown("<h2 style='color:#38bdf8; margin-bottom:0;'>AI 儀器智慧比對顧問</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:0.8rem; margin-bottom:30px;'>數據分析系統</p>", unsafe_allow_html=True)

        with st.form(key="login_form"):
            password = st.text_input("密碼", type="password", placeholder="請輸入訪問代碼", label_visibility="collapsed")
            submit = st.form_submit_button("進入系統") # 此按鈕會自動套用上面的藍色流動效果

            if submit:
                if password == "aaaaaaaa":
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
    st.markdown("<p class='sub-text'>HIOKI、FLUKE、FLIR、R&S、RKC、OPTRIS 專業儀器數據分析系統</p>", unsafe_allow_html=True)

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











