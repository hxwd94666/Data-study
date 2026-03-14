"""字符串基本操作"""
s="hello world"
print(s[0])
print(s[-1])
#字符串不可修改
# s[5]="a"
# print(s) #错误

#字符串切片
print(s[0:5])
print(s[:5])
print(s[::-1])

"""字符串常用方法"""
#find（）查找字符
print(s.find("l"))
print(s.find("l",0,1))#指定位置查找

#count()统计字符出现的次数
print(s.count("l"))
print(s.count("l",0,1))

#upper ()/lower() 转换大小写
print(s.upper())
print(s.lower())

#split()指定分隔符符，将字符串分割为列表
print(s.split(" "))
print(s.split("l"))

#strip去除字符串前后空格或指定字符
print(s.strip())
print(s.strip("d"))

#replace()替换字符串
print(s.replace("l","a"))
print(s.replace("l","a",1))#指定替换次数

#startswith（）判断字符串是否以指定字符开头，返回布尔值
print(s.startswith("h"))
print(s.startswith("h",0,1))
#endswith（）判断字符串是否以指定字符结尾
print(s.endswith("d"))
print(s.endswith("d",0,5))

"""字符串案例：邮箱验证"""
#用户输入一个邮箱，判断邮箱格式是否正确（至少一个@和至少一个.）
#方法1，使用in
email=input("请输入邮箱：")
if "@" in email and "." in email:
    print("邮箱格式正确")
else:
    print("邮箱格式错误")
#方法2，使用count()
email=input("请输入邮箱：")
if email.count("@")>=1 and email.count(".")>=1:
    print("邮箱格式正确")
else:
    print("邮箱格式错误")