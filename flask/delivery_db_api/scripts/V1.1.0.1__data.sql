INSERT INTO environment_type (environment_type_id,environment_type_name)  VALUES (1,"DEV"),(2,"SIT"),(3,"UAT"),(4,"PER"),(5,"OAT"),(6,"PREPOD"),(7,"PROD");
UPDATE disk_type SET disk_type_description="Standard OS disk" WHERE disk_type_id = 1;
UPDATE disk_type SET disk_type_description="Standard Data disk" WHERE disk_type_id = 2;
UPDATE disk_type SET disk_type_description="Premium OS disk" WHERE disk_type_id = 3;
INSERT INTO disk_type (disk_type_id,disk_type_description,min_size,MAX_SIZE,host_type_id) VALUES (4,"Premium Data disk",150,NULL,2);