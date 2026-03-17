"""匿名函数"""
#匿名函数，也叫 lambda 函数，是一种创建函数的语法，可以理解为匿名函数。
#匿名函数的语法格式为：lambda [参数列表]: [表达式]
square1 = lambda x: x*x
def square2(x):
    return x*x
hello1 = lambda : print("hello world")
def hello2():
    print("hello world")
#参数列表为空时，参数列表可以省略

#运用案例
#完成下列排序，按照每一个元素的字符串长度进行排序
a = ["hello","world","python","java"]
a.sort(key=lambda x:len(x))#适合作为一次性回调函数
print(a)


"""递归"""
#递归，是指函数调用自身，递归函数必须包含一个递归终止条件，否则会进入无限循环。
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

""""电商订单计算器"""
#定义一个函数，用于根据传入的一批商品信息（商品名称，商品价格，商品数量），优惠（满减、打折），运费信息计算订单的总价。
#优惠规则如下：优惠券需要商品金额慢5000，且优惠券金额不能超过商品总价
#积分抵扣 需要商品金额慢5000，100积分抵扣一元，积分只能整百抵扣

def order_calculator(*args,coupon_price,integral):

#计算商品总价
    total_price = sum([x[1]*x[2] for x in args])
#优惠券
    if total_price > 5000 and coupon_price <= total_price:
        total_price -= coupon_price
#积分抵扣
    if total_price > 5000 and integral % 100 == 0:
        total_price -= integral // 100
#运费
    if total_price < 100:
        total_price += 10
#返回订单总价
    return total_price

"""map,filter,reduce"""
#map会将函数作用于序列的每一个元素，并返回一个迭代器。
#filter会将函数作用于序列的每一个元素，并返回一个迭代器，返回的迭代器中只包含函数返回值为True的元素。
#reduce会将函数作用于序列的每一个元素，并返回一个值。
#map
def square(x):
    return x*x
a = [1,2,3,4,5]
b = [2,3,4,5,6]
print(list(map(square,a)))
#filter
def is_even(x):
    return x % 2 == 0
print(list(filter(is_even,a)))
#reduce
from functools import reduce
def add(x,y):
    return x+y
print(reduce(add,a))