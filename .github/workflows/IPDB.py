import os
import requests
import zipfile
import re
import random
import base64
from datetime import datetime, timedelta

# 设置当前工作目录为脚本所在的路径
script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)

# 获取 GitHub secrets
github_token = os.environ.get("ME_GITHUB_TOKEN", "")
ipdb_url = os.environ.get("IPDB", "")
other_url = os.environ.get("OTHER", "")
other2_url = "https://ipdb.api.030101.xyz/other2"

def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'{url} 下载成功，保存为 {filename}')
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'下载 {url} 时发生错误: {e}')

def unzip_file(zip_filename, extract_folder):
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        print(f'{zip_filename} 解压完成，保存到 {extract_folder}')
    except Exception as e:
        raise RuntimeError(f'解压 {zip_filename} 时发生错误: {e}')

def merge_txt_files(folder_path, output_filename):
    try:
        with open(output_filename, 'w') as output_file:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.txt') or file.endswith('.csv'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as input_file:
                            output_file.write(input_file.read())
        print(f'{folder_path} 内的所有txt和csv文件已合并为 {output_filename}')
    except Exception as e:
        raise RuntimeError(f'合并文件时发生错误: {e}')

def extract_ips_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # 使用正则表达式提取IP地址
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', content)
            return ips
    except Exception as e:
        raise RuntimeError(f'提取IP地址时发生错误: {e}')

def write_ips_to_file(ips, output_file_path):
    try:
        with open(output_file_path, 'w') as output_file:
            for ip in ips:
                output_file.write(ip + '\n')
        print(f'所有IP地址已提取并保存到 {output_file_path}，随机打乱完成')
    except Exception as e:
        raise RuntimeError(f'写入文件时发生错误: {e}')

# 获取当前时间
start_time = datetime.now() + timedelta(hours=8)
start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
print(f"\n{start_time_str} 正在下载更新的代理IP库...\n")

# 下载链接 1 的文件，并命名为 1.zip
url1 = ipdb_url
filename1 = '1.zip'
try:
    download_file(url1, filename1)
except RuntimeError as e:
    print(e)
    exit(1)

# 解压 1.zip 到文件夹 1
extract_folder1 = '1'
try:
    unzip_file(filename1, extract_folder1)
except RuntimeError as e:
    print(e)
    exit(1)

# 下载链接 2 的文件，并命名为 2.zip
url2 = other_url
filename2 = '2.zip'
try:
    download_file(url2, filename2)
except RuntimeError as e:
    print(e)
    exit(1)

# 解压 2.zip 到文件夹 2
extract_folder2 = '2'
try:
    unzip_file(filename2, extract_folder2)
except RuntimeError as e:
    print(e)
    exit(1)

# 下载链接 3 的文件，并命名为 3.zip
url3 = other2_url
filename3 = '3.zip'
try:
    download_file(url3, filename3)
except RuntimeError as e:
    print(e)
    exit(1)

# 解压 3.zip 到文件夹 3
extract_folder3 = '3'
try:
    unzip_file(filename3, extract_folder3)
except RuntimeError as e:
    print(e)
    exit(1)

# 合并1文件夹里的所有txt文件为all1.txt
try:
    merge_txt_files('1', 'all1.txt')
except RuntimeError as e:
    print(e)
    exit(1)

# 合并2文件夹里cloudflare文件夹中的所有txt文件为all2.txt
try:
    merge_txt_files(os.path.join(extract_folder2, 'cloudflare-better-ip-main', 'cloudflare'), 'all2.txt')
except RuntimeError as e:
    print(e)
    exit(1)

# 合并3文件夹里的所有txt和csv文件为all3.txt
try:
    merge_txt_files('3', 'all3.txt')
except RuntimeError as e:
    print(e)
    exit(1)

# 提取all1.txt中的IP地址，并去重
try:
    ips_all1 = list(set(extract_ips_from_file('all1.txt')))
except RuntimeError as e:
    print(e)
    exit(1)

# 提取all2.txt中的IP地址，并去重
try:
    ips_all2 = list(set(extract_ips_from_file('all2.txt')))
except RuntimeError as e:
    print(e)
    exit(1)

# 提取all3.txt中的IP地址，并去重
try:
    ips_all3 = list(set(extract_ips_from_file('all3.txt')))
except RuntimeError as e:
    print(e)
    exit(1)

# 合并三个列表中的IP地址
all_ips = ips_all1 + ips_all2 + ips_all3

# 随机打乱IP地址
random.shuffle(all_ips)

# 输出到proxy.txt
try:
    write_ips_to_file(all_ips, 'proxy.txt')
except RuntimeError as e:
    print(e)
    exit(1)

# GitHub上传代码
proxy_txt_file_path = "proxy.txt"
username = "ymyuuu"
repo_name = "IPDB"
start_time = datetime.now() + timedelta(hours=8)
start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
print(f"\n{start_time_str} 正在上传代理IP文件至GitHub...\n")

try:
    with open(proxy_txt_file_path, "r") as file:
        proxy_txt_content = file.read()

    proxy_txt_content_base64 = base64.b64encode(proxy_txt_content.encode()).decode()

    get_sha_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/proxy.txt"
    headers = {
        "Authorization": f"token {github_token}",
    }
    sha_response = requests.get(get_sha_url, headers=headers)

    if sha_response.status_code == 200:
        current_sha = sha_response.json().get("sha", "")
        data = {
            "message": f"Update proxy.txt - {start_time_str} (Total IPs: {len(proxy_txt_content.splitlines())})",
            "content": proxy_txt_content_base64,
            "sha": current_sha,
        }

        upload_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/proxy.txt"
        response = requests.put(upload_url, headers=headers, json=data)

        if response.status_code == 200:
            current_time_str = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{current_time_str} GitHub上proxy.txt文件更新成功!")
        else:
            print(f"Error uploading file, HTTP status code: {response.status_code}, Error: {response.text}")
            exit(1)
    else:
        print(f"Failed to get current proxy.txt SHA value: {sha_response.text}")
        exit(1)

except Exception as e:
    print(f"Error uploading file to GitHub: {str(e)}")
    exit(1)
