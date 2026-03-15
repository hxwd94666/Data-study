#力扣283移动零
"""给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
请注意 ，必须在不复制数组的情况下原地对数组进行操作。"""
#自写代码（双指针）
from typing import List
class Solution:
    def moveZeroes(self,nums:List[int])->List:
        slow=0
        for fast in range(len(nums)):
            if nums[fast] !=0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                #利用元组解包和组包实现交换赋值
                slow+=1
        return nums

#方法二，把nums当做栈处理
# class Solution:
#     def moveZeroes(self, nums: List[int]) -> None:
#         stack_size = 0
#         for x in nums:
#             if x:
#                 nums[stack_size] = x  # 把 x 入栈
#                 stack_size += 1
#         for i in range(stack_size, len(nums)):
#             nums[i] = 0