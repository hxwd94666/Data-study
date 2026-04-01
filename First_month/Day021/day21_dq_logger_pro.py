import logging
import sys


class DataQualityInspector:
    """
    DQ 自动化巡检底座
    """
    def __init__(self):
        # 配置全局的日志输出格式
        logging.basicConfig(
            stream=sys.stdout, #从错误管道切回标准输出管道
            level=logging.INFO,  #设置日志拦截门槛，INFO及以上级别的才输出
            format='%(asctime)s - %(levelname)s - %(message)s'  # 强行规定日志长什么样
        )
        logging.info("DQ 监控探针初始化完成，准备接入数据源...")

        self.logger = logging.getLogger("DQ_Probe") #创建自定义日志记录器
        self.logger.setLevel(logging.INFO)

        # 为了防止重复添加管道，先清空历史管道。由于是自定义日志记录器，所以可以放心地清空
        if self.logger.handlers:
            self.logger.handlers.clear()

        # 🚰 管线 A：标准输出管道 (StreamHandler) -> 打在屏幕上给人看
        console_handler = logging.StreamHandler(sys.stdout) #创建输出管道，输出到控制台，标准输出
        console_handler.setLevel(logging.INFO)
        # 装上格式化喷头
        console_formatter = logging.Formatter('%(asctime)s - [Console] %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # 💾 管线 B：硬盘落盘管道 (FileHandler) -> 存进磁盘给机器查
        # a（append）模式代表追加写入，utf-8 防止中文乱码
        file_handler = logging.FileHandler(r'E:\hxwd\Desktop\数开\First_month\Day021\dq_error.log', mode='a', encoding='utf-8') #file输出需要格式
        # 🚨 这根管子的拦截阀门调到最高！只有 ERROR 才能流进硬盘！
        file_handler.setLevel(logging.ERROR)
        # 装上硬盘专属的格式化喷头
        file_formatter = logging.Formatter('%(asctime)s - [File] %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # 🔌 将两根管子同时插在引擎总泵上 (多路复用 Multiplexing)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        self.logger.info("DQ 监控探针初始化完成，双管线已接通...")

    def compare_row_counts(self, source_cnt: int, target_cnt: int) -> float:
        """
        执行数据量比对的业务逻辑，并自带防崩溃装甲
        """
        logging.info(f"开始执行表级比对: 源端数据量={source_cnt}, 目标端数据量={target_cnt}")

        try:
            # 1. 制造悬崖：强制计算比例。遇到分母为0直接宕机跳入 except
            ratio = source_cnt / target_cnt

            # 2. 只有没报错（分母不为0），才会走到这里输出真实的差异率
            logging.info(f"【DQ 算力播报】源端={source_cnt}, 目标端={target_cnt}, 当前同步比例为: {ratio:.4f}")

            # 3. 引入大厂的“阈值（Threshold）”概念（假设误差在 5% 以内都算正常）
            if 0.95 <= ratio <= 1.05:
                logging.info("✅ 数据同步差异率在 5% 的安全阈值内，绿灯放行！")
            else:
                logging.warning(f"⚠️ 警告！数据差异率 {ratio:.4f} 严重偏离安全基线，请 DBA 介入核查！")

        except ZeroDivisionError as e:
            # 异常熔断区：当目标端(target_cnt)为 0 时，Python 会抛出除零异常。
            # 🚨 使用对象调用实例变量将error输出到本地文件中
            self.logger.error("致命级预警：目标表数据量为 0，触发除零异常！", exc_info=True) # exc_info打印异常信息
            return -1.0  # 返回一个错误的差异率，用于下游的处理逻辑

        finally:
            logging.info("数据库探针连接已安全断开。\n" + "-" * 40)


# ==========================================
# 🚀 实例化与压测区 (Sandbox)
# ==========================================
if __name__ == '__main__':
    # 1. 实例化这个巡检类
    inspector = DataQualityInspector()

    # 2. 正常压测：传入正常的数据量
    inspector.compare_row_counts(100, 100)

    # 3. 极端压测：人为传入分母 0
    inspector.compare_row_counts(100, 0)