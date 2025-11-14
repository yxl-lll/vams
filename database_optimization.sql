-- 校园志愿者活动管理系统 - 数据库性能优化脚本
-- 添加必要的索引以提高查询性能

USE volunteer;

-- 活动计划表索引
CREATE INDEX idx_volunteer_plans_status ON volunteer_plans(status);
CREATE INDEX idx_volunteer_plans_activity_date ON volunteer_plans(activity_date);
CREATE INDEX idx_volunteer_plans_activity_type ON volunteer_plans(activity_type);
CREATE INDEX idx_volunteer_plans_user_id ON volunteer_plans(user_id);
CREATE INDEX idx_volunteer_plans_created_at ON volunteer_plans(created_at);

-- 活动参与记录表索引
CREATE INDEX idx_participation_activity_id ON participation(activity_id);
CREATE INDEX idx_participation_user_id ON participation(user_id);
CREATE INDEX idx_participation_status ON participation(status);
CREATE INDEX idx_participation_activity_date ON participation(activity_date);
CREATE INDEX idx_participation_created_at ON participation(created_at);

-- 活动类型表索引
CREATE INDEX idx_activity_type_type_name ON activity_type(type_name);
CREATE INDEX idx_activity_type_difficulty_level ON activity_type(difficulty_level);

-- 活动审核表索引
CREATE INDEX idx_activity_audit_activity_id ON activity_audit(activity_id);
CREATE INDEX idx_activity_audit_auditor_id ON activity_audit(auditor_id);
CREATE INDEX idx_activity_audit_audit_status ON activity_audit(audit_status);
CREATE INDEX idx_activity_audit_audit_time ON activity_audit(audit_time);

-- 志愿者档案表索引
CREATE INDEX idx_volunteer_profile_user_id ON volunteer_profile(user_id);
CREATE INDEX idx_volunteer_profile_volunteer_level ON volunteer_profile(volunteer_level);
CREATE INDEX idx_volunteer_profile_join_date ON volunteer_profile(join_date);

-- 通知消息表索引
CREATE INDEX idx_notification_target_user_id ON notification(target_user_id);
CREATE INDEX idx_notification_type ON notification(type);
CREATE INDEX idx_notification_is_read ON notification(is_read);
CREATE INDEX idx_notification_priority ON notification(priority);
CREATE INDEX idx_notification_created_at ON notification(created_at);

-- 用户表索引
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_user_phone ON user(phone);

-- 角色表索引
CREATE INDEX idx_role_role_name ON role(role_name);

-- 菜单表索引
CREATE INDEX idx_menu_parent_id ON menu(parent_id);
CREATE INDEX idx_menu_menu_name ON menu(menu_name);

-- 复合索引
CREATE INDEX idx_volunteer_plans_status_date ON volunteer_plans(status, activity_date);
CREATE INDEX idx_participation_user_status ON participation(user_id, status);
CREATE INDEX idx_notification_user_read ON notification(target_user_id, is_read);

-- 查看索引创建结果
SHOW INDEX FROM volunteer_plans;
SHOW INDEX FROM participation;
SHOW INDEX FROM activity_type;
SHOW INDEX FROM activity_audit;
SHOW INDEX FROM volunteer_profile;
SHOW INDEX FROM notification;
