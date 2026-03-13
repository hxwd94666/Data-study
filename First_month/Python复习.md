1.Python中用换行符作为终止符，只有同行有两个语句以上才会使用"；"分割

2.布尔类型本质也是整数类型（True -1 False 0）

3.连续赋值：a，b=1，"Python"

4.标识符区分大小写，False/True不可作为标识符，但是false/true可以作为标识符

5.Python代码命名规范为PEP8

6.isinstance（数据，类型）检查数据是否属于指定的类型，返回bool值

7.三引号可定义多行字符串，也可以作为多行伪注释。\ ’ 表示单引号，\ "表示双引号，\ t （制表符）表示缩进。

8.字符串可直接拼接，也可以"+"拼接，但"+"拼接只能拼接字符串

9.字符串格式化：（1）%s占位符    print（"我的%s是%s" %（a，b）

​          推荐这个>   （2） f"内容{表达式/变量}"    print（f"大家好，我是{name}"）

10.运算符：/为除法（有小数），//为整除（无小数），**为次方根，这些都可以赋值运算符 

11.模式匹配 match xxx： case  "xxx" ： xxx （case _:表示都没匹配上，即else）

12.while后也可以加else：，不过影响不了while自己的循环

13.print（"*"，end=""） 一般输出一段字符串默认换行，可用end去改变这个默认"\n"

14.break：彻底退出整个循环（非外层循环）

​	continue：跳过当前这一次循环剩下的步骤，开始下一次循环

​	break常用于节省遍历资源，异常情况终止，账密登录交互

​	continue常用于无效数据清洗（元素in数组），特定数据忽略，简化复杂if-else嵌套

for user in users:
    if not user.is_active():
        continue  # 不活跃用户直接过滤
    if user.age < 18:
        continue  # 未成年过滤
    if not user.has_paid():
        continue  # 未付费过滤

​	send_vip_content(user)  #走到这一步的都是符合条件的用户，直接执行核心操作

15.