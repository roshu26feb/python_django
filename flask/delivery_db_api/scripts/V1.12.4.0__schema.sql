CREATE TABLE `instance_allocation` (
  `instance_allocation_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_element_id` int(11) DEFAULT NULL,
  `system_id` int(11) DEFAULT NULL,
  `instance_id` int(11) DEFAULT NULL,
  `environment_id` int(11) DEFAULT NULL,
  `system_version_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`instance_allocation_id`),
  KEY `system_element_id` (`system_element_id`),
  KEY `system_id` (`system_id`),
  KEY `instance_id` (`instance_id`),
  KEY `environment_id` (`environment_id`),
  KEY `system_version_id` (`system_version_id`),
  CONSTRAINT `instance_allocation_ibfk_1` FOREIGN KEY (`system_element_id`) REFERENCES `system_element` (`system_element_id`),
  CONSTRAINT `instance_allocation_ibfk_2` FOREIGN KEY (`system_id`) REFERENCES `system` (`system_id`),
  CONSTRAINT `instance_allocation_ibfk_3` FOREIGN KEY (`instance_id`) REFERENCES `instance` (`instance_id`),
  CONSTRAINT `instance_allocation_ibfk_4` FOREIGN KEY (`environment_id`) REFERENCES `environment` (`environment_id`),
  CONSTRAINT `instance_allocation_ibfk_5` FOREIGN KEY (`system_version_id`) REFERENCES `system_version` (`system_version_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

ALTER TABLE `deployment` ADD COLUMN system_version_id int(11);
ALTER TABLE `deployment` ADD CONSTRAINT FOREIGN KEY (`system_version_id`) REFERENCES `system_version` (`system_version_id`);


