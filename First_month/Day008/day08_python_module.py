"""常见模块"""
#常见的模块有：
#os模块：os模块提供了与操作系统交互的功能，如创建、删除文件和目录等等。
#sys模块：sys模块提供了与Python解释器进行交互的功能，如获取命令行参数等等。
#math模块：math模块提供了与数学运算相关的功能，如计算平方根、正弦、余弦等等。
#random模块：random模块提供了与随机数相关的功能，如生成随机数、随机选择等等。
#time模块：time模块提供了与时间相关的功能，如获取当前时间、计算时间差等等。
#datetime模块：datetime模块提供了与日期和时间相关的功能，如创建日期对象、计算时间差等等。
#re模块：re模块提供了与正则表达式相关的功能，如匹配字符串、替换字符串等等。
#csv模块：csv模块提供了与CSV文件相关的功能，如读取CSV文件、写入CSV文件等等。

"""模块导入方法"""
#import 模块名
import os
print(os.getcwd())
#import 模块名 as 别名
import os as o
print(o.getcwd())
#from 模块名 import 功能名
from random import choice
print(choice([1,2,3,4,5]))
#from 模块名 import 功能名 as 别名
from random import choice as c
print(c([1,2,3,4,5]))
#from 模块名 import *
from random import *
print(choice([1,2,3,4,5]))

#自定义模块
#创建一个模块，将功能封装在模块中，然后导入使用。
#from 文件名 import 函数名

#测试函数
#__name__ == '__main__'
#当模块被直接运行时，__name__ 被设置为模块名。当模块被导入时，__name__ 被设置为模块名。
#执行当前文件，则会执行如下代码。如果被当做模块导入，则不会执行。
if __name__ == '__main__':
    print('hello world')

#__all__
#__all__ 是一个列表，用于指定模块中哪些对象被导入时，哪些对象不被导入。
from math import  *
__all__ =  ['sqrt', 'pow', 'pi']#此时其他的功能都不能被导入了

"""软件包"""
#软件包（package）是一个目录，包含多个模块。
#文件夹中含有__init__.py文件，则该文件夹被Python解释器识别为软件包。
#__init__.py文件可以包含模块的初始化代码，或者描述这个包的一些信息。

#包的导入方式
#import 包名.模块名
#from 包名 import 模块名
#from 包名 import *，此时需要在包的__init__.py文件中添加__all__ = [模块名]控制允许导入的模块
#import 包名.模块名 import 函数名
#from 包名.模块名 import 函数名

#模块会在当前文件夹中搜索，如果没有找到，则从系统路径中搜索。
#如果模块名以/开头，则从系统路径中搜索。
#如果模块名以./开头，则从当前文件夹中搜索。
#如果模块名以../开头，则从当前文件夹的父目录中搜索。
#比如包x在a文件下，而需要调用包x的文件在b文件下，a与b同在c下，则可以import c.a.x