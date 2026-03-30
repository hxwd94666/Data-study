import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

"""
🎯 [压测靶点]: Python 内存级数据库模拟 + SQL LEAD() 窗口函数
🚨 [架构修正]: 无需安装 MySQL！利用 Python 内置 sqlite3 在内存中拉起 DB 实例，完美契合 Phase 1 "本地狂暴造数" 铁律！
"""

# 1. 在内存中拉起一个数据库实例 (一跑就建，跑完即焚，不留垃圾)
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# 2. 物理建表 (DDL)
cursor.execute('''
CREATE TABLE ods_user_click_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(20) NOT NULL,
    page_id VARCHAR(50) NOT NULL,
    action_time DATETIME NOT NULL
)
''')

# 3. Python 狂暴造数 (模拟数据倾斜与连续点击)
print("正在往内存数据库暴力打入测试数据...")
mock_data = []
base_time = datetime(2026, 3, 30, 9, 0, 0)
for i in range(20): # 生成 20 条极端测试数据
    user = random.choice(['User_A', 'User_B'])  # 只有两个用户，人为制造数据倾斜
    page = random.choice(['/home', '/cart', '/checkout'])
    # 时间递增，模拟点击流
    action_time = base_time + timedelta(minutes=random.randint(1, 30) * i)
    mock_data.append((user, page, action_time.strftime('%Y-%m-%d %H:%M:%S')))

# 将脏数据批量压入 SQLite
cursor.executemany('INSERT INTO ods_user_click_log (user_id, page_id, action_time) VALUES (?, ?, ?)', mock_data)
conn.commit()

# 4. 🔥 核武级 SQL 压测：执行 LEAD() 开窗
print("\n执行高阶窗口函数压测：计算页面停留时长...")
sql_query = """
SELECT 
    user_id,
    page_id,
    action_time AS current_time,
    -- 核心：用 LEAD 拉取下一次点击时间，找不到就用当前时间兜底 (模拟停留 0 秒)
    COALESCE(
        LEAD(action_time, 1) OVER (PARTITION BY user_id ORDER BY action_time ASC), 
        action_time
    ) AS next_time
FROM ods_user_click_log;
"""

# 5. 用 Pandas 直接接收 SQL 执行结果，降维打印！
df_result = pd.read_sql_query(sql_query, conn)
print("\n--- 压测结果输出 ---")
print(df_result)

# 释放物理内存
conn.close()