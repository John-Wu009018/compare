import streamlit as st
import google.generativeai as genai

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="HIOKI AI 分析顧問", layout="centered")

# --- 2. 科技感 UI 注入 (修正輸入靈敏度) ---
st.markdown("""
    <style>
    /* 移除原生雜訊 */
    [data-testid="stHeader"], [data-testid="stFooter"], header, footer {display: none !important;}
    
    /* 背景與全域字體 */
    .stApp {
        background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
        color: #f1f5f9;
    }

    /* 限制主容器寬度，達成置中感 */
    .block-container {
        max-width: 400px !important;
        padding-top: 10rem !important;
        margin: auto;
    }

    /* 登入卡片裝飾 */
    .stForm {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 16px !important;
        padding: 30px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    /* 文字樣式修正 */
    .login-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .login-header h2 {
        color: #38bdf8;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .login-header p {
        color: #94a3b8;
        font-size: 0.85rem;
    }

    /* 輸入框：加大點擊區域 */
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: white !important;
        border-radius: 8px !important;
        height: 45px !important;
        text-align: center !important;
        font-size: 16px !important; /* 避免手機端縮放 */
    }

    /* 按鈕：與輸入框等寬且對齊 */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        height: 45px !important;
        font-weight: 600 !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3);
    }

    /* 移除下方空白與無用框 */
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 登入邏輯 ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # 建立一個簡單的表單容器
    st.markdown("""
        <div class="login-header">
            <h2>SYSTEM ACCESS</h2>
            <p>請輸入授權碼啟動顧問系統</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        # 直接使用原生組件，確保 100% 可點擊與方便輸入
        pw = st.text_input("ACCESS CODE", type="password", label_visibility="collapsed", placeholder="請輸入密碼")
        submit = st.form_submit_button("　　　　　進入系統　　　　　▶️")
        
        if submit:
            if pw == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("密碼錯誤，請重新輸入")
    st.stop()

# --- 4. 登入後的分析介面 ---

# 這裡移除剛才登入用的 Padding 限制，讓主頁面寬度恢復正常
st.markdown("<style>.block-container { max-width: 800px !important; padding-top: 3rem !important; }</style>", unsafe_allow_html=True)

# AI 模型配置
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("系統配置異常")
    st.stop()

st.markdown("<h2 style='text-align:center; color:#38bdf8;'>🛡️ AI 智慧比對顧問</h2>", unsafe_allow_html=True)

# 8 格輸入框
names = []
for i in range(2):
    cols = st.columns(4)
    for j in range(4):
        with cols[j]:
            n = st.text_input("", key=f"main_v{i*4+j}", label_visibility="collapsed", placeholder=f"#{i*4+j+1}")
            names.append(n)

if st.button("🚀 執行深度分析報告"):
    valid = [x.strip() for x in names if x.strip()]
    if len(valid) < 2:
        st.warning("請至少輸入兩個型號")
    else:
        with st.spinner('📡 數據同步中...'):
            try:
                res = model.generate_content(f"精密儀器專家比對：{', '.join(valid)}。含表格與專業建議。繁中回答。")
                st.markdown("<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:12px; border:1px solid rgba(255,255,255,0.1); margin-top:20px;'>", unsafe_allow_html=True)
                st.markdown(res.text)
                st.markdown("</div>", unsafe_allow_html=True)
            except:
                st.error("分析失敗")

# 登出
st.write("<div style='height:50px'></div>", unsafe_allow_html=True)
if st.button("安全登出"):
    st.session_state.authenticated = False
    st.rerun()



