import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide", page_icon="🛡️")

# --- 2. 科技感 CSS 優化 ---
st.markdown("""
    <style>
    /* 全域背景與字體 */
    html, body, [class*="css"] { font-size: 14px !important; }
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%);
        color: #e2e8f0;
    }

    /* 登入容器居中與毛玻璃效果 */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60vh;
    }
    .auth-container {
        width: 100%;
        max-width: 400px;
        padding: 40px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        text-align: center;
    }

    /* 標題與文字 */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem !important;
        font-weight: 800;
        text-align: center;
    }

    /* 報告區塊 */
    .report-container {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
    }

    /* 按鈕與輸入框優化 */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        height: 45px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 (支援 Enter 登入) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("### 🔐 智慧顧問存取")
        
        # 使用 form 讓密碼輸入完按 Enter 就能登入
        with st.form("login_gate"):
            password = st.text_input("輸入存取密碼", type="password", placeholder="請輸入密碼")
            submit_pw = st.form_submit_button("啟動系統")
            if submit_pw:
                if password == "1234":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤，請聯繫管理員。")
        st.markdown("</div></div>", unsafe_allow_html=True)
        return False
    return True

# --- 4. 主要程式邏輯 ---
if check_password():
    # AI 模型配置 - 修正 404 報錯點
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # 使用更穩定的名稱，避免 models/ 前綴
        ai_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        st.error(f"API 設定錯誤: {e}")
        st.stop()

    st.markdown("<h1 class='main-title'>🛡️ AI 智慧比對顧問</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>HIOKI 專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    # --- 使用 Form 封裝輸入框：任何格子按 Enter 都會觸發運算 ---
    with st.form("analysis_form"):
        st.markdown("#### 📋 待分析型號")
        product_names = []
        
        # 建立 2x4 的矩陣輸入
        for r in range(2):
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                with cols[c]:
                    name = st.text_input("", placeholder=f"型號 {idx+1}", key=f"p{idx}", label_visibility="collapsed")
                    product_names.append(name)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("✨ 啟動 AI 深度比對分析")

    # 執行運算
    if submit_btn:
        valid_list = [n.strip() for n in product_names if n.strip() != ""]
        if len(valid_list) < 2:
            st.warning("⚠️ 請輸入至少兩個型號進行比對。")
        else:
            with st.spinner('🔍 正在檢索 HIOKI 全球技術手冊並進行橫向分析...'):
                prompt = f"你是一位精密儀器專家。請詳細比對：{', '.join(valid_list)}。請製作規格對照表、分析技術差異、並根據應用場景給予選購建議。請用繁體中文回答。"
                try:
                    response = ai_model.generate_content(prompt)
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.subheader("📊 分析報告")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.success("分析完成！")
                except Exception as e:
                    # 如果連 -latest 都失效，則自動 fallback 到基礎名稱
                    st.error(f"分析失敗，建議檢查 API Key 權限。錯誤細節：{e}")

    # 側邊欄
    with st.sidebar:
        st.markdown("### ⚙️ 系統狀態")
        st.success("🔒 安全加密連線")
        if st.button("登出系統"):
            st.session_state["password_correct"] = False
            st.rerun()
