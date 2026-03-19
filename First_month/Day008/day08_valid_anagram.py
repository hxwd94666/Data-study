#力扣242：有效的字母异位词
"""
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的 字母异位词。
字母异位词是通过重新排列不同单词或短语的字母而形成的单词或短语，并使用所有原字母一次。
"""
#自解没解出来，以下代码来自灵茶山艾府
from collections import Counter
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
#直接统计字符出现的次数是否一致

#解法2
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        cnt = [0] * 26
        for c in s:
            cnt[ord(c) - ord('a')] += 1 #ord转换为数字判断是否相等
        for c in t:
            cnt[ord(c) - ord('a')] -= 1
        return all(c == 0 for c in cnt) #all函数加上生成器表达式
