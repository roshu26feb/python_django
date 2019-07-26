ALTER TABLE `release` DROP COLUMN `release_note_url`;
ALTER TABLE `release` DROP COLUMN `remarks`;
ALTER TABLE `release` DROP FOREIGN KEY release_ibfk_1;
ALTER TABLE `release` DROP COLUMN `release_status_id`;

ALTER TABLE `release` ADD COLUMN release_summary varchar(5000);

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

ALTER TABLE `release_item` DROP FOREIGN KEY release_item_ibfk_2;
ALTER TABLE `release_item` DROP FOREIGN KEY release_item_ibfk_3;
ALTER TABLE `release_item` DROP COLUMN `system_element_component_id`;
ALTER TABLE `release_item` DROP COLUMN `release_id`;

ALTER TABLE `release_item` ADD COLUMN release_note_url varchar(5000);

ALTER TABLE `release_item` ADD COLUMN system_version_id int(11);
ALTER TABLE `release_item` ADD CONSTRAINT FOREIGN KEY (`system_version_id`) REFERENCES `system_version` (`system_version_id`);

ALTER TABLE `release_item` ADD COLUMN release_version_id int(11);
ALTER TABLE `release_item` ADD CONSTRAINT FOREIGN KEY (`release_version_id`) REFERENCES `release_version` (`release_version_id`);

CREATE TABLE `parameter_type` (
  `parameter_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`parameter_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `deployment_parameter` (
  `deployment_parameter_id` int(11) NOT NULL AUTO_INCREMENT,
  `deployment_parameter_value` varchar(255) DEFAULT NULL,
  `parameter_type_id` int(11) DEFAULT NULL,
  `deployment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`deployment_parameter_id`),
  KEY `parameter_type_id` (`parameter_type_id`),
  KEY `deployment_id` (`deployment_id`),
  CONSTRAINT `deployment_parameter_ibfk_1` FOREIGN KEY (`parameter_type_id`) REFERENCES `parameter_type` (`parameter_type_id`),
  CONSTRAINT `deployment_parameter_ibfk_2` FOREIGN KEY (`deployment_id`) REFERENCES `deployment` (`deployment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `parameter_value` (
  `parameter_value_id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter_value` varchar(255) DEFAULT NULL,
  `parameter_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`parameter_value_id`),
  KEY `parameter_type_id` (`parameter_type_id`),
  CONSTRAINT `parameter_value_ibfk_1` FOREIGN KEY (`parameter_type_id`) REFERENCES `parameter_type` (`parameter_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `delivery_db`.`deployment` ADD COLUMN system_element_id INT(11) NULL AFTER `deployment_id`;
ALTER TABLE `delivery_db`.`deployment` ADD COLUMN `requested_date` DATETIME NULL AFTER `system_element_id`;
ALTER TABLE `delivery_db`.`deployment` ADD COLUMN `infra_code_flag` TINYINT(1) NULL AFTER `requested_date`;
ALTER TABLE `delivery_db`.`deployment` ADD COLUMN `infra_config_flag` TINYINT(1) NULL AFTER `infra_code_flag`;
ALTER TABLE `delivery_db`.`deployment` ADD COLUMN `app_flag` TINYINT(1) NULL AFTER `infra_config_flag`;
ALTER TABLE `delivery_db`.`deployment` ADD COLUMN `infra_template_id` INT(11) NULL AFTER `app_flag`;
ALTER TABLE `delivery_db`.`deployment` ADD CONSTRAINT `system_element_id` FOREIGN KEY (`system_element_id`) REFERENCES `delivery_db`.`system_element`(`system_element_id`);
ALTER TABLE `delivery_db`.`deployment` ADD CONSTRAINT `infra_template_id` FOREIGN KEY (`infra_template_id`) REFERENCES `delivery_db`.`infrastructure_template`(`infra_template_id`);