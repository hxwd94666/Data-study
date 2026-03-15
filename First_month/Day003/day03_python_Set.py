"""集合基本操作"""
#集合是无序的，不能重复，无索引，不支持索引和切片
s=set()#不能使用{}创建，那是字典
s={1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10}
print(s)

"""集合常用方法"""
#add()添加元素
s.add(11)
print(s)

#remove()删除元素
s.remove(11)
print(s)

#pop()删除并返回一个元素,默认删除第一个元素
print(s.pop())

#clear()清空集合
s.clear()
print(s)

#difference()差集,包含在第一个集合中，但不包含在第二个集合中
s1={1,2,3,4,5,6,7,8,9,10}
s2={10,11,12,13,14,15,16,17,18,19,20}
print(s1.difference(s2))
#可以使用-运算符
print(s1-s2)

#union()并集
print(s1.union(s2))
#可以使用|运算符
print(s1|s2)

#intersection()交集
print(s1.intersection(s2))
#可以使用&运算符
print(s1&s2)

#count()集合元素个数
print(s1.count(1))

"""集合推导式"""
#语法：{表达式 for 变量 in 集合 if 条件}
s1={i for i in range(1,10)}
print(s1)

"""集合实例"""
#选修篮球名单
basketball={"小王","小李","小张"}
#选修足球名单
football={"小杨","小王"}
#获取每个学生选修的课程数量
all_list=[*basketball,*football]
for name in all_list:
    print("{}选修的课程有{}".format(name,all_list.count(name)))

