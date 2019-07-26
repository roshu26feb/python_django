DROP TABLE IF EXISTS `system_component`;

/*Table structure for table `deployment_type` */

DROP TABLE IF EXISTS `deployment_type`;

CREATE TABLE `deployment_type` (
  `deployment_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `deployment_type_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`deployment_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `delivery_db`.`component` ADD COLUMN deployment_type_id int(11);
ALTER TABLE `delivery_db`.`component` ADD CONSTRAINT FOREIGN KEY (`deployment_type_id`) REFERENCES `deployment_type` (`deployment_type_id`);

/*Table structure for table `tag_type` */

DROP TABLE IF EXISTS `tag_type`;

CREATE TABLE `tag_type` (
  `tag_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`tag_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `deployment_tag` */

DROP TABLE IF EXISTS `deployment_tag`;

CREATE TABLE `deployment_tag` (
  `deployment_tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_value` varchar(255) DEFAULT NULL,
  `tag_type_id` int(11) DEFAULT NULL,
  `deployment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`deployment_tag_id`),
  KEY `tag_type_id` (`tag_type_id`),
  KEY `deployment_id` (`deployment_id`),
  CONSTRAINT `deployment_tag_ibfk_1` FOREIGN KEY (`tag_type_id`) REFERENCES `tag_type` (`tag_type_id`),
  CONSTRAINT `deployment_tag_ibfk_2` FOREIGN KEY (`deployment_id`) REFERENCES `deployment` (`deployment_id`)
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

