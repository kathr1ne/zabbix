# Alert 报警目录

    Alert 报警目录 企业微信报警示例

## 简单介绍

1. 首先要有企业微信 点击 <https://work.weixin.qq.com> 申请即可 创建完成即可获取 企业ID 很重要 后面会用到

2. 注册企业微信之后 创建应用 创建之后 会看到 Agentid 和 Secret 很重要 后面会用到

3. 企业微信设置好 报警应用(第二步创建) 以及 相关部门的可见范围

4. 企业微信相关信息准备好之后 修改zabbix_server.conf

    ```Bash
    grep ^Alert /etc/zabbix/zabbix_server.conf
    AlertScriptsPath=/usr/lib/zabbix/alertscripts   # 修改该配置为你报警脚本存放的目录
    systemctl restart zabbix-server # 修改配置后都需要重启
    ```

5. 按照官方文档在web配置事件通知(告警) <https://www.zabbix.com/documentation/4.0/zh/manual/config/notifications>

6. wechatAlert.py 为我自己写的wechat告警脚本 直接拿来使用即可 把相关的参数换成自己的 即上面提到的 企业ID/Agentid/Secret 等 脚本相关参考微信API接口调用文档 <https://work.weixin.qq.com/api/doc#90000/90135/90664>

  ```Text
   备注：
   1. access_token 我使用缓存到配置文件的方式进行2小时的缓存 过期再重新请求token 否则会因为请求频率限制出现错误
   2. 其余配置 我也一并写到的setting.ini配置文件 如要使用直接修改为自己的即可
   3. setting.ini 配置文件里面
      corpid 为上面创建企业微信的企业ID
      secret 为创建自定义应用之后 给到的Secret
      agentid 为创建自定义应用之后 给到的 Agentid
   ```