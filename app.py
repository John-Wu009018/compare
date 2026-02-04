import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

# --- 2. 科技感 CSS (縮小至 80% 並優化視覺) ---
st.markdown("""
    <style>
    /* 全域縮小至約 80% */
    html, body, [class*="css"] { font-size: 13.5px !important; }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* 隱藏預設元件讓介面更乾淨 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 標題與文字 */
    h1 { color: #38bdf8 !important; font-size: 1.7rem !important; font-weight: 800; }
    .sub-text { color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }

    /* 密碼區塊樣式 */
    .auth-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 30px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        text-align: center;
    }

    /* 8 格輸入框排版緊湊化 */
    div[data-testid="stHorizontalBlock"] { gap: 0.5rem !important; }
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }

    /* 報告區塊玻璃擬態 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
    }

    /* 按鈕科技藍 */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 密碼驗證邏輯 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        st.markdown("### 🔐 私密訪問控制")
        password = st.text_input("請輸入訪問密碼", type="password")
        if st.button("確認登入"):
            # 在此修改您的密碼
            if password == "149131313": 
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("密碼錯誤，請聯繫管理員。")
        st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

# --- 4. 主要程式邏輯 ---
if check_password():
    # AI 模型配置
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        ai_model = genai.GenerativeModel(model_name)
    except:
        st.error("API 連線失敗，請檢查 Secrets 設定。")
        st.stop()

    # 頁面標題
    st.title("🛡️ AI 智慧比對顧問")
    st.markdown("<p class='sub-text'>HIOKI 專業儀器數據橫向分析系統</p>", unsafe_allow_html=True)

    # 固定 8 格輸入框 (4x2 矩陣)
    st.markdown("#### 📋 待分析型號")
    product_names = []
    for r in range(2):
        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            with cols[c]:
                # 隱藏標籤，使用 placeholder 提示
                name = st.text_input("", placeholder=f"型號 {idx+1}", key=f"p{idx}", label_visibility="collapsed")
                product_names.append(name)

    st.markdown("<br>", unsafe_allow_html=True)

    # 執行比對
    if st.button("✨ 啟動 AI 深度比對分析"):
        valid_list = [n.strip() for n in product_names if n.strip() != ""]
        if len(valid_list) < 2:
            st.warning("⚠️ 請輸入至少兩個型號。")
        else:
            with st.spinner('🔍 正在檢索全球數據並分析中...'):
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

    # 側邊欄狀態
    with st.sidebar:
        st.markdown("### ⚙️ 系統狀態")
        st.success("🔒 已受保護的私密連線")
        if st.button("登出系統"):
            st.session_state["password_correct"] = False
            st.rerun()

