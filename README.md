# 🚀 180-Day 大数据开发核心架构突击

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-Advanced-orange.svg?logo=mysql&logoColor=white)]()
[![Apache Spark](https://img.shields.io/badge/Apache_Spark-PySpark-E25A1C.svg?logo=apachespark&logoColor=white)]()
[![Apache Hive](https://img.shields.io/badge/Apache_Hive-Data_Warehouse-FDEE21.svg?logo=apachehive&logoColor=black)]()
[![Airflow](https://img.shields.io/badge/Airflow-Task_Scheduling-017CEE.svg?logo=apacheairflow&logoColor=white)]()

> **"Data is the new oil, but pipelines are the refineries."** > 致力于构建高可用、低延迟、强一致性的企业级数据流水线。

## 👨‍💻 About Me

你好，我是来自重庆邮电大学（CQUPT）**数据计算及应用**专业的大四学生。

在先前的职业实践中，我曾于 **德勤 (Deloitte)** 担任大数据开发实习生，参与了企业级数仓新老集群迁移、Airflow 任务调度优化以及大规模数据质量（DQ）自动化巡检体系的建设。

本仓库是我发起的 **“180天数据开发硬核拉练计划”**。旨在将我过去的工程实践经验进行底层理论化，系统性重构从离线数仓建模、分布式计算引擎（Spark）调优到全链路工作流调度的核心技术栈，以迎接未来的严峻技术挑战。

## 🛠️ Tech Stack & Core Competencies

* 💻 **编程语言与算法**: Python (OOP, Type Hinting, Docstrings), 高阶 SQL (Window Functions, CTEs)
* 🏛️ **数据仓库体系**: Kimball 维度建模理论, ODS/DWD/DWS/ADS 分层架构设计
* 🐘 **大数据生态系统**: Hadoop (HDFS/YARN), Apache Hive (存储格式与数据倾斜调优)
* ⚡ **分布式计算引擎**: Apache Spark, PySpark DataFrame API, Spark UI 性能调优
* ⏱️ **任务流调度与运维**: Apache Airflow (DAGs, Dependencies), Linux Shell (awk/sed/grep)
* ⚙️ **工程化实践**: Git 约定式提交 (Conventional Commits), 数据质量监控断言开发

## 📂 Repository Structure (仓库导航)

* 👉 **[`/01_Daily_Execution_Logs`](./01_Daily_Execution_Logs)**: 每日技术迭代日志。记录技术难点攻坚过程、踩坑复盘与源码级解析。
* 👉 **[`/02_Code_Achievements`](./02_Code_Achievements)**: 核心代码沉淀区。包含企业级规范编写的 Python 算法题解、复杂业务 SQL 实现及数据自动化脚本。
* 👉 **[`/03_Data_Pipeline_Projects`](./03_Data_Pipeline_Projects)**: 个人全链路离线数仓项目实战源码（建设中）。

---

## 🗺️ 180-Day Execution Roadmap & Progress Tracker

> 本计划采用敏捷开发思维，按周划定 Sprint 目标，严格践行 Git 开源提交规范。

### 🛡️ Phase 1: Data Engineering Foundations (Week 1-6)
*聚焦于 Python 底层特性剖析、高难度 SQL 场景攻坚与企业级代码规范落地。*

- [x] **Week 1:** Python 内存机制与双指针算法实战，确立 PEP 8 与 Type Hint 规范。
- [ ] **Week 2:** 哈希映射底层逻辑与复杂多表级联（JOIN）业务场景优化。
- [ ] **Week 3:** 🔥 **核武级 SQL 攻坚**：彻底掌握窗口函数 (Window Functions) 体系（连续登录、留存率、各类 TopN 业务）。
- [ ] **Week 4:** Python 面向对象编程 (OOP) 与企业级异常拦截 (Try-Except/Logging) 机制开发。
- [ ] **Week 5:** Linux 服务器文本处理大师：熟练运用 Shell 三剑客 (`grep`, `awk`, `sed`) 进行海量日志提纯。
- [ ] **Week 6:** Hadoop 生态宏观架构剖析：HDFS 读写全流程原理与 YARN 资源调度策略。

### 🏗️ Phase 2: Data Warehouse Architecture (Week 7-12)
*聚焦于 Kimball 维度建模、海量数据调度治理与实习级业务场景的底层重构。*

- [ ] **Week 7:** Hive 底层架构 (HQL 转换 MapReduce 原理) 与 Parquet/ORC 列式存储性能对比。
- [ ] **Week 8:** 海量数据治理：Hive 动态分区 (Partition) 与分桶 (Bucket) 的实战应用。
- [ ] **Week 9:** 🔥 **数仓灵魂建设**：深挖 Kimball 维度建模，彻底吃透 ODS -> DWD -> DWS -> ADS 数据流转闭环。
- [ ] **Week 10:** 调度中枢重构：Apache Airflow DAG 进阶开发，精准控制复杂 Task 的时序与血缘依赖。
- [ ] **Week 11:** 解决大厂痛点：深入剖析数据倾斜 (Data Skew) 成因，掌握加盐、MapJoin、两阶段聚合等 7 种破解方案。
- [ ] **Week 12:** 数据质量 (Data Quality) 闭环：基于 Python 开发自动化数据一致性比对与抽样巡检脚本。

### ⚔️ Phase 3: Distributed Computing & Spark Tuning (Week 13-18)
*聚焦于现代大数据引擎的核心原理、流批一体化代码开发与 Web UI 性能调优。*

- [ ] **Week 13:** Spark 核心架构解析：RDD 弹性分布式数据集、宽窄依赖底层机制与 Stage 划分原理。
- [ ] **Week 14:** PySpark 数据管道开发：熟练使用 DataFrame API 与 Spark SQL 混合编程。
- [ ] **Week 15:** 🔥 **集群性能调优**：深入 Spark Web UI，定位 GC 停顿、数据倾斜及 Executor 资源分配瓶颈。
- [ ] **Week 16:** 💻 **【全链路实战】(上游)**：PySpark 数仓环境搭建、亿级模拟业务数据接入与 ODS 层落盘。
- [ ] **Week 17:** 💻 **【全链路实战】(中台)**：基于 PySpark 实施 DWD/DWS 层复杂聚合，接入 Airflow 实现无人值守调度。
- [ ] **Week 18:** AI 赋能前瞻：探索 LLM 在数据开发领域的提效应用 (Prompt 辅助 SQL 生成与异常检测)。

### 🏆 Phase 4: Advanced Tuning & Open Source (Week 19-24)
*聚焦于知识体系的极致内化、底层源码八股文防御及开源社区探索。*

- [ ] **Week 19:** 核心底层防御：Python GIL 锁与 GC 机制；MySQL 聚簇索引树与 MVCC 隔离级别。
- [ ] **Week 20:** 大数据组件深层防御：Spark 内存动态分配机制；Hive 谓词下推与向量化查询调优。
- [ ] **Week 21:** 业务场景答辩演练：基于 STAR 法则，对大规模数仓迁移与质量保障业务进行深度沙盘推演。
- [ ] **Week 22:** 算法肌肉记忆复盘：LeetCode 核心数据结构高频题极致优化，确保 Bug-Free 手撕能力。
- [ ] **Week 23:** 高效信息检索与匹配：聚焦头部外企科技岗、金融科技中心与新能源数据平台，开启全面技术检验。
- [ ] **Week 24:** 沉淀与进化：整理高压面试复盘文档，查漏补缺，拥抱开源，向下一个里程碑进发！