--如果对MySQL表名字或类型有所更改，请手手动进行ALTER
CREATE TABLE IF NOT EXISTS user_info (
    qid BIGINT PRIMARY KEY COMMENT '用户QQid',
    nickname VARCHAR(16) NOT NULL DEFAULT "您" COMMENT '用户名称',
    integral BIGINT NOT NULL DEFAULT 0 COMMENT '用户积分',
    sign_time TIMESTAMP COMMENT '签到时间',
    liking TINYINT NOT NULL DEFAULT 0 COMMENT '好感度',
    sign_group BIGINT NOT NULL COMMENT '在哪个群或个人签到',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间',
    signs SMALLINT NOT NULL  DEFAULT 0 COMMENT '累计签到次数',
    continuous SMALLINT NOT NULL DEFAULT 0 COMMENT '连续签到次数',
    month_signs TINYINT NOT NULL  DEFAULT 0 COMMENT '本月累计次数',
    repeats TINYINT NOT NULL DEFAULT 0 COMMENT '重复签到次数'
)
