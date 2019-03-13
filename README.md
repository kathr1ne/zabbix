# zabbix

    zabbix 4.0 简要安装记录
    系统环境：centos 7.x
    默认系统已进行相关初始化：ntp同步 iptables已开放相关端口 配置network 禁用selinx等

## LNMP环境

    tips: zabbix官方包安装之后 web用的apache 官方直接提供../httpd/conf.d/zabbix.conf的配置文件 使用apache会比较方便

* MySQL

    ```Bash
    yum install -y mariadb-server   # 安装mysql数据库 7.x默认为mariadb
    systemctl restart mariadb    # 启动
    mysql_secure_installation    # improve MySQL installation security
    ```

* PHP

    ```Bash
    yum install -y php  # 安装PHP
    ```

* NGINX
    nginx官网yum源配置链接： <http://nginx.org/en/linux_packages.html#RHEL-CentOS>

    ```Bash
    yum install -y nginx
    ```

  * 配置php环境
    apache 和 nginx 配置php环境有所不同

    * apache

        需要修改apache的配置文件httpd.conf以得到PHP的解析

        ```Bash
        1. 在LoadModule中添加：LoadModule php5_module     modules/libphp5.so
        2. 在AddType application/x-gzip .gz .tgz下面添加:
            AddType application/x-httpd-php .php
            AddType application/x-httpd-php-source .phps
        3. 在DirectoryIndex增加 index.php 以便apache识别PHP格式的index
            <IfModule dir_module>
                DirectoryIndex index.html index.php
            </IfModule>
        4. 重启httpd 自行验证PHP环境是否配置成功

        ```

    * nginx

        通过php-fpm设置
        参考文档：<https://medium.com/@iven00000000/%E6%96%BCcentos7%E5%AE%89%E8%A3%9D-nginx-php7-php-fpm-laravel5-6-df8631681acf>

        ```Bash
        yum install -y php-fpm  # 安装php-fpm
        cp /etc/php-fpm.d/www.conf{,.backup}    # 备份
        sed -i '/^user/s/apache/nginx/' /etc/php-fpm.d/www.conf     # 修改user和group为nginx
        sed -i '/^group/s/apache/nginx/' /etc/php-fpm.d/www.conf
        # 如果要改为使用socket file(预设使用 127.0.0.1:9000) 则需修改如下配置
        listen = /path/to/unix/socket
        listen.owner = nobody
        listen.group = nobody
        listen.mode = 0666

        systemctl restart php-fpm   # 重启并设置开机启动
        systemctl enable php-fpm
        ```
