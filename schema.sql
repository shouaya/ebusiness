-- MySQL dump 10.13  Distrib 5.6.26, for osx10.8 (x86_64)
--
-- Host: localhost    Database: EB_SUPPORT
-- ------------------------------------------------------
-- Server version	5.6.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_client`
--

DROP TABLE IF EXISTS `eb_client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `japanese_spell` varchar(30) DEFAULT NULL,
  `president` varchar(30) DEFAULT NULL,
  `found_date` date DEFAULT NULL,
  `capital` bigint(20) DEFAULT NULL,
  `employee_count` int(11) DEFAULT NULL,
  `sale_amount` bigint(20) DEFAULT NULL,
  `post_code` varchar(8) DEFAULT NULL,
  `address1` varchar(200) DEFAULT NULL,
  `address2` varchar(200) DEFAULT NULL,
  `tel` varchar(15) DEFAULT NULL,
  `fax` varchar(15) DEFAULT NULL,
  `payment_type` varchar(2) DEFAULT NULL,
  `payment_day` varchar(2) DEFAULT NULL,
  `comment` longtext,
  `created_date` datetime NOT NULL,
  `updated_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_clientmember`
--

DROP TABLE IF EXISTS `eb_clientmember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_clientmember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `client_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eb_clientmember_2bfe9d72` (`client_id`),
  CONSTRAINT `eb_clientmember_client_id_3fcceff40bc69e07_fk_eb_client_id` FOREIGN KEY (`client_id`) REFERENCES `eb_client` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_company`
--

DROP TABLE IF EXISTS `eb_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `post_code` varchar(8) DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `tel` varchar(15) DEFAULT NULL,
  `release_month_count` int(11) NOT NULL,
  `display_count` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_member`
--

DROP TABLE IF EXISTS `eb_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  `salesperson_id` int(11),
  `section_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`),
  KEY `eb_member_447d3092` (`company_id`),
  KEY `eb_member_611cf3bd` (`salesperson_id`),
  KEY `eb_member_730f6511` (`section_id`),
  CONSTRAINT `eb_member_company_id_5919b31c76581a6b_fk_eb_company_id` FOREIGN KEY (`company_id`) REFERENCES `eb_company` (`id`),
  CONSTRAINT `eb_member_salesperson_id_76aae674c1191ecd_fk_eb_salesperson_id` FOREIGN KEY (`salesperson_id`) REFERENCES `eb_salesperson` (`id`),
  CONSTRAINT `eb_member_section_id_5562abdf77da938b_fk_eb_section_id` FOREIGN KEY (`section_id`) REFERENCES `eb_section` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_project`
--

DROP TABLE IF EXISTS `eb_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` varchar(30) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `boss_id` int(11) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `middleman_id` int(11),
  `salesperson_id` int(11),
  `status_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`),
  KEY `eb_project_29f95c03` (`boss_id`),
  KEY `eb_project_2bfe9d72` (`client_id`),
  KEY `eb_project_a4849c17` (`middleman_id`),
  KEY `eb_project_611cf3bd` (`salesperson_id`),
  KEY `eb_project_dc91ed4b` (`status_id`),
  CONSTRAINT `eb_project_boss_id_262b0fbcc07e897c_fk_eb_clientmember_id` FOREIGN KEY (`boss_id`) REFERENCES `eb_clientmember` (`id`),
  CONSTRAINT `eb_project_client_id_146951a2422197e8_fk_eb_client_id` FOREIGN KEY (`client_id`) REFERENCES `eb_client` (`id`),
  CONSTRAINT `eb_project_middleman_id_68819d83dcf185af_fk_eb_clientmember_id` FOREIGN KEY (`middleman_id`) REFERENCES `eb_clientmember` (`id`),
  CONSTRAINT `eb_project_salesperson_id_7d01e50ad8fdb11b_fk_eb_salesperson_id` FOREIGN KEY (`salesperson_id`) REFERENCES `eb_salesperson` (`id`),
  CONSTRAINT `eb_project_status_id_12d168efe614137b_fk_eb_projectstatus_id` FOREIGN KEY (`status_id`) REFERENCES `eb_projectstatus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_projectactivity`
--

DROP TABLE IF EXISTS `eb_projectactivity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_projectactivity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `open_date` datetime NOT NULL,
  `address` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `created_date` datetime NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eb_projectactivity_b098ad43` (`project_id`),
  CONSTRAINT `eb_projectactivity_project_id_1cbd2a9c2c1c7eb0_fk_eb_project_id` FOREIGN KEY (`project_id`) REFERENCES `eb_project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_projectactivity_client_members`
--

DROP TABLE IF EXISTS `eb_projectactivity_client_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_projectactivity_client_members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projectactivity_id` int(11) NOT NULL,
  `clientmember_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `projectactivity_id` (`projectactivity_id`,`clientmember_id`),
  KEY `eb_projectactivity_client_members_7533f817` (`projectactivity_id`),
  KEY `eb_projectactivity_client_members_2abbd8d5` (`clientmember_id`),
  CONSTRAINT `eb__projectactivity_id_3cf243b4d80b518e_fk_eb_projectactivity_id` FOREIGN KEY (`projectactivity_id`) REFERENCES `eb_projectactivity` (`id`),
  CONSTRAINT `eb_projec_clientmember_id_2ad7a7b84f496602_fk_eb_clientmember_id` FOREIGN KEY (`clientmember_id`) REFERENCES `eb_clientmember` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_projectactivity_members`
--

DROP TABLE IF EXISTS `eb_projectactivity_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_projectactivity_members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projectactivity_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `projectactivity_id` (`projectactivity_id`,`member_id`),
  KEY `eb_projectactivity_members_7533f817` (`projectactivity_id`),
  KEY `eb_projectactivity_members_b5c3e75b` (`member_id`),
  CONSTRAINT `eb__projectactivity_id_5ff2a877661d3247_fk_eb_projectactivity_id` FOREIGN KEY (`projectactivity_id`) REFERENCES `eb_projectactivity` (`id`),
  CONSTRAINT `eb_projectactivity_me_member_id_28e8727cec55c92c_fk_eb_member_id` FOREIGN KEY (`member_id`) REFERENCES `eb_member` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_projectactivity_salesperson`
--

DROP TABLE IF EXISTS `eb_projectactivity_salesperson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_projectactivity_salesperson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projectactivity_id` int(11) NOT NULL,
  `salesperson_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `projectactivity_id` (`projectactivity_id`,`salesperson_id`),
  KEY `eb_projectactivity_salesperson_7533f817` (`projectactivity_id`),
  KEY `eb_projectactivity_salesperson_611cf3bd` (`salesperson_id`),
  CONSTRAINT `eb__projectactivity_id_37a4b87eb70fcbcd_fk_eb_projectactivity_id` FOREIGN KEY (`projectactivity_id`) REFERENCES `eb_projectactivity` (`id`),
  CONSTRAINT `eb_projecta_salesperson_id_123d81dda3dfed2a_fk_eb_salesperson_id` FOREIGN KEY (`salesperson_id`) REFERENCES `eb_salesperson` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_projectmember`
--

DROP TABLE IF EXISTS `eb_projectmember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_projectmember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `price` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eb_projectmember_b5c3e75b` (`member_id`),
  KEY `eb_projectmember_b098ad43` (`project_id`),
  CONSTRAINT `eb_projectmember_member_id_bdb4047dbad75f1_fk_eb_member_id` FOREIGN KEY (`member_id`) REFERENCES `eb_member` (`id`),
  CONSTRAINT `eb_projectmember_project_id_660d81d7d9c2f043_fk_eb_project_id` FOREIGN KEY (`project_id`) REFERENCES `eb_project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_projectskill`
--

DROP TABLE IF EXISTS `eb_projectskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_projectskill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `period` int(11) DEFAULT NULL,
  `description` longtext,
  `project_id` int(11) NOT NULL,
  `skill_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eb_projectskill_b098ad43` (`project_id`),
  KEY `eb_projectskill_d38d4c39` (`skill_id`),
  CONSTRAINT `eb_projectskill_project_id_5618f18ff72c1a59_fk_eb_project_id` FOREIGN KEY (`project_id`) REFERENCES `eb_project` (`id`),
  CONSTRAINT `eb_projectskill_skill_id_7728affb32478b29_fk_eb_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `eb_skill` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_projectstatus`
--

DROP TABLE IF EXISTS `eb_projectstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_projectstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_salesperson`
--

DROP TABLE IF EXISTS `eb_salesperson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_salesperson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  `section_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`),
  KEY `eb_salesperson_447d3092` (`company_id`),
  KEY `eb_salesperson_730f6511` (`section_id`),
  CONSTRAINT `eb_salesperson_company_id_3e14ab4c9e4c43f1_fk_eb_company_id` FOREIGN KEY (`company_id`) REFERENCES `eb_company` (`id`),
  CONSTRAINT `eb_salesperson_section_id_1bd71f3cb031686f_fk_eb_section_id` FOREIGN KEY (`section_id`) REFERENCES `eb_section` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_section`
--

DROP TABLE IF EXISTS `eb_section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_section` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eb_section_447d3092` (`company_id`),
  CONSTRAINT `eb_section_company_id_30bb5521d56f41d_fk_eb_company_id` FOREIGN KEY (`company_id`) REFERENCES `eb_company` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eb_skill`
--

DROP TABLE IF EXISTS `eb_skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eb_skill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-08 21:02:20
