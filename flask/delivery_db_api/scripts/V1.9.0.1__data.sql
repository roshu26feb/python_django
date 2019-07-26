UPDATE host_type set host_name='Azure' where host_type_id=2;
UPDATE host_type set host_name='AWS' where host_type_id=4;
DELETE from host_type where host_type_id = 6;

UPDATE environment_subscription_type set environment_subscription_type_name='PROD' where environment_subscription_type_id=1;
UPDATE environment_subscription_type set environment_subscription_type_name='NON_PROD' where environment_subscription_type_id=2;
UPDATE environment_type set environment_subscription_type_id= 2 where environment_subscription_type_id in (1,2,3,4);
UPDATE environment_type set environment_subscription_type_id= 1 where environment_subscription_type_id=5;
DELETE from environment_subscription_type where environment_subscription_type_id in (3,4);

INSERT INTO system_network_set (system_network_set_id,system_network_set_name,system_network_set_short_name) VALUES (1,'Retail','r'),(2,'Supply Chain','s'),(3,'Corporate','c'),(4,'Digital','d');
INSERT INTO system_element_type (system_element_type_id,system_element_type_name,system_element_type_short_name) VALUES (1,'Application','app'),(2,'Database','db'),(3,'DMZ','dmz');
INSERT INTO host_region (host_region_id,host_region_name,host_region_description,host_type_id) VALUES (1,'APAC','Australia/NewZeland',2),(2,'EMEA','Europe,Middle East and Africa',2),(3,'UK','United Kingdom',1);
INSERT INTO host_site (host_site_id,host_site_name,host_site_description,host_region_id) VALUES (1,'em4','Azure Amsterdam - West Europe',2),(2,'em2','Azure Dublin - North Europe',2),(3,'ap6s','Azure Sydney',1),(4,'ap6m','Azure Melbourne',1),(5,'f6','Forum 6 Office, Whiteley, Southampton, GBR',3);
