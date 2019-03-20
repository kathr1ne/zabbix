# Grafana-Zabbix

 使用grafana展示zabbix收集到的数据

 ## 相关资料

Grafana-Zabbix文档：<http://alexanderzobnin.github.io/grafana-zabbix>
Grafana官方文档：<http://docs.grafana.org>
其他参考文档：<https://www.cnblogs.com/kevingrace/p/7108060.html>

## 安装

- 安装grafana

  ```Bash
  # 使用rpm安装方式 参考上面 官方文档给出的rpm包
  wget https://dl.grafana.com/oss/release/grafana-6.0.2-1.x86_64.rpm  # 获取最新版本rpm包
  yum install -y grafana-6.0.2-1.x86_64.rpm
  systemctl enable grafana-server  # 开机启动
  ```

- 安装zabbix插件

  ```Bash
  grafana-cli plugins list-remote   # 获取可用的插件列表
  grafana-cli plugins install alexanderzobnin-zabbix-app    # 安装zabbix插件
  systemctl restart grafana-server   # 安装完重新启动grafana
  # 重启之后即可访问grafana的web界面开始配置 datasource 添加zabbix 
  # 可以参考上面给出的文档进行相关配置
  ```