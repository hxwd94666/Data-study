#力扣209长度最小的子数组
"""
给定一个含有 n 个正整数的数组和一个正整数 target 。
找出该数组中满足其总和大于等于 target 的长度最小的 子数组 [numsl, numsl+1, ..., numsr-1, numsr] ，
并返回其长度。如果不存在符合条件的子数组，返回 0 。
示例 1：
输入：target = 7, nums = [2,3,1,2,4,3]
输出：2
解释：子数组 [4,3] 是该条件下的长度最小的子数组。
"""
#自解
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        count = 0
        min_length = 0
        for right in range(len(nums)):
            count += nums[right]

            while count >= target:
                count -= nums[left]
                if min_length == 0 or min_length > right - left + 1:
                    min_length = right - left + 1
                left += 1

        return min_length

#ai优化
# 时间复杂度：严格 O(N)。`right` 指针和 `left` 指针最多各遍历数组一次，总操作次数 2N。
# 空间复杂度：O(1)。仅维护几个整型物理游标，不占用额外堆内存。
from typing import List
class Solution:
    """
    🔑 [核心架构]: 动态缩容滑动窗口 + 正无穷状态初始化
    """
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        current_sum = 0

        # 💡 架构防御：求最小值时，初始值设为物理极限“正无穷 (infinity)”
        # 彻底消灭冗余的 if == 0 边界判断，提升 CPU 分支预测效率
        min_length = float('inf') #一个浮点数，代表正无穷大

        for right in range(len(nums)):
            # 绝对铁律：先进窗口！累加当前元素
            current_sum += nums[right]

            # 总和达标，动态弹簧开始压缩！
            while current_sum >= target:
                # 趁着合法状态，立刻更新极小值
                min_length = min(min_length, right - left + 1)

                # 吐数据：左侧元素物理出栈，左指针右移，尝试挑战更短纪录
                current_sum -= nums[left]
                left += 1

        # 优雅降级：如果游标依然是正无穷，说明全量加总都不达标，返回 0
        return min_length if min_length != float('inf') else 0