import csv
import random
import  uuid
from datetime import  datetime,timedelta

total_rows=1000000
file_name='ods_user_action_log_mock.csv'
null_rate=0.15

# 预设一些随机池，提高生成速度
ACTION_TYPES = ['click', 'view', 'add_cart', 'purchase', 'search']
PAGES = ['/home', '/product/detail', '/cart', '/checkout', '/search_result']

print(f"🚀 引擎启动：准备向本地磁盘生成 {total_rows} 条测试数据...")
print(f"⚠️ 警告：已开启 15% NULL 值投毒机制，用于后续 Hive 倾斜压测！")

# 必须使用 utf-8 编码，newline='' 防止 Windows 平台产生多余空行
with open(file_name, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter='\t')

    for i in range(total_rows):
        # 1.使用uuid 生成唯一 log_id
        log_id = str(uuid.uuid4())

        # 2. 生成 user_id，并执行 15% 的概率投毒
        # random.random() 会生成 0~1 之间的小数。如果小于 0.15，我们就强行赋值为 '\N'
        # (注：在 Hive 的底层文本格式中，'\N' 是标准的 NULL 值占位符)
        if random.random() < null_rate:
            user_id = '\\N'
        else:
            user_id = f"USER_{random.randint(1, 10000):05d}"

        # 3. 随机抽取行为和页面
        action_type = random.choice(ACTION_TYPES)
        page_url = f"https://www.company.com{random.choice(PAGES)}"

        # 4. 生成最近 3 天内的随机时间
        random_seconds = random.randint(0, 3 * 24 * 3600)
        action_time = (datetime.now() - timedelta(seconds=random_seconds)).strftime('%Y-%m-%d %H:%M:%S')

        # 5. 随机伪造一个内网或外网 IP
        client_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"

        # 6. 将这一行数据打包成列表，直接刷入硬盘！
        row_data = [log_id, user_id, action_type, page_url, action_time, client_ip]
        writer.writerow(row_data)

        # 性能监控：每生成 10 万条打印一次进度，防止你以为程序死机了
        if (i + 1) % 100000 == 0:
            print(f"✅ 已成功写入 {i + 1} 条数据...")

print(f"🎉 任务完成！造数引擎已安全关闭。请在当前目录下查看文件：{file_name}")