-- Set up table and procedures for user authentication

-- Table for users
CREATE TABLE ds_recruit.tbl_user (
  user_id BIGINT NOT NULL AUTO_INCREMENT,
  user_name VARCHAR(256) NULL,
  user_username VARCHAR(256) NULL,
  user_password VARCHAR(256) NULL,
  PRIMARY KEY (user_id));


-- Procedure for creating users
DELIMITER $$
CREATE DEFINER=root@localhost PROCEDURE ds_recruit.sp_createUser(
    IN p_name VARCHAR(256),
    IN p_username VARCHAR(256),
    IN p_password VARCHAR(256)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );

    END IF;
END$$
DELIMITER ;

-- Procedure for validating login
DELIMITER $$
CREATE DEFINER=root@localhost PROCEDURE ds_recruit.sp_validateLogin(
IN p_username VARCHAR(255)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;

-- Global settings
SET @@global.sql_mode= 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';