--sql窗口函数中的前后函数
--lead表达式：lead(col,n,default) over(order by col)
--表达式解释：lead函数返回col列的"""当前行之后"""的第n行数据，如果当前行之后的第n行数据不存在，则返回default值。
--示例：
 select
     id,
     name,
      lead(name,1,'无') over(order by id) as lead_name
 from
     t_user;
     --结果：
     +----+------+----------+
     | id | name | lead_name|
     +----+------+----------+
     |  1 | 张三 |      无  |
     |  2 | 李四 |      张三|
     |  3 | 王五 |      李四|
     |  4 | 赵六 |      王五|
     |  5 | 孙七 |      赵六|
     +----+------+----------+

--lag表达式：lag(col,n,default) over(order by col)
--表达式解释：lag函数返回col列的"""当前行之前"""的第n行数据，如果当前行之前的第n行数据不存在，则返回default值。
