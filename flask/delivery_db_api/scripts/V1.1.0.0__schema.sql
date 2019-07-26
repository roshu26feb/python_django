/*Table structure for table `environment_type` */
CREATE TABLE `environment_type` (
  `environment_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_type_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`environment_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Table structure for table `environment` */

CREATE TABLE `environment` (
  `environment_id` int(11) NOT NULL AUTO_INCREMENT,
  `environment_name` varchar(255) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  `environment_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`environment_id`),
  KEY `environment_type_id` (`environment_type_id`),
  CONSTRAINT `environment_ibfk_1` FOREIGN KEY (`environment_type_id`) REFERENCES `environment_type` (`environment_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Added new column `network_set_name` to `network_set` table*/
ALTER TABLE `delivery_db`.`network_set` ADD COLUMN `network_set_name` VARCHAR(255) NULL AFTER `network_set_id`;

/* Added new column `environment_id` to `deployment` table*/
ALTER TABLE `delivery_db`.`deployment` ADD COLUMN `environment_id` INT NULL; 
ALTER TABLE `delivery_db`.`deployment` ADD CONSTRAINT FOREIGN KEY (`environment_id`) REFERENCES `environment` (`environment_id`);
