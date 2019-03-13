# zabbix
    zabbix 4.0 简要安装记录
    系统环境：centos 7.x

# LNMP环境
    tips: zabbix官方包安装之后 web用的apache 官方直接提供../httpd/conf.d/zabbix.conf的配置文件 使用apache会比较方便
    1. MySQL  
    yum install -y mariadb-server   # 安装mysql数据库 7.x默认为mariadb
    systemctl restart mariadb	# 启动
    mysql_secure_installation	# improve MySQL installation security
    2. PHP  
    yum install -y php
    3. NGINX  
    [nginx官网yum源配置](http://nginx.org/en/linux_packages.html#RHEL-CentOS)
    yum install -y nginx
