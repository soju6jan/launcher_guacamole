CREATE DATABASE guacamole_db;
CREATE USER 'guacamole_user'@'%' IDENTIFIED BY 'sjva';
GRANT SELECT,INSERT,UPDATE,DELETE ON guacamole_db.* TO 'guacamole_user'@'%';
FLUSH PRIVILEGES;
quit