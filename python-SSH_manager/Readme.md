# SSH简单管理工具-练习程序

### 作者介绍：

- author：FengGuofu
- My Blog：  http://blog.csdn.net/fgf00

### 功能介绍：

1. 主机分组
2. 登录后显示主机分组，选择分组后查看主机列表
3. 可批量执行命令、发送文件，结果实时返回
4. 主机用户名密码可以不同

### 目录结构：

```
├── run.py			# 入口程序
├── bin				# 命令目录
├── conf			# 配置目录
│   ├── hosts.json		# 主机信息
│   └── settings.py		# 配置程序
├── core			# 源码目录
│   ├── main.py			# 主程序
│   ├── ssh_connect.py	# ssh命令运行
│   └── transmission.py	# 传输文件
└── log				# 日志目录
    ├── logger.py		# 日志程序
    ├── os.log			# 日志文件
```



### 运行说明：

- 程序入口文件文件：run.py
- 用户名： admin ， 密码：admin
- 上传文件路径：run.py同级目录文件，或绝对路径文件
- 日志文件在：log\os.log
- 建议在linux下运行，window是下运行颜色不打印（但不影响运行结果）

