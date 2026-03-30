class Solution:
    """
    🎯 [算法靶点]: LeetCode 20. 有效的括号 (Valid Parentheses)

    🔑 [Algorithm Trigger (核心触发器)]:
    - 业务特征: 遇到"一一对应"、"成对闭合"、"对称剥洋葱"的场景。
    - 物理映射: 大脑无条件调取 `dict` (用于 O(1) 映射) + `list` (用于 O(1) 压栈/弹栈)。绝不写 if-else 面条代码！

    🚨 [Cache Miss / Refactoring Log (宕机与重构日志)]:
    - 宕机断点 (v1.0): 脑子里只剩下先进后出，但实现时用了一大堆 `elif char == ']' and stack[-1] == '['`，代码极度丑陋且无法扩展。
    - 架构重构 (v2.0): 引入 Hash 映射 `mapping = {')': '(', ...}`，左括号存入，右括号弹出对比。
    - 致命踩坑: 在执行出栈 `pop()` 时，如果没有判空防御，遇到只传一个 `]` 的测试用例会直接触发 IndexError 异常。

    🛡️ [Interview Defense (面试防御)]:
    - Q: 如果日志文件里有几十亿个括号，内存撑爆 (OOM) 怎么办？
    - A: 栈要求全局上下文比对，超大文件无法全量压入。但在真实的业务场景（如编译器语法树分析）中，作用域通常是有限的。如果真的出现几十亿级别的流式符号匹配，我会反问业务方该场景的合理性，或者建议在写入端进行分块校验 (Chunking)。
    """

    def isValid(self, s: str) -> bool:
        if len(s) % 2 != 0:
            return False

        stack = []
        mapping = {')': '(', '}': '{', ']': '['}

        for char in s:
            if char in mapping:
                top_element = stack.pop() if stack else '#'
                if mapping[char] != top_element:
                    return False
            else:
                stack.append(char)

        return not stack