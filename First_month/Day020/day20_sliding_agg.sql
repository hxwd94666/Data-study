--窗口函数中的 ROWS BETWEEN 子句物理意义
'🎯 业务场景 (Business Scenario)
模拟电商平台数据仓库（DW）层每日批处理任务。计算两项核心指标：
1. 历史累计充值 (Cumulative Sum)：计算截至当日，该用户的总充值水位。
2. 近 3 天滑动平均充值 (Moving Average)：计算包含当日在内，往前推 2 天（共 3 天）的充值均值，用于平滑消除单日数据的剧烈抖动。'

-- 拉起测试靶场
CREATE TABLE user_recharge_logs (
    user_id VARCHAR(20),
    log_date DATE,
    amount DECIMAL(10, 2)
);

-- 注入连续与断点测试数据
INSERT INTO user_recharge_logs (user_id, log_date, amount) VALUES
('U_001', '2026-03-01', 100.00),
('U_001', '2026-03-02', 50.00),
('U_001', '2026-03-03', 200.00),
('U_001', '2026-03-04', 10.00),
('U_001', '2026-03-05', 140.00);


SELECT
    user_id,
    log_date,
    amount,

    -- 历史绝对累计
    SUM(amount) OVER (
        PARTITION BY user_id
        ORDER BY log_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_amount,

    -- 近3日物理窗口滑动
    AVG(amount) OVER (
        PARTITION BY user_id
        ORDER BY log_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3d

FROM
    user_recharge_logs;

-- `CURRENT ROW` = 当前指针所在的位置。
-- `n PRECEDING` = 往上（历史）推n行。
-- `n FOLLOWING` = 往下（未来）推n行。
-- `UNBOUNDED PRECEDING/FOLLOWING` = 顶到内存物理边界（最前或最后）。