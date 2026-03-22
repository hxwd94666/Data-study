#grep 命令用于在文件中搜索指定的字符串。
#语法：grep [选项] 模式 [文件...]
#举例：
grep -i "string" filename
grep -v "string" filename
#模式是搜索的字符串
#常用选项：
#-i 忽略大小写
#-v 显示不匹配的行
#-c 显示匹配的行数
#-n 显示匹配的行号
#-l 显示匹配的行
#-r/-R 递归查找
#-m N 只显示匹配的N行

#管道符|:将左侧命令的标准输出作为右侧命令的标准输入，实现命令串联。
command1 | command2 #command1的输出作为command2的输入