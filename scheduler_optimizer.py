import streamlit as st

# 設定網頁標題與介紹
st.title("📊 半導體廠排班與會議時程優化器")
st.caption("Shift & Meeting Scheduler Optimizer — 為解決產線複雜班表與會議衝突而設計的自動化工具")

st.markdown("""
### 💡 專案動機
在大型半導體晶圓廠中，工程師多採取「四班三輪」機制。本工具能自動媒合員工班表與預計會議時間，**自動抓出衝突並發出警告**，提升跨部門協作效率。
""")

st.sidebar.header("⚙️ 模擬資料設定區")
st.sidebar.markdown("可在這裡調整員工班表 (1:早班, 2:中班, 3:夜班) 與預計會議")

# 1. 定義員工與期望班表
employee_preferences = {
    "Alice": [1, 1, 2, 2, 3],
    "Bob": [3, 3, 1, 1, 2],
    "Charlie": [2, 2, 3, 3, 1]
}

# 2. 定義會議時間
scheduled_meetings = [
    {"name": "製程改善會議 (Process Improvement)", "day": 2, "shift": 2},
    {"name": "交接溝通會議 (Handover Communication)", "day": 4, "shift": 3}
]

# 執行按鈕
if st.button("🚀 開始執行自動化衝突檢查 (Run Optimizer)"):
    st.success("分析完成！優化報告如下：")
    
    for meeting in scheduled_meetings:
        m_day = meeting["day"]
        m_shift = meeting["shift"]
        m_name = meeting["name"]
        
        st.subheader(f"🔍 檢查會議：{m_name}")
        st.text(f"時間設定：第 {m_day+1} 天，班別 {m_shift}")
        
        attendees = []
        for emp, pref in employee_preferences.items():
            if pref[m_day] == m_shift:
                attendees.append(emp)
                
        st.write(f"👉 **預計可出席人員：** `{attendees}`")
        
        # 衝突警告邏輯
        if len(attendees) < 2:
            st.error("⚠️ 警告：出席人數過少，關鍵工程師可能正在輪休或跨班，建議調整會議時間！")
        else:
            st.info("✅ 此時段出席人數充足，可正常召開會議。")
            
