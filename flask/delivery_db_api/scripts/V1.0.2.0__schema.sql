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
  `component_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`component_id`),
  KEY `component_type_id` (`component_type_id`),
  CONSTRAINT `component_ibfk_1` FOREIGN KEY (`component_type_id`) REFERENCES `component_type` (`component_type_id`)
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
  `deployment_step` int(11) DEFAULT NULL,
  `instance_id` int(11) DEFAULT NULL,
  `release_item_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`deployment_id`),
  KEY `instance_id` (`instance_id`),
  KEY `release_item_id` (`release_item_id`),
  CONSTRAINT `deployment_ibfk_1` FOREIGN KEY (`instance_id`) REFERENCES `instance` (`instance_id`),
  CONSTRAINT `deployment_ibfk_2` FOREIGN KEY (`release_item_id`) REFERENCES `release_item` (`release_item_id`)
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
  PRIMARY KEY (`infra_template_id`),
  KEY `host_type_id` (`host_type_id`),
  CONSTRAINT `infrastructure_template_ibfk_1` FOREIGN KEY (`host_type_id`) REFERENCES `host_type` (`host_type_id`)
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
  PRIMARY KEY (`instance_id`),
  KEY `infra_template_id` (`infra_template_id`),
  CONSTRAINT `instance_ibfk_1` FOREIGN KEY (`infra_template_id`) REFERENCES `infrastructure_template` (`infra_template_id`)
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

/*Table structure for table `network_set` */

DROP TABLE IF EXISTS `network_set`;

CREATE TABLE `network_set` (
  `network_set_id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_range_start` varchar(255) DEFAULT NULL,
  `ip_range_end` varchar(20) DEFAULT NULL,
  `subnet` varchar(2000) DEFAULT NULL,
  `host_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`network_set_id`),
  KEY `host_type_id` (`host_type_id`),
  CONSTRAINT `network_set_ibfk_1` FOREIGN KEY (`host_type_id`) REFERENCES `host_type` (`host_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `release` */

DROP TABLE IF EXISTS `release`;

CREATE TABLE `release` (
  `release_id` int(11) NOT NULL AUTO_INCREMENT,
  `release_name` varchar(250) DEFAULT NULL,
  `release_note_url` varchar(250) DEFAULT NULL,
  `release_owner` varchar(250) DEFAULT NULL,
  `remarks` varchar(250) DEFAULT NULL,
  `release_status_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`release_id`),
  KEY `release_status_id` (`release_status_id`),
  CONSTRAINT `release_ibfk_1` FOREIGN KEY (`release_status_id`) REFERENCES `status` (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `release_item` */

DROP TABLE IF EXISTS `release_item`;

CREATE TABLE `release_item` (
  `release_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_component_id` int(11) DEFAULT NULL,
  `logical_instance_name` varchar(255) DEFAULT NULL,
  `release_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`release_item_id`),
  KEY `system_component_id` (`system_component_id`),
  KEY `release_id` (`release_id`),
  CONSTRAINT `release_item_ibfk_1` FOREIGN KEY (`system_component_id`) REFERENCES `system_component` (`system_component_id`),
  CONSTRAINT `release_item_ibfk_2` FOREIGN KEY (`release_id`) REFERENCES `release` (`release_id`)
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
  PRIMARY KEY (`system_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system_component` */

DROP TABLE IF EXISTS `system_component`;

CREATE TABLE `system_component` (
  `system_component_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_version_id` int(11) DEFAULT NULL,
  `component_version_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`system_component_id`),
  KEY `system_version_id` (`system_version_id`),
  KEY `component_version_id` (`component_version_id`),
  CONSTRAINT `system_component_ibfk_1` FOREIGN KEY (`system_version_id`) REFERENCES `system_version` (`system_version_id`),
  CONSTRAINT `system_component_ibfk_2` FOREIGN KEY (`component_version_id`) REFERENCES `component_version` (`component_version_id`)
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

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;