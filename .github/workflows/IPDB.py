import os
import requests
import zipfile
import re
import random
import base64
from datetime import datetime, timedelta

# 设置脚本工作目录
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# 获取环境变量中的GitHub token和文件下载链接
github_token = os.environ.get("ME_GITHUB_TOKEN", "")
ipdb_url = os.environ.get("IPDB", "")

def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)

def unzip_file(zip_filename, extract_folder):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

def merge_txt_files(folder_path, output_filename):
    with open(output_filename, 'w') as output_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.txt'):
                    with open(os.path.join(root, file), 'r') as input_file:
                        output_file.write(input_file.read())

def extract_ips_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', content)

def write_ips_to_file(ips, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for ip in ips:
            output_file.write(ip + '\n')

# 记录当前时间
start_time_str = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
print(f"\n{start_time_str} Downloading updated proxy IP library...")

# 下载并解压文件
download_file(ipdb_url, 'ipdb.zip')
unzip_file('ipdb.zip', 'ipdb')

# 合并文件并提取IP地址
merge_txt_files('ipdb', 'all_ips.txt')
ips = list(set(extract_ips_from_file('all_ips.txt')))
random.shuffle(ips)
write_ips_to_file(ips, 'proxy.txt')

# 上传文件到GitHub
with open('proxy.txt', "r") as file:
    proxy_txt_content = file.read()

proxy_txt_content_base64 = base64.b64encode(proxy_txt_content.encode()).decode()
get_sha_url = f"https://proxy.api.030101.xyz/https://api.github.com/repos/ymyuuu/IPDB/contents/proxy.txt"
headers = {"Authorization": f"token {github_token}"}
sha_response = requests.get(get_sha_url, headers=headers)

if sha_response.status_code == 200:
    current_sha = sha_response.json().get("sha", "")
    data = {
        "message": f"Update proxy.txt - {start_time_str} (Total IPs: {len(proxy_txt_content.splitlines())})",
        "content": proxy_txt_content_base64,
        "sha": current_sha,
    }
    upload_url = f"https://proxy.api.030101.xyz/https://api.github.com/repos/ymyuuu/IPDB/contents/proxy.txt"
    response = requests.put(upload_url, headers=headers, json=data)
    if response.status_code == 200:
        current_time_str = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{current_time_str} GitHub update successful for proxy.txt file!")
    else:
        print(f"Error uploading file, HTTP status code: {response.status_code}, Error: {response.text}")
else:
    print(f"Failed to get current proxy.txt SHA value: {sha_response.text}")

print(f"\nOther")

def get_ips(ip_type):
    try:
        resp = requests.post('https://api.hostmonit.com/get_optimization_ip', json={"key": "iDetkOys", "type": ip_type}).json()
        if isinstance(resp.get('info', []), list):
            return ','.join({item['ip'] for item in resp['info']})
        return ""
    except (requests.exceptions.RequestException, ValueError, KeyError):
        return ""

def update_dns_record(ip_type, name):
    ip_addresses = get_ips(ip_type)
    response = requests.get(f"http://dns.api.030101.xyz/upd?type={'a' if ip_type == 'v4' else 'aaaa'}&name={name}&ip={ip_addresses}")
    print(response.text)

update_dns_record("v4", "cf2dnsv4")
update_dns_record("v6", "cf2dnsv6")
