--sql中处理null值
select * from t where isnull(a) --输出所有a为null的行（非标准函数）
select * from t where a is null --输出所有a为null的行
select * from t where coalesce(a,0) --输出所有a不为NULL且a≠0的行
--ISNULL(expr1, expr2)：若 expr1 不为 NULL，则返回 expr1；否则返回 expr2。
--COALESCE(expr1, expr2, ..., default)：从左到右依次检查，返回第一个非 NULL 的表达式；若所有表达式均为 NULL，则返回 default
--coalesce函数可以传入多个参数，而isnull函数只能传入两个参数
