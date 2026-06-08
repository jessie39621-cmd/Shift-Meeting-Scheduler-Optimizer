# 模擬美光四班三輪的基礎排班衝突檢查器
import datetime

# 1. 定義員工與他們期望的班表 (1: 早班, 2: 中班, 3: 夜班)
employee_preferences = {
    "Alice": [1, 1, 2, 2, 3],  # 員工五天的期望
    "Bob": [3, 3, 1, 1, 2],
    "Charlie": [2, 2, 3, 3, 1]
}

# 2. 定義會議時間 (天數, 班別)
scheduled_meetings = [
    {"name": "製程改善會議", "day": 2, "shift": 2}, # 第3天中班
    {"name": "交接溝通會議", "day": 4, "shift": 3}  # 第5天夜班
]

print("=== 自動排班與會議衝突優化系統 ===")

# 3. 自動檢查衝突邏輯
for meeting in scheduled_meetings:
    m_day = meeting["day"]
    m_shift = meeting["shift"]
    m_name = meeting["name"]
    
    print(f"\n檢查會議: {m_name} (第 {m_day+1} 天, 班別 {m_shift})")
    attendees = []
    
    for emp, pref in employee_preferences.items():
        # 如果員工當天上的班跟會議班別一樣，代表可以出席
        if pref[m_day] == m_shift:
            attendees.append(emp)
            
    print(f"👉 預計可出席人員: {attendees}")
    if len(attendees) < 2:
        print("⚠️ 警告：出席人數過少，建議優化會議時間！")
