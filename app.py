import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="課程回饋表單",
    page_icon="📝",
    layout="centered"
)

st.title("📝 課程回饋與滿意度調查")
st.caption("感謝您參與本學期課程，請花 1~2 分鐘填寫回饋，協助我們持續改進教學品質。")

# 使用 st.form 批量提交，避免輸入時頁面頻繁 rerun
with st.form(key="course_feedback_form", clear_on_submit=False):
    
    st.subheader("基本資料")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("姓名 *", placeholder="例如：王小明")
    with col2:
        student_id = st.text_input("學號（選填）", placeholder="例如：B11200001")

    department_options = ["資訊工程系", "資訊管理系", "電子工程系", "電機工程系", "其他"]
    department = st.selectbox("就讀科系 *", department_options)

    # 選擇「其他」時動態填寫具體科系
    other_dept = ""
    if department == "其他":
        other_dept = st.text_input("請註明您的科系 *", placeholder="請輸入系所全名")

    st.divider()

    st.subheader("學習體驗評估")
    
    # 滿意度滑桿
    satisfaction = st.slider(
        "整體課程滿意度 *",
        min_value=1,
        max_value=5,
        value=4,
        help="1 分代表非常不滿意，5 分代表非常滿意"
    )

    # 多選題：最具收穫的環節
    highlights = st.multiselect(
        "您認為本課程最具收穫的部分？（可多選）",
        options=["課堂理論解說", "實作練習 / 專案實讀", "助教課輔諮詢", "期末專題發表", "同儕討論互動"],
        default=["實作練習 / 專案實讀"]
    )

    # 意見回饋
    feedback = st.text_area(
        "其他具體建議或想對老師說的話",
        placeholder="例如：希望增加專案實作的時間、某章節概念希望能多舉例說明...",
        height=120
    )

    # 送出按鈕（Form 的提交觸發點）
    submitted = st.form_submit_button("送出回饋 🚀", use_container_width=True)

# 提交後的邏輯處理與防呆驗證
if submitted:
    # 必填驗證
    if not name.strip():
        st.error("請填寫姓名！")
    elif department == "其他" and not other_dept.strip():
        st.error("選擇「其他」時，請務必填寫具體科系名稱！")
    else:
        actual_dept = other_dept.strip() if department == "其他" else department
        
        # 整理收集到的資料物件
        feedback_data = {
            "填寫時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "姓名": name.strip(),
            "學號": student_id.strip() if student_id else "未提供",
            "科系": actual_dept,
            "滿意度": f"{satisfaction} / 5",
            "亮點單元": ", ".join(highlights) if highlights else "無",
            "回饋意見": feedback.strip() if feedback else "無"
        }

        st.success(f"感謝您的回饋，{name}！資料已成功送出。")
        
        # 摺疊區塊顯示提交內容摘要
        with st.expander("查看您本次提交的內容摘要", expanded=True):
            df_summary = pd.DataFrame(list(feedback_data.items()), columns=["欄位", "內容"])
            st.table(df_summary)
            
            # 提供轉存 CSV 的選項
            csv = df_summary.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="下載回饋紀錄 (CSV)",
                data=csv,
                file_name=f"feedback_{name}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )