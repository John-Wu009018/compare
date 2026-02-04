import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 1. 頁面風格設定 (純淨白底 + 藍色側邊欄 + 淺藍輸入框 + 灰色表格線) ---
st.set_page_config(page_title="AI 專業儀器比對工具", layout="wide")

st.markdown("""
    <style>
    /* 全域背景與文字 */
    .stApp { background-color: #FFFFFF; color: #000000; }
    h1, h2, h3, p, span, label { color: #000000 !important; }

    /* 側邊欄改為深藍色 */
    [data-testid="stSidebar"] { background-color: #1A365D; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }

    /* 輸入框：淺藍色背景，黑色文字 */
    .stTextInput input {
        background-color: #EBF8FF !important; 
        color: #000000 !important; 
        border: 1px solid #90CDF4 !important;
        border-radius: 8px !important;
    }

    /* 報告容器與表格框線修正 */
    .report-container { 
        padding: 30px; 
        border: 1px solid #DDDDDD; 
        border-radius: 12px; 
        background-color: #FFFFFF;
    }
    
    /* 強制 Markdown 表格顯示灰色框線 */
    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    th, td { border: 1px solid #CCCCCC !important; padding: 12px; text-align: left; }
    th { background-color: #F7FAFC; }

    /* 按鈕樣式 */
    .stButton>button { background-color: #2B6CB0; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI 模型設定
GEMINI_API_KEY = "AIzaSyDqe2MZSucHCnRhumslFC2ZKxTgTcJtpgs"

def get_best_model():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        priority = ['models/gemini-1.5-flash', 'models/gemini-pro']
        for p in priority:
            if p in models: return genai.GenerativeModel(p)
        return genai.GenerativeModel(models[0]) if models else None
    except: return None

# 3. 介面佈局
st.title("⚡ 產品 AI 智慧比對系統")

with st.sidebar:
    st.header("⚙️ 設定")
    num_products = st.slider("比對產品數量", 2, 8, 3)
    st.divider()
    st.write("🤖 **使用 AI 模組：** GOOGLE GEMINI")

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

# 4. 執行比對
if st.button("🚀 啟動 AI 深度比對"):
    valid_list = [n for n in product_names if n.strip() != ""]
    if len(valid_list) < 2:
        st.warning("⚠️ 請輸入至少兩個型號。")
    else:
        ai_model = get_best_model()
        if ai_model:
            with st.spinner('🤖 正在檢索圖片與技術規格...'):
               
                # AI 內容產出
                prompt = f"""
                你是一位量測儀器顧問。請詳細比對以下型號：{', '.join(valid_list)}。
                1. 製作一個專業的規格對照表 (Markdown 表格)。
                2. 說明核心技術差異。
                3. 給予選購建議。
                請務必使用『繁體中文』回答。
                不顯示使用者類型。
                在表格最下方顯示產品圖片，透過網路搜尋截圖顯示。
                """
                
                try:
                    response = ai_model.generate_content(prompt)
                    
                    # 這是要被拍照的區域
                    st.markdown('<div id="capture-area" class="report-container">', unsafe_allow_html=True)
                    st.subheader("📊 AI 選購關鍵分析報告")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 5. 修正版：拍照功能 (加入延遲處理確保圖片加載)
                    st.divider()
                    screenshot_html = f"""
                    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
                    <div style="text-align: center; padding: 20px;">
                        
                    </div>
                    <script>
                    function downloadReport() {{
                        // 鎖定 Streamlit 的主容器
                        const area = window.parent.document.getElementById("capture-area");
                        html2canvas(area, {{
                            backgroundColor: "#FFFFFF",
                            useCORS: true,
                            scale: 2 // 提高解析度
                        }}).then(canvas => {{
                            const link = document.createElement('a');
                            link.download = 'HIOKI_AI_Report.png';
                            link.href = canvas.toDataURL("image/png");
                            link.click();
                        }});
                    }}
                    </script>
                    """
                    components.html(screenshot_html, height=150)
                    
                except Exception as e:
                    st.error(f"分析失敗：{e}")