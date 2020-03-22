#!/bin/sh
if [ -z "$1" ];then
    echo "Usage: $0 [port]"
    exit 1
fi
sed "s/8080/$1/g" < /var/lib/tomcat/conf/server.xml > /tmp/server.xml \
    && /var/lib/tomcat/bin/catalina.sh start -config /tmp/server.xml
