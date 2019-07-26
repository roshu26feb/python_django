DROP TABLE IF EXISTS `system_element_infrastructure`;

CREATE TABLE `system_network_set` (
  `system_network_set_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_network_set_name` varchar(255) DEFAULT NULL,
  `system_network_set_short_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`system_network_set_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `system_element_type` (
  `system_element_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_element_type_name` varchar(255) DEFAULT NULL,
  `system_element_type_short_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`system_element_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `system` ADD COLUMN system_network_set_id int(11);
ALTER TABLE `system` ADD CONSTRAINT FOREIGN KEY (`system_network_set_id`) REFERENCES `system_network_set` (`system_network_set_id`);

ALTER TABLE `system_element` ADD COLUMN system_element_type_id int(11);
ALTER TABLE `system_element` ADD CONSTRAINT FOREIGN KEY (`system_element_type_id`) REFERENCES `system_element_type` (`system_element_type_id`);

CREATE TABLE `host_region` (
  `host_region_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_region_name` varchar(255) DEFAULT NULL,
  `host_region_description` varchar(255) DEFAULT NULL,
  `host_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`host_region_id`),
  KEY `host_type_id` (`host_type_id`),
  CONSTRAINT `host_region_ibfk_1` FOREIGN KEY (`host_type_id`) REFERENCES `host_type` (`host_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `host_site` (
  `host_site_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_site_name` varchar(255) DEFAULT NULL,
  `host_site_description` varchar(255) DEFAULT NULL,
  `host_region_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`host_site_id`),
  KEY `host_region_id` (`host_region_id`),
  CONSTRAINT `host_site_ibfk_1` FOREIGN KEY (`host_region_id`) REFERENCES `host_region` (`host_region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

ALTER TABLE `network_set` DROP FOREIGN KEY network_set_ibfk_1;
ALTER TABLE `network_set` DROP COLUMN host_type_id;


ALTER TABLE `network_set` ADD COLUMN host_site_id int(11);
ALTER TABLE `network_set` ADD CONSTRAINT FOREIGN KEY (`host_site_id`) REFERENCES `host_site` (`host_site_id`);

ALTER TABLE `network_set` ADD COLUMN host_subscription_id int(11);
ALTER TABLE `network_set` ADD CONSTRAINT FOREIGN KEY (`host_subscription_id`) REFERENCES `host_subscription` (`host_subscription_id`);

ALTER TABLE `network_set` ADD COLUMN environment_type_id int(11);
ALTER TABLE `network_set` ADD CONSTRAINT FOREIGN KEY (`environment_type_id`) REFERENCES `environment_type` (`environment_type_id`);

ALTER TABLE `network_set` ADD COLUMN system_element_type_id int(11);
ALTER TABLE `network_set` ADD CONSTRAINT FOREIGN KEY (`system_element_type_id`) REFERENCES `system_element_type` (`system_element_type_id`);
