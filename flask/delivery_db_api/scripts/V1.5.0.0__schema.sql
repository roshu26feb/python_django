drop table deployment_tag;
CREATE TABLE infrastructure_type (
  `infrastructure_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `infrastructure_type_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`infrastructure_type_id`)
);

ALTER TABLE deployment DROP FOREIGN KEY deployment_ibfk_2;
ALTER TABLE deployment DROP COLUMN release_item_id;
ALTER TABLE infrastructure_template ADD COLUMN infrastructure_type_id INT(11);
ALTER TABLE infrastructure_template ADD CONSTRAINT FOREIGN KEY (`infrastructure_type_id`) REFERENCES `infrastructure_type` (`infrastructure_type_id`);
ALTER TABLE deployment_parameter CHANGE `deployment_parameter_value` `deployment_parameter_value` MEDIUMTEXT NULL;
  