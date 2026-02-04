# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感 CSS (修正頂部空白與置中登入框) ---
st.markdown("""
    <style>
    /* 移除頂部空白 */
    .block-container {
        padding-top: 2rem !important; 
        padding-bottom: 1rem !important;
    }
    
    /* 全域縮小比例 */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* 隱藏預設元件 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} /* 隱藏頂部裝飾線 */

    /* 登入框絕對置中樣式 */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 70vh; /* 讓它在視窗中間 */
    }
    .auth-container {
        width: 320px;
        padding: 25px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        text-align: center;
    }

    /* 輸入框排版緊湊化 */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 (修改為置中模式) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # 使用 HTML 容器包裹來達成置中
        st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
            st.markdown("### 🔐 私密訪問")
            password = st.text_input("PASSWORD", type="password", label_visibility="collapsed", placeholder="請輸入密碼")
            if st.button("ENTER"):
                if password == "1234": # 您可以自行修改密碼
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True
