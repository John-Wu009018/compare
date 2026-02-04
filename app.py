import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide", page_icon="🛡️")

# --- 2. 科技感 CSS (確保排版對齊) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%); color: #e2e8f0; }
    .main-title { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.2rem !important; font-weight: 800; text-align: center; }
    .auth-container { max-width: 400px; margin: 80px auto; padding: 40px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 20px; text-align: center; }
    .report-container { background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 25px; margin-top: 20px; }
    div[data-testid="stFormSubmitButton"]>button { background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%) !important; color: white !important; border: none !important; width: 100%; height: 45px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("### 🔐 智慧顧問存取")
        with st.form("login_gate"):
            password = st.text_input("輸入密碼", type="password")
            if st.form_submit_button("登入"):
                if password == "1234":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤")
        st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

# --- 4. 主要邏輯 ---
if check_password():
    # 修正 404：嘗試多種可能的模型名稱名稱格式
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 這裡不直接初始化模型，等按下按鈕再初始化，增加彈性
    except Exception as e:
        st.error(f"API 設定錯誤: {e}")
        st.stop()

    st.markdown("<h1 class='main-title'>🛡️ AI 智慧比對顧問</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>HIOKI 專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    with st.form("analysis_form"):
        st.markdown("#### 📋 待分析型號 (輸入後按 Enter 即可啟動)")
        product_names = []
        for r in range(2):
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                product_names.append(cols[c].text_input("", placeholder=f"型號 {idx+1}", key=f"p{idx}", label_visibility="collapsed"))
        
        submit_btn = st.form_submit_button("✨ 啟動 AI 深度比對分析")

    if submit_btn:
        valid_list = [n.strip() for n in product_names if n.strip() != ""]
        if len(valid_list) < 2:
            st.warning("⚠️ 請輸入至少兩個型號。")
        else:
            with st.spinner('🔍 正在嘗試連線至最佳分析模型...'):
                # 嘗試模型列表 (由新到舊)
                models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
                response = None
                error_msg = ""
                
                for m_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(m_name)
                        prompt = f"你是一位精密儀器專家。請詳細比對：{', '.join(valid_list)}。請製作規格對照表、分析技術差異、並給予選購建議。請用繁體中文回答。"
                        response = model.generate_content(prompt)
                        if response: break # 成功就跳出迴圈
                    except Exception as e:
                        error_msg = str(e)
                        continue # 失敗就試下一個
                
                if response:
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.subheader("📊 分析報告")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.success(f"分析完成 (由 {m_name} 驅動)")
                else:
                    st.error(f"分析失敗。請確認 API Key 是否有效。最後一個錯誤訊息：{error_msg}")

    with st.sidebar:
        st.markdown("### ⚙️ 系統狀態")
        st.success("🔒 安全加密連線")
        if st.button("登出系統"):
            st.session_state["password_correct"] = False
            st.rerun()
