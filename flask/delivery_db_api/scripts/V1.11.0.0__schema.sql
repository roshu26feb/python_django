ALTER TABLE `system_element` DROP FOREIGN KEY system_element_ibfk_1;
ALTER TABLE `system_element` DROP COLUMN system_version_id;

ALTER TABLE `system_element` ADD COLUMN system_id int(11);
ALTER TABLE `system_element` ADD CONSTRAINT FOREIGN KEY (`system_id`) REFERENCES `system` (`system_id`);

ALTER TABLE `system_element_component` ADD COLUMN system_version_id int(11);
ALTER TABLE `system_element_component` ADD CONSTRAINT FOREIGN KEY (`system_version_id`) REFERENCES `system_version` (`system_version_id`);
