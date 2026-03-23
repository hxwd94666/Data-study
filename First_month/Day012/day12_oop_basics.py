"""面向对象编程"""
#面向过程编程：把一个问题分解为多个函数，然后调用这些函数来完成该问题
#面向对象编程：把问题抽象为对象，把事物的特征和功能打包，对象之间通过方法来完成交互

#类：描述的是一组具有相同属性和方法的模板
#对象：类的实例化对象

"""类与对象"""
#类的定义
#类名命名规则：必须使用大写字母开头，后面若还有单词必须使用大写字母开头
#定义类的语法如下：
class 类名:
    pass    #这种方式不推荐，他动态的为对象添加属性，没有为对象指定属性
#创建对象：
对象名=类名()
对象名.属性名=属性值

class Person:
    pass
p1=Person()
p1.name="张三"
p1.sex="男"
print(p1.__dict__)#会将对象中的属性值以字典的方式输出
print(p1)#会直接输出对象内存地址

#__init__方法
#__init__方法：在创建对象时，会自动调用__init__方法，__init__方法可以给对象添加属性
class Person:
    def __init__(self,name,sex):
        self.name=name
        self.sex=sex
#创建对象：
p1=Person("张三","男")
print(p1.__dict__)
#使用init创建后对象的属性就无法动态添加了

"""实例方法"""
#实例方法：实例方法就是类中的方法，实例方法必须通过对象调用
class Person:
    def __init__(self,name,sex):
        self.name=name
        self.sex=sex
    def show(self): #实例方法
        print("姓名：%s,性别：%s"%(self.name,self.sex))

#创建对象：
p1=Person("张三","男")
p1.show()

"""魔法方法"""
#魔法方法：在类中定义的方法，在使用的时候不需要调用，系统会自动调用
#魔法方法是以双下划线开头，以双下划线结尾的特殊方法

#__str__方法：在打印对象时，会自动调用__str__方法，__str__方法返回的字符串会打印出来
class Person:
    def __init__(self,name,sex):
        self.name=name
        self.sex=sex
    def __str__(self):
        return "姓名：%s,性别：%s"%(self.name,self.sex)

#创建对象：
p1=Person("张三","男")
print(p1)

#__eq__:比较两个对象是否相等
#如果不使用__eq__方法，直接使用==会是比较两个对象的内存地址是否相等
class Person:
    def __init__(self,name,sex):
        self.name=name
        self.sex=sex
    def __eq__(self, other):
        return self.name==other.name and self.sex==other.sex
#创建对象：
p1=Person("张三","男")
p2=Person("张三","男")
print(p1==p2)
print(p1)

#类似的比较方法还有：
#__gt__:大于
#__lt__:小于
#__ge__:大于等于
#__le__:小于等于
#__ne__:不等于
class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def __gt__(self, other):
        return self.age>other.age
#创建对象：
p1=Person("张三","18")
p2=Person("张四","16")
print(p1>p2)

"""实例属性与类属性"""
#实例属性：实例属性是定义在实例方法中的属性，实例属性是针对每一个对象单独定义的属性
#类属性：类属性是定义在类方法中的属性，类属性是针对所有对象共享的属性
class Person:
    count=0 #类属性
    def __init__(self,name,sex):    #实例属性
        self.name=name
        self.sex=sex
        Person.count+=1
#创建对象：
p1=Person("张三","男")
print(p1.__dict__)  #不会输出类属性
#查找属性时候，先查找实例属性，如果实例属性不存在，再查找类属性