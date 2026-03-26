'【核心考点对齐】：
`ROW_NUMBER()`：绝对唯一排名 (1, 2, 3, 4)。
注意，多个相同数据，排序随机且变化，建议使用多个排序字段。
`RANK()`：并列跳跃排名 (1, 1, 3, 4)。
`DENSE_RANK()`：并列不跳跃排名 (1, 1, 2, 3)。
在业务中，需要考虑到并列情况，同时注意业务需求和预算需求'

WITH AS t1 ( --CTE与子查询不同，名字必须写在 AS 的前面
     SELECT uuid,
            page_url,
            action_time,
            ROW_NUMBER() OVER (PARTITION BY page_url ORDER BY action_time ASC) AS rn
     FROM ods_user_action_log
     WHERE user_id != '\\N'
    )

SELECT uuid,
        page_url,
        action_time
FROM t1
WHERE rn <= 3 ;

--1.窗口函数的执行顺序极靠后（只在 SELECT 阶段执行），所以它绝对不能直接放在 WHERE 里面作为过滤条件！
--2.运行顺序：
-- FROM / JOIN (找材料)：引擎先去 HDFS 硬盘里，把 ods_user_action_log 这个表（100万条数据）搬进内存。
-- WHERE (粗筛烂菜叶)：引擎立刻进行第一轮物理过滤，把 user_id = '\N' 的 15 万条脏数据直接扔进垃圾桶。
-- GROUP BY (按种类分堆)：如果有的话，把数据按指定的列分堆。
-- HAVING (精筛整堆数据)：对分好堆的数据进行第二轮过滤。
-- SELECT (深加工 & 贴标签)：注意！直到这个时候，引擎才开始真正提取你想要的列，并且执行极其消耗 CPU 的窗口函数 ROW_NUMBER()，给数据贴上 rn 标签！
-- ORDER BY (最终排序)：按要求把结果集排个序。
-- LIMIT (装车发货)：截取前几条，扔给客户端（你的屏幕）。
--3.高低层过滤逻辑分离：
--必须在最底层 WHERE 踢掉脏数据，否则脏数据会额外消耗算力，这也是防止结果中“垃圾占位”。