import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="centered")

# --- 2. 強力精簡 CSS (極小化、集中化) ---
st.markdown("""
    <style>
    /* 移除所有 Streamlit 雜訊 */
    [data-testid="stHeader"], [data-testid="stFooter"], [data-testid="stSidebarNav"] {display: none !important;}
    footer {display: none !important;}
    header {display: none !important;}
    
    /* 背景與全域字體 (縮小至 80%) */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    html, body, [class*="css"] { 
        font-size: 13px !important; 
    }

    /* 讓內容極度集中在中間 */
    .block-container {
        max-width: 450px !important; /* 限制整體內容非常窄 */
        padding-top: 5rem !important;
        margin: 0 auto !important;
    }

    /* 登入框：幾何置中 */
    .auth-wrapper {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
    }
    .auth-container {
        width: 260px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 10px;
        text-align: center;
    }

    /* 輸入框：小巧置中 */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: white !important;
        height: 30px !important;
        text-align: center !important;
        font-size: 12px !important;
    }

    /* 按鈕：窄版置中 */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white;
        border-radius: 5px;
        font-weight: 600;
        width: 100% !important;
        height: 35px !important;
    }

    /* 移除下方多餘的空框架與線條 */
    div[data-testid="stVerticalBlock"] > div:empty {display: none !important;}
    hr {display: none !important;}
    
    /* 報告顯示區域 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 登入邏輯 (極簡版) ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'><div class='auth-container'>", unsafe_allow_html=True)
    st.markdown("### 🔐 管理登入")
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="密碼")
    if st.button("登入"):
        if pwd == "1234": # 這裡修改密碼
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("錯誤")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 4. 主介面 (僅在登入後顯示) ---

# AI 配置
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Error")
    st.stop()

# 置中標題
st.markdown("<h2 style='text-align:center; color:#38bdf8; margin-bottom:5px;'>AI 智慧比對顧問</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:11px; margin-bottom:20px;'>HIOKI 專業儀器數據分析</p>", unsafe_allow_html=True)

# 8 格輸入框 (2x4 緊湊排列)
names = []
for i in range(2):
    cols = st.columns(4)
    for j in range(4):
        with cols[j]:
            n = st.text_input(f"v{i*4+j}", key=f"v{i*4+j}", label_visibility="collapsed", placeholder=f"#{i*4+j+1}")
            names.append(n)

st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

if st.button("✨ 啟動深度分析"):
    valid = [x.strip() for x in names if x.strip()]
    if len(valid) < 2:
        st.warning("請填寫至少兩個型號")
    else:
        with st.spinner('分析中...'):
            try:
                res = model.generate_content(f"精密儀器專家比對：{', '.join(valid)}。含表格、技術差異、建議。繁中回答。")
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.markdown(res.text)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("分析失敗")

# 登出按鈕 (放在最下面，小小的)
if st.button("登出", use_container_width=False):
    st.session_state.auth = False
    st.rerun()
