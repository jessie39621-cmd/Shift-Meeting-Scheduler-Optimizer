import streamlit as pd
import pandas as pd
import datetime

# 1. 網頁基本設定
st.set_page_config(page_title="半導體廠排班與會議時程優化器", layout="wide")

st.title("📊 半導體廠排班與會議時程優化器")
st.markdown("---")

# 2. 側邊欄：前端輸入元件（讓使用者調參數）
st.sidebar.header("⚙️ 參數設定面板")

# 讓使用者選擇日期
target_date = st.sidebar.date_input("選擇檢查日期", datetime.date(2026, 6, 9))

# 讓使用者篩選班別
shift_filter = st.sidebar.multiselect(
    "篩選特定班別（留空代表全選）",
    options=["常日班", "早班", "夜班"],
    default=[]
)

# 模擬的資料庫（當使用者沒有上傳 Excel 時的預設真正數據）
default_schedule = {
    "員工姓名": ["工程師小明", "工程師小華", "工程師阿強", "工程師小美"],
    "值班班別": ["早班 (07:00-15:00)", "夜班 (23:00-07:00)", "常日班 (08:30-17:30)", "早班 (07:00-15:00)"],
    "預計會議時間": ["10:00 - 11:30", "02:00 - 03:00 (凌晨)", "14:00 - 15:30", "16:00 - 17:00"]
}
df_default = pd.DataFrame(default_schedule)

# 3. 後台連接：支援 Excel 上傳功能
st.subheader("📁 1. 資料源連接 (Excel / Database)")
uploaded_file = st.file_uploader("上傳產線排班與會議行事曆 Excel 檔", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # 如果使用者有上傳檔案，就讀取使用者的檔案
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("✅ 成功讀取自訂排班資料！")
    except Exception as e:
        st.error(f"檔案讀取失敗，請檢查格式。錯誤訊息: {e}")
        df = df_default
else:
    # 沒上傳時，使用預設的真實數據，並提供範例下載
    df = df_default
    st.info("💡 目前使用系統預設排班資料。您也可以上傳自己的 Excel 檔。")
    
    # 製作一個簡單的下載按鈕，讓使用者知道 Excel 該長怎樣
    @st.cache_data
    def convert_df(df_to_convert):
        return df_to_convert.to_csv(index=False).encode('utf-8-sig')
    csv_data = convert_df(df_default)
    st.download_button("📥 下載範例 Excel 格式", data=csv_data, file_name="排班範例.csv", mime="text/csv")

# 顯示目前的排班與會議數據
st.write("### 當前排班與會議清單", df)

st.markdown("---")

# 4. 優化與衝突檢查邏輯（即時運算）
st.subheader("🚀 2. 自動化衝突檢查與即時運算")

# 讓使用者動態勾選想檢查的人名
all_engineers = df["員工姓名"].unique().tolist()
selected_engineers = st.multiselect("勾選要加入即時運算的工程師：", options=all_engineers, default=all_engineers)

# 按鈕：按下後即時運算
if st.button("開始執行自動化衝突檢查 (Run Optimizer)"):
    st.loading_placeholder = st.empty()
    with st.spinner("演算法分析中... 正在比對輪班時間與會議時程..."):
        
        # 根據前端元件的參數，進行即時資料篩選
        filtered_df = df[df["員工姓名"].isin(selected_engineers)]
        
        # 這裡模擬演算法的即時運算邏輯
        results = []
        for index, row in filtered_df.iterrows():
            name = row["員工姓名"]
            shift = row["值班班別"]
            meeting = row["預計會議時間"]
            
            # 衝突判斷邏輯
            conflict = "無衝突"
            reason = "會議在正常工作時間內"
            status_color = "🟢"
            
            if "夜班" in shift and "凌晨" in meeting:
                conflict = "⚠️ 嚴重衝突"
                reason = "該工程師正在機台產線值大夜班，無法抽身參加跨部門會議！"
                status_color = "🔴"
            elif "早班" in shift and "16:00" in meeting:
                conflict = "⚠️ 潛在衝突"
                reason = "會議時間已超出早班下班時間 (15:00)，屬於超時加班開會。"
                status_color = "🟡"
                
            results.append({
                "狀態": status_color,
                "日期": target_date.strftime("%Y-%m-%d"),
                "員工姓名": name,
                "目前班別": shift,
                "預計會議": meeting,
                "檢查結果": conflict,
                "詳細原因與優化建議": reason
            })
            
        result_df = pd.DataFrame(results)
        
        # 5. 輸出與視覺化
        st.success("📊 即時運算完成！優化結果如下：")
        
        # 使用表格漂亮地呈現結果
        st.dataframe(
            result_df, 
            column_config={
                "狀態": st.column_config.TextColumn("狀態", width="small"),
                "檢查結果": st.column_config.TextColumn("檢查結果", width="medium"),
            },
            use_container_width=True
        )
        
        # 獨立跳出嚴重警告標示
        warning_count = result_df[result_df["檢查結果"] == "⚠️ 嚴重衝突"].shape[0]
        if warning_count > 0:
            st.error(f"🚨 偵測到 {warning_count} 筆嚴重的產線與會議時間撞期！請相關主管重新協調時程。")
        else:
            st.balloons()
            st.success("🎉 太棒了！當前排程沒有嚴重的跨部門時間衝突。")
