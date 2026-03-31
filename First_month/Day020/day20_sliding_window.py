#力扣3无重复字符的最长子串
"""
给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。
示例 1:
输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。注意 "bca" 和 "cab" 也是正确答案。
"""
#多次改错后的自解
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        number = set()
        max_length = 0
        left = 0

        for right in range(len(s)): #字符串无法使用索引，所以直接right循环
            in_number = s[right]

            while in_number in number: #撞车后开始删除左指针直到不撞车
                number.remove(s[left])
                left += 1

            number.add(in_number)

            if right - left + 1 > max_length: #字符长度就是两个指针之间的长度
                max_length = right - left + 1

        return max_length

#跳跃型滑动窗口
class Solution:
    """
    🎯 [算法靶点]: LeetCode 3. 无重复字符的最长子串 (最优解)
    🔑 [核心架构]: 跳跃型滑动窗口 + 字典物理地址映射
    """
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index_map = {}
        max_length = 0
        left = 0

        for right in range(len(s)):
            current_char = s[right]

            # 如果字符在注册表中，并且它的历史物理地址在当前 left 指针的右边或重合
            if current_char in char_index_map and char_index_map[current_char] >= left:
                # 触发跃迁：left 指针无需逐个驱逐，直接跳到该重复字符历史地址的下一位
                left = char_index_map[current_char] + 1

            char_index_map[current_char] = right

            current_length = right - left + 1
            if current_length > max_length:
                max_length = current_length

        return max_length