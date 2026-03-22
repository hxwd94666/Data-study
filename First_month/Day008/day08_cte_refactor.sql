--cte是临时命名的结果集，只对当前sql有效，可定义多个，但名字必须唯一
--语法结构：
WITH cte_name AS (
    SELECT column1, column2
    ...
)
--使用CTE
SELECT * FROM cte_name;

--cte可递归（引用自身）
WITH RECURSIVE cte_name AS (
    SELECT column1, column2
    UNION ALL--必须包含 UNION ALL
    SELECT column1, column2
    FROM cte_name
)