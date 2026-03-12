# 🎯 大数据开发180天学习计划

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced-orange.svg)]()
[![Airflow](https://img.shields.io/badge/Airflow-Data_Pipeline-green.svg)]()
[![Status](https://img.shields.io/badge/Status-In_Progress-brightgreen.svg)]()


## 👤 About Me

你好，我是重庆邮电大学（CQUPT）**数据计算及应用专业**的大四学生。
此前，我曾在 **德勤** 担任大数据开发实习生，参与宝⻢数仓新⽼集群迁移，负责数据任务适配、质量保障及上线表格开发，⽀撑平台平稳切换。。

这个仓库记录了我备战 2026 年秋招的核心轨迹。面对即将到来的职场，我发起了这项为期 180 天的硬核技术突击计划，致力于从底层逻辑到上层架构，全面夯实我的数据开发（Data Engineering）能力，并向着构建高可用企业级数据管道的目标迈进。

## 🛠️ Tech Stack Focus

* **开发语言**: Python (Type Hinting & OOP), 进阶 SQL (Window Functions, Complex Joins)
* **大数据生态体系**: Hadoop, Hive, Apache Spark (PySpark)
* **工作流与任务调度**: Linux，Apache Airflow
* **工程化规范**: Git, 盲打指法重塑, Google Docstring 规范

## 📂 Repository Structure (仓库导航)

为了保持清晰的工程结构，本仓库分为以下两个核心模块：

*  每日日程区。记录这 180 天真实的打怪升级过程，包含技术细分与每日规划。
*  个人成果沉淀区。包含所有跑通的 Python 算法题（按企业级规范编写）、复杂的 SQL 业务题解、以及后期的完整项目源码。


## 🗺️ 180-Day Roadmap (行军路线图)

我的学习链路被严格划分为四个阶段，聚焦于“做减法、抓核心、重实战”：

* **Phase 1: 语言基石与算法重塑 (Week 1-6)**
  * 全面转向 Python 数据开发栈，掌握企业级代码规范。
  * 攻克高阶 SQL 语法，使用 Python 刷穿 LeetCode 核心数据结构与算法。
* **Phase 2: 数仓理论与生态突围 (Week 7-12)**
  * 深挖 Kimball 维度建模理论，彻底搞懂 ODS 到 ADS 的分层逻辑。
  * 死磕 Hive 架构与底层原理，攻坚“数据倾斜”等企业级痛点。
  * 重构实习经历，深入编写 Airflow DAG 调度脚本。
* **Phase 3: 计算引擎与全链路实战 (Week 13-18)**
  * 掌握现代大数据主流引擎 Spark 的核心原理（RDD/DAG/宽窄依赖）。
  * **核心产出**：独立落地一个基于 `PySpark + Hive` 的完整电商/物流离线数据仓库项目。
* **Phase 4: 性能调优与开源贡献 (Week 19-24)**
  * 组件底层原理剖析与 JVM/Python 底层机制探索。
  * 尝试参与 Apache Airflow 等开源社区的微小贡献 (PR)。

## 🚀 180天突击进度条 (180-Day Progress Tracker)

### 🛡️ Phase 1: 语言基石与算法重塑 (Week 1-6)
- [x] **Week 1:** Python 基建落地、标准盲打指法重塑、算法破冰（双指针/二分查找）
- [ ] **Week 2:** Python 核心数据结构（字典/集合/列表推导式）、函数进阶与基础 SQL 联表查询
- [ ] **Week 3:** 🔥 **SQL 核心攻坚**：彻底掌握窗口函数 (Window Functions) 与复杂行转列/列转行
- [ ] **Week 4:** Python 面向对象编程 (OOP)、企业级异常处理 (Try-Except) 与 LeetCode 哈希表/字符串
- [ ] **Week 5:** Linux Shell 进阶（三剑客: grep/awk/sed 基础）与 LeetCode 栈与队列
- [ ] **Week 6:** Hadoop 核心生态扫盲 (HDFS/YARN 存储与调度原理) 与 Phase 1 阶段复盘

### 🏗️ Phase 2: 数仓理论与生态突围 (Week 7-12)
- [ ] **Week 7:** Hive 底层架构 (HQL 转换原理)、内部表/外部表实操与底层存储格式 (Parquet/ORC)
- [ ] **Week 8:** Hive 高阶优化：分区表 (Partition)、分桶表 (Bucket) 与复杂 UDF (用户自定义函数) 概念
- [ ] **Week 9:** 🔥 **数仓核心**：Kimball 维度建模理论（搞懂事实表、维度表、星型/雪花模型）
- [ ] **Week 10:** 数仓分层架构设计 (ODS -> DWD -> DWS -> ADS)，**完成德勤实习经历的“专业化黑话”重构**
- [ ] **Week 11:** 大厂面试必考：数据倾斜 (Data Skew) 的成因排查与 7 种企业级解决方案
- [ ] **Week 12:** Apache Airflow 进阶实战：使用 Python 编写 DAG 脚本，搞懂任务依赖 (Upstream/Downstream)

### ⚔️ Phase 3: 计算引擎与全链路项目实战 (Week 13-18)
- [ ] **Week 13:** 现代大数据引擎核心：Spark 架构原理、RDD 概念、宽窄依赖与 Stage 划分
- [ ] **Week 14:** PySpark 实战：精通 PySpark DataFrame API 与 Spark SQL 的混合流数据清洗
- [ ] **Week 15:** 💻 **【项目实战-启动】**：离线数仓项目环境搭建、模拟数据生成与 ODS 原始层接入
- [ ] **Week 16:** 💻 **【项目实战-数仓建设】**：基于 PySpark 的 DWD 层明细数据清洗与 DWS 层轻度汇总计算
- [ ] **Week 17:** 💻 **【项目实战-调度调度】**：将所有 PySpark 脚本接入 Airflow，实现全链路自动化定时调度
- [ ] **Week 18:** 💻 **【项目实战-闭环】**：数据质量校验 (DQ) 脚本编写，完成项目 README 沉淀与 Phase 3 复盘

### 🏆 Phase 4: 八股文突击与秋招海投 (Week 19-24)
- [ ] **Week 19:** 简历终极精修。Python 面试八股文突击（GIL锁、垃圾回收机制、深浅拷贝、装饰器底层）
- [ ] **Week 20:** 数据库底层八股文突击（MySQL 聚簇索引/非聚簇索引、事务隔离级别、MVCC）
- [ ] **Week 21:** 大数据高频面经突击（Hive HQL 调优、Spark 内存管理机制、Airflow 常见坑点）
- [ ] **Week 22:** 算法手感保持（LeetCode Top 100 肌肉记忆复盘），开启针对性模拟面试（自我介绍与项目拷问）
- [ ] **Week 23:** 🔥 **海投大作战**：锁定外企数据岗、银行科技部、新能源车企，完成每日 10+ 简历投递与网申笔试
- [ ] **Week 24:** 查漏补缺，整理笔试/面试错题本，心态调节，迎接秋招首个 Offer 破局！

---
*"Talk is cheap. Show me the code."* — Linus Torvalds
