DROP SCHEMA IF EXISTS dsrecruit;
CREATE SCHEMA dsrecruit;

CREATE TABLE dsrecruit.tbl_user (
	user_id 		BIGSERIAL PRIMARY KEY
	,user_name		VARCHAR(45) 
	,user_username	VARCHAR(45)
	,user_password 	VARCHAR(45) 
);

