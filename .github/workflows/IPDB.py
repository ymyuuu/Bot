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

def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f'Error downloading {url}: {e}')

def unzip_file(zip_filename, extract_folder):
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
    except Exception as e:
        print(f'Error unzipping {zip_filename}: {e}')

def merge_txt_files(folder_path, output_filename):
    try:
        with open(output_filename, 'w') as output_file:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as input_file:
                            output_file.write(input_file.read())
    except Exception as e:
        print(f'Error merging files: {e}')

def extract_ips_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # 使用正则表达式提取IP地址
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', content)
            return ips
    except Exception as e:
        print(f'Error extracting IP addresses: {e}')
        return []

def write_ips_to_file(ips, output_file_path):
    try:
        with open(output_file_path, 'w') as output_file:
            for ip in ips:
                output_file.write(ip + '\n')
    except Exception as e:
        print(f'Error writing to file: {e}')

# 获取当前时间
start_time = datetime.now() + timedelta(hours=8)
start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
# print(f"\n{start_time_str} 正在下载更新的代理IP库...\n")
print(f"\n{start_time_str} Downloading updated proxy IP library...\n")


# 下载链接 1 的文件，并命名为 1.zip
url1 = ipdb_url
filename1 = '1.zip'
download_file(url1, filename1)

# 解压 1.zip 到文件夹 1
extract_folder1 = '1'
unzip_file(filename1, extract_folder1)

# 下载链接 2 的文件，并命名为 2.zip
url2 = other_url
filename2 = '2.zip'
download_file(url2, filename2)

# 解压 2.zip 到文件夹 2
extract_folder2 = '2'
unzip_file(filename2, extract_folder2)

# 找到2文件夹里cloudflare-better-ip-main文件夹下的cloudflare文件夹
cloudflare_folder_path = os.path.join(extract_folder2, 'cloudflare-better-ip-main', 'cloudflare')

# 合并1文件夹里的所有txt文件为all1.txt
merge_txt_files('1', 'all1.txt')

# 合并2文件夹里cloudflare文件夹中的所有txt文件为all2.txt
merge_txt_files(cloudflare_folder_path, 'all2.txt')

# 提取all1.txt中的IP地址，并去重
ips_all1 = list(set(extract_ips_from_file('all1.txt')))

# 提取all2.txt中的IP地址，并去重
ips_all2 = list(set(extract_ips_from_file('all2.txt')))

# 合并两个列表中的IP地址
all_ips = ips_all1 + ips_all2

# 随机打乱IP地址
random.shuffle(all_ips)

# 输出到proxy.txt
write_ips_to_file(all_ips, 'proxy.txt')

# GitHub上传代码
proxy_txt_file_path = "proxy.txt"
username = "ymyuuu"
repo_name = "IPDB"

try:
    with open(proxy_txt_file_name, "r") as file:  # 修改文件名为 proxy.txt
        proxy_txt_content = file.read()

    proxy_txt_content_base64 = base64.b64encode(proxy_txt_content.encode()).decode()

    get_sha_url = f"https://proxy.api.030101.xyz/https://api.github.com/repos/{username}/{repo_name}/contents/{proxy_txt_file_name}"  # 修改文件名为 proxy.txt
    headers = {
        "Authorization": f"token {token}",
    }
    sha_response = requests.get(get_sha_url, headers=headers)

    if sha_response.status_code == 200:
        current_sha = sha_response.json().get("sha", "")
        data = {
            "message": f"Updated {proxy_txt_file_name} - {start_time_str} (Total IPs: {len(ip_set)})",
            "content": proxy_txt_content_base64,
            "sha": current_sha,
        }

        upload_url = f"https://proxy.api.030101.xyz/https://api.github.com/repos/{username}/{repo_name}/contents/{proxy_txt_file_name}"  # 修改文件名为 proxy.txt

        response = requests.put(upload_url, headers=headers, json=data)

        if response.status_code == 200:
            current_time_str = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{current_time_str} Successfully updated {proxy_txt_file_name} file on GitHub!")
        else:
            print(f"Failed to upload file, HTTP status code: {response.status_code}, Error: {response.text}")
    else:
        print(f"Failed to get current {proxy_txt_file_name}'s SHA: {sha_response.text}")

except Exception as e:
    print(f"Error uploading file to GitHub: {str(e)}")
