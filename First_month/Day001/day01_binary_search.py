##力扣704二分查找
"""给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target，
写一个函数搜索 nums 中的 target，如果 target 存在返回下标，否则返回 -1。
你必须编写一个具有 O(log n) 时间复杂度的算法。"""

##列表是左闭右闭
from typing import List
class Solution:
    def binary_search(self,nums:List[int],target:int) -> int:
        """
        :param nums:升序排列的整数列表
        :param target: 需要查找的目标数
        :return: 目标存在则返回索引，不存在则返回-1
        """
        if not nums:
            return -1
        ##列表为空则直接返回-1

        left_index:int = 0
        right_index:int = len(nums)-1

        while left_index <= right_index:
            mid_index:int=left_index+(right_index-left_index)//2
            ##确定中间索引

            if nums[mid_index] == target:
                return mid_index
            elif nums[mid_index] < target:
                left_index = mid_index+1 #目标更大，右区间不动，left往右收缩
            else:
                right_index = mid_index-1 #目标更小，左区间不动，right往左收缩
        return -1

##列表是左闭右开
# from typing import List
# class Solution:
# def binary_search(self,nums:List[int],target:int) -> int:
#
#     if not nums:
#         return -1
#
#     left_index:int = 0
#     right_index:int = len(nums)-1
#
#     while left_index < right_index:
#     ##此时left和right不会相等，否则左闭右开不成立
#         mid_index:int=left_index+(right_index-left_index)//2
#
#         if nums[mid_index] == target:
#             return mid_index
#         elif nums[mid_index] < target:
#             left_index = mid_index+1
#         else:
#             right_index = mid_index
#             ##right直接等于middle，因为右开代表right不在列表内，与排除middle效果一致
#     return -1

