#!/bin/bash

# 选择语言 / Choose language
echo "请选择语言 / Please select language:"
echo "1. 中文 (Chinese)"
echo "2. English"
read -p "选择 / Choice (1/2): " lang_choice

if [ "$lang_choice" = "2" ]; then
    # English
    echo "Installing required dependencies..."
    sudo apt update
    sudo apt install -y python3 python3-pip
    pip3 install requests

    # Prompt user for API token
    echo "Please enter your IPinfo API token (you can get it from https://ipinfo.io/signup):"
    read api_token

    # Update API token in the script
    sed -i "s/API_TOKEN = \"YOUR_API_TOKEN\"/API_TOKEN = \"$api_token\"/g" ip_query.py

    echo "Setup complete! Now you can run the script using the following commands:"
    echo "For interactive mode:"
    echo "python3 ip_query.py -l en"
    echo "For file input:"
    echo "python3 ip_query.py -f example_ips.txt -l en"
    echo "For more options, run: python3 ip_query.py --help"
else
    # 中文
    echo "正在安装所需的依赖..."
    sudo apt update
    sudo apt install -y python3 python3-pip
    pip3 install requests

    # 提示用户输入API令牌
    echo "请输入您的IPinfo API令牌（可以从 https://ipinfo.io/signup 获取）："
    read api_token

    # 更新脚本中的API令牌
    sed -i "s/API_TOKEN = \"YOUR_API_TOKEN\"/API_TOKEN = \"$api_token\"/g" ip_query.py

    echo "设置完成！现在您可以使用以下命令运行脚本："
    echo "交互式模式："
    echo "python3 ip_query.py"
    echo "文件输入模式："
    echo "python3 ip_query.py -f example_ips.txt"
    echo "更多选项，请运行: python3 ip_query.py --help"
fi