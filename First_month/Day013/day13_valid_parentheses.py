#力扣20有效的括号
#参考灵茶山艾府的代码
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s)%2==1:
            return False
        a={')':'(',']':'[','}':'{'} #括号匹配字典
        b=[]    #模拟栈
        for i in s:
            if i not in a:  #匹配键，如果不是右括号（即是左括号）
                b.append(i) #打入栈中
            else:
                if not b or b.pop()!=a[i]: #栈为空，或者栈顶元素与字典的值不匹配（括号不匹配）
                    return False
        return not b #栈为空，则返回True

#也可以在哈希表/数组中保存每个左括号对应的右括号。在遍历到左括号时，把对应的右括号入栈。这样遍历到右括号时，只需看栈顶括号是否一样即可。
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2:  # s 长度必须是偶数
            return False
        mp = {'(': ')', '[': ']', '{': '}'}
        st = []
        for c in s:
            if c in mp:  # c 是左括号
                st.append(mp[c])  # 入栈对应的右括号
            elif not st or st.pop() != c:  # c 是右括号
                return False  # 没有左括号，或者左括号类型不对
        return not st  # 所有左括号必须匹配完毕

#用 if-else 代替 mp
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2:  # s 长度必须是偶数
            return False
        st = []
        for c in s:
            if c == '(':
                st.append(')')  # 入栈对应的右括号
            elif c == '[':
                st.append(']')
            elif c == '{':
                st.append('}')
            elif not st or st.pop() != c:  # c 是右括号
                return False  # 没有左括号，或者左括号类型不对
        return not st  # 所有左括号必须匹配完毕