#力扣232.用栈实现队列
"""
请你仅使用两个栈实现先入先出队列。队列应当支持一般队列支持的所有操作（push、pop、peek、empty）：
实现 MyQueue 类：
void push(int x) 将元素 x 推到队列的末尾
int pop() 从队列的开头移除并返回元素
int peek() 返回队列开头的元素
boolean empty() 如果队列为空，返回 true ；否则，返回 false
说明：
你 只能 使用标准的栈操作 —— 也就是只有 push to top, peek/pop from top, size, 和 is empty 操作是合法的。
你所使用的语言也许不支持栈。你可以使用 list 或者 deque（双端队列）来模拟一个栈，只要是标准的栈操作即可。
"""
#参考代码随想录
class MyQueue:

    def __init__(self):
        self.stack_in = [] #这个栈用来存数据
        self.stack_out = [] #这个栈用来取数据

    def push(self, x: int) -> None:
        self.stack_in.append(x)

    def pop(self) -> int:
        if self.empty(): #要弹出数据，先确定是否有数据
            return None

        #这个方法，一旦要使用出栈的数据，必须把stack_in的数据全部倒到stack_out中
        if self.stack_out:
            return self.stack_out.pop() #出栈有数据，代表入栈内数据已经全部倒到出栈中
        else:
            while self.stack_in: #入栈数据全部倒到出栈中
                self.stack_out.append(self.stack_in.pop())
            return self.stack_out.pop()

    def peek(self) -> int:
        ans = self.pop()  # 复用 pop 的查找逻辑，再用 self.stack_in.append(ans) 把它补回去。
        self.stack_out.append(ans)
        return ans

    def empty(self) -> bool:
        return not (self.stack_in or self.stack_out) #两个栈如果都为空，则说明没数据