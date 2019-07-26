ALTER TABLE `deployment` ADD COLUMN network_set_id int(11);
ALTER TABLE `deployment` ADD CONSTRAINT FOREIGN KEY (`network_set_id`) REFERENCES `network_set` (`network_set_id`);

ALTER TABLE `route_to_live` ADD COLUMN route_to_live_order int(11);
ALTER TABLE `route_to_live` ADD COLUMN critical tinyint(1);
