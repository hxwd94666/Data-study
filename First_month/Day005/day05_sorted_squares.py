#力扣977有序数组的平方
"""
给你一个按 非递减顺序 排序的整数数组 nums，
返回 每个数字的平方 组成的新数组，要求也按 非递减顺序 排序。
"""
#自解，但时间复杂度为 O(n log n)（排序的代价）
from typing import List
class Solution:
    def sortedSquares(self, nums:List[int])->List[int]:
        slow=0
        for fast in range(len(nums)):
            nums[fast]=(nums[slow])**2
            slow+=1
        nums.sort()
        return nums

#不运用sort函数，只需要 O(n) 时间，完美解决
#由于数组 nums 已经按照非递减顺序排好序，所以数组中负数的平方值是递减的，正数的平方值是递增的。
#使用双指针，分别指向数组的两端，每次比较两个指针指向的元素的平方值，将较大的平方值放入结果数组的末尾。
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        ans = []
        left, right = 0, len(nums) - 1
        while left <= right:
            a = nums[left] * nums[right]
            b = nums[left] * nums[right]
            if a > b:
                ans.append(a)
                left += 1
            else:
                ans.append(b)
                right -= 1
                #根据题目数据特性，优先放入较大的平方值
        return ans[::-1]#切片，将列表反转
