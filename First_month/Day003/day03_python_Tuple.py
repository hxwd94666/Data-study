"""元组基本操作"""
t=(1,2,3,4,5,6)
print(t[0])
print(t[-1])
#元组不可修改,错误
#t[5]=7

#count元组元素个数
print(t.count(1))
#index获取元组元素的索引
print(t.index(1))

#元组切片
print(t[0:5])

#定义元组
t0=()
t1=(1,)
t2=(1)
print(type(t0))
print(type(t1))
print(type(t2))
#定义单个元素的元组，需要加逗号

"""元组解包与组包"""
#组包
t1=(1,2,3,4,5,6)
t2=tuple([1,2,3,4,5,6])
t3=1,2,3,4,5,6
print(type(t1),type(t2),type(t3))

#基础解包
a,b,c,d,e,f=t1
print(a,b,c,d,e,f)

#扩展解包（*）
a,*b,c=t1   #剩余元素放在b中
print(a,b,c)
a,*b=t1
print(a,b)
*a,b=t1
print(a,b)

"""元组案例：交换两个变量的值"""
a=10
b=20
a,b=b,a
print(a,b)#3个元素及以上也能实现
#其实这就是一个元组解包


"""元组案例：计算各个学生的各科目成绩以及总分"""
student=( ("小王",90,80,70), ("小李",80,90,90))
for name,chinese,math,english in student:
    total=chinese+math+english
    print("{}的考试成绩为：语文{}, 数学{}, 英语{}, 总分{}".format(name,chinese,math,english,total))

