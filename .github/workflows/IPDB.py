import os
import requests
import zipfile
import re
import random
import base64
from datetime import datetime, timedelta

script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)

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
        raise RuntimeError(f'Error downloading {url}: {e}')

def unzip_file(zip_filename, extract_folder):
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
    except Exception as e:
        raise RuntimeError(f'Error unzipping {zip_filename}: {e}')

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
        raise RuntimeError(f'Error merging files: {e}')

def extract_ips_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', content)
            return ips
    except Exception as e:
        raise RuntimeError(f'Error extracting IP addresses: {e}')

def write_ips_to_file(ips, output_file_path):
    try:
        with open(output_file_path, 'w') as output_file:
            for ip in ips:
                output_file.write(ip + '\n')
    except Exception as e:
        raise RuntimeError(f'Error writing to file: {e}')

start_time = datetime.now() + timedelta(hours=8)
start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
print(f"\n{start_time_str} Downloading updated proxy IP library...")

url1 = ipdb_url
filename1 = '1.zip'
try:
    download_file(url1, filename1)
except RuntimeError as e:
    print(e)
    exit(1)

extract_folder1 = '1'
try:
    unzip_file(filename1, extract_folder1)
except RuntimeError as e:
    print(e)
    exit(1)

url2 = other_url
filename2 = '2.zip'
try:
    download_file(url2, filename2)
except RuntimeError as e:
    print(e)
    exit(1)

extract_folder2 = '2'
try:
    unzip_file(filename2, extract_folder2)
except RuntimeError as e:
    print(e)
    exit(1)

cloudflare_folder_path = os.path.join(extract_folder2, 'cloudflare-better-ip-main', 'cloudflare')

try:
    merge_txt_files('1', 'all1.txt')
except RuntimeError as e:
    print(e)
    exit(1)

try:
    merge_txt_files(cloudflare_folder_path, 'all2.txt')
except RuntimeError as e:
    print(e)
    exit(1)

try:
    ips_all1 = list(set(extract_ips_from_file('all1.txt')))
except RuntimeError as e:
    print(e)
    exit(1)

try:
    ips_all2 = list(set(extract_ips_from_file('all2.txt')))
except RuntimeError as e:
    print(e)
    exit(1)

all_ips = ips_all1 + ips_all2

random.shuffle(all_ips)

try:
    write_ips_to_file(all_ips, 'proxy.txt')
except RuntimeError as e:
    print(e)
    exit(1)

proxy_txt_file_path = "proxy.txt"
username = "ymyuuu"
repo_name = "IPDB"

try:
    with open(proxy_txt_file_path, "r") as file:
        proxy_txt_content = file.read()

    proxy_txt_content_base64 = base64.b64encode(proxy_txt_content.encode()).decode()

    get_sha_url = f"https://proxy.api.030101.xyz/https://api.github.com/repos/{username}/{repo_name}/contents/proxy.txt"
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

        upload_url = f"https://proxy.api.030101.xyz/https://api.github.com/repos/{username}/{repo_name}/contents/proxy.txt"
        response = requests.put(upload_url, headers=headers, json=data)

        if response.status_code == 200:
            current_time_str = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{current_time_str} GitHub update successful for proxy.txt file!")
        else:
            print(f"Error uploading file, HTTP status code: {response.status_code}, Error: {response.text}")
            exit(1)
    else:
        print(f"Failed to get current proxy.txt SHA value: {sha_response.text}")
        exit(1)

except Exception as e:
    print(f"Error uploading file to GitHub: {str(e)}")
    exit(1)
# https://chat.openai.com/share/1688b20a-8734-4582-b641-2e285841d35d

# other
print(f"\nOther")

def get_ips(ip_type):
    resp = requests.post('https://api.hostmonit.com/get_optimization_ip', json={"key": "iDetkOys", "type": ip_type}).json()
    return ','.join({item['ip'] for item in resp.get('info', [])})

def update_dns_record(ip_type, name):
    ip_addresses = get_ips(ip_type)
    print(ip_addresses)  # 输出IP地址
    response = requests.get(f"http://dns.api.030101.xyz/upd?type={'a' if ip_type == 'v4' else 'aaaa'}&name={name}&ip={ip_addresses}")
    print(response.text)

update_dns_record("v4", "cf2dnsv4")
update_dns_record("v6", "cf2dnsv6")
