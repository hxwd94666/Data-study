--数据定义语言ddl
/**
 * 📝 架构师核心笔记 (Code as Notes): Hive DDL 企业级建表规范
 * 📁 归属层级: ODS (贴源数据层 - Operational Data Store)
 * 🛡️ 核心灾备防御机制 (面试核心防御话术):
 * 1. 外部表防御 (EXTERNAL): 强行剥夺 Hive 对底层数据的物理删除权。当执行 DROP TABLE 时，
 * 仅销毁 RDBMS 中的元数据(皮)，HDFS 底层真实物理文件(肉)毫发无伤，实现防误删跑路。
 * 2. 分区裁剪 (PARTITIONED BY): 按日期(dt)进行目录级物理隔离。查询时触发
 * 谓词下推 (Predicate Pushdown)，直接跳过无关目录，杜绝全表扫描引发的算力宕机。
 */

-- 1. 切换目标数据库 (环境准备)
CREATE DATABASE IF NOT EXISTS ods COMMENT '贴源数据层';
USE ods;

-- 2. 强制标准：ODS 层原始数据表必须为 EXTERNAL 外部表
CREATE EXTERNAL TABLE IF NOT EXISTS ods_user_action_log (
    `log_id`        STRING      COMMENT '全局唯一日志追踪ID',
    `user_id`       STRING      COMMENT '用户唯一标识符(UUID/DeviceID)',
    `action_type`   STRING      COMMENT '前端埋点行为类型(如: click, view, add_cart)',
    `page_url`      STRING      COMMENT '用户当前所处页面完整URL',
    `action_time`   TIMESTAMP   COMMENT '行为发生服务器时间(精确到毫秒)',
    `client_ip`     STRING      COMMENT '客户端发起请求的合法IP地址'
)
COMMENT 'ODS层-用户前端埋点行为流水日志表'

-- 3. 强制标准：增量流水数据必须使用时间分区
PARTITIONED BY (
    `dt`            STRING      COMMENT '业务增量日期分区键(标准格式: yyyy-MM-dd)'
)

-- 4. 强制标准：明确定义 HDFS 底层纯文本的反序列化切割规则
ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '\t'   -- 字段级分隔符：强制使用 Tab 键 (防止由于 URL 中带逗号导致字段错位)
    LINES TERMINATED BY '\n'    -- 行级分隔符：标准换行符

-- 5. 明确存储压缩格式与 HDFS 挂载绝对路径
STORED AS TEXTFILE
LOCATION '/warehouse/ods/ods_user_action_log/';