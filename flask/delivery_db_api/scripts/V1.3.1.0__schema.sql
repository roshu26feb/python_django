/*Table structure for table `method_creation_type` */

CREATE TABLE `method_creation_type` (
  `method_creation_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(3) NOT NULL,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY (`method_creation_type_id`)
);

ALTER TABLE `instance` ADD COLUMN method_creation_type_id int(11);
ALTER TABLE `instance` ADD CONSTRAINT FOREIGN KEY (`method_creation_type_id`) REFERENCES `method_creation_type` (`method_creation_type_id`);

ALTER TABLE `instance` ADD COLUMN network_set_id int(11);
ALTER TABLE `instance` ADD CONSTRAINT FOREIGN KEY (`network_set_id`) REFERENCES `network_set` (`network_set_id`);
