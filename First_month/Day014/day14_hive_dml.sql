/* hive sql dml */

--加载数据load：将本地数据文件移动到hdfs对应目录下(本质是复制），hive会自动识别数据格式并生成表结构
--语法：load data [local] inpath 'hdfs_file_path' [overwrite] into table dst_table [partition(partcol1=val1, partcol2=val2 ...)];
load data local inpath '/data/ods_user_action_log.txt' overwrite into table ods_user_action_log partition(dt='2020-05-01');
--解释: 将本地文件/data/ods_user_action_log.txt移动到对应目录下，并生成表结构
--这个local 是可选的，如果不加这个，hive会自动去hdfs上寻找这个文件，本质是剪切/移动！！！
--overwrite 是可选的，如果加这个，则会覆盖掉这个表对应的目录下的数据
--如果不加分区，hive会把load改写为insert as select

'插入数据insert：将数据插入表'
--不能使用insert+values语法，这在hive中用时很久，他会在hdfs中创建一个临时文件，然后移动到对应目录下
--语法1：
     -- insert into table tablename1 [partition(partcol1=val1, partcol2=val2 ...)] select_statement;
--语法2：
     -- insert overwrite table tablename1 [partition(partcol1=val1, partcol2=val2 ...)] select_statement;
--select_statement是具体select from语句

'多重插入Multiple Insert：一次扫描，多次插入（优化性能）'
--语法：
from tablename1
insert into table tablename2
select xxx
insert overwrite table tablename3
select xxx;

'动态分区插入Dynamic Partition Insert：一次扫描，一次插入，一次分区'
--需要先开启动态分区功能：set hive.exec.dynamic.partition=true;

--动态分区模式:hive.exec.dynamic.partition.mode
-- 静态分区：硬编码。你必须在 SQL 里写死 `PARTITION(dt='2026-03-25')`。
-- 痛点：如果上游一次性推过来了过去 100 天的历史补偿数据，你用静态分区必须写 100 句 `INSERT`，极其愚蠢且无法自动化。
-- 动态分区：引擎自适应。你不写死日期，只写 `PARTITION(dt)`。Hive 会*自动读取 `SELECT` 查询结果集的最后一列，发现是几号，就自动在 HDFS 上创建几号的目录，并把对应数据塞进去。

-- 动态覆写标准语法
INSERT OVERWRITE TABLE dwd_user_action_log PARTITION (dt)
SELECT
    log_id,
    user_id,
    action_type,
    -- ... 其他清洗后的字段
    dt  -- ⚠️极其致命的规范：动态分区字段必须放在 SELECT 语句的最后面！
FROM ods_user_action_log

-- 动态分区插入混合语法
INSERT OVERWRITE TABLE dwd_log PARTITION (dt='2026-03-25', hour)
SELECT log_id, user_id, action_time,
       hour(action_time) -- 注意：SELECT 里面只需要跟 hour 即可，dt 已经在上面写死了
FROM ods_log;
-- 两层分区，注意静态分区字段必须放在动态分区字段的前面

'导出数据insert directory'
--⚠️注意导出数据是覆盖操作
--语法：insert overwrite [local] directory 'hdfs_dir_path'
-- [ROW FORMAT DELIMITED FIELDS TERMINATED BY ',']
-- select_statement;

-- 1. 出仓与交付 (Data Export)
-- 应用场景：数据分析师或业务运营部门需要你把 Hive 里跑完的报表，直接导成一个 `.csv` 或文本文件发给他们。
-- 物理流转：将底层的分布式计算结果（MapReduce/Spark），物理提取并输出到指定的操作系统目录中。
-- 2. 加不加 LOCAL？
-- `INSERT OVERWRITE LOCAL DIRECTORY`：
-- 导出目的地：本地服务器的 Linux/Mac 硬盘系统
-- `INSERT OVERWRITE DIRECTORY` (不加 LOCAL)：
-- 导出目的地：HDFS 分布式文件系统。
-- ⚠️致命雷区 (格式崩塌)：如果你仅仅执行导出，Hive 默认会使用键盘上打不出来的 `^A` (`\001`) 作为列分隔符。业务方拿到文件用 Excel 一打开，所有列全部挤在一个单元格里，当场崩溃！
--
-- *架构师标准写法 (必须强制指定分隔符)：
-- 将 VIP 用户名单导出到本地服务器，并强制指定逗号分隔，方便业务方使用 Excel 打开
INSERT OVERWRITE LOCAL DIRECTORY '/opt/module/hive/export_data/vip_users'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' -- 强制指定分隔符
SELECT
    user_id,
    total_amount
FROM dws_user_purchase_summary
WHERE dt = '2026-03-24' AND total_amount > 10000;