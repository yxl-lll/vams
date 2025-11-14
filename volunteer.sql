/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80019
 Source Host           : localhost:3306
 Source Schema         : volunteer

 Target Server Type    : MySQL
 Target Server Version : 80019
 File Encoding         : 65001

 Date: 15/07/2025 18:54:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单ID',
  `menu_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单名称',
  `p_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '0' COMMENT '父菜单ID，顶级菜单为0',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单链接地址',
  `hurl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `icon` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单图标',
  `sort` int(0) NOT NULL DEFAULT 0 COMMENT '菜单排序',
  `menu_status` int(0) NOT NULL DEFAULT 1 COMMENT '菜单状态，0表示禁用，1表示启用',
  `created_at` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `type` int(0) NULL DEFAULT NULL COMMENT '类型',
  `auth_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `parent_id`(`p_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '菜单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES ('1', '首页', '0', NULL, 'static/views/home/index.html', 'layui-icon-home ', 1000, 1, '2025-04-28 14:57:43', '2025-07-25 03:20:35', 1, '1');
INSERT INTO `menu` VALUES ('10', '用户管理', '13', 'user', 'static/views/user/list.html', 'layui-icon-username', 3, 1, NULL, '2025-05-20 21:14:30', 1, 'sys:user:page');
INSERT INTO `menu` VALUES ('11', '角色管理', '13', 'role', 'static/views/role/list.html', 'layui-icon-auz', 1, 1, NULL, '2025-06-19 00:56:42', 1, 'sys:role:page');
INSERT INTO `menu` VALUES ('13', '系统管理', '0', 'sys', NULL, 'layui-icon-slider', 100, 1, NULL, '2025-05-23 04:56:17', 2, NULL);
INSERT INTO `menu` VALUES ('14', '菜单管理', '13', 'menu', 'static/views/menu/list.html', 'user', 2, 1, NULL, '2025-05-20 21:15:11', 1, 'sys:menu:page');
INSERT INTO `menu` VALUES ('1c731dd0-d3a3-4036-b8c8-8cefd5183252', '活动参与记录', '0', NULL, 'static/views/participation/list.html', 'layui-icon-copyright', 700, 1, '2025-07-30 02:34:48', '2025-07-30 02:34:48', 1, '');
INSERT INTO `menu` VALUES ('a67011f2-db66-49aa-b904-57c4571fe441', '活动类型管理', '0', NULL, 'static/views/activity-type/list.html', 'layui-icon-CI', 900, 1, '2025-07-30 02:35:14', '2025-07-30 02:35:14', 1, '');
INSERT INTO `menu` VALUES ('c8410c1e-4f71-4710-bc6a-986adc4dd76e', '活动计划管理', '0', NULL, 'static/views/volunteer-plans/list.html', 'layui-icon-trademark', 800, 1, '2025-07-30 02:34:22', '2025-07-30 02:34:22', 1, '');
INSERT INTO `menu` VALUES ('d1e731dd0-d3a3-4036-b8c8-8cefd5183253', '活动审核管理', '0', NULL, 'static/views/activity-audit/list.html', 'layui-icon-verification', 650, 1, '2025-07-30 02:34:48', '2025-07-30 02:34:48', 1, '');
INSERT INTO `menu` VALUES ('e1e731dd0-d3a3-4036-b8c8-8cefd5183254', '志愿者档案', '0', NULL, 'static/views/volunteer-profile/list.html', 'layui-icon-user', 750, 1, '2025-07-30 02:34:48', '2025-07-30 02:34:48', 1, '');
INSERT INTO `menu` VALUES ('f1e731dd0-d3a3-4036-b8c8-8cefd5183255', '通知消息管理', '0', NULL, 'static/views/notification/list.html', 'layui-icon-notice', 550, 1, '2025-07-30 02:34:48', '2025-07-30 02:34:48', 1, '');

-- ----------------------------
-- Table structure for menu_role
-- ----------------------------
DROP TABLE IF EXISTS `menu_role`;
CREATE TABLE `menu_role`  (
  `menu_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单ID',
  `role_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`menu_id`, `role_id`) USING BTREE,
  INDEX `idx_menu_id`(`menu_id`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  CONSTRAINT `menu_role_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `menu_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '菜单与角色对应关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menu_role
-- ----------------------------
INSERT INTO `menu_role` VALUES ('1', '300c55c2-a7ce-429f-bbce-56e102616746');
INSERT INTO `menu_role` VALUES ('1', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');
INSERT INTO `menu_role` VALUES ('10', '300c55c2-a7ce-429f-bbce-56e102616746');
INSERT INTO `menu_role` VALUES ('11', '300c55c2-a7ce-429f-bbce-56e102616746');
INSERT INTO `menu_role` VALUES ('13', '300c55c2-a7ce-429f-bbce-56e102616746');
INSERT INTO `menu_role` VALUES ('14', '300c55c2-a7ce-429f-bbce-56e102616746');
INSERT INTO `menu_role` VALUES ('1c731dd0-d3a3-4036-b8c8-8cefd5183252', '300c55c2-a7ce-429f-bbce-56e102616746');
INSERT INTO `menu_role` VALUES ('1c731dd0-d3a3-4036-b8c8-8cefd5183252', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');

INSERT INTO `menu_role` VALUES ('b2e279e7-1075-419f-a818-04b37805ab63', '300c55c2-a7ce-429f-bbce-56e102616746');

INSERT INTO `menu_role` VALUES ('c8410c1e-4f71-4710-bc6a-986adc4dd76e', '300c55c2-a7ce-429f-bbce-56e102616746');
INSERT INTO `menu_role` VALUES ('c8410c1e-4f71-4710-bc6a-986adc4dd76e', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');




-- ----------------------------
-- Table structure for participation
-- ----------------------------
DROP TABLE IF EXISTS `participation`;
CREATE TABLE `participation`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `activity_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动ID',
  `activity_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动名称',
  `activity_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '活动图片',
  `activity_date` datetime(0) NULL DEFAULT NULL COMMENT '活动日期',
  `activity_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动类型',
  `service_hours` decimal(5,2) NULL DEFAULT 0.00 COMMENT '服务时长(小时)',
  `participant_count` int(0) NULL DEFAULT 1 COMMENT '参与人数',
  `check_in_time` datetime(0) NULL DEFAULT NULL COMMENT '签到时间',
  `check_out_time` datetime(0) NULL DEFAULT NULL COMMENT '签退时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'registered' COMMENT '状态：registered-已报名/checked_in-已签到/completed-已完成/cancelled-已取消',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
  `user_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户姓名',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_activity_id`(`activity_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '活动参与记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of participation
-- ----------------------------
INSERT INTO `participation` VALUES ('p001', 'vp001', '社区环保清洁活动', NULL, '2025-08-15 09:00:00', '环保活动', 3.00, 1, '2025-08-15 08:45:00', '2025-08-15 12:00:00', 'completed', '积极参与，表现优秀', 'b380df2e-2488-4cbd-96f6-5e6ec03e76f5', '张三', '2025-07-15 10:00:00', '2025-08-15 12:00:00');
INSERT INTO `participation` VALUES ('p002', 'vp002', '贫困学生助学活动', NULL, '2025-08-20 14:00:00', '教育支持', 4.00, 1, '2025-08-20 13:30:00', '2025-08-20 18:00:00', 'completed', '教学认真，学生反馈良好', 'c480df2e-2488-4cbd-96f6-5e6ec03e76f6', '李四', '2025-07-16 10:00:00', '2025-08-20 18:00:00');
INSERT INTO `participation` VALUES ('p003', 'vp004', '科技知识普及讲座', NULL, '2025-08-30 19:00:00', '科技普及', 2.50, 1, '2025-08-30 18:30:00', '2025-08-30 21:30:00', 'completed', '讲解生动，听众反应热烈', 'f780df2e-2488-4cbd-96f6-5e6ec03e76f9', '孙七', '2025-07-18 10:00:00', '2025-08-30 21:30:00');
INSERT INTO `participation` VALUES ('p004', 'vp007', '体育健身指导活动', NULL, '2025-09-15 16:00:00', '体育健身', 2.00, 1, '2025-09-15 15:45:00', '2025-09-15 18:00:00', 'completed', '指导专业，学员进步明显', 'f42f0f7d-c835-45a4-b36c-dca85a2f09c7', '体育志愿者', '2025-07-21 10:00:00', '2025-09-15 18:00:00');
INSERT INTO `participation` VALUES ('p005', 'vp008', '社区服务日活动', NULL, '2025-09-20 08:00:00', '社区服务', 4.50, 1, '2025-09-20 07:30:00', '2025-09-20 12:00:00', 'completed', '服务周到，居民满意度高', '32f2a899-7cf0-4a8a-bccf-907711a0e1b1', '社区志愿者', '2025-07-22 10:00:00', '2025-09-20 12:00:00');
INSERT INTO `participation` VALUES ('p006', 'vp001', '社区环保清洁活动', NULL, '2025-08-15 09:00:00', '环保活动', 3.00, 1, '2025-08-15 08:50:00', '2025-08-15 12:00:00', 'completed', '认真负责，团队合作好', 'e680df2e-2488-4cbd-96f6-5e6ec03e76f8', '赵六', '2025-07-23 10:00:00', '2025-08-15 12:00:00');
INSERT INTO `participation` VALUES ('p007', 'vp004', '科技知识普及讲座', NULL, '2025-08-30 19:00:00', '科技普及', 2.50, 1, '2025-08-30 18:45:00', '2025-08-30 21:30:00', 'completed', '积极参与互动，学习态度好', 'c480df2e-2488-4cbd-96f6-5e6ec03e76f6', '李四', '2025-07-24 10:00:00', '2025-08-30 21:30:00');
INSERT INTO `participation` VALUES ('p008', 'vp005', '传统文化传承活动', NULL, '2025-09-05 10:00:00', '文化传播', 3.50, 1, '2025-09-05 09:30:00', '2025-09-05 13:00:00', 'ongoing', '表演精彩，观众反响热烈', 'a5a0b9da-708a-4535-86de-b7f717fea48a', '文化志愿者', '2025-07-25 10:00:00', '2025-09-05 13:00:00');
INSERT INTO `participation` VALUES ('p009', 'vp003', '社区健康义诊活动', NULL, '2025-08-25 09:00:00', '医疗健康', 5.00, 1, NULL, NULL, 'registered', '已报名，等待活动开始', 'd580df2e-2488-4cbd-96f6-5e6ec03e76f7', '王五', '2025-07-26 10:00:00', '2025-07-26 10:00:00');
INSERT INTO `participation` VALUES ('p010', 'vp006', '应急救援培训活动', NULL, '2025-09-10 09:00:00', '应急救援', 6.00, 1, NULL, NULL, 'registered', '已报名，期待学习应急技能', 'd6cfeb20-0a67-4869-8778-900dd0e7238f', '应急志愿者', '2025-07-27 10:00:00', '2025-07-27 10:00:00');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `role_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '名称',
  `role_desc` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('300c55c2-a7ce-429f-bbce-56e102616746', '管理员', '管理员', '2025-05-08 00:37:25', '2025-07-30 06:09:49');
INSERT INTO `role` VALUES ('b2168c4f-b972-4d05-ad1b-ff8558c04388', '默认角色', '默认角色不允许删除', '2025-05-12 00:04:55', '2025-07-30 07:16:44');

-- ----------------------------
-- Table structure for volunteer_plans
-- ----------------------------
DROP TABLE IF EXISTS `volunteer_plans`;
CREATE TABLE `volunteer_plans`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `activity_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动名称',
  `activity_date` datetime(0) NULL DEFAULT NULL COMMENT '活动日期',
  `activity_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动类型',
  `location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动地点',
  `service_hours` decimal(5,2) NOT NULL COMMENT '预计服务时长(小时)',
  `max_participants` int(0) NOT NULL DEFAULT 1 COMMENT '最大参与人数',
  `current_participants` int(0) NULL DEFAULT 0 COMMENT '当前报名人数',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'draft' COMMENT '状态：draft-草稿/pending-待审核/approved-已通过/rejected-已拒绝/ongoing-进行中/completed-已完成/cancelled-已取消',
  `requirements` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '参与要求',
  `benefits` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '活动福利',
  `contact_person` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系人',
  `contact_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系电话',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '备注',
  `user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '创建用户ID',
  `user_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '创建用户姓名',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_activity_type`(`activity_type`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '志愿者活动计划' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of volunteer_plans
-- ----------------------------
INSERT INTO `volunteer_plans` VALUES ('vp001', '社区环保清洁活动', '2025-08-15 09:00:00', '环保活动', '北京市朝阳区社区公园', 3.00, 20, 15, 'approved', '身体健康，有环保意识', '提供工作餐，颁发志愿者证书', '李主任', '13800138001', '定期社区环保活动，提升居民环保意识', 'b380df2e-2488-4cbd-96f6-5e6ec03e76f5', '张三', '2025-07-15 10:00:00', '2025-07-15 10:00:00');
INSERT INTO `volunteer_plans` VALUES ('vp002', '贫困学生助学活动', '2025-08-20 14:00:00', '教育支持', '河北省张家口市希望小学', 4.00, 10, 8, 'approved', '有教学经验，耐心细致', '提供交通补贴，住宿安排', '王老师', '13800138002', '为贫困地区学生提供教育支持', 'c480df2e-2488-4cbd-96f6-5e6ec03e76f6', '李四', '2025-07-16 10:00:00', '2025-07-16 10:00:00');
INSERT INTO `volunteer_plans` VALUES ('vp003', '社区健康义诊活动', '2025-08-25 09:00:00', '医疗健康', '北京市海淀区社区服务中心', 5.00, 15, 12, 'pending', '具备医疗资质，有临床经验', '提供专业培训，颁发证书', '张医生', '13800138003', '为社区居民提供免费健康检查', 'd580df2e-2488-4cbd-96f6-5e6ec03e76f7', '王五', '2025-07-17 10:00:00', '2025-07-17 10:00:00');
INSERT INTO `volunteer_plans` VALUES ('vp004', '科技知识普及讲座', '2025-08-30 19:00:00', '科技普及', '北京市西城区科技馆', 2.50, 50, 35, 'approved', '具备科技知识，有讲解能力', '提供学习资料，颁发参与证书', '陈教授', '13800138004', '向公众普及科技知识', 'f780df2e-2488-4cbd-96f6-5e6ec03e76f9', '孙七', '2025-07-18 10:00:00', '2025-07-18 10:00:00');
INSERT INTO `volunteer_plans` VALUES ('vp005', '传统文化传承活动', '2025-09-05 10:00:00', '文化传播', '北京市东城区文化馆', 3.50, 30, 22, 'ongoing', '热爱传统文化，有表演经验', '提供表演服装，颁发荣誉证书', '刘老师', '13800138005', '传承和弘扬中华传统文化', 'a5a0b9da-708a-4535-86de-b7f717fea48a', '文化志愿者', '2025-07-19 10:00:00', '2025-07-19 10:00:00');
INSERT INTO `volunteer_plans` VALUES ('vp006', '应急救援培训活动', '2025-09-10 09:00:00', '应急救援', '北京市丰台区消防训练基地', 6.00, 25, 18, 'draft', '身体健康，有应急意识', '提供专业培训，颁发应急证书', '赵队长', '13800138006', '提升公众应急救援能力', 'd6cfeb20-0a67-4869-8778-900dd0e7238f', '应急志愿者', '2025-07-20 10:00:00', '2025-07-20 10:00:00');
INSERT INTO `volunteer_plans` VALUES ('vp007', '体育健身指导活动', '2025-09-15 16:00:00', '体育健身', '北京市石景山区体育中心', 2.00, 40, 28, 'approved', '具备体育技能，有教学经验', '提供运动装备，颁发指导证书', '孙教练', '13800138007', '指导社区居民科学健身', 'f42f0f7d-c835-45a4-b36c-dca85a2f09c7', '体育志愿者', '2025-07-21 10:00:00', '2025-07-21 10:00:00');
INSERT INTO `volunteer_plans` VALUES ('vp008', '社区服务日活动', '2025-09-20 08:00:00', '社区服务', '北京市通州区社区广场', 4.50, 35, 30, 'completed', '有服务意识，沟通能力强', '提供工作餐，颁发服务证书', '周主任', '13800138008', '为社区居民提供便民服务', '32f2a899-7cf0-4a8a-bccf-907711a0e1b1', '社区志愿者', '2025-07-22 10:00:00', '2025-07-22 10:00:00');

-- ----------------------------
-- Table structure for activity_type
-- ----------------------------
DROP TABLE IF EXISTS `activity_type`;
CREATE TABLE `activity_type`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `type_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '类型名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '类型描述',
  `difficulty_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'normal' COMMENT '难度等级：easy-简单/normal-普通/hard-困难',
  `required_skills` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '所需技能',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '活动类型分类' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of activity_type
-- ----------------------------
INSERT INTO `activity_type` VALUES ('32f2a899-7cf0-4a8a-bccf-907711a0e1b1', '社区服务', '为社区居民提供各种便民服务', 'normal', '沟通能力、服务意识', '', '2025-07-30 05:09:21', '2025-07-15 11:07:24');
INSERT INTO `activity_type` VALUES ('402fdac3-dc5c-480d-8c6d-74feb1d616be', '环保活动', '环境保护相关的志愿活动', 'easy', '环保意识、团队合作', '', '2025-07-15 11:08:30', '2025-07-15 11:08:30');
INSERT INTO `activity_type` VALUES ('a13d2c9e-848f-437a-b45f-92839e54fc59', '教育支持', '为贫困学生提供教育帮助', 'hard', '教学能力、耐心', '', '2025-07-30 05:09:14', '2025-07-15 11:07:34');
INSERT INTO `activity_type` VALUES ('a43751df-6e37-430a-951f-7fca57578642', '医疗健康', '医疗健康相关的志愿活动', 'hard', '医疗知识、急救技能', '', '2025-07-30 05:09:04', '2025-07-15 11:08:09');
INSERT INTO `activity_type` VALUES ('a5a0b9da-708a-4535-86de-b7f717fea48a', '文化传播', '文化传承和传播活动', 'normal', '文化知识、表达能力', '', '2025-07-30 05:09:33', '2025-07-15 11:07:46');
INSERT INTO `activity_type` VALUES ('d6cfeb20-0a67-4869-8778-900dd0e7238f', '应急救援', '突发事件应急救援活动', 'hard', '应急技能、心理素质', '', '2025-07-30 05:09:09', '2025-07-15 11:08:01');
INSERT INTO `activity_type` VALUES ('f42f0f7d-c835-45a4-b36c-dca85a2f09c7', '体育健身', '体育健身相关的志愿活动', 'normal', '体育技能、组织能力', '', '2025-07-30 05:09:28', '2025-07-15 11:08:13');
INSERT INTO `activity_type` VALUES ('f6cee33f-0ab3-4a79-8652-539ddfe0324d', '科技普及', '科技知识普及活动', 'normal', '科技知识、讲解能力', '', '2025-07-15 11:07:16', '2025-07-15 11:08:16');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '人员ID',
  `gender` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '1' COMMENT '性别',
  `birthday` date NULL DEFAULT NULL COMMENT '出生日期',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号码',
  `nick_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '昵称',
  `email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电子邮件',
  `address` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地址',
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '登录账号',
  `password` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '登录密码',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '状态，0表示禁用，1表示启用',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '头像',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_username`(`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '人员表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('2a40f198-47e3-471c-ad38-7422fc1d7b38', '1', '2025-05-14', '15610101721', '系统管理员', 'admin@admin.com', 'di', 'admin', 'd5d7d8507e2fabc8e116ecfcc98d91a7', 1, '2025-05-12 08:53:42', '2025-07-15 16:31:18', '/apfile/MTcxNjM3MDQ2NjE3NF8xLnBuZw==');
INSERT INTO `user` VALUES ('b380df2e-2488-4cbd-96f6-5e6ec03e76f5', '1', '2025-07-16', '15610101721', '张三', 'zhangsan@volunteer.com', '北京市朝阳区', 'zhangsan', 'd5d7d8507e2fabc8e116ecfcc98d91a7', 1, '2025-05-11 09:14:39', '2025-07-15 16:33:35', '');
INSERT INTO `user` VALUES ('c480df2e-2488-4cbd-96f6-5e6ec03e76f6', '2', '2025-07-16', '15610101722', '李四', 'lisi@volunteer.com', '北京市海淀区', 'lisi', 'd5d7d8507e2fabc8e116ecfcc98d91a7', 1, '2025-05-11 09:14:39', '2025-07-15 16:33:35', '');
INSERT INTO `user` VALUES ('d580df2e-2488-4cbd-96f6-5e6ec03e76f7', '1', '2025-07-16', '15610101723', '王五', 'wangwu@volunteer.com', '北京市西城区', 'wangwu', 'd5d7d8507e2fabc8e116ecfcc98d91a7', 1, '2025-05-11 09:14:39', '2025-07-15 16:33:35', '');
INSERT INTO `user` VALUES ('e680df2e-2488-4cbd-96f6-5e6ec03e76f8', '2', '2025-07-16', '15610101724', '赵六', 'zhaoliu@volunteer.com', '北京市东城区', 'zhaoliu', 'd5d7d8507e2fabc8e116ecfcc98d91a7', 1, '2025-05-11 09:14:39', '2025-07-15 16:33:35', '');
INSERT INTO `user` VALUES ('f780df2e-2488-4cbd-96f6-5e6ec03e76f9', '1', '2025-07-16', '15610101725', '孙七', 'sunqi@volunteer.com', '北京市丰台区', 'sunqi', 'd5d7d8507e2fabc8e116ecfcc98d91a7', 1, '2025-05-11 09:14:39', '2025-07-15 16:33:35', '');
INSERT INTO `user` VALUES ('g880df2e-2488-4cbd-96f6-5e6ec03e76f0', '1', '2025-07-16', '15610101726', '普通用户', 'test@test.com', NULL, 'user', 'd5d7d8507e2fabc8e116ecfcc98d91a7', 1, '2025-05-11 09:14:39', '2025-07-15 16:33:35', '');

-- ----------------------------
-- Table structure for user_role
-- ----------------------------
DROP TABLE IF EXISTS `user_role`;
CREATE TABLE `user_role`  (
  `user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '人员ID',
  `role_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`, `role_id`) USING BTREE,
  INDEX `idx_role_id`(`role_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '人员与角色中间表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_role
-- ----------------------------
INSERT INTO `user_role` VALUES ('2a40f198-47e3-471c-ad38-7422fc1d7b38', '300c55c2-a7ce-429f-bbce-56e102616746');
INSERT INTO `user_role` VALUES ('b380df2e-2488-4cbd-96f6-5e6ec03e76f5', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');
INSERT INTO `user_role` VALUES ('c480df2e-2488-4cbd-96f6-5e6ec03e76f6', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');
INSERT INTO `user_role` VALUES ('d580df2e-2488-4cbd-96f6-5e6ec03e76f7', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');
INSERT INTO `user_role` VALUES ('e680df2e-2488-4cbd-96f6-5e6ec03e76f8', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');
INSERT INTO `user_role` VALUES ('f780df2e-2488-4cbd-96f6-5e6ec03e76f9', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');
INSERT INTO `user_role` VALUES ('g880df2e-2488-4cbd-96f6-5e6ec03e76f0', 'b2168c4f-b972-4d05-ad1b-ff8558c04388');

-- ----------------------------
-- Table structure for activity_audit
-- ----------------------------
DROP TABLE IF EXISTS `activity_audit`;
CREATE TABLE `activity_audit`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `activity_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动ID',
  `activity_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动名称',
  `activity_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动类型',
  `organizer_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织者姓名',
  `organizer_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织者电话',
  `activity_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动地点',
  `start_time` datetime(0) NOT NULL COMMENT '开始时间',
  `end_time` datetime(0) NOT NULL COMMENT '结束时间',
  `expected_participants` int(0) NOT NULL COMMENT '预计参与人数',
  `activity_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '活动描述',
  `auditor_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '审核人ID',
  `auditor_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '审核人姓名',
  `audit_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '审核状态：pending-待审核/approved-已通过/rejected-已拒绝',
  `audit_remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '审核备注',
  `audit_time` datetime(0) NULL DEFAULT NULL COMMENT '审核时间',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_activity_id`(`activity_id`) USING BTREE,
  INDEX `idx_auditor_id`(`auditor_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '活动审核记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of activity_audit
-- ----------------------------
INSERT INTO `activity_audit` VALUES ('aa001', 'vp001', '社区环保清洁活动', '环保活动', '张三', '15610101721', '北京市朝阳区社区公园', '2025-08-15 09:00:00', '2025-08-15 12:00:00', 20, '定期社区环保活动，提升居民环保意识，包括垃圾分类、清洁卫生等', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'approved', '活动内容积极向上，组织安排合理，同意开展', '2025-07-16 14:30:00', '2025-07-15 10:00:00', '2025-07-16 14:30:00');
INSERT INTO `activity_audit` VALUES ('aa002', 'vp002', '贫困学生助学活动', '教育支持', '李四', '15610101722', '河北省张家口市希望小学', '2025-08-20 14:00:00', '2025-08-20 18:00:00', 10, '为贫困地区学生提供教育支持，包括课程辅导、心理关怀等', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'approved', '教育意义重大，志愿者资质符合要求，同意开展', '2025-07-17 15:20:00', '2025-07-16 10:00:00', '2025-07-17 15:20:00');
INSERT INTO `activity_audit` VALUES ('aa003', 'vp003', '社区健康义诊活动', '医疗健康', '王五', '15610101723', '北京市海淀区社区服务中心', '2025-08-25 09:00:00', '2025-08-25 14:00:00', 15, '为社区居民提供免费健康检查，包括血压、血糖、心电图等基础检查', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'pending', '等待审核', NULL, '2025-07-17 10:00:00', '2025-07-17 10:00:00');
INSERT INTO `activity_audit` VALUES ('aa004', 'vp004', '科技知识普及讲座', '科技普及', '孙七', '15610101725', '北京市西城区科技馆', '2025-08-30 19:00:00', '2025-08-30 21:30:00', 50, '向公众普及科技知识，包括人工智能、新能源、环保科技等前沿话题', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'approved', '科技普及意义重大，讲师资质优秀，同意开展', '2025-07-19 16:45:00', '2025-07-18 10:00:00', '2025-07-19 16:45:00');
INSERT INTO `activity_audit` VALUES ('aa005', 'vp005', '传统文化传承活动', '文化传播', '刘老师', '13800138005', '北京市东城区文化馆', '2025-09-05 10:00:00', '2025-09-05 13:30:00', 30, '传承和弘扬中华传统文化，包括书法、国画、戏曲等艺术形式', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'approved', '文化传承意义深远，活动安排合理，同意开展', '2025-07-20 11:15:00', '2025-07-19 10:00:00', '2025-07-20 11:15:00');
INSERT INTO `activity_audit` VALUES ('aa006', 'vp006', '应急救援培训活动', '应急救援', '赵队长', '13800138006', '北京市丰台区消防训练基地', '2025-09-10 09:00:00', '2025-09-10 15:00:00', 25, '提升公众应急救援能力，包括心肺复苏、止血包扎、火灾逃生等技能培训', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'pending', '等待审核', NULL, '2025-07-20 10:00:00', '2025-07-20 10:00:00');
INSERT INTO `activity_audit` VALUES ('aa007', 'vp007', '体育健身指导活动', '体育健身', '孙教练', '13800138007', '北京市石景山区体育中心', '2025-09-15 16:00:00', '2025-09-15 18:00:00', 40, '指导社区居民科学健身，包括太极拳、广场舞、健身操等运动项目', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'approved', '健身指导专业，场地设施完善，同意开展', '2025-07-22 14:20:00', '2025-07-21 10:00:00', '2025-07-22 14:20:00');
INSERT INTO `activity_audit` VALUES ('aa008', 'vp008', '社区服务日活动', '社区服务', '周主任', '13800138008', '北京市通州区社区广场', '2025-09-20 08:00:00', '2025-09-20 12:30:00', 35, '为社区居民提供便民服务，包括理发、修鞋、法律咨询等', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'approved', '便民服务贴近民生，志愿者经验丰富，同意开展', '2025-07-23 10:30:00', '2025-07-22 10:00:00', '2025-07-23 10:30:00');
INSERT INTO `activity_audit` VALUES ('aa009', 'vp009', '校园安全教育活动', '教育支持', '安全老师', '13800138009', '北京市昌平区第一中学', '2025-09-25 14:00:00', '2025-09-25 16:00:00', 200, '为中学生开展安全教育，包括交通安全、网络安全、防欺凌等知识普及', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'pending', '等待审核', NULL, '2025-07-24 10:00:00', '2025-07-24 10:00:00');
INSERT INTO `activity_audit` VALUES ('aa010', 'vp010', '老年人关爱活动', '社区服务', '关爱志愿者', '13800138010', '北京市房山区敬老院', '2025-09-30 09:00:00', '2025-09-30 11:30:00', 20, '为敬老院老人提供关爱服务，包括陪伴聊天、健康检查、文艺表演等', '2a40f198-47e3-471c-ad38-7422fc1d7b38', '系统管理员', 'pending', '等待审核', NULL, '2025-07-25 10:00:00', '2025-07-25 10:00:00');

-- ----------------------------
-- Table structure for volunteer_profile
-- ----------------------------
DROP TABLE IF EXISTS `volunteer_profile`;
CREATE TABLE `volunteer_profile`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
  `user_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户姓名',
  `real_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '真实姓名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号',
  `id_card` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '身份证号',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '男' COMMENT '性别',
  `birth_date` date NULL DEFAULT NULL COMMENT '出生日期',
  `total_service_hours` decimal(8,2) NULL DEFAULT 0.00 COMMENT '累计服务时长(小时)',
  `total_activities` int(0) NULL DEFAULT 0 COMMENT '参与活动总数',
  `skills` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '技能标签',
  `interests` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '兴趣标签',
  `volunteer_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'bronze' COMMENT '志愿者等级：bronze-青铜/silver-白银/gold-黄金/platinum-铂金',
  `join_date` date NULL DEFAULT NULL COMMENT '加入志愿者时间',
  `status` tinyint(1) NULL DEFAULT 1 COMMENT '状态：0-禁用/1-正常',
  `remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '备注',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '志愿者档案' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of volunteer_profile
-- ----------------------------
INSERT INTO `volunteer_profile` VALUES ('vp001', 'b380df2e-2488-4cbd-96f6-5e6ec03e76f5', '普通用户', '张三', '15610101721', '110101199001011234', '男', '1990-01-01', 45.50, 12, '沟通能力,组织能力,急救技能', '环保,教育,医疗', 'gold', '2024-01-15', 1, '经验丰富的志愿者，多次参与大型活动', '2025-01-15 10:00:00', '2025-07-15 10:00:00');
INSERT INTO `volunteer_profile` VALUES ('vp002', 'c480df2e-2488-4cbd-96f6-5e6ec03e76f6', '李四', '李四', '15610101722', '110101199002021234', '女', '1990-02-02', 32.00, 8, '教学能力,耐心,沟通能力', '教育,文化', 'silver', '2024-03-20', 1, '专注于教育支持活动', '2025-03-20 10:00:00', '2025-07-15 10:00:00');
INSERT INTO `volunteer_profile` VALUES ('vp003', 'd580df2e-2488-4cbd-96f6-5e6ec03e76f7', '王五', '王五', '15610101723', '110101199003031234', '男', '1990-03-03', 78.50, 20, '医疗知识,急救技能,应急处理', '医疗,应急救援', 'platinum', '2023-06-10', 1, '专业医疗志愿者，具备丰富经验', '2025-06-10 10:00:00', '2025-07-15 10:00:00');
INSERT INTO `volunteer_profile` VALUES ('vp004', 'e680df2e-2488-4cbd-96f6-5e6ec03e76f8', '赵六', '赵六', '15610101724', '110101199004041234', '女', '1990-04-04', 15.00, 4, '环保意识,团队合作', '环保', 'bronze', '2024-09-15', 1, '环保活动新人，积极参与', '2025-09-15 10:00:00', '2025-07-15 10:00:00');
INSERT INTO `volunteer_profile` VALUES ('vp005', 'f780df2e-2488-4cbd-96f6-5e6ec03e76f9', '孙七', '孙七', '15610101725', '110101199005051234', '男', '1990-05-05', 56.00, 15, '科技知识,讲解能力,组织能力', '科技,文化', 'gold', '2024-02-28', 1, '科技普及活动专家', '2025-02-28 10:00:00', '2025-07-15 10:00:00');

-- ----------------------------
-- Table structure for notification
-- ----------------------------
DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '通知标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '通知内容',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'system' COMMENT '通知类型：system-系统通知/activity-活动通知/reminder-提醒通知/announcement-公告消息',
  `target_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '目标用户ID，NULL表示全体通知',
  `is_read` tinyint(1) NULL DEFAULT 0 COMMENT '是否已读：0-未读/1-已读',
  `priority` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'normal' COMMENT '优先级：low-低/normal-普通/high-高/urgent-紧急',
  `expire_time` datetime(0) NULL DEFAULT NULL COMMENT '过期时间',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_target_user_id`(`target_user_id`) USING BTREE,
  INDEX `idx_type`(`type`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '通知消息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notification
-- ----------------------------
INSERT INTO `notification` VALUES ('n001', '系统维护通知', '系统将于2025年8月1日凌晨2:00-4:00进行维护升级，期间可能影响正常使用，请提前做好准备。', 'system', NULL, 0, 'high', '2025-08-02 00:00:00', '2025-07-25 09:00:00', '2025-07-25 09:00:00');
INSERT INTO `notification` VALUES ('n002', '新活动上线通知', '新的志愿者活动"社区环保清洁活动"已上线，欢迎各位志愿者报名参与！', 'activity', NULL, 0, 'normal', '2025-08-31 23:59:59', '2025-07-25 10:00:00', '2025-07-25 10:00:00');
INSERT INTO `notification` VALUES ('n003', '活动提醒', '您报名的"科技知识普及讲座"将于明天晚上7点开始，请提前30分钟到达现场。', 'reminder', 'f780df2e-2488-4cbd-96f6-5e6ec03e76f9', 0, 'high', '2025-08-31 23:59:59', '2025-07-25 11:00:00', '2025-07-25 11:00:00');
INSERT INTO `notification` VALUES ('n004', '志愿者等级提升', '恭喜您！由于积极参与活动，您的志愿者等级已从"白银"提升至"黄金"，感谢您的贡献！', 'system', 'c480df2e-2488-4cbd-96f6-5e6ec03e76f6', 0, 'normal', '2025-12-31 23:59:59', '2025-07-25 12:00:00', '2025-07-25 12:00:00');
INSERT INTO `notification` VALUES ('n005', '活动审核结果', '您提交的"社区健康义诊活动"已通过审核，可以开始招募志愿者了。', 'activity', 'd580df2e-2488-4cbd-96f6-5e6ec03e76f7', 0, 'normal', '2025-12-31 23:59:59', '2025-07-25 13:00:00', '2025-07-25 13:00:00');
INSERT INTO `notification` VALUES ('n006', '服务时长统计', '本月您的服务时长统计已完成，总计15.5小时，继续保持！', 'reminder', 'b380df2e-2488-4cbd-96f6-5e6ec03e76f5', 0, 'low', '2025-08-31 23:59:59', '2025-07-25 14:00:00', '2025-07-25 14:00:00');
INSERT INTO `notification` VALUES ('n007', '志愿者招募', '新活动"应急救援培训活动"正在招募志愿者，要求身体健康，有应急意识，欢迎报名！', 'announcement', NULL, 0, 'normal', '2025-09-30 23:59:59', '2025-07-25 15:00:00', '2025-07-25 15:00:00');
INSERT INTO `notification` VALUES ('n008', '活动取消通知', '原定于8月25日的"社区健康义诊活动"因场地原因暂时取消，具体时间另行通知。', 'activity', NULL, 0, 'high', '2025-08-31 23:59:59', '2025-07-25 16:00:00', '2025-07-25 16:00:00');
INSERT INTO `notification` VALUES ('n009', '志愿者培训通知', '为提高志愿者服务质量，将于8月10日举办志愿者技能培训，请各位志愿者积极参加。', 'announcement', NULL, 0, 'normal', '2025-08-31 23:59:59', '2025-07-25 17:00:00', '2025-07-25 17:00:00');

-- ----------------------------
-- Table structure for service_hours
-- ----------------------------
DROP TABLE IF EXISTS `service_hours`;
CREATE TABLE `service_hours`  (
  `id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
  `activity_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动ID',
  `activity_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '活动名称',
  `service_hours` decimal(5,2) NOT NULL COMMENT '服务时长(小时)',
  `service_date` date NOT NULL COMMENT '服务日期',
  `check_in_time` datetime(0) NULL DEFAULT NULL COMMENT '签到时间',
  `check_out_time` datetime(0) NULL DEFAULT NULL COMMENT '签退时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'pending' COMMENT '状态：pending-待确认/confirmed-已确认/rejected-已拒绝',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE,
  INDEX `idx_activity_id`(`activity_id`) USING BTREE,
  INDEX `idx_service_date`(`service_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '服务时长记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of service_hours
-- ----------------------------
INSERT INTO `service_hours` VALUES ('sh001', 'b380df2e-2488-4cbd-96f6-5e6ec03e76f5', 'vp001', '社区环保清洁活动', 3.00, '2025-08-15', '2025-08-15 08:45:00', '2025-08-15 12:00:00', 'confirmed', '积极参与，表现优秀', '2025-08-15 12:00:00', '2025-08-15 12:00:00');
INSERT INTO `service_hours` VALUES ('sh002', 'c480df2e-2488-4cbd-96f6-5e6ec03e76f6', 'vp002', '贫困学生助学活动', 4.00, '2025-08-20', '2025-08-20 13:30:00', '2025-08-20 18:00:00', 'confirmed', '教学认真，学生反馈良好', '2025-08-20 18:00:00', '2025-08-20 18:00:00');
INSERT INTO `service_hours` VALUES ('sh003', 'f780df2e-2488-4cbd-96f6-5e6ec03e76f9', 'vp004', '科技知识普及讲座', 2.50, '2025-08-30', '2025-08-30 18:30:00', '2025-08-30 21:30:00', 'confirmed', '讲解生动，听众反应热烈', '2025-08-30 21:30:00', '2025-08-30 21:30:00');
INSERT INTO `service_hours` VALUES ('sh004', 'f42f0f7d-c835-45a4-b36c-dca85a2f09c7', 'vp007', '体育健身指导活动', 2.00, '2025-09-15', '2025-09-15 15:45:00', '2025-09-15 18:00:00', 'confirmed', '指导专业，学员进步明显', '2025-09-15 18:00:00', '2025-09-15 18:00:00');
INSERT INTO `service_hours` VALUES ('sh005', '32f2a899-7cf0-4a8a-bccf-907711a0e1b1', 'vp008', '社区服务日活动', 4.50, '2025-09-20', '2025-09-20 07:30:00', '2025-09-20 12:00:00', 'confirmed', '服务周到，居民满意度高', '2025-09-20 12:00:00', '2025-09-20 12:00:00');
INSERT INTO `service_hours` VALUES ('sh006', 'e680df2e-2488-4cbd-96f6-5e6ec03e76f8', 'vp001', '社区环保清洁活动', 3.00, '2025-08-15', '2025-08-15 08:50:00', '2025-08-15 12:00:00', 'confirmed', '认真负责，团队合作好', '2025-08-15 12:00:00', '2025-08-15 12:00:00');
INSERT INTO `service_hours` VALUES ('sh007', 'c480df2e-2488-4cbd-96f6-5e6ec03e76f6', 'vp004', '科技知识普及讲座', 2.50, '2025-08-30', '2025-08-30 18:45:00', '2025-08-30 21:30:00', 'confirmed', '积极参与互动，学习态度好', '2025-08-30 21:30:00', '2025-08-30 21:30:00');
INSERT INTO `service_hours` VALUES ('sh008', 'a5a0b9da-708a-4535-86de-b7f717fea48a', 'vp005', '传统文化传承活动', 3.50, '2025-09-05', '2025-09-05 09:30:00', '2025-09-05 13:00:00', 'confirmed', '表演精彩，观众反响热烈', '2025-09-05 13:00:00', '2025-09-05 13:00:00');
INSERT INTO `service_hours` VALUES ('sh009', 'b380df2e-2488-4cbd-96f6-5e6ec03e76f5', 'vp002', '贫困学生助学活动', 4.00, '2025-08-20', '2025-08-20 13:45:00', '2025-08-20 18:00:00', 'confirmed', '耐心辅导，学生进步明显', '2025-08-20 18:00:00', '2025-08-20 18:00:00');
INSERT INTO `service_hours` VALUES ('sh010', 'd580df2e-2488-4cbd-96f6-5e6ec03e76f7', 'vp003', '社区健康义诊活动', 5.00, '2025-08-25', '2025-08-25 09:00:00', '2025-08-25 14:00:00', 'pending', '等待确认', '2025-08-25 14:00:00', '2025-08-25 14:00:00');

SET FOREIGN_KEY_CHECKS = 1;
