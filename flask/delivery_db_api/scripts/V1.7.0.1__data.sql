UPDATE component_type set component_type_description='Application' where component_type_id=1;
UPDATE component_type set component_type_description='Infrastructure Configuration' where component_type_id=2;
UPDATE component_type set component_type_description='Infrastructure' where component_type_id=3;
UPDATE environment_data_type set environment_data_type_name='Manufactured' where environment_data_type_id=1;
UPDATE environment_subscription_type set environment_subscription_type_name='Development' where environment_subscription_type_id=1;
UPDATE environment_type set identifier='D' where environment_type_id=1;
UPDATE environment_type set identifier='T' where environment_type_id=1;
UPDATE environment_type set identifier='A' where environment_type_id=1;
UPDATE environment_type set identifier='R' where environment_type_id=1;
UPDATE environment_type set identifier='P' where environment_type_id=1;
INSERT INTO host_type (host_type_id,host_name) VALUES (6,'Azure - EU');
UPDATE host_type set host_name='On-premise - RHEV' where host_type_id=1;
UPDATE host_type set host_name='Azure - AU' where host_type_id=2;
UPDATE host_type set host_name='Sunguard' where host_type_id=3;
UPDATE host_type set host_name='AWS - EU' where host_type_id=4;
UPDATE host_type set host_name='Oracle Cloud' where host_type_id=5;
UPDATE component set component_type_id = 1 where component_id in (6,7,11,16);
UPDATE component set component_type_id = 3 where component_id in (18);
UPDATE component set component_type_id = 2 where component_id in (1,2,3,4,5,8,9,10,12,13,14,15,17,19,20,21,22,23,24,25,26,27,28,29);
DELETE from component_type where component_type_id in(4,5);