# zabbix

    zabbix 4.0 简要安装记录
    系统环境：centos 7.x
    默认系统已进行相关初始化：ntp时间同步 iptables已开放相关端口 配置network 禁用selinx等

## LNMP环境

    tips: zabbix官方包安装之后 web用的apache 官方直接提供../httpd/conf.d/zabbix.conf的配置文件 使用apache会比较方便

* MySQL

    ```Bash
    yum install -y mariadb-server   # 安装mysql数据库 7.x默认为mariadb
    systemctl restart mariadb    # 启动
    systemctl enable mariadb     # 设置开机启动
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
    systemctl enable nginx
    systemctl restart nginx    # 后面修改了文件记得重启 或者reload
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

## zabbix-server

参考zabbix官方文档操作步骤即可：
<https://www.zabbix.com/documentation/4.0/zh/manual/installation/install_from_packages/rhel_centos>

* 安装zabbix-server和zabbix-web

    ```Bash
    rpm -ivh http://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm
    yum install -y zabbix-server-mysql # 安装 Zabbix server并使用 MySQL 数据库
    yum install -y zabbix-web-mysql    # 安装 Zabbix 前端并使用 MySQL 数据库
    ```

* MySQL配置

    ```MySQL
    mysql -uroot -p<password>
    create database zabbix character set utf8 collate utf8_bin;
    grant all privileges on zabbix.* to zabbix@localhost identified by '<password>';
    quit;
    ```

    ```Bash
    # 使用 MySQL 来导入 Zabbix server 的初始数据库 schema 和数据
    zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz | mysql -uzabbix -p zabbix
    ```

* zabbix配置修改

    ```Bash
    编辑 zabbix_server.conf 或 zabbix_proxy.conf 文件以使用已创建的数据库
    # vim /etc/zabbix/zabbix_server.conf
    DBHost=localhost
    DBName=zabbix
    DBUser=zabbix
    DBPassword=<password>
    ```

    ```Bash
    配置完成之后 重启 nginx或者httpd 访问web即可 nginx的zabbix.conf见附件 apache的自带该配置文件
    注意：
    1. 使用nginx 需要修改/etc/zabbix/web/目录权限 默认为apache用户的权限
    chown nginx.nginx -R /etc/zabbix/web/
    2. web配置界面如果 Next Step如果点击没有反应 执行下面权限 默认为：root.apache
    chown root.nginx -R /var/lib/php/session/
    ```

* setup web界面配置

   ```Bash
    根据web界面 跟着点下一步配置即可
    Check of pre-requisites 步骤 如果有Required为Fail的 根据建议修改/etc/php.ini文件配置 然后重启php-fpm即可
    cp /etc/php.ini{,.backup}
    vim /etc/php.ini    ...  # 修改建议配置
    sytemctl restart php-fpm

    如果配置mysql的时候 点NextStep出现502错误
    nginx错误日志: upstream sent too big header while reading response header from upstream
    vim /etc/nginx/nginx.conf # 修改http段 加入如下配置 重启nginx
    fastcgi_buffer_size 128k;
    fastcgi_buffers 4 256k;
    fastcgi_busy_buffers_size 256k;

    配置成功之后 使用默认用户名密码登录即可
    User: Admin
    Passwd: <your password>

    访问web: http://192.168.xx.xx/profile.php以修改密码 设置语言等
    # 字体乱码问题
    从windows拷贝一个简体字体到服务器 比如: simkai.ttf # 附件直接给出
    mv simkai.ttf /usr/share/zabbix/fonts/graphfont.ttf  # 替换掉即可
    ```

    备注：[zabbix-server配置详解] <https://www.zabbix.com/documentation/4.0/zh/manual/appendix/config/zabbix_server>

## zabbix-agent

  ```Bash
    # 同样下载yum源仓库（本地安装建议把依赖包全部下载做本地仓库）
    rpm -ivh http://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm
    yum install -y zabbix-agent    # 安装agent
    vim /etc/zabbix/zabbix_agentd.conf  # 配置配置文件 调整相关配置

    # 本地简单的测试配置
    sed '/^#/d;/^$/d' /etc/zabbix/zabbix_agentd.conf
    PidFile=/var/run/zabbix/zabbix_agentd.pid
    LogFile=/var/log/zabbix/zabbix_agentd.log
    LogFileSize=0
    Server=192.168.40.132
    ServerActive=192.168.40.132
    Hostname=vm02
    Include=/etc/zabbix/zabbix_agentd.d/*.conf
   ```

  相关配置含义直接看配置文件注释 或者 参考官方文档给出的含义介绍 十分详细
  [zabbix-agent配置详解] <https://www.zabbix.com/documentation/4.0/zh/manual/appendix/config/zabbix_agentd>
  [额外参考] <https://blog.51cto.com/lookingdream/1839558>