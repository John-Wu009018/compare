import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="centered")

# --- 2. 精準對齊 CSS ---
st.markdown("""
    <style>
    /* 移除所有 Streamlit 內建的空白、Header 與 Footer */
    [data-testid="stHeader"], [data-testid="stFooter"], [data-testid="stSidebarNav"] {display: none !important;}
    footer {display: none !important;}
    header {display: none !important;}
    
    /* 移除底部所有的 Padding */
    .main .block-container {
        padding-top: 5rem !important;
        padding-bottom: 0rem !important;
        max-width: 450px !important;
        margin: 0 auto !important;
    }

    /* 背景與全域字體 */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    html, body, [class*="css"] { font-size: 13px !important; }

    /* 登入框：幾何置中且寬度固定 */
    .auth-wrapper {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
    }
    .auth-container {
        width: 260px; /* 固定寬度 */
        padding: 25px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 10px;
        text-align: center;
    }

    /* 登入按鈕拉長與密碼框對齊 */
    .auth-container .stButton > button {
        width: 100% !important; /* 填滿容器寬度 */
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white;
        border: none;
        border-radius: 5px;
        height: 38px !important;
        font-weight: 600;
        margin-top: 10px;
    }

    /* 輸入框置中對齊 */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: white !important;
        height: 35px !important;
        text-align: center !important;
    }

    /* 移除下方奇怪的空框與線條 */
    div[data-testid="stVerticalBlock"] > div { margin-bottom: 0px !important; padding-bottom: 0px !important; }
    iframe { display: none; } /* 隱藏可能的後台隱形元件 */
    
    /* 報告顯示區 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 登入邏輯 ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # 確保登入時背景乾淨
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>🔐 系統登入</h3>", unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="請輸入密碼")
    if st.button("登入系統"):
        if pwd == "1234": # 密碼設定
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("密碼錯誤")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 4. 主程式介面 ---

# AI 模型連線
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API 密鑰無效")
    st.stop()

# 置中標題
st.markdown("<h2 style='text-align:center; color:#38bdf8; margin-bottom:0;'>AI 智慧比對顧問</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:11px; margin-bottom:20px;'>HIOKI 專業量測儀器數據分析</p>", unsafe_allow_html=True)

# 8 格輸入框
names = []
for i in range(2):
    cols = st.columns(4)
    for j in range(4):
        with cols[j]:
            n = st.text_input("", key=f"v{i*4+j}", label_visibility="collapsed", placeholder=f"#{i*4+j+1}")
            names.append(n)

st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

if st.button("✨ 啟動深度分析"):
    valid = [x.strip() for x in names if x.strip()]
    if len(valid) < 2:
        st.warning("請填寫至少兩個型號")
    else:
        with st.spinner('AI 正在分析中...'):
            try:
                res = model.generate_content(f"精密儀器專家比對：{', '.join(valid)}。含表格、差異分析、選購建議。繁體中文。")
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.markdown(res.text)
                st.markdown('</div>', unsafe_allow_html=True)
            except:
                st.error("分析過程發生錯誤")

# 登出小按鈕
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("登出", use_container_width=False):
    st.session_state.auth = False
    st.rerun()
