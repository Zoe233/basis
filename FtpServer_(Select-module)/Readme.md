# FTP_server(select协程实现)-练习

### 作者介绍：

- author：FengGuofu

- My Blog：  

  [python(十)下：事件驱动与 阻塞IO、非阻塞IO、IO多路复用、异步IO](http://blog.csdn.net/fgf00/article/details/52793739)

  [python(十)线程与进程（中）：进程、协程](http://blog.csdn.net/fgf00/article/details/52790360)

### 功能介绍：

1. 协程实现并行同时下载文件

2. 协程实现并行同时上传文件

3. 支持同时下载并上传


###代码思路：

1. 服务器的数据读、写都交由select模块纳管，所以不能有阻塞事件、如socket的accept、recv，以及文件读取不能循环读取，读一次、select一次。
2. 可并行但传输速度下降，以为是频繁打开文件导致，尝试只打开一下传完关闭，速度依然慢，原因待定


### 目录结构：

```python
.
├── bin					# 命令目录
│   └── __init__.py
├── core				# 代码目录
│   ├── ftp_client.py		# ftp客户端主程序
│   ├── ftp_server.py		# ftp服务端主程序
│   └── __init__.py
├── data				# 数据存放目录
│   ├── client_data			# 客户端数据存放目录
│   └── server_data			# 客户端数据存放目录
├── ftp_client.py		# ftp客户端启动程序
├── ftp_server.py		# ftp服务端启动程序
├── model				# 第三方模块目录
│   ├── __init__.py
│   └── prettytable.py		# 将输出内容如表格方式整齐
└── Readme.md
```

### 运行说明：

- Ftp服务端启动程序：ftp_server.py

  - 数据存放目录：data\server_data

- Ftp客户端启动程序：ftp_client.py

  - 数据存放目录：data\client_data

  ​


运行环境：

```
系统环境：Windows 、 linux
软件版本：Python3.0及以上
```

使用方法：

```python
put filename  # 客户端上传
get filename  # 客户端下载
```

