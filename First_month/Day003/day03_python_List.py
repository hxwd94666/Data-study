"""列表切片"""
s=["A","B","C","D","E","F","G","H","I","J"]
#序列数据[开始索引：结束索引：步长]

print(s[0:5:1])
print(s[0:5])
print(s[:5])
print(s[:])
#各位置默认数值
print(s[::-1])
print(s[::1])
#步长决定截取间隔和顺序


"""列表常用方法"""
l=[1,2,3,4,5,6]

#append添加元素
l.append(7)
print(l)

#insert插入元素(在指定位置前插入元素)
l.insert(0,0)
print(l)

#remove删除元素
l.remove(0)
print(l)

#pop删除指定位置的元素，并返回该元素，默认删除最后一个元素
print(l.pop())
print(l.pop(0))

#sort列表排序
l=[1,5,3,4,2,6]
l.sort()
print(l)

#reverse列表翻转
l=[1,2,3,4,5,6]
l.reverse()
print(l)

"""列表解包"""
a,b,c,d,e,f=l
print(a,b,c,d,e,f)
print(*l)
#列表合并
l1=[1,2,3]
l2=[4,5,6]
l3=l1+l2
#以下两种方法也可以
#l3=l1.extend(l2)
#l3=[*l1,*l2]

"""列表推导式"""
l1=[i for i in range(1,10)]
print(l1)
l2=[i*i for i in range(1,10) if i%2==0]
print(l2)