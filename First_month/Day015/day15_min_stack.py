#力扣155、最小栈
"""
设计一个支持 push ，pop ，top 操作，并能在常数时间内检索到最小元素的栈。
实现 MinStack 类:
MinStack() 初始化堆栈对象。
void push(int val) 将元素val推入堆栈。
void pop() 删除堆栈顶部的元素。
int top() 获取堆栈顶部的元素。
int getMin() 获取堆栈中的最小元素。
"""
#自解，虽然纠错了两次
class MinStack:

    def __init__(self):
        self.stack=[] #主栈
        self.stack_min=[] #辅助栈，存储最小值，实现O（1）检索

    def push(self, val: int) -> None:
        self.stack.append(val)
        #下面可优化为self.stack_min.append(min(x, self.stack_min[-1]))
        if not self.stack_min: #辅助栈为空，直接存入
            self.stack_min.append(val)
        elif self.stack_min[-1]<=val:
            self.stack_min.append(self.stack_min[-1])
        elif self.stack_min[-1]>val:
            self.stack_min.append(val)
        # 影子栈，每次存入当前最小元素到栈顶，与主栈进行同步

    def pop(self) -> None:
        self.stack.pop()
        self.stack_min.pop()
        # 影子栈，与主栈进行同步，故不会出现删元素为最小元素就出错的情况
    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.stack_min[-1]


#1.Python中可用索引，那么stack[len(stack)-1]直接使用stack[-1]就行
#2.Python的if else就是elif ，且后面需要跟条件
#力扣会自动调用函数，无需在意函数的调用
#创建变量要使用self.xx，否则变量会是局部变量

#他人优秀解法：使用单栈实现，利用元组存储数据，元组第一个元素为数据，第二个元素为最小值
class MinStack(object):

    def __init__(self):
        self.stack = []

    def push(self, x):
        if not self.stack:
            self.stack.append((x, x))
        else:
            self.stack.append((x, min(x, self.stack[-1][1])))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]


























