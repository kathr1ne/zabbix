# zabbix
    zabbix 4.0 简要安装记录
    系统环境：centos 7.x

# LNMP环境
    tips: zabbix官方包安装之后 web用的apache 官方直接提供../httpd/conf.d/zabbix.conf的配置文件 使用apache会比较方便
* MySQL
    yum install -y mariadb-server   # 安装mysql数据库 7.x默认为mariadb
    systemctl restart mariadb	# 启动
    mysql_secure_installation	# improve MySQL installation security
* PHP
    yum install -y php
* NGINX
    [http://nginx.org/en/linux_packages.html#RHEL-CentOS] # 按照官网配置nginx yum源
    yum install -y nginx
