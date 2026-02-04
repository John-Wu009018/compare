import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. 頁面風格設定 ---
st.set_page_config(page_title="AI 專業儀器比對工具", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    h1, h2, h3, p, span, label { color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #1A365D; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .stTextInput input {
        background-color: #EBF8FF !important; 
        color: #000000 !important; 
        border: 1px solid #90CDF4 !important;
        border-radius: 8px !important;
    }
    .report-container { 
        padding: 30px; 
        border: 1px solid #DDDDDD; 
        border-radius: 12px; 
        background-color: #FFFFFF;
    }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    th, td { border: 1px solid #CCCCCC !important; padding: 12px; text-align: left; color: #000000; }
    th { background-color: #F7FAFC; }
    .stButton>button { background-color: #2B6CB0; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI 模型設定 (自動偵測可用模型版) ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 自動尋找目前帳號支援的模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 優先順序：1.5-flash > 1.5-pro > gemini-pro > 第一個可用的
    if 'models/gemini-1.5-flash' in available_models:
        model_name = 'models/gemini-1.5-flash'
    elif 'models/gemini-1.5-pro' in available_models:
        model_name = 'models/gemini-1.5-pro'
    elif 'models/gemini-pro' in available_models:
        model_name = 'models/gemini-pro'
    else:
        model_name = available_models[0] if available_models else None
        
    if model_name:
        ai_model = genai.GenerativeModel(model_name)
    else:
        st.error("❌ 您的 API 金鑰目前不支援任何生成模型。")
        ai_model = None
        
except Exception as e:
    st.error(f"❌ AI 初始化失敗：{e}")
    ai_model = None

# --- 3. 介面佈局 ---
st.title("⚡ 產品 AI 智慧比對系統")

with st.sidebar:
    st.header("⚙️ 設定")
    num_products = st.slider("比對產品數量", 2, 8, 3)
    st.divider()
    st.write("🤖 **使用 AI 模組：** GOOGLE GEMINI 1.5 FLASH")
    st.info("提示：輸入型號後點擊下方按鈕即可生成報告。")

# 產品型號輸入
product_names = []
rows = (num_products + 3) // 4
for r in range(rows):
    cols = st.columns(4)
    for c in range(4):
        idx = r * 4 + c
        if idx < num_products:
            with cols[c]:
                name = st.text_input(f"型號 {idx+1}", placeholder="如: HIOKI RM3545", key=f"p{idx}")
                product_names.append(name)

# --- 4. 執行比對 ---
if st.button("🚀 啟動 AI 深度比對"):
    valid_list = [n.strip() for n in product_names if n.strip() != ""]
    
    if len(valid_list) < 2:
        st.warning("⚠️ 請輸入至少兩個型號。")
    elif ai_model is None:
        st.error("⚠️ AI 模型未就緒，請檢查 API Key 設定。")
    else:
        with st.spinner('🤖 正在檢索技術規格並生成分析報告...'):
            prompt = f"""
            你是一位專業的量測儀器顧問。請針對以下型號進行深度比對：{', '.join(valid_list)}。
            
            請依照以下結構輸出：
            1. 製作一個詳細的規格對照表 (Markdown 表格)。
            2. 重點說明各型號間的核心技術差異 (如精度、速度、量測範圍)。
            3. 根據不同應用場景給予選購建議。
            
            注意事項：
            - 請務必使用『繁體中文』回答。
            - 規格必須力求準確。
            - 回答風格要專業且易於閱讀。
            """
            
            try:
                response = ai_model.generate_content(prompt)
                
                # 顯示報告內容
                st.markdown('---')
                st.markdown('<div id="capture-area" class="report-container">', unsafe_allow_html=True)
                st.subheader("📊 AI 選購關鍵分析報告")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 提示使用者可以使用瀏覽器右鍵另存成 PDF
                st.success("✅ 分析完成！您可以直接複製上方內容或使用瀏覽器列印功能存成 PDF。")
                
            except Exception as e:
                st.error(f"分析失敗，錯誤原因：{e}")

# 頁尾標記
st.caption("© 2024 AI 儀器顧問系統 | Powered by Google Gemini")



