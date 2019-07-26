INSERT INTO deployment_type (deployment_type_id,deployment_type_description) VALUES (1,"Manual"),(2,"Partially Automated"),(3,"Fully Automated");
UPDATE component SET deployment_type_id = 3;