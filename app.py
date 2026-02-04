import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 精準控制視覺的 CSS ---
st.markdown("""
    <style>
    /* 移除頂部空白與原生 Header */
    [data-testid="stHeader"] {display: none;}
    .block-container {
        padding-top: 2rem !important; 
        max-width: 800px !important; /* 限制整體內容寬度，避免拉太長 */
        margin: 0 auto !important;
    }
    
    /* 全域文字縮小至 80% */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* 登入框絕對幾何置中 */
    .auth-wrapper {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
    }
    .auth-container {
        width: 280px;
        padding: 30px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
        text-align: center;
    }

    /* 讓 8 格輸入框區塊靠中且不要拉長 */
    .input-grid-container {
        max-width: 600px;
        margin: 0 auto;
    }

    /* 輸入框對齊與樣式 */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 6px !important;
        height: 32px !important;
        text-align: center;
    }

    /* 分析報告容器 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }

    /* 按鈕置中且控制寬度 */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white; border: none; border-radius: 6px; font-weight: 600;
        width: 200px; margin: 0 auto; display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-wrapper'><div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("### 🔐 私密訪問")
        pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed", placeholder="請輸入訪問密碼")
        if st.button("ENTER"):
            if pwd == "1234": 
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("密碼錯誤")
        st.markdown("</div></div>", unsafe_allow_html=True)
        return False
    return True

# --- 4. 主程式 ---
if check_password():
    # AI 設定
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        ai_model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.error("系統配置異常")
        st.stop()

    # 置中標題
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.title("🛡️ AI 智慧比對顧問")
    st.markdown("<p style='color:#94a3b8;'>專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 限制 8 格輸入框的寬度
    st.markdown("<div class='input-grid-container'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-weight:bold; margin-bottom:10px;'>📋 請輸入待分析型號</p>", unsafe_allow_html=True)
    
    product_names = []
    # 使用 2x4 佈局，但被外層 container 限制寬度，所以不會拉很長
    for r in range(2):
        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            with cols[c]:
                name = st.text_input("", placeholder=f"#{idx+1}", key=f"p{idx}", label_visibility="collapsed")
                product_names.append(name)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✨ 啟動深度分析"):
        valid_list = [n.strip() for n in product_names if n.strip() != ""]
        if len(valid_list) < 2:
            st.warning("⚠️ 請輸入至少兩個型號。")
        else:
            with st.spinner('🔍 正在檢索數據...'):
                try:
                    prompt = f"你是一位精密量測儀器專家。請針對以下產品進行深度比對：{', '.join(valid_list)}。請製作規格對照表格、分析技術核心差異、並給予專業應用建議。請使用繁體中文。"
                    response = ai_model.generate_content(prompt)
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"分析失敗：{e}")
    st.markdown("</div>", unsafe_allow_html=True)

    # 側邊欄
    with st.sidebar:
        st.markdown("### ⚙️ 系統狀態")
        st.success("🔒 安全存取中")
        if st.button("登出退出"):
            st.session_state["password_correct"] = False
            st.rerun()
