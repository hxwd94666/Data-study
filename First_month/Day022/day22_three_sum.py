#力扣3三数之和
"""
给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，
同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。
注意：答案中不可以包含重复的三元组。
"""
#自解没解出来，以下代码来自AI
from typing import List
class Solution:
    """
    🎯 [算法靶点]: LeetCode 15. 三数之和
    🔑 [核心架构]: 排序定海神针 + 双向对撞推土机 + 滑步去重
    """

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # 必须排序，这是双指针能生效的绝对前提
        nums.sort()
        result = []
        n = len(nums)

        # 定义i为最小数，因为后面还需要留至少两个位置给 left 和 right，所以 i 最多走到 n - 2
        for i in range(n - 2):

            # 💡 顶级熔断防御：如果排完序后，当前最小的数都已经大于 0，绝对凑不出0。立刻停机！
            if nums[i] > 0:
                break

            # 💡 钢钉滑步去重：如果 i 踩到的这个数字，跟前一个数字一模一样，直接跳过！
            # 不能 nums[i] == nums[i + 1]，i+1只取最后一个i，可能造成 [i,i,-2i]这种结果丢失
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # 永远在钢钉 i 的【右侧区间】拉起双指针
            left = i + 1
            right = n - 1

            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]

                if current_sum < 0:
                    # 太小了，左指针向右爬坡（找更大的数）
                    left += 1
                elif current_sum > 0:
                    # 太大了，右指针向左下坡（找更小的数）
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])

                    # 既然已经命中，我们需要寻找【下一组】可能的解，必须避开重复值
                    # 左指针：只要下一个数跟现在一样，就一直往右滑行
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # 右指针：只要前一个数跟现在一样，就一直往左滑行
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    # 注意这里的nums=nums和前面的钢钉滑步去重是有差别的

                    # 彻底越过重复的雷区后，两个指针正式推进一步，开启下一轮寻宝
                    left += 1
                    right -= 1

        return result