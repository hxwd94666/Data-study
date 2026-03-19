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