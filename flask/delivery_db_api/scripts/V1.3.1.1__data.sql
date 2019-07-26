INSERT INTO method_creation_type (method_creation_type_id,name,description) VALUES (1,"B","Build Pipeline"),(2,"D","Deployment Pipeline"),(3,"M","Manual");
UPDATE `instance` set method_creation_type_id=1;
UPDATE `instance` set method_creation_type_id=2 where instance_id IN (273,274,269,251,203,238,252,212,160);
UPDATE `component_type` set component_type_description = "Infrastructure Code" where component_type_id=2;
UPDATE `component_type` set component_type_description = "Infrastructure Tool" where component_type_id=5;