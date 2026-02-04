import streamlit as st
import google.generativeai as genai

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="HIOKI AI 分析顧問", layout="centered")

# --- 2. 科技感 UI 注入 (核心重點) ---
st.markdown("""
    <style>
    /* 強力清除原生組件與空白 */
    [data-testid="stHeader"], [data-testid="stFooter"], header, footer {display: none !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    
    /* 全域背景：深色漸層 */
    .stApp {
        background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* 登入卡片：幾何置中 */
    .login-wrapper {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 320px;
        z-index: 10000;
        text-align: center;
    }
    
    .login-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 16px;
        padding: 40px 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    .login-card h2 {
        color: #38bdf8;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }

    .login-card p {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-bottom: 25px;
    }

    /* 修正輸入框與按鈕的寬度與對齊 */
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: white !important;
        border-radius: 8px !important;
        height: 42px !important;
        text-align: center !important;
        transition: 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }

    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        height: 42px !important;
        font-weight: 600 !important;
        margin-top: 15px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
    }

    /* 分析主介面：集中式卡片 */
    .main-grid {
        max-width: 500px;
        margin: 80px auto;
        background: rgba(255, 255, 255, 0.02);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* 徹底移除下方不知道什麼作用的框框 (Streamlit Gap) */
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; height: 0 !important; margin: 0 !important; padding: 0 !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 登入邏輯 (具有質感的卡片佈局) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <div class="login-wrapper">
            <div class="login-card">
                <h2>SYSTEM ACCESS</h2>
                <p>請輸入授權碼以啟動 AI 分析顧問</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 將輸入框與按鈕放在 wrapper 裡面
    with st.container():
        # 為了置中對齊，我們在卡片內部使用空位來精準定位
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("<div style='height:215px'></div>", unsafe_allow_html=True) # 調整這裡讓輸入框對齊卡片內
            pw = st.text_input("PASSWORD", type="password", label_visibility="collapsed", placeholder="ACCESS CODE")
            if st.button("AUTHENTICATE"):
                if pw == "1234":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Access Denied")
    st.stop()

# --- 4. 登入後的分析介面 ---

# AI 模型連線
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API 連線異常")
    st.stop()

# 主介面容器
st.markdown("<div class='main-grid'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#38bdf8;'>AI 比對顧問</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:12px;'>請輸入 HIOKI 型號進行交叉分析</p>", unsafe_allow_html=True)

# 8 格輸入框
names = []
for i in range(2):
    cols = st.columns(4)
    for j in range(4):
        with cols[j]:
            n = st.text_input("", key=f"v{i*4+j}", label_visibility="collapsed", placeholder=f"#{i*4+j+1}")
            names.append(n)

st.write("<div style='height:15px'></div>", unsafe_allow_html=True)

if st.button("🚀 執行智能比對分析"):
    valid = [x.strip() for x in names if x.strip()]
    if len(valid) < 2:
        st.warning("請至少輸入兩個型號")
    else:
        with st.spinner('📡 數據同步與分析中...'):
            try:
                res = model.generate_content(f"精密儀器專家比對：{', '.join(valid)}。請提供詳細表格與選購核心建議。繁體中文。")
                st.markdown("<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; margin-top:20px;'>", unsafe_allow_html=True)
                st.markdown(res.text)
                st.markdown("</div>", unsafe_allow_html=True)
            except:
                st.error("分析失敗")

# 登出按鈕
st.write("<div style='height:30px'></div>", unsafe_allow_html=True)
if st.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
