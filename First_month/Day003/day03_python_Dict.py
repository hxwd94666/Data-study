"""字典基本操作"""
#字典是无序的，不能重复，可修改，无索引，不支持切片
#字典里面存放的是键值对，可以根据键值获取对应的值
#键值key是唯一的，不能重复
d={}
d={"name":"小王","age":18}
print(d["name"])
#value值可以是任意类型，但key键值不能是可变类型（list、set、dict）

"""字典常用操作"""
#添加操作
d["sex"]="男"
print(d)

#删除操作，删除key返回删除的value
print(d.pop("sex"))
#删除操作，删除键值对
d["sex"]="男"
del d["sex"]
print(d)

#修改操作，与添加操作一样
d["name"]="小李"
print(d)

#查询操作
print(d["name"])#字典名称[key]
print(d.get("name"))#字典名称.get(key)
print(d.keys())#字典名称.keys()返回所有key的集合
print(d.values())#字典名称.values()返回所有value的集合
print(d.items())#字典名称.items()返回所有键值对的集合


"""案例：开发一个购物车系统"""
#创建购物车：用户根据提示输入商品名称以及商品的价格和数量，添加到购物车中
cart={"name":"mate80","price":6999,"num":1}
#这种方法不行，因为购物车有多个商品
cart=[{"name":"mate80","price":6999,"num":1},{...}]
#这种方法也不行，因为键值对查询是靠key的，而这里的key name 是唯一的，所以查询不到
cart={"mate80":{"price":6999,"num":1},"mate10":{"price":5999,"num":1}}
#正确的方法