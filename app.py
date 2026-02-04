import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感極簡 CSS ---
st.markdown("""
    <style>
    /* 移除頂部空白與原生裝飾 */
    [data-testid="stHeader"] {display: none;}
    .block-container {
        padding-top: 1.5rem !important; 
        padding-bottom: 1rem !important;
    }
    
    /* 全域文字縮小至約 80% */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* 隱藏預設選單與頁尾 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 登入框絕對置中 */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60vh;
    }
    .auth-container {
        width: 300px;
        padding: 30px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
        text-align: center;
    }

    /* 標題與副標題樣式 */
    h1 { color: #38bdf8 !important; font-size: 1.6rem !important; font-weight: 800; margin-bottom: 0px !important; }
    .sub-text { color: #94a3b8; font-size: 0.85rem; margin-bottom: 25px; }

    /* 輸入框排版緊湊 */
    div[data-testid="stHorizontalBlock"] { gap: 0.4rem !important; }
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 6px !important;
        height: 32px !important;
    }

    /* 報告區塊玻璃擬態 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }

    /* 按鈕樣式 */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white; border: none; border-radius: 6px; font-weight: 600; width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
            st.markdown("### 🔐 私密訪問")
            # 這裡設定您的密碼，目前預設為 1234
            pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed", placeholder="請輸入訪問密碼")
            if st.button("登入系統"):
                if pwd == "1234": 
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

# --- 4. 主程式執行 ---
if check_password():
    # AI 模型配置與自動偵測
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # 優先選擇 flash 1.5
        model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        ai_model = genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"系統連線異常，請聯繫管理員。")
        st.stop()

    # 頂部標題區
    st.title("🛡️ AI 智慧比對顧問")
    st.markdown("<p class='sub-text'>HIOKI 專業量測儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    # 固定 8 格輸入框 (4x2 矩陣)
    st.markdown("##### 📋 待分析型號輸入")
    product_names = []
    for r in range(2):
        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            with cols[c]:
                name = st.text_input("", placeholder=f"型號 {idx+1}", key=f"p{idx}", label_visibility="collapsed")
                product_names.append(name)

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    # 分析按鈕
    if st.button("✨ 啟動深度分析報告"):
        valid_list = [n.strip() for n in product_names if n.strip() != ""]
        if len(valid_list) < 2:
            st.warning("⚠️ 請輸入至少兩個型號進行比對。")
        else:
            with st.spinner('🔍 正在檢索技術文件並合成數據...'):
                prompt = f"你是一位精密量測儀器專家。請針對以下產品進行深度比對：{', '.join(valid_list)}。請製作規格對照表格、分析技術核心差異、並給予專業應用建議。請使用繁體中文。"
                try:
                    response = ai_model.generate_content(prompt)
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:#38bdf8; font-size:1.2rem;'>📊 技術分析報告：{ ' vs '.join(valid_list) }</h3>", unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.success("分析報告產出成功。")
                except Exception as e:
                    st.error(f"分析失敗：{e}")

    # 側邊欄狀態顯示
    with st.sidebar:
        st.markdown("### ⚙️ 系統資訊")
        st.info("已啟動加密存取控制")
        st.markdown(f"**核心模型:** \n`{model_name.split('/')[-1]}`")
        if st.button("登出"):
            st.session_state["password_correct"] = False
            st.rerun()
        st.divider()
        st.caption("© 2026 AI Intelligence Consultant")
