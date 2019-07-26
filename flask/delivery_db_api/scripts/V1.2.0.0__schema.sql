/*Table structure for table `system_element` */


CREATE TABLE `system_element` (
  `system_element_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_element_name` varchar(255) DEFAULT NULL,
  `system_version_id` int(11) NOT NULL,
  PRIMARY KEY (`system_element_id`),
  KEY `system_version_id` (`system_version_id`),
  CONSTRAINT `system_element_ibfk_1` FOREIGN KEY (`system_version_id`) REFERENCES `system_version` (`system_version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system_element_component` */


CREATE TABLE `system_element_component` (
  `system_element_component_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_order` int(11) DEFAULT NULL,
  `system_element_id` int(11) NOT NULL,
  `component_version_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`system_element_component_id`),
  KEY `system_element_id` (`system_element_id`),
  KEY `component_version_id` (`component_version_id`),
  CONSTRAINT `system_element_component_ibfk_1` FOREIGN KEY (`system_element_id`) REFERENCES `system_element` (`system_element_id`),
  CONSTRAINT `system_element_component_ibfk_2` FOREIGN KEY (`component_version_id`) REFERENCES `component_version` (`component_version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `system_element_infrastructure` */

CREATE TABLE `system_element_infrastructure` (
  `system_element_infrastructure_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_element_id` int(11) NOT NULL,
  `environment_type_id` int(11) NOT NULL,
  `infra_template_id` int(11) NOT NULL,
  PRIMARY KEY (`system_element_infrastructure_id`),
  KEY `system_element_id` (`system_element_id`),
  KEY `environment_type_id` (`environment_type_id`),
  KEY `infra_template_id` (`infra_template_id`),
  CONSTRAINT `system_element_infrastructure_ibfk_1` FOREIGN KEY (`system_element_id`) REFERENCES `system_element` (`system_element_id`),
  CONSTRAINT `system_element_infrastructure_ibfk_2` FOREIGN KEY (`environment_type_id`) REFERENCES `environment_type` (`environment_type_id`),
  CONSTRAINT `system_element_infrastructure_ibfk_3` FOREIGN KEY (`infra_template_id`) REFERENCES `infrastructure_template` (`infra_template_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `delivery_db`.`release_item` DROP FOREIGN KEY release_item_ibfk_1;
ALTER TABLE `delivery_db`.`release_item` drop column system_component_id;
ALTER TABLE `delivery_db`.`release_item` DROP COLUMN logical_instance_name;
ALTER TABLE `delivery_db`.`release_item` ADD COLUMN system_element_component_id int(11);
ALTER TABLE `delivery_db`.`release_item` ADD CONSTRAINT FOREIGN KEY (`system_element_component_id`) REFERENCES `system_element_component` (`system_element_component_id`);
ALTER TABLE `delivery_db`.`deployment` DROP COLUMN deployment_step;
ALTER TABLE `delivery_db`.`environment` ADD COLUMN production_data_flag tinyint(1);
ALTER TABLE `delivery_db`.`environment` ADD CONSTRAINT `CONSTRAINT_1` CHECK (`production_data_flag` in (0,1));
ALTER TABLE `delivery_db`.`component` ADD COLUMN linked_ci_flag tinyint(1);