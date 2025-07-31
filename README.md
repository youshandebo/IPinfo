# IP信息批量查询工具

这是一个使用IPinfo Lite API批量查询IP地址信息并将结果保存到文本文件的Python脚本。

## 功能

- 批量查询多个IP地址的信息
- 支持从文件读取IP地址列表
- 查询结果包括IP、ASN、AS名称、AS域名、国家代码和国家名称
- 将查询结果保存到文本文件
- 支持中文和英文界面切换
- 表格化输出格式，提高可读性

## 使用前准备

1. 确保您的Ubuntu VPS上已安装Python 3和pip

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. 安装所需的Python库

   ```bash
   pip3 install requests
   ```

3. 获取IPinfo API令牌
   - 访问 https://ipinfo.io/signup 注册一个免费账户
   - 登录后获取您的API令牌

4. 编辑`ip_query.py`文件，将您的API令牌填入`API_TOKEN`变量

   ```python
   API_TOKEN = "YOUR_API_TOKEN"  # 替换为您的实际API令牌
   ```

## 使用方法

### 方式一：命令行参数（新版）

脚本现在支持更灵活的命令行参数：

```bash
python3 ip_query.py [-f FILE] [-o OUTPUT] [-l LANGUAGE]
```

参数说明：
- `-f, --file`: 包含IP地址的文件路径
- `-o, --output`: 结果输出文件（默认为`ip_results.txt`）
- `-l, --language`: 语言选择，可选值为`zh`（中文）或`en`（英文），默认为`zh`

示例：

1. 使用英文界面查询IP文件

   ```bash
   python3 ip_query.py -f example_ips.txt -l en
   ```

2. 指定输出文件名

   ```bash
   python3 ip_query.py -f example_ips.txt -o my_results.txt
   ```

3. 使用英文界面并指定输出文件

   ```bash
   python3 ip_query.py -f example_ips.txt -o my_results.txt -l en
   ```

### 方式二：交互式查询

1. 直接运行脚本，不带任何参数（可以指定语言）

   ```bash
   python3 ip_query.py
   # 或者指定使用英文界面
   python3 ip_query.py -l en
   ```

2. 根据提示选择查询模式：
   - 选项1：从文件读取IP地址
   - 选项2：手动输入IP地址

3. 如果选择手动输入模式，按照提示输入要查询的IP地址，每行一个，输入空行结束

4. 指定结果保存的文件名（默认为`ip_results.txt`）

5. 查看生成的结果文件

   ```bash
   cat ip_results.txt
   ```

## 注意事项

- IPinfo免费计划每月限制50,000次请求
- 脚本默认使用IPinfo Lite API，它提供基本的IP信息
- 批量查询模式每次最多处理100个IP地址（可在脚本中修改`BATCH_SIZE`变量）

## 输出格式

输出文件现在使用表格格式，提高可读性，包含以下字段：

```
IP地址         | ASN        | AS名称                          | AS域名                          | 国家代码      | 国家名称
--------------- | ---------- | ------------------------------ | ------------------------------ | ------------ | ---------------
8.8.8.8         | AS15169    | Google LLC                     | google.com                     | US           | United States
```

英文界面下的输出格式：

```
IP Address      | ASN        | AS Name                         | AS Domain                       | Country Code | Country
--------------- | ---------- | ------------------------------ | ------------------------------ | ------------ | ---------------
8.8.8.8         | AS15169    | Google LLC                     | google.com                     | US           | United States
```