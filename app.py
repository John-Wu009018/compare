import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. 頁面風格設定 (科技感深色模式 + 漸層 + 玻璃擬態) ---
st.set_page_config(page_title="HIOKI AI 儀器顧問", layout="wide")

st.markdown("""
    <style>
    /* 全域背景：深色科技漸層 */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* 標題樣式：霓虹字體 */
    h1 {
        color: #38bdf8 !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        letter-spacing: -1px;
    }

    /* 側邊欄改為玻璃感深色 */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }

    /* 輸入框樣式：深色透明感 */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }

    /* 報告容器：玻璃擬態卡片 */
    .report-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        margin-top: 25px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* 表格美化 */
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 20px 0;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    th {
        background-color: rgba(56, 189, 248, 0.1) !important;
        color: #38bdf8 !important;
        padding: 15px !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    td {
        background-color: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 12px !important;
        color: #cbd5e1 !important;
    }

    /* 按鈕樣式：漸層藍色 */
    .stButton>button {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-weight: 700;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
        color: white;
    }

    /* Slider 顏色調整 */
    .stSlider [data-baseweb="slider"] {
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI 模型設定 (自動偵測可用模型) ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 挑選最佳模型
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
st.title("🛡️ HIOKI AI 智慧比對顧問")
st.markdown("<p style='color: #94a3b8;'>專業量測儀器數據分析與選購建議系統</p>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://www.hioki.com/themes/hioki/logo.svg", width=150) # 示意圖，如連結失效可移除
    st.markdown("### ⚙️ 控制面板")
    num_products = st.slider("比對產品數量", 2, 4, 2)
    st.divider()
    st.markdown("#### 🚀 核心版本")
    st.code("Gemini 1.5 Flash")
    st.info("輸入型號後，AI 將自動抓取最新技術規格進行橫向比對。")

# 產品型號輸入區
product_names = []
cols = st.columns(num_products)
for i in range(num_products):
    with cols[i]:
        st.markdown(f"**產品型號 {i+1}**")
        name = st.text_input("", placeholder=f"例如: HIOKI RM3545", key=f"p{i}", label_visibility="collapsed")
        product_names.append(name)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. 執行比對 ---
if st.button("✨ 啟動 AI 深度分析與評估"):
    valid_list = [n.strip() for n in product_names if n.strip() != ""]
    
    if len(valid_list) < 2:
        st.warning("⚠️ 請輸入至少兩個型號以進行比對分析。")
    elif ai_model is None:
        st.error("❌ 系統偵測到 API 設定問題。")
    else:
        with st.spinner('🔍 正在檢索全球資料庫並進行數據合成...'):
            prompt = f"""
            你是一位享譽國際的精密量測儀器專家。請針對以下產品進行嚴謹的技術比對：{', '.join(valid_list)}。
            
            請依照以下專業格式輸出：
            1. 技術規格橫向對照表 (使用 Markdown 表格，欄位需包含關鍵參數、精度、連線介面等)。
            2. 核心優勢分析 (用項目符號條列每個型號的殺手級特點)。
            3. 應用場景適配性 (說明哪款適合實驗室、哪款適合產線)。
            4. 最終採購建議。
            
            要求：
            - 使用繁體中文。
            - 語氣必須具備權威性、專業感。
            - 數字規格需力求精確。
            """
            
            try:
                response = ai_model.generate_content(prompt)
                
                # 顯示報告內容
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.markdown(f"<h2 style='color: #38bdf8; text-align: center;'>{ ' vs '.join(valid_list) } 技術分析報告</h2>", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.success("🎯 分析報告已完成。您可以直接列印此頁面作為 PDF 呈報使用。")
                
            except Exception as e:
                st.error(f"分析失敗，錯誤原因：{e}")

# 頁尾
st.markdown("<br><hr><center style='color: #475569;'>HIOKI 專業儀器比對系統 | 僅供技術參考 | 2024 AI Powered</center>", unsafe_allow_html=True)
