# 计算机网络课程实习 - README

**姓名：** 高范铖  

**学号：** 230203205  

**班级：** 计算机23-3  

**指导教师：** 齐建东  


-----

## 项目概述

本项目包含前后两个基于Python Socket编程的网络课程实习任务，本部分为Task1，在 **PyCharm 2024.1.4** 环境下开发完成。

  * **Task 1** 实现了一个多线程的TCP服务器，能够接收客户端发送的文本文件，分块进行字符串反转并返回结果。

## Git 仓库地址

[https://github.com/vanchengking/TCP.git](https://github.com/vanchengking/TCP.git)

-----

## 1\. 运行环境与依赖

  * **操作系统**:  Windows 11
  * **Python 版本**: python 3.12.6
  * **需要安装的库**: `pandas` (仅Task2的客户端需要)
      * 安装命令:
        ```bash
        pip install pandas
        ```

-----

## 2\. Task 1: TCP 字符串反转服务

### 文件列表

  * `reversetcpserver.py`
  * `reversetcpclient.py`

### 运行指南

#### ① 启动服务器

在终端中运行以下命令，服务器将启动并监听在 **12345** 端口。

```bash
python reversetcpserver.py
```

#### ② 启动客户端

在另一个终端中运行以下命令。客户端需要5个命令行参数。

```bash
python reversetcpclient.py <服务器IP> <服务器端口> <文件名> <Lmin> <Lmax>
```

  * `<服务器IP>`: 服务器所在的IP地址。如果在同一台机器上测试，请使用 `127.0.0.1`。
  * `<服务器端口>`: 服务器监听的端口号，应为 `12345`。
  * `<文件名>`: 需要发送给服务器进行反转的本地文件名 (例如: `test.txt`)。
  * `<Lmin>`: 随机数据块的最小字节数。
  * `<Lmax>`: 随机数据块的最大字节数。

#### ③ 运行示例

```bash
python reversetcpclient.py 127.0.0.1 12345 test.txt 10 100
```

-----
