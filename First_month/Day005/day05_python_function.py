"""函数基础"""
#形参，函数定义时使用的参数
#实参，函数调用时使用的参数
#函数的说明文档，三引号注释，用来描述函数的用途

#函数要先定义，再调用
#函数嵌套遵循栈结构，后进先出

"""函数进阶-变量作用域"""
#全局变量：定义在函数外，函数内都可以访问
#局部变量：定义在函数内，函数外无法访问
#global：使得在函数内部可以修改全局变量
a = 10
def a1():
    a = 20
    print(a)
a1()        # 输出 20
print(a)    # 输出 10（全局 a 未被修改）

b = 10
def b1():
    global b # 使函数内修改全局变量
    b = 20
    print(b)
b1()        # 输出 20
print(b)    # 输出 20（全局 b 被修改）


#尽量避免使用全局变量，考虑使用函数参数传递数据，而不是依赖全局变量
total = 0  # 全局变量
def add(x):
    global total
    total += x
    print(f"累加后 total = {total}")
add(5)   # total = 5

def add(f, x):
    new_total = f + x
    print(f"{f} + {x} = {new_total}")
    return new_total
total = 0
total = add(total, 5)   # 0 + 5 = 5

"""函数进阶-传参方式"""
#位置参数，函数调用时，参数按顺序传入

#关键字参数，参数按“键=值”名称传入，不要求顺序传入
def xy(x,y):
    print(x,y)
xy(y=1,x=2)
#两种参数方式可以混用，但关键字参数必须放在位置参数之后

"""函数进阶-默认参数"""
#默认参数也称为缺省参数，函数调用时，如果没有传入参数，则使用默认参数
def xy(x,y=1):
    print(x,y)
xy(1)
xy(1,2)

"""函数进阶-不定长参数"""
#*args：可变参数，函数调用时，可传入多个参数，参数会以元组形式传入
def xy(*args):
    print(args)
xy(1,2,3,4,5)
#**kwargs：关键字参数，函数调用时，可传入多个参数，参数会以字典形式传入
def xy(**kwargs):
    print(kwargs)
xy(x=1,y=2,z=3)
#*args和**kwargs可以同时使用
def xy(*args,**kwargs):
    print(args)
    print(kwargs)
xy(1,2,3,4,5,x=1,y=2,z=3)
#args适合处理数量不确定的数据，kwargs适合处理数量不确定的选项

"""函数进阶-参数类型"""
#普通参数：数字，字符串，布尔值，列表，元组，字典等
#特殊参数：函数
def xy(a,b):
    print(a,b)
xy(1,2)

def nm(a,b,xy):#这里的xy是一个函数
    return xy(a,b)
nm(1,2,xy)

