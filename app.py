import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide", page_icon="🛡️")

# --- 2. 科技感 CSS (優化對齊與視覺) ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; font-family: 'Inter', sans-serif; }
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #e2e8f0;
    }
    /* 登入容器置中與美化 */
    .auth-container {
        max-width: 450px;
        margin: 80px auto;
        padding: 40px;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        text-align: center;
    }
    /* 標題與輸入框優化 */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem !important;
        font-weight: 800;
        text-align: center;
    }
    .stTextInput input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 10px !important;
    }
    /* 報告區塊 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* 按鈕樣式 */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("### 🔐 系統安全存取")
        st.markdown("<p style='color:#94a3b8;'>請輸入授權金鑰以啟動 HIOKI 分析顧問</p>", unsafe_allow_html=True)
        
        # 使用 form 讓登入也能按 Enter
        with st.form("login_form"):
            password = st.text_input("密碼", type="password", placeholder="Password", label_visibility="collapsed")
            submit = st.form_submit_button("登入系統")
            if submit:
                if password == "1234":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤，請重新輸入")
        st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

# --- 4. 主要程式邏輯 ---
if check_password():
    # AI 模型配置 (修正 404 問題)
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # 修正點：使用不帶 'models/' 的簡潔名稱
        ai_model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API 初始化失敗: {e}")
        st.stop()

    st.markdown("<h1 class='main-title'>🛡️ AI 智慧比對顧問</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>HIOKI 專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    # --- 使用 Form 封裝輸入框，實現按 Enter 啟動 ---
    with st.form("comparison_form"):
        st.markdown("#### 📋 待分析型號")
        product_names = []
        for r in range(2):
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                with cols[c]:
                    name = st.text_input("", placeholder=f"型號 {idx+1}", key=f"p{idx}", label_visibility="collapsed")
                    product_names.append(name)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("✨ 啟動 AI 深度比對分析")

    # 執行比對邏輯
    if submit_btn:
        valid_list = [n.strip() for n in product_names if n.strip() != ""]
        if len(valid_list) < 2:
            st.warning("⚠️ 請輸入至少兩個型號進行比對。")
        else:
            with st.spinner('🔍 正在檢索 HIOKI 技術規範並分析中...'):
                prompt = f"你是一位精密儀器專家。請詳細比對：{', '.join(valid_list)}。請製作規格對照表、分析技術差異、並給予選購建議。請用繁體中文回答。"
                try:
                    response = ai_model.generate_content(prompt)
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.subheader("📊 分析報告")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.success("分析完成！")
                except Exception as e:
                    st.error(f"分析失敗：{e}")

    # 側邊欄
    with st.sidebar:
        st.markdown("### ⚙️ 系統狀態")
        st.success("🔒 安全連線中")
        if st.button("登出系統"):
            st.session_state["password_correct"] = False
            st.rerun()
