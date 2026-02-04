import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 幾何置中與極簡科技 CSS ---
st.markdown("""
    <style>
    /* 移除所有預設間距與 Header */
    [data-testid="stHeader"], [data-testid="stSidebarNav"] {display: none;}
    .block-container { padding: 0 !important; }
    
    /* 全域文字縮小 80% */
    html, body, [class*="css"] { 
        font-size: 13.5px !important; 
        overflow: hidden; /* 防止登入頁面出現滾動條 */
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* 登入框：絕對幾何置中 */
    .auth-wrapper {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        width: 300px;
    }
    .auth-container {
        padding: 30px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
        text-align: center;
    }

    /* 主頁面佈局調整 (登入後) */
    .main-content {
        padding: 2rem 5rem !important;
    }

    /* 輸入框對齊與精緻化 */
    div[data-testid="stHorizontalBlock"] { 
        align-items: flex-end !important; /* 確保垂直對齊線條一致 */
        gap: 0.5rem !important; 
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 6px !important;
        height: 35px !important;
        text-align: center; /* 文字置中輸入 */
    }

    /* 分析報告容器 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 25px;
        margin-top: 20px;
        overflow-y: auto;
        max-height: 60vh;
    }

    /* 按鈕樣式 */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white; border: none; border-radius: 6px; font-weight: 600; 
        height: 35px !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 (幾何置中版) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("### 🔐 私密訪問")
        pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed", placeholder="請輸入訪問密碼")
        if st.button("登入系統"):
            if pwd == "1234": # 密碼可在此修改
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("密碼錯誤")
        st.markdown("</div></div>", unsafe_allow_html=True)
        return False
    return True

# --- 4. 主程式 ---
if check_password():
    # 允許登入後內容滾動
    st.markdown("<style>html, body { overflow: auto !important; }</style>", unsafe_allow_html=True)

    # AI 設定
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        ai_model = genai.GenerativeModel(model_name)
    except:
        st.error("系統配置異常")
        st.stop()

    # 介面渲染
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("🛡️ AI 智慧比對顧問")
    st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>HIOKI 專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    # 8 格輸入框
    st.markdown("##### 📋 待分析型號")
    product_names = []
    for r in range(2):
        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            with cols[c]:
                name = st.text_input("", placeholder=f"型號 {idx+1}", key=f"p{idx}", label_visibility="collapsed")
                product_names.append(name)

    if st.button("✨ 啟動深度分析報告"):
        valid_list = [n.strip() for n in product_names if n.strip() != ""]
        if len(valid_list) < 2:
            st.warning("⚠️ 請輸入至少兩個型號。")
        else:
            with st.spinner('🔍 正在檢索數據...'):
                try:
                    prompt = f"你是一位精密量測儀器專家。請針對以下產品進行深度比對：{', '.join(valid_list)}。請製作規格對照表格、分析技術差異、並給予專業建議。請使用繁體中文。"
                    response = ai_model.generate_content(prompt)
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:#38bdf8;'>📊 技術分析報告：{ ' vs '.join(valid_list) }</h3>", unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"分析失敗：{e}")
    st.markdown("</div>", unsafe_allow_html=True)

    # 側邊欄
    with st.sidebar:
        st.markdown("### ⚙️ 系統資訊")
        st.caption(f"模型版本: {model_name.split('/')[-1]}")
        if st.button("登出退出"):
            st.session_state["password_correct"] = False
            st.rerun()
