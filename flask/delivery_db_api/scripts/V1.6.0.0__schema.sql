CREATE TABLE `environment_data_type` (
  `environment_data_type_id` INT(11) NOT NULL AUTO_INCREMENT,
  `environment_data_type_name` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`environment_data_type_id`));

CREATE TABLE `environment_subscription_type`(  
  `environment_subscription_type_id` INT(11) NOT NULL AUTO_INCREMENT,
  `environment_subscription_type_name` VARCHAR(255),
  PRIMARY KEY (`environment_subscription_type_id`)
);

CREATE TABLE `environment_use` (
  `environment_use_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_use_name` varchar(255) DEFAULT NULL,
  `environment_use_short_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`environment_use_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `route_to_live` (
  `route_to_live_id` int(11) NOT NULL AUTO_INCREMENT,
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
  CONSTRAINT `route_to_live_ibfk_4` FOREIGN KEY (`environment_id`) REFERENCES `environment` (`environment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


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


ALTER TABLE environment DROP COLUMN production_data_flag;
ALTER TABLE environment ADD COLUMN environment_data_type_id int(11);
ALTER TABLE environment ADD CONSTRAINT FOREIGN KEY (`environment_data_type_id`) REFERENCES `environment_data_type` (`environment_data_type_id`);
ALTER TABLE environment_type ADD COLUMN environment_type_short_name VARCHAR(5);
ALTER TABLE environment_type ADD COLUMN environment_subscription_type_id INT(11);
ALTER TABLE environment_type ADD CONSTRAINT `env_subscription` FOREIGN KEY (`environment_subscription_type_id`) REFERENCES environment_subscription_type(`environment_subscription_type_id`);  
ALTER TABLE environment ADD COLUMN system_id  int(11);
ALTER TABLE environment ADD CONSTRAINT `systemid` FOREIGN KEY (`system_id`) REFERENCES system(`system_id`);

ALTER TABLE parameter_type CHANGE COLUMN `parameter_name`  `parameter_type` varchar(255);
ALTER TABLE deployment_parameter DROP FOREIGN KEY `deployment_parameter_ibfk_1`;
ALTER TABLE deployment_parameter CHANGE COLUMN `parameter_type_id`  `parameter_id` INT(11);
ALTER TABLE deployment_parameter ADD CONSTRAINT FOREIGN KEY (`parameter_id`) REFERENCES `parameter` (`parameter_id`);
ALTER TABLE parameter_value DROP FOREIGN KEY `parameter_value_ibfk_1`;
ALTER TABLE parameter_value CHANGE COLUMN `parameter_type_id`  `parameter_id` INT(11);
DELETE FROM parameter_value;
DELETE FROM parameter_type;
ALTER TABLE parameter_value ADD CONSTRAINT FOREIGN KEY (`parameter_id`) REFERENCES `parameter` (`parameter_id`);