/*
SQLyog Community v10.3 
MySQL - 5.5.5-10.2.8-MariaDB : Database - delivery_db
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`delivery_db` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `delivery_db`;

/*Table structure for table `artefact_store_type` */

DROP TABLE IF EXISTS `artefact_store_type`;

CREATE TABLE `artefact_store_type` (
  `artefact_store_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `artefact_store_type_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`artefact_store_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `component` */

DROP TABLE IF EXISTS `component`;

CREATE TABLE `component` (
  `component_id` int(11) NOT NULL AUTO_INCREMENT,
  `component_name` varchar(255) DEFAULT NULL,
  `component_short_name` varchar(255) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `linked_ci_flag` tinyint(1) DEFAULT NULL,
  `component_type_id` int(11) DEFAULT NULL,
  `deployment_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`component_id`),
  KEY `component_type_id` (`component_type_id`),
  KEY `deployment_type_id` (`deployment_type_id`),
  CONSTRAINT `component_ibfk_1` FOREIGN KEY (`component_type_id`) REFERENCES `component_type` (`component_type_id`),
  CONSTRAINT `component_ibfk_2` FOREIGN KEY (`deployment_type_id`) REFERENCES `deployment_type` (`deployment_type_id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`linked_ci_flag` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `component_type` */

DROP TABLE IF EXISTS `component_type`;

CREATE TABLE `component_type` (
  `component_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `component_type_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`component_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `component_version` */

DROP TABLE IF EXISTS `component_version`;

CREATE TABLE `component_version` (
  `component_version_id` int(11) NOT NULL AUTO_INCREMENT,
  `component_version_name` varchar(255) DEFAULT NULL,
  `stable_flag` int(11) DEFAULT NULL,
  `artefact_store_url` varchar(2000) DEFAULT NULL,
  `source_code_repository_url` varchar(2000) DEFAULT NULL,
  `source_tag_reference` varchar(255) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `component_id` int(11) DEFAULT NULL,
  `artefact_store_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`component_version_id`),
  KEY `component_id` (`component_id`),
  KEY `artefact_store_type_id` (`artefact_store_type_id`),
  CONSTRAINT `component_version_ibfk_1` FOREIGN KEY (`component_id`) REFERENCES `component` (`component_id`),
  CONSTRAINT `component_version_ibfk_2` FOREIGN KEY (`artefact_store_type_id`) REFERENCES `artefact_store_type` (`artefact_store_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `deployment` */

DROP TABLE IF EXISTS `deployment`;

CREATE TABLE `deployment` (
  `deployment_id` int(11) NOT NULL AUTO_INCREMENT,
  `deployment_name` varchar(255) DEFAULT NULL,
  `planned_deployment_date` datetime DEFAULT NULL,
  `deployer_name` varchar(255) DEFAULT NULL,
  `requested_date` datetime DEFAULT NULL,
  `infra_code_flag` tinyint(1) DEFAULT NULL,
  `infra_config_flag` tinyint(1) DEFAULT NULL,
  `app_flag` tinyint(1) DEFAULT NULL,
  `system_element_id` int(11) DEFAULT NULL,
  `infra_template_id` int(11) DEFAULT NULL,
  `instance_id` int(11) DEFAULT NULL,
  `environment_id` int(11) DEFAULT NULL,
  `network_set_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`deployment_id`),
  KEY `system_element_id` (`system_element_id`),
  KEY `infra_template_id` (`infra_template_id`),
  KEY `instance_id` (`instance_id`),
  KEY `environment_id` (`environment_id`),
  KEY `network_set_id` (`network_set_id`),
  CONSTRAINT `deployment_ibfk_1` FOREIGN KEY (`system_element_id`) REFERENCES `system_element` (`system_element_id`),
  CONSTRAINT `deployment_ibfk_2` FOREIGN KEY (`infra_template_id`) REFERENCES `infrastructure_template` (`infra_template_id`),
  CONSTRAINT `deployment_ibfk_3` FOREIGN KEY (`instance_id`) REFERENCES `instance` (`instance_id`),
  CONSTRAINT `deployment_ibfk_4` FOREIGN KEY (`environment_id`) REFERENCES `environment` (`environment_id`),
  CONSTRAINT `deployment_ibfk_5` FOREIGN KEY (`network_set_id`) REFERENCES `network_set` (`network_set_id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`infra_code_flag` in (0,1)),
  CONSTRAINT `CONSTRAINT_2` CHECK (`infra_config_flag` in (0,1)),
  CONSTRAINT `CONSTRAINT_3` CHECK (`app_flag` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `deployment_audit` */

DROP TABLE IF EXISTS `deployment_audit`;

CREATE TABLE `deployment_audit` (
  `deployment_audit_id` int(11) NOT NULL AUTO_INCREMENT,
  `deployment_id` int(11) DEFAULT NULL,
  `deployment_status_id` int(11) DEFAULT NULL,
  `deployment_remarks` varchar(255) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `audit_date` datetime DEFAULT NULL,
  PRIMARY KEY (`deployment_audit_id`),
  KEY `deployment_id` (`deployment_id`),
  KEY `deployment_status_id` (`deployment_status_id`),
  CONSTRAINT `deployment_audit_ibfk_1` FOREIGN KEY (`deployment_id`) REFERENCES `deployment` (`deployment_id`),
  CONSTRAINT `deployment_audit_ibfk_2` FOREIGN KEY (`deployment_status_id`) REFERENCES `status` (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `deployment_component` */

DROP TABLE IF EXISTS `deployment_component`;

CREATE TABLE `deployment_component` (
  `deployment_component_id` int(11) NOT NULL AUTO_INCREMENT,
  `deployment_id` int(11) DEFAULT NULL,
  `system_element_component_id` int(11) DEFAULT NULL,
  `deployment_component_status_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`deployment_component_id`),
  KEY `deployment_id` (`deployment_id`),
  KEY `system_element_component_id` (`system_element_component_id`),
  KEY `deployment_component_status_id` (`deployment_component_status_id`),
  CONSTRAINT `deployment_component_ibfk_1` FOREIGN KEY (`deployment_id`) REFERENCES `deployment` (`deployment_id`),
  CONSTRAINT `deployment_component_ibfk_2` FOREIGN KEY (`system_element_component_id`) REFERENCES `system_element_component` (`system_element_component_id`),
  CONSTRAINT `deployment_component_ibfk_3` FOREIGN KEY (`deployment_component_status_id`) REFERENCES `status` (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `deployment_parameter` */

DROP TABLE IF EXISTS `deployment_parameter`;

CREATE TABLE `deployment_parameter` (
  `deployment_parameter_id` int(11) NOT NULL AUTO_INCREMENT,
  `deployment_parameter_value` mediumtext DEFAULT NULL,
  `parameter_id` int(11) DEFAULT NULL,
  `deployment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`deployment_parameter_id`),
  KEY `parameter_id` (`parameter_id`),
  KEY `deployment_id` (`deployment_id`),
  CONSTRAINT `deployment_parameter_ibfk_1` FOREIGN KEY (`parameter_id`) REFERENCES `parameter` (`parameter_id`),
  CONSTRAINT `deployment_parameter_ibfk_2` FOREIGN KEY (`deployment_id`) REFERENCES `deployment` (`deployment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `deployment_type` */

DROP TABLE IF EXISTS `deployment_type`;

CREATE TABLE `deployment_type` (
  `deployment_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `deployment_type_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`deployment_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `disk_type` */

DROP TABLE IF EXISTS `disk_type`;

CREATE TABLE `disk_type` (
  `disk_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `disk_type_description` varchar(255) DEFAULT NULL,
  `min_size` int(11) DEFAULT NULL,
  `max_size` int(11) DEFAULT NULL,
  `host_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`disk_type_id`),
  KEY `host_type_id` (`host_type_id`),
  CONSTRAINT `disk_type_ibfk_1` FOREIGN KEY (`host_type_id`) REFERENCES `host_type` (`host_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `environment` */

DROP TABLE IF EXISTS `environment`;

CREATE TABLE `environment` (
  `environment_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_name` varchar(255) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `environment_type_id` int(11) DEFAULT NULL,
  `environment_data_type_id` int(11) DEFAULT NULL,
  `system_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`environment_id`),
  KEY `environment_type_id` (`environment_type_id`),
  KEY `environment_data_type_id` (`environment_data_type_id`),
  KEY `system_id` (`system_id`),
  CONSTRAINT `environment_ibfk_1` FOREIGN KEY (`environment_type_id`) REFERENCES `environment_type` (`environment_type_id`),
  CONSTRAINT `environment_ibfk_2` FOREIGN KEY (`environment_data_type_id`) REFERENCES `environment_data_type` (`environment_data_type_id`),
  CONSTRAINT `environment_ibfk_3` FOREIGN KEY (`system_id`) REFERENCES `system` (`system_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `environment_data_type` */

DROP TABLE IF EXISTS `environment_data_type`;

CREATE TABLE `environment_data_type` (
  `environment_data_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_data_type_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`environment_data_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `environment_set` */

DROP TABLE IF EXISTS `environment_set`;

CREATE TABLE `environment_set` (
  `environment_set_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_set_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`environment_set_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `environment_set_link` */

DROP TABLE IF EXISTS `environment_set_link`;

CREATE TABLE `environment_set_link` (
  `environment_set_link_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_set_id` int(11) DEFAULT NULL,
  `environment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`environment_set_link_id`),
  KEY `environment_set_id` (`environment_set_id`),
  KEY `environment_id` (`environment_id`),
  CONSTRAINT `environment_set_link_ibfk_1` FOREIGN KEY (`environment_set_id`) REFERENCES `environment_set` (`environment_set_id`),
  CONSTRAINT `environment_set_link_ibfk_2` FOREIGN KEY (`environment_id`) REFERENCES `environment` (`environment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `environment_subscription_type` */

DROP TABLE IF EXISTS `environment_subscription_type`;

CREATE TABLE `environment_subscription_type` (
  `environment_subscription_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_subscription_type_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`environment_subscription_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `environment_type` */

DROP TABLE IF EXISTS `environment_type`;

CREATE TABLE `environment_type` (
  `environment_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_type_name` varchar(255) DEFAULT NULL,
  `environment_type_short_name` varchar(5) DEFAULT NULL,
  `identifier` varchar(1) DEFAULT NULL,
  `environment_subscription_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`environment_type_id`),
  KEY `environment_subscription_type_id` (`environment_subscription_type_id`),
  CONSTRAINT `environment_type_ibfk_1` FOREIGN KEY (`environment_subscription_type_id`) REFERENCES `environment_subscription_type` (`environment_subscription_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `environment_use` */

DROP TABLE IF EXISTS `environment_use`;

CREATE TABLE `environment_use` (
  `environment_use_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_use_name` varchar(255) DEFAULT NULL,
  `environment_use_short_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`environment_use_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `host_region` */

DROP TABLE IF EXISTS `host_region`;

CREATE TABLE `host_region` (
  `host_region_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_region_name` varchar(255) DEFAULT NULL,
  `host_region_description` varchar(255) DEFAULT NULL,
  `host_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`host_region_id`),
  KEY `host_type_id` (`host_type_id`),
  CONSTRAINT `host_region_ibfk_1` FOREIGN KEY (`host_type_id`) REFERENCES `host_type` (`host_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `host_site` */

DROP TABLE IF EXISTS `host_site`;

CREATE TABLE `host_site` (
  `host_site_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_site_name` varchar(255) DEFAULT NULL,
  `host_site_description` varchar(255) DEFAULT NULL,
  `host_region_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`host_site_id`),
  KEY `host_region_id` (`host_region_id`),
  CONSTRAINT `host_site_ibfk_1` FOREIGN KEY (`host_region_id`) REFERENCES `host_region` (`host_region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `host_subscription` */

DROP TABLE IF EXISTS `host_subscription`;

CREATE TABLE `host_subscription` (
  `host_subscription_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_subscription_key` varchar(255) DEFAULT NULL,
  `host_subscription_description` varchar(255) DEFAULT NULL,
  `host_region_id` int(11) DEFAULT NULL,
  `system_network_set_id` int(11) DEFAULT NULL,
  `environment_subscription_type_id` int(11) DEFAULT NULL,
  `environment_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`host_subscription_id`),
  KEY `host_region_id` (`host_region_id`),
  KEY `system_network_set_id` (`system_network_set_id`),
  KEY `environment_subscription_type_id` (`environment_subscription_type_id`),
  KEY `environment_type_id` (`environment_type_id`),
  CONSTRAINT `host_subscription_ibfk_1` FOREIGN KEY (`host_region_id`) REFERENCES `host_region` (`host_region_id`),
  CONSTRAINT `host_subscription_ibfk_2` FOREIGN KEY (`system_network_set_id`) REFERENCES `system_network_set` (`system_network_set_id`),
  CONSTRAINT `host_subscription_ibfk_3` FOREIGN KEY (`environment_subscription_type_id`) REFERENCES `environment_subscription_type` (`environment_subscription_type_id`),
  CONSTRAINT `host_subscription_ibfk_4` FOREIGN KEY (`environment_type_id`) REFERENCES `environment_type` (`environment_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `host_type` */

DROP TABLE IF EXISTS `host_type`;

CREATE TABLE `host_type` (
  `host_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`host_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `infrastructure_template` */

DROP TABLE IF EXISTS `infrastructure_template`;

CREATE TABLE `infrastructure_template` (
  `infra_template_id` int(11) NOT NULL AUTO_INCREMENT,
  `infra_template_name` varchar(255) DEFAULT NULL,
  `host_template_description` varchar(255) DEFAULT NULL,
  `memory_size` float DEFAULT NULL,
  `cpu` int(11) DEFAULT NULL,
  `max_no_disk` int(11) DEFAULT NULL,
  `host_type_id` int(11) DEFAULT NULL,
  `infrastructure_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`infra_template_id`),
  KEY `host_type_id` (`host_type_id`),
  KEY `infrastructure_type_id` (`infrastructure_type_id`),
  CONSTRAINT `infrastructure_template_ibfk_1` FOREIGN KEY (`host_type_id`) REFERENCES `host_type` (`host_type_id`),
  CONSTRAINT `infrastructure_template_ibfk_2` FOREIGN KEY (`infrastructure_type_id`) REFERENCES `infrastructure_type` (`infrastructure_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `infrastructure_type` */

DROP TABLE IF EXISTS `infrastructure_type`;

CREATE TABLE `infrastructure_type` (
  `infrastructure_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `infrastructure_type_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`infrastructure_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `instance` */

DROP TABLE IF EXISTS `instance`;

CREATE TABLE `instance` (
  `instance_id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_name` varchar(255) DEFAULT NULL,
  `host_instance_name` varchar(255) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `last_update_date` datetime DEFAULT NULL,
  `instance_state` varchar(255) DEFAULT NULL,
  `assigned_ip` varchar(20) DEFAULT NULL,
  `remarks` varchar(2000) DEFAULT NULL,
  `infra_template_id` int(11) DEFAULT NULL,
  `method_creation_type_id` int(11) DEFAULT NULL,
  `network_set_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`instance_id`),
  KEY `infra_template_id` (`infra_template_id`),
  KEY `method_creation_type_id` (`method_creation_type_id`),
  KEY `network_set_id` (`network_set_id`),
  CONSTRAINT `instance_ibfk_1` FOREIGN KEY (`infra_template_id`) REFERENCES `infrastructure_template` (`infra_template_id`),
  CONSTRAINT `instance_ibfk_2` FOREIGN KEY (`method_creation_type_id`) REFERENCES `method_creation_type` (`method_creation_type_id`),
  CONSTRAINT `instance_ibfk_3` FOREIGN KEY (`network_set_id`) REFERENCES `network_set` (`network_set_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `instance_disk` */

DROP TABLE IF EXISTS `instance_disk`;

CREATE TABLE `instance_disk` (
  `instance_disk_id` int(11) NOT NULL AUTO_INCREMENT,
  `disk_size` int(11) DEFAULT NULL,
  `disk_size_type` varchar(10) DEFAULT NULL,
  `instance_id` int(11) DEFAULT NULL,
  `disk_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`instance_disk_id`),
  KEY `instance_id` (`instance_id`),
  KEY `disk_type_id` (`disk_type_id`),
  CONSTRAINT `instance_disk_ibfk_1` FOREIGN KEY (`instance_id`) REFERENCES `instance` (`instance_id`),
  CONSTRAINT `instance_disk_ibfk_2` FOREIGN KEY (`disk_type_id`) REFERENCES `disk_type` (`disk_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `method_creation_type` */

DROP TABLE IF EXISTS `method_creation_type`;

CREATE TABLE `method_creation_type` (
  `method_creation_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(3) NOT NULL,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY (`method_creation_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `network_set` */

DROP TABLE IF EXISTS `network_set`;

CREATE TABLE `network_set` (
  `network_set_id` int(11) NOT NULL AUTO_INCREMENT,
  `network_set_name` varchar(255) DEFAULT NULL,
  `ip_range_start` varchar(255) DEFAULT NULL,
  `ip_range_end` varchar(20) DEFAULT NULL,
  `subnet` varchar(2000) DEFAULT NULL,
  `host_site_id` int(11) DEFAULT NULL,
  `host_subscription_id` int(11) DEFAULT NULL,
  `environment_type_id` int(11) DEFAULT NULL,
  `system_element_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`network_set_id`),
  KEY `host_site_id` (`host_site_id`),
  KEY `host_subscription_id` (`host_subscription_id`),
  KEY `environment_type_id` (`environment_type_id`),
  KEY `system_element_type_id` (`system_element_type_id`),
  CONSTRAINT `network_set_ibfk_1` FOREIGN KEY (`host_site_id`) REFERENCES `host_site` (`host_site_id`),
  CONSTRAINT `network_set_ibfk_2` FOREIGN KEY (`host_subscription_id`) REFERENCES `host_subscription` (`host_subscription_id`),
  CONSTRAINT `network_set_ibfk_3` FOREIGN KEY (`environment_type_id`) REFERENCES `environment_type` (`environment_type_id`),
  CONSTRAINT `network_set_ibfk_4` FOREIGN KEY (`system_element_type_id`) REFERENCES `system_element_type` (`system_element_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `parameter` */

DROP TABLE IF EXISTS `parameter`;

CREATE TABLE `parameter` (
  `parameter_id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter_name` varchar(255) DEFAULT NULL,
  `mandatory` tinyint(1) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `parameter_type_id` int(11) DEFAULT NULL,
  `component_type_id` int(11) DEFAULT NULL,
  `component_id` int(11) DEFAULT NULL,
  `component_version_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`parameter_id`),
  KEY `parameter_type_id` (`parameter_type_id`),
  KEY `component_type_id` (`component_type_id`),
  KEY `component_id` (`component_id`),
  KEY `component_version_id` (`component_version_id`),
  CONSTRAINT `parameter_ibfk_1` FOREIGN KEY (`parameter_type_id`) REFERENCES `parameter_type` (`parameter_type_id`),
  CONSTRAINT `parameter_ibfk_2` FOREIGN KEY (`component_type_id`) REFERENCES `component_type` (`component_type_id`),
  CONSTRAINT `parameter_ibfk_3` FOREIGN KEY (`component_id`) REFERENCES `component` (`component_id`),
  CONSTRAINT `parameter_ibfk_4` FOREIGN KEY (`component_version_id`) REFERENCES `component_version` (`component_version_id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`mandatory` in (0,1)),
  CONSTRAINT `CONSTRAINT_2` CHECK (`active` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `parameter_type` */

DROP TABLE IF EXISTS `parameter_type`;

CREATE TABLE `parameter_type` (
  `parameter_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`parameter_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `parameter_value` */

DROP TABLE IF EXISTS `parameter_value`;

CREATE TABLE `parameter_value` (
  `parameter_value_id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter_value` varchar(255) DEFAULT NULL,
  `parameter_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`parameter_value_id`),
  KEY `parameter_id` (`parameter_id`),
  CONSTRAINT `parameter_value_ibfk_1` FOREIGN KEY (`parameter_id`) REFERENCES `parameter` (`parameter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `release` */

DROP TABLE IF EXISTS `release`;

CREATE TABLE `release` (
  `release_id` int(11) NOT NULL AUTO_INCREMENT,
  `release_name` varchar(250) DEFAULT NULL,
  `release_owner` varchar(250) DEFAULT NULL,
  `release_summary` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`release_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `release_item` */

DROP TABLE IF EXISTS `release_item`;

CREATE TABLE `release_item` (
  `release_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `release_note_url` varchar(255) DEFAULT NULL,
  `system_version_id` int(11) DEFAULT NULL,
  `release_version_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`release_item_id`),
  KEY `system_version_id` (`system_version_id`),
  KEY `release_version_id` (`release_version_id`),
  CONSTRAINT `release_item_ibfk_1` FOREIGN KEY (`system_version_id`) REFERENCES `system_version` (`system_version_id`),
  CONSTRAINT `release_item_ibfk_2` FOREIGN KEY (`release_version_id`) REFERENCES `release_version` (`release_version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `release_version` */

DROP TABLE IF EXISTS `release_version`;

CREATE TABLE `release_version` (
  `release_version_id` int(11) NOT NULL AUTO_INCREMENT,
  `release_version_name` varchar(255) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `target_release_date` datetime DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `release_id` int(11) DEFAULT NULL,
  `release_version_status_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`release_version_id`),
  KEY `release_id` (`release_id`),
  KEY `release_version_status_id` (`release_version_status_id`),
  CONSTRAINT `release_version_ibfk_1` FOREIGN KEY (`release_id`) REFERENCES `release` (`release_id`),
  CONSTRAINT `release_version_ibfk_2` FOREIGN KEY (`release_version_status_id`) REFERENCES `status` (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `role` */

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `route_to_live` */

DROP TABLE IF EXISTS `route_to_live`;

CREATE TABLE `route_to_live` (
  `route_to_live_id` int(11) NOT NULL AUTO_INCREMENT,
  `route_to_live_order` int(11) DEFAULT NULL,
  `critical` tinyint(1) DEFAULT NULL,
  `release_id` int(11) DEFAULT NULL,
  `system_id` int(11) DEFAULT NULL,
  `environment_use_id` int(11) DEFAULT NULL,
  `environment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`route_to_live_id`),
  KEY `release_id` (`release_id`),
  KEY `system_id` (`system_id`),
  KEY `environment_use_id` (`environment_use_id`),
  KEY `environment_id` (`environment_id`),
  CONSTRAINT `route_to_live_ibfk_1` FOREIGN KEY (`release_id`) REFERENCES `release` (`release_id`),
  CONSTRAINT `route_to_live_ibfk_2` FOREIGN KEY (`system_id`) REFERENCES `system` (`system_id`),
  CONSTRAINT `route_to_live_ibfk_3` FOREIGN KEY (`environment_use_id`) REFERENCES `environment_use` (`environment_use_id`),
  CONSTRAINT `route_to_live_ibfk_4` FOREIGN KEY (`environment_id`) REFERENCES `environment` (`environment_id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`critical` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `status` */

DROP TABLE IF EXISTS `status`;

CREATE TABLE `status` (
  `status_id` int(11) NOT NULL AUTO_INCREMENT,
  `status_description` varchar(255) DEFAULT NULL,
  `status_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system` */

DROP TABLE IF EXISTS `system`;

CREATE TABLE `system` (
  `system_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_name` varchar(255) DEFAULT NULL,
  `system_short_name` varchar(50) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `system_network_set_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`system_id`),
  KEY `system_network_set_id` (`system_network_set_id`),
  CONSTRAINT `system_ibfk_1` FOREIGN KEY (`system_network_set_id`) REFERENCES `system_network_set` (`system_network_set_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system_element` */

DROP TABLE IF EXISTS `system_element`;

CREATE TABLE `system_element` (
  `system_element_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_element_name` varchar(255) DEFAULT NULL,
  `system_element_short_name` varchar(7) DEFAULT NULL,
  `system_id` int(11) NOT NULL,
  `system_element_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`system_element_id`),
  KEY `system_id` (`system_id`),
  KEY `system_element_type_id` (`system_element_type_id`),
  CONSTRAINT `system_element_ibfk_1` FOREIGN KEY (`system_id`) REFERENCES `system` (`system_id`),
  CONSTRAINT `system_element_ibfk_2` FOREIGN KEY (`system_element_type_id`) REFERENCES `system_element_type` (`system_element_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system_element_component` */

DROP TABLE IF EXISTS `system_element_component`;

CREATE TABLE `system_element_component` (
  `system_element_component_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_order` int(11) DEFAULT NULL,
  `system_element_id` int(11) NOT NULL,
  `system_version_id` int(11) NOT NULL,
  `component_version_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`system_element_component_id`),
  KEY `system_element_id` (`system_element_id`),
  KEY `system_version_id` (`system_version_id`),
  KEY `component_version_id` (`component_version_id`),
  CONSTRAINT `system_element_component_ibfk_1` FOREIGN KEY (`system_element_id`) REFERENCES `system_element` (`system_element_id`),
  CONSTRAINT `system_element_component_ibfk_2` FOREIGN KEY (`system_version_id`) REFERENCES `system_version` (`system_version_id`),
  CONSTRAINT `system_element_component_ibfk_3` FOREIGN KEY (`component_version_id`) REFERENCES `component_version` (`component_version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system_element_type` */

DROP TABLE IF EXISTS `system_element_type`;

CREATE TABLE `system_element_type` (
  `system_element_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_element_type_name` varchar(255) DEFAULT NULL,
  `system_element_type_short_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`system_element_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system_network_set` */

DROP TABLE IF EXISTS `system_network_set`;

CREATE TABLE `system_network_set` (
  `system_network_set_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_network_set_name` varchar(255) DEFAULT NULL,
  `system_network_set_short_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`system_network_set_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system_version` */

DROP TABLE IF EXISTS `system_version`;

CREATE TABLE `system_version` (
  `system_version_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_version_name` varchar(255) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `system_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`system_version_id`),
  KEY `system_id` (`system_id`),
  CONSTRAINT `system_version_ibfk_1` FOREIGN KEY (`system_id`) REFERENCES `system` (`system_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `user_display_name` varchar(255) DEFAULT NULL,
  `email_address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `user_role` */

DROP TABLE IF EXISTS `user_role`;

CREATE TABLE `user_role` (
  `user_role_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_role_id`),
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
