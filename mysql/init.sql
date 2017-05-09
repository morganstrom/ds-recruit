-- Set up database and procedure for bucket list app

CREATE DATABASE BucketList;

CREATE TABLE BucketList.tbl_user (
  user_id BIGINT NOT NULL AUTO_INCREMENT,
  user_name VARCHAR(256) NULL,
  user_username VARCHAR(256) NULL,
  user_password VARCHAR(256) NULL,
  PRIMARY KEY (user_id));

DELIMITER $$
CREATE DEFINER=root@localhost PROCEDURE BucketList.sp_createUser(
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

SET @@global.sql_mode= 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';