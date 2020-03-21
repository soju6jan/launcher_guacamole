#!/bin/sh
apk add --no-cache openjdk8
#wget http://apache.tt.co.kr/tomcat/tomcat-8/v8.5.50/bin/apache-tomcat-8.5.50.tar.gz
wget http://apache.tt.co.kr/tomcat/tomcat-8/v8.5.51/bin/apache-tomcat-8.5.51.tar.gz
tar xvzf apache-tomcat-8.5.51.tar.gz
mv apache-tomcat-8.5.51 /var/lib/tomcat
cp -R /app/data/custom/launcher_guacamole/guacamole /etc/guacamole/
ln -s /etc/guacamole/guacamole.war /var/lib/tomcat/webapps/
export GUACAMOLE_HOME=/etc/guacamole
apk add --no-cache mariadb mariadb-client mariadb-server-utils pwgen
/etc/guacamole/create.sh
mv /app/data/custom/launcher_guacamole/guacamole/my.cnf /etc/
chmod 0444 /etc/my.cnf
#mysql --user=root --password=sjva < /etc/guacamole/create.sql
#mysql --user=root --password=sjva guacamole_db < /etc/guacamole/initdb.sql
#kill -9 `ps -ef | grep mysqld | awk '{print $1}'`
 
