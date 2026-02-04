import streamlit as st

def check_password():
    # 注入自定義 CSS
    st.markdown("""
        <style>
        /* 跑馬燈動畫 */
        @keyframes marquee {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .marquee-container {
            width: 100%;
            overflow: hidden;
            background: #e1f5fe;
            padding: 10px 0;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .marquee-text {
            white-space: nowrap;
            display: inline-block;
            animation: marquee 15s linear infinite;
            color: #0277bd;
            font-weight: bold;
        }

        /* 登入容器樣式 */
        .auth-container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
        }

        /* 修改 Streamlit 表單按鈕樣式 */
        div[data-testid="stForm"] button {
            background-color: #007bff !important; /* 藍色 */
            color: white !important;
            border: none !important;
            padding: 10px 20px !important;
            transition: all 0.3s ease-in-out !important; /* 動畫過渡 */
            border-radius: 8px !important;
        }

        /* 按鈕滑動過去的動畫效果 */
        div[data-testid="stForm"] button:hover {
            background-color: #0056b3 !important; /* 深藍色 */
            transform: scale(1.03); /* 輕微放大 */
            box-shadow: 0 6px 12px rgba(0, 123, 255, 0.3) !important;
        }
        
        .sub-text {
            color: #666;
        }
        </style>
    """, unsafe_allow_html=True)

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # 跑馬燈效果
        st.markdown("""
            <div class='marquee-container'>
                <div class='marquee-text'>
                    ⚠️ 歡迎訪問內部系統：請輸入授權密碼以解鎖進階功能。系統維護時間：每週日 00:00 - 04:00。
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 登入容器內容
        st.markdown("""
            <div class='auth-container'>
                <h3 style='margin-top:0;'>🔐 私密訪問控制</h3>
                <p class='sub-text'>請輸入您的專屬密碼</p>
            </div>
            """, unsafe_allow_html=True)

        # 使用 form
        with st.form(key="login_form"):
            password = st.text_input(
                "密碼",
                type="password",
                placeholder="輸入訪問密碼...",
                label_visibility="collapsed"
            )

            submit_button = st.form_submit_button("確認登入", use_container_width=True)

            if submit_button:
                if password == "1234":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("❌ 密碼錯誤，請聯繫管理員。")
        
        return False

    return True

# 主程式調用
if check_password():
    st.success("✅ 登入成功！")
    st.write("這裡是您的私密內容...")
