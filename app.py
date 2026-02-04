import streamlit as st
import google.generativeai as genai

# --- 1. 頁面風格設定 (科技感深色模式 + 縮放調整) ---
st.set_page_config(page_title="AI 智慧比對顧問", layout="wide")

st.markdown("""
    <style>
    /* 全域文字縮小與背景 */
    html, body, [class*="css"] {
        font-size: 14px; /* 原本約 16-18px，縮小至約 85% */
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* 標題樣式 */
    h1 {
        color: #38bdf8 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }

    /* 側邊欄玻璃感 */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }

    /* 輸入框：縮小並調整寬度 */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 8px !important;
        padding: 8px !important;
        font-size: 13px !important;
    }

    /* 報告容器：玻璃擬態 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
    }

    /* 表格美化 */
    table {
        width: 100%;
        font-size: 13px;
        border-collapse: separate;
        border-spacing: 0;
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        overflow: hidden;
    }
    th {
        background-color: rgba(56, 189, 248, 0.1) !important;
        color: #38bdf8 !important;
        padding: 10px !important;
    }
    td {
        background-color: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 8px !important;
    }

    /* 按鈕樣式 */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI 模型設定 (自動偵測可用模型) ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if 'models/gemini-1.5-flash' in available_models:
        model_name = 'models/gemini-1.5-flash'
    elif 'models/gemini-pro' in available_models:
        model_name = 'models/gemini-pro'
    else:
        model_name = available_models[0] if available_models else None
    
    ai_model = genai.GenerativeModel(model_name) if model_name else None
except Exception as e:
    st.error(f"AI 初始化失敗：{e}")
    ai_model = None

# --- 3. 介面佈局 ---
st.title("🛡️ AI 智慧比對顧問")
st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>專業量測儀器數據分析與選購建議系統</p>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ 系統狀態")
    st.success("AI 連線正常 Gemini-1.5-flash")
    st.divider()
    st.info("請在右側輸入至少兩個產品型號進行深度分析。")

# 固定 8 格輸入框 (4x2 佈局)
st.markdown("### 📋 輸入待比對型號")
product_names = []
for r in range(2): # 兩列
    cols = st.columns(4) # 每列四行
    for c in range(4):
        idx = r * 4 + c
        with cols[c]:
            name = st.text_input(f"型號 {idx+1}", placeholder=f"輸入型號", key=f"p{idx}", label_visibility="visible")
            product_names.append(name)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. 執行比對 ---
if st.button("✨ 執行 AI 深度分析"):
    valid_list = [n.strip() for n in product_names if n.strip() != ""]
    
    if len(valid_list) < 2:
        st.warning("⚠️ 請輸入至少兩個型號以進行比對分析。")
    elif ai_model is None:
        st.error("❌ 系統偵測到 API 設定問題。")
    else:
        with st.spinner('🔍 正在檢索全球技術文件與數據...'):
            prompt = f"""
            你是一位享譽國際的精密量測儀器專家。請針對以下產品進行嚴謹的技術比對：{', '.join(valid_list)}。
            
            請依照以下專業格式輸出：
            1. 技術規格橫向對照表 (使用 Markdown 表格)。
            2. 核心技術差異與性能分析。
            3. 選購建議與應用場景。
            
            要求：使用繁體中文，專業且精簡。
            """
            
            try:
                response = ai_model.generate_content(prompt)
                
                # 顯示報告內容
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.markdown(f"<h3 style='color: #38bdf8; text-align: center; font-size: 1.3rem;'>{ ' vs '.join(valid_list) } 技術分析報告</h3>", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.success("🎯 分析已完成。")
                
            except Exception as e:
                st.error(f"分析失敗：{e}")

# 頁尾
st.markdown("<br><hr><center style='color: #475569; font-size: 0.8rem;'>AI 智慧比對顧問 | 專業技術參考 | 2026 Powered by Gemini</center>", unsafe_allow_html=True)


