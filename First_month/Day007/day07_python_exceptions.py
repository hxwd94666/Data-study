"""异常学习"""
#异常，也叫bug，程序运行时发生的错误，导致程序无法继续运行
#try:
#    可能出现错误的代码
#    ……
#except [异常类型 as 异常变量]:
#    出现异常后的处理代码

try:
    a=10
    print(a/0)
except ZeroDivisionError as e:
    print("除数不能为0:", e)
#加异常变量会显示错误原因，不加的错误信息不会显示

#不用的异常需要写不同的异常类型，如NameError
#不过可以捕获所有异常，异常类型直接用Exception
try:
    a=10
    print(a/0)
except Exception as e:
    print("未知错误:", e)

#可选：
#[finally；
#    不管是否发生异常，都会执行的代码]
try:
    a=10
    print(a/0)
except Exception as e:
    print("未知错误:", e)
finally :
    print("资源释放")

"""异常传递"""
def func1():
    print("func1")
    func2()
def func2():
    print("func2")
    func3()
def func3():
    print("func3")
    print(my_close)

if __name__ == '__main__':
    try:
        func1()
    except Exception as e:
        print("未知错误:", e)