#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os
from datetime import datetime
import argparse

# IPinfo Lite API 配置
API_TOKEN = "YOUR_API_TOKEN"  # 请替换为您的API令牌
API_URL = "https://api.ipinfo.io/lite/"  # Lite API的URL
BATCH_SIZE = 100  # 批量查询的IP数量，IPinfo支持最多1000个IP的批量查询

# 语言设置
LANGUAGE = "zh"  # 默认语言：zh-中文，en-英文

def query_single_ip(ip):
    """查询单个IP地址的信息"""
    url = f"{API_URL}{ip}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            if LANGUAGE == "en":
                print(f"Failed to query IP {ip}: {response.status_code} - {response.text}")
            else:
                print(f"查询IP {ip} 失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        if LANGUAGE == "en":
            print(f"Error occurred while querying IP {ip}: {str(e)}")
        else:
            print(f"查询IP {ip} 时发生错误: {str(e)}")
        return None

def query_batch_ips(ip_list):
    """批量查询IP地址信息"""
    url = "https://api.ipinfo.io/batch"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 构建批量查询请求
    batch_urls = [f"lite/{ip}" for ip in ip_list]
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(batch_urls))
        if response.status_code == 200:
            return response.json()
        else:
            if LANGUAGE == "en":
                print(f"Batch query failed: {response.status_code} - {response.text}")
            else:
                print(f"批量查询失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        if LANGUAGE == "en":
            print(f"Error occurred during batch query: {str(e)}")
        else:
            print(f"批量查询时发生错误: {str(e)}")
        return None

def save_results_to_file(results, output_file):
    """将查询结果保存到文本文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        if LANGUAGE == "en":
            f.write(f"# IP Query Results - Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Format: IP | ASN | AS Name | AS Domain | Country Code | Country\n\n")
            header = "{:<15} | {:<10} | {:<30} | {:<30} | {:<12} | {:<15}\n"
            f.write(header.format("IP Address", "ASN", "AS Name", "AS Domain", "Country Code", "Country"))
            f.write("-" * 120 + "\n")
        else:
            f.write(f"# IP查询结果 - 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# 格式: IP | ASN | AS名称 | AS域名 | 国家代码 | 国家名称\n\n")
            header = "{:<15} | {:<10} | {:<30} | {:<30} | {:<12} | {:<15}\n"
            f.write(header.format("IP地址", "ASN", "AS名称", "AS域名", "国家代码", "国家名称"))
            f.write("-" * 120 + "\n")
        
        for ip, data in results.items():
            if data:
                # 提取所需字段，如果字段不存在则使用'N/A'
                asn = data.get('asn', 'N/A')
                as_name = data.get('as_name', 'N/A')
                as_domain = data.get('as_domain', 'N/A')
                country_code = data.get('country_code', 'N/A')
                country = data.get('country', 'N/A')
                
                # 写入文件 - 使用表格格式提高可读性
                row_format = "{:<15} | {:<10} | {:<30} | {:<30} | {:<12} | {:<15}\n"
                f.write(row_format.format(ip, asn, as_name[:30], as_domain[:30], country_code, country))
            else:
                if LANGUAGE == "en":
                    f.write(f"{ip:<15} | {'Query Failed':<100}\n")
                else:
                    f.write(f"{ip:<15} | {'查询失败':<100}\n")

def process_ip_file(input_file, output_file):
    """处理包含IP地址的输入文件"""
    # 读取IP地址列表
    try:
        with open(input_file, 'r') as f:
            ip_list = [line.strip() for line in f if line.strip()]
        
        if LANGUAGE == "en":
            print(f"Read {len(ip_list)} IP addresses from file {input_file}")
        else:
            print(f"从文件 {input_file} 中读取了 {len(ip_list)} 个IP地址")
        
        # 存储所有查询结果
        all_results = {}
        
        # 分批处理IP地址
        for i in range(0, len(ip_list), BATCH_SIZE):
            batch = ip_list[i:i+BATCH_SIZE]
            if LANGUAGE == "en":
                print(f"Querying batch {i//BATCH_SIZE + 1}, total {len(batch)} IP addresses...")
            else:
                print(f"正在查询第 {i//BATCH_SIZE + 1} 批，共 {len(batch)} 个IP地址...")
            
            # 批量查询
            batch_results = query_batch_ips(batch)
            
            if batch_results:
                all_results.update(batch_results)
            else:
                # 如果批量查询失败，尝试单个查询
                if LANGUAGE == "en":
                    print("Batch query failed, switching to single IP query mode...")
                else:
                    print("批量查询失败，切换到单个IP查询模式...")
                for ip in batch:
                    result = query_single_ip(ip)
                    if result:
                        all_results[ip] = result
                    else:
                        all_results[ip] = None
        
        # 保存结果到文件
        save_results_to_file(all_results, output_file)
        if LANGUAGE == "en":
            print(f"Query results saved to file: {output_file}")
        else:
            print(f"查询结果已保存到文件: {output_file}")
    except IOError as e:
        if LANGUAGE == "en":
            print(f"Error: Could not read file {input_file}. {str(e)}")
        else:
            print(f"错误: 无法读取文件 {input_file}。{str(e)}")
        return

def get_ip_input_from_user():
    """从用户输入获取IP地址列表"""
    if LANGUAGE == "en":
        print("Enter IP addresses to query, one per line, press Enter on an empty line to finish:")
    else:
        print("请输入要查询的IP地址，每行一个IP，输入空行结束：")
    ip_list = []
    while True:
        ip = input().strip()
        if not ip:
            break
        ip_list.append(ip)
    return ip_list

def process_user_input_ips(ip_list, output_file):
    """处理用户输入的IP地址列表"""
    if LANGUAGE == "en":
        print(f"You entered {len(ip_list)} IP addresses")
    else:
        print(f"您输入了 {len(ip_list)} 个IP地址")
    
    # 存储所有查询结果
    all_results = {}
    
    # 分批处理IP地址
    for i in range(0, len(ip_list), BATCH_SIZE):
        batch = ip_list[i:i+BATCH_SIZE]
        if LANGUAGE == "en":
            print(f"Querying batch {i//BATCH_SIZE + 1}, total {len(batch)} IP addresses...")
        else:
            print(f"正在查询第 {i//BATCH_SIZE + 1} 批，共 {len(batch)} 个IP地址...")
        
        # 批量查询
        batch_results = query_batch_ips(batch)
        
        if batch_results:
            all_results.update(batch_results)
        else:
            # 如果批量查询失败，尝试单个查询
            if LANGUAGE == "en":
                print("Batch query failed, switching to single IP query mode...")
            else:
                print("批量查询失败，切换到单个IP查询模式...")
            for ip in batch:
                result = query_single_ip(ip)
                if result:
                    all_results[ip] = result
                else:
                    all_results[ip] = None
    
    # 保存结果到文件
    save_results_to_file(all_results, output_file)
    if LANGUAGE == "en":
        print(f"Query results saved to file: {output_file}")
    else:
        print(f"查询结果已保存到文件: {output_file}")

def main():
    global LANGUAGE
    
    # 使用argparse解析命令行参数
    parser = argparse.ArgumentParser(description='IP信息查询工具 / IP Information Query Tool')
    parser.add_argument('-f', '--file', help='包含IP地址的文件路径 / File containing IP addresses')
    parser.add_argument('-o', '--output', default='ip_results.txt', help='结果输出文件 / Output file for results')
    parser.add_argument('-l', '--language', choices=['zh', 'en'], default='zh', help='语言选择 (zh-中文, en-英文) / Language selection (zh-Chinese, en-English)')
    args = parser.parse_args()
    
    # 设置语言
    LANGUAGE = args.language
    
    # 检查命令行参数
    if args.file:
        # 检查输入文件是否存在
        if not os.path.exists(args.file):
            if LANGUAGE == "en":
                print(f"Error: Input file {args.file} does not exist")
            else:
                print(f"错误: 输入文件 {args.file} 不存在")
            return
        # 处理IP文件
        process_ip_file(args.file, args.output)
    else:
        # 交互式模式
        if LANGUAGE == "en":
            print("Please select query mode:")
            print("1. Read IP addresses from file")
            print("2. Manually input IP addresses")
            mode = input("Enter option (1/2): ").strip()
            
            output_file = input("Enter filename to save results (default 'ip_results.txt'): ").strip() or "ip_results.txt"
        else:
            print("请选择查询模式：")
            print("1. 从文件读取IP地址")
            print("2. 手动输入IP地址")
            mode = input("请输入选项 (1/2): ").strip()
            
            output_file = input("请输入结果保存的文件名 (默认为'ip_results.txt'): ").strip() or "ip_results.txt"
        
        if mode == "1":
            if LANGUAGE == "en":
                input_file = input("Enter the path to the file containing IP addresses: ").strip()
            else:
                input_file = input("请输入包含IP地址的文件路径: ").strip()
            # 检查输入文件是否存在
            if not os.path.exists(input_file):
                if LANGUAGE == "en":
                    print(f"Error: Input file {input_file} does not exist")
                else:
                    print(f"错误: 输入文件 {input_file} 不存在")
                return
            # 处理IP文件
            process_ip_file(input_file, output_file)
        elif mode == "2":
            ip_list = get_ip_input_from_user()
            if not ip_list:
                if LANGUAGE == "en":
                    print("No IP addresses entered, exiting program")
                else:
                    print("未输入任何IP地址，退出程序")
                return
            process_user_input_ips(ip_list, output_file)
        else:
            if LANGUAGE == "en":
                print("Invalid option, exiting program")
            else:
                print("无效的选项，退出程序")
            return

if __name__ == "__main__":
    # 检查API令牌是否已设置
    if API_TOKEN == "YOUR_API_TOKEN":
        print("警告/Warning: 请在脚本中设置您的API令牌 / Please set your API token in the script")
        print("您可以在 https://ipinfo.io/signup 注册获取免费的API令牌 / You can register for a free API token at https://ipinfo.io/signup")
        sys.exit(1)
    
    main()