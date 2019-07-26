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

ALTER TABLE `system_element` ADD COLUMN `system_element_short_name` varchar(7);