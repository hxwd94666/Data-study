import logging
import sys

class StreamCleaner:
    def __init__(self):
        # 1. 拉起 Day 21 的日志底座（Stream + File 多路复用）
        self.logger = logging.getLogger("DQ_Stream")
        self.logger.setLevel(logging.INFO)
        if self.logger.handlers:
            self.logger.handlers.clear()

        # 屏幕管道
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)

        # 硬盘管道（ERROR级专线）
        file_handler = logging.FileHandler(r'E:\hxwd\Desktop\数开\First_month\Day022\dq_error.log', mode='a', encoding='utf-8')
        file_handler.setLevel(logging.ERROR)
        self.logger.addHandler(file_handler)

    def csv_stream_reader(self, file_path: str):
        """
        🚀 防 OOM 的流式清洗生成器
        """
        self.logger.info(f"开启流式清洗管线，目标文件: {file_path}")
        line_number = 0

        try:
            # 用 open() 建立文件游标
            with open(file_path, 'r', encoding='utf-8') as file:

                # 迭代器逐行拉取数据，绝不全量加载readlines()
                for line in file:
                    line_number += 1

                    # 假设第一行是表头，直接跳过
                    if line_number == 1:
                        continue

                    # 物理清洗：去除换行符和首尾空格
                    clean_line = line.strip()
                    if not clean_line:
                        continue # 跳过空行

                    # 按照逗号拆分字段
                    fields = clean_line.split(',')

                    # 🚨 脏数据熔断检测：必须有3个字段，且每个字段都不能为空串
                    # all() 函数会检查列表里每一个元素，如果有一个为空，就返回 False
                    if len(fields) != 3 or not all(field.strip() for field in fields): #空格也是ASCII码，需要去除
                        # 触发错误日志落盘，跳过该行，但绝不中断整个程序的运行
                        self.logger.error(f"行号 {line_number} 触发熔断，脏数据: {clean_line}")
                        continue

                    # 组装合格的字典
                    row_dict = {
                        "id": fields[0].strip(),
                        "name": fields[1].strip(),
                        "age": fields[2].strip()
                    }

                    # ⚡️ 核武器爆发：将字典挂起抛出！函数在此刻物理冻结！
                    yield row_dict

        except FileNotFoundError:
            self.logger.error(f"致命异常：找不到文件 {file_path}", exc_info=True)


# 🚀 外部调用测试 (大厂的流式消费模式)
if __name__ == '__main__':
    cleaner = StreamCleaner()

    # 注意：调用带有 yield 的函数，它不会直接运行，而是返回一个“生成器对象”
    stream_generator = cleaner.csv_stream_reader('test_data.csv')

    self_logger = cleaner.logger
    self_logger.info("下游系统开始消费数据...")

    # 外界通过 for 循环，一次次地“唤醒” generator，要一条，给一条
    for valid_row in stream_generator:
        self_logger.info(f"✅ 成功清洗并消费入库: {valid_row}")