@echo off
setlocal enabledelayedexpansion

echo 请选择语言 / Please select language:
echo 1. 中文 (Chinese)
echo 2. English
set /p lang_choice=选择 / Choice (1/2): 

if "%lang_choice%"=="2" (
    set LANG=en
    echo IP Information Batch Query Tool
    echo ============================

    REM Check if Python is installed
    python --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo Error: Python not detected, please install Python 3 first
        echo You can download and install Python from https://www.python.org/downloads/
        pause
        exit /b
    )

    REM Check if requests library is installed
    pip show requests >nul 2>&1
    if !errorlevel! neq 0 (
        echo Installing requests library...
        pip install requests
        if !errorlevel! neq 0 (
            echo Failed to install requests library, please run manually: pip install requests
            pause
            exit /b
        )
    )

    REM Check if API token is set
    findstr /C:"API_TOKEN = \"YOUR_API_TOKEN\"" ip_query.py >nul
    if !errorlevel! equ 0 (
        echo Please set your API token first
        echo You can register for a free API token at https://ipinfo.io/signup
        echo Then edit the ip_query.py file and replace the API_TOKEN variable value with your token
        pause
        exit /b
    )

    echo Starting IP query tool...
    python ip_query.py -l en

    if !errorlevel! equ 0 (
        echo Query completed! Results have been saved to ip_results.txt
        echo Do you want to view the results? (Y/N)
        set /p view=
        if /i "!view!"=="Y" (
            type ip_results.txt
        )
    )
) else (
    set LANG=zh
    echo IP信息批量查询工具
    echo ==================

    REM 检查Python是否已安装
    python --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo 错误: 未检测到Python，请先安装Python 3
        echo 您可以从 https://www.python.org/downloads/ 下载并安装Python
        pause
        exit /b
    )

    REM 检查requests库是否已安装
    pip show requests >nul 2>&1
    if !errorlevel! neq 0 (
        echo 正在安装requests库...
        pip install requests
        if !errorlevel! neq 0 (
            echo 安装requests库失败，请手动运行: pip install requests
            pause
            exit /b
        )
    )

    REM 检查API令牌是否已设置
    findstr /C:"API_TOKEN = \"YOUR_API_TOKEN\"" ip_query.py >nul
    if !errorlevel! equ 0 (
        echo 请先设置您的API令牌
        echo 您可以在 https://ipinfo.io/signup 注册获取免费的API令牌
        echo 然后编辑ip_query.py文件，将API_TOKEN变量的值替换为您的令牌
        pause
        exit /b
    )

    echo 正在启动IP查询工具...
    python ip_query.py -l zh

    if !errorlevel! equ 0 (
        echo 查询完成！结果已保存到ip_results.txt
        echo 是否要查看结果？(Y/N)
        set /p view=
        if /i "!view!"=="Y" (
            type ip_results.txt
        )
    )
)

pause