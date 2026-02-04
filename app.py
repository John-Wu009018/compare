import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide", page_icon="🛡️")

# --- 2. 科技感 CSS (優化對齊與視覺) ---
st.markdown("""
    <style>
    /* 全域字體與背景 */
    html, body, [class*="css"] { font-size: 14px !important; font-family: 'Inter', -apple-system, sans-serif; }
    
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #e2e8f0;
    }

    /* 隱藏預設元件 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 標題樣式 */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-text { color: #94a3b8; text-align: center; font-size: 1rem; margin-bottom: 2rem; }

    /* 登入容器優化 */
    .auth-outer {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 10vh;
    }
    .auth-container {
        width: 400px;
        padding: 40px;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        text-align: center;
    }

    /* 輸入框樣式優化 */
    .stTextInput input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4) !important;
    }

    /* 報告區塊玻璃擬態 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
    }

    /* 按鈕樣式 (Form Submit Button) */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        height: 45px;
        width: 100%;
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(56, 189, 248, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 (視覺優化) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # 使用空的 container 來置中
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            st.markdown("<div class='auth-outer'>", unsafe_allow_html=True)
            with st.form("login_form"):
                st.markdown("### 🔐 私密訪問控制")
                st.markdown("<p style='color:#94a3b8;'>請輸入授權密碼以開啟分析系統</p>", unsafe_allow_html=True)
                password = st.text_input("密碼", type="password", label_visibility="collapsed", placeholder="請輸入密碼")
                submit = st.form_submit_button("確認登入")
                if submit:
                    if password == "1234": 
                        st.session_state["password_correct"] = True
                        st.rerun()
                    else:
                        st.error("❌ 密碼錯誤，請聯繫管理員。")
            st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

# --- 4. 主要程式邏輯 ---
if check_password():
    # AI 模型配置 (優化 API Key 讀取)
    # --- 修正後的模型配置區塊 ---
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("未偵測到 API Key")
        st.stop()
        
    genai.configure(api_key=api_key)
    
    # 修正點：直接使用模型名稱，不加 "models/" 前綴
    # 並且改用較穩定的 gemini-1.5-flash-latest 或 gemini-pro
    model_name = 'gemini-1.5-flash' 
    ai_model = genai.GenerativeModel(model_name)
    
except Exception as e:
    st.error(f"系統初始化失敗: {e}")
    st.stop()

    # 頁面標題
    st.markdown("<h1 class='main-title'>🛡️ AI 智慧比對顧問</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>HIOKI 專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    # 使用 st.form 包裹輸入框，達到「按 Enter 執行」的功能
    with st.form("analysis_form", clear_on_submit=False):
        st.markdown("#### 📋 待分析型號 (輸入後按 Enter 即可啟動)")
        
        product_names = []
        # 建立 2x4 的網格
        for r in range(2):
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                with cols[c]:
                    name = st.text_input(
                        f"P{idx}", 
                        placeholder=f"型號 {idx+1}", 
                        key=f"p{idx}", 
                        label_visibility="collapsed"
                    )
                    product_names.append(name)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 表單提交按鈕
        submit_button = st.form_submit_button("✨ 啟動 AI 深度比對分析")

    # 按鈕觸發後的執行邏輯
    if submit_button:
        valid_list = [n.strip() for n in product_names if n.strip() != ""]
        if len(valid_list) < 2:
            st.warning("⚠️ 請輸入至少兩個型號進行比對。")
        else:
            with st.spinner('🔍 正在檢索全球數據並分析中...'):
                prompt = f"""你是一位精密儀器專家，特別精通 HIOKI (日置) 等品牌的測量儀器。
                請詳細比對以下型號：{', '.join(valid_list)}。
                
                輸出要求：
                1. 製作一個規格對照 Markdown 表格。
                2. 分析各型號間的核心技術差異。
                3. 根據不同的應用場景給予選購建議。
                4. 請使用繁體中文。"""
                
                try:
                    response = ai_model.generate_content(prompt)
                    st.markdown('<div class="report-container">', unsafe_allow_html=True)
                    st.subheader("📊 分析報告")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.success("分析完成！")
                except Exception as e:
                    st.error(f"分析失敗：{e}")

    # 側邊欄狀態
    with st.sidebar:
        st.markdown("### ⚙️ 系統狀態")
        st.info(f"Model: `Gemini 1.5 Flash`")
        st.success("🔒 安全連線中")
        if st.button("登出系統"):
            st.session_state["password_correct"] = False
            st.rerun()

