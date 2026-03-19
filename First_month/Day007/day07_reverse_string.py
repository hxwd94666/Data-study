#力扣344反转字符串
"""
编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 s 的形式给出。
不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。
"""
#自解（双指针）
from typing import List
class Solution:
    def reverseString(self,s:str)->str:
        left=0
        right=len(s)-1
        while left<right:
            s[right],s[left]=s[left],s[right]
            left+=1
            right-=1
        return s

#单指针写法
class Solution:
    def reverseString(self, s: List[str]) -> None:
        for i in range(len(s) // 2):
            s[i], s[-i - 1] = s[-i - 1], s[i]