--  1. 灾难现场 (The Disaster)
--- 现象：Hadoop/Spark 任务跑到 99% 卡死，迟迟不结束，或者直接报 OOM (Out Of Memory)。
--- 根本原因：底层采用 Hash Shuffle 分发机制。如果两表 JOIN 的关联键 (如 user_id)
--          含有极其海量的相同值（尤其是几十上千万的 NULL 空值），这些脏数据会被引擎强行
--          路由到集群的【同一个 Task 节点】上。
--- 结局：99台机器闲置，1台机器被撑爆。
--* 2. 降维打击策略 (The Solution)
--- 核心思想：打散脏数据！既然 NULL 会聚拢，我们就把 NULL 变成互不相同的随机数。
--- 武器：COALESCE() + RAND()
--- 效果：原本挤在一台机器上的 2000 万条 NULL 数据，被均匀分发到了 100 台机器上，
--       且因为带有 'skew_' 前缀，绝对不会与右表的正常业务数据发生错误匹配。
-- 场景：流水表 (A) LEFT JOIN 用户维表 (B)
-- 痛点：表 A 中存在大量 user_id 为 NULL 的脏日志

SELECT 
    A.order_id,
    A.action_time,
    A.user_id     AS original_user_id,
    B.user_name,
    B.department
FROM 
    ods_user_action_log A 
LEFT JOIN 
    dim_user_info B 
-- 核心防御线：防倾斜关联条件
ON 
    -- 如果 A.user_id 非空，按正常逻辑关联
    -- 如果 A.user_id 为空，将其替换为 'null_skew_0.2341...' 格式的随机字符串强制打散
    COALESCE(A.user_id, CONCAT('null_skew_', CAST(RAND() AS STRING))) = B.user_id
-- CONCAT() 函数用于拼接字符串，CONCAT() 函数的参数可以是任意多个字符串。
-- 补充规范：在企业级数仓中，对于不可控的外表，始终保持对关联键的敬畏。