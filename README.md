# zabbix
    zabbix 4.0 简要安装记录
    系统环境：centos 7.x

# LNMP环境
    tips: zabbix官方包安装之后 web用的apache 官方直接提供../httpd/conf.d/zabbix.conf的配置文件 使用apache会比较方便
* MySQL  
    ```Bash
    yum install -y mariadb-server   # 安装mysql数据库 7.x默认为mariadb
    systemctl restart mariadb	# 启动
    mysql_secure_installation	# improve MySQL installation security
    ```
* PHP  
    ```Bash
    yum install -y php  # 安装PHP
    ```
* NGINX  
    [nginx官网yum源配置] http://nginx.org/en/linux_packages.html#RHEL-CentOS
    ```Bash
    yum install -y nginx
    ```
    * 配置php环境  
    apache 和 nginx 配置php环境有所不同  
        * apache  
        ```Bash
        # apache
        需要修改apache的配置文件httpd.conf以得到PHP的解析
        1. 在LoadModule中添加：LoadModule php5_module     modules/libphp5.so
        2. 在AddType application/x-gzip .gz .tgz下面添加:
            AddType application/x-httpd-php .php
            AddType application/x-httpd-php-source .phps
        3. 在DirectoryIndex增加 index.php 以便apache识别PHP格式的index
            <IfModule dir_module>  
                DirectoryIndex index.html index.php  
            </IfModule>
        4. 重启httpd 自行验证PHP环境是否配置成功

        # nginx
        通过php-fpm设置
        yum install -y php-fpm  # 安装php-fpm
        cp /etc/php-fpm.d/www.conf{,.backup}
        sed -i '/^user/s/apache/nginx/' /etc/php-fpm.d/www.conf
        sed -i '/^group/s/apache/nginx/' /etc/php-fpm.d/www.conf
        ```  
        * nginx

