#力扣27移除元素
"""
给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素。
元素的顺序可能发生改变。然后返回 nums 中与 val 不同的元素的数量。
假设 nums 中不等于 val 的元素数量为 k，要通过此题，您需要执行以下操作：
更改 nums 数组，使 nums 的前 k 个元素包含不等于 val 的元素。nums 的其余元素和 nums 的大小并不重要。
返回 k。
"""
#自解
from typing import List
class Solution:
    def removeElement(self,nums:List[int],val:int)->int:
        slow:int=0
        fast:int=0
        for fast in range(len(nums)):
            if (nums[fast]!=val):
                nums[slow]=nums[fast]
                slow+=1
        ##遍历nums的每一个元素，覆盖非题中val值的元素。后面的元素无视
        return slow

#快慢指针法
# class Solution:
#     def removeElement(self, nums: List[int], val: int) -> int:
#         fast = 0
#         slow = 0
#         size = len(nums)
#         while fast < size:  # 不加等于是因为，a = size 时，nums[a] 会越界
#             # slow 用来收集不等于 val 的值，如果 fast 对应值不等于 val，则把它与 slow 替换
#             if nums[fast] != val:
#                 nums[slow] = nums[fast]
#                 slow += 1
#             fast += 1
#         return slow
#与我的一致，只是用了while进行判断，需要手动给fast加一

# 暴力法
# class Solution:
#     def removeElement(self, nums: List[int], val: int) -> int:
#         i, l = 0, len(nums)
#         while i < l:
#             if nums[i] == val: # 找到等于目标值的节点
#                 for j in range(i+1, l): # 移除该元素，并将后面元素向前平移
#                     nums[j - 1] = nums[j]
#                 l -= 1
#                 i -= 1
#             i += 1
#         return l
#时间复杂度O(n²)，很坏，每一次更改所有元素都进行了更改

# 相向双指针法
# class Solution:
#     def removeElement(self, nums: List[int], val: int) -> int:
#         n = len(nums)
#         left, right  = 0, n - 1
#         while left <= right:
#             while left <= right and nums[left] != val:
#                 left += 1
#             while left <= right and nums[right] == val:
#                 right -= 1
#             if left < right:
#                 nums[left] = nums[right]
#                 left += 1
#                 right -= 1
#         return left
#有点类似于二分查找，条件判断有点多，但是复杂度没什么问题