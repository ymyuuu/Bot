import os
import requests
import zipfile
import re
import base64
from datetime import datetime, timedelta

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

download_url = os.environ.get("IPDB", "")
zip_file_name = "data.zip"
proxy_txt_file_name = "proxy.txt"  # 修改文件名为 proxy.txt

username = "ymyuuu"
repo_name = "IPDB"
token = os.environ.get("ME_GITHUB_TOKEN", "")

start_time = datetime.now() + timedelta(hours=8)

start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
print(f"\n{start_time_str} Downloading updated proxy IP library...\n")

try:
    response = requests.get(download_url)
    response.raise_for_status()
    with open(zip_file_name, "wb") as zip_file:
        zip_file.write(response.content)
except requests.exceptions.RequestException as e:
    print(f"Error downloading ZIP file: {str(e)}")
    exit()

try:
    with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
        zip_ref.extractall("data_folder")
except Exception as e:
    print(f"Error extracting ZIP file: {str(e)}")
    exit()

ip_set = set()
ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

for root, _, files in os.walk("data_folder"):
    for file in files:
        if file.endswith(".txt"):
            try:
                with open(os.path.join(root, file), "r") as txt_file:
                    for line in txt_file:
                        line = line.strip()
                        if line:
                            matched_ips = ip_pattern.findall(line)
                            for ip in matched_ips:
                                parts = ip.split('.')
                                valid_ip = all(0 <= int(part) <= 255 for part in parts)
                                if valid_ip:
                                    ip_set.add(ip)
            except Exception as e:
                print(f"Error reading and merging txt files: {str(e)}")

try:
    with open(proxy_txt_file_name, "w") as new_proxy_file:  # 修改文件名为 proxy.txt
        for ip in sorted(ip_set, key=lambda x: [int(part) for part in x.split('.')]):
            new_proxy_file.write(ip + '\n')
except Exception as e:
    print(f"Error saving new proxy records: {str(e)}")

try:
    with open(proxy_txt_file_name, "r") as file:  # 修改文件名为 proxy.txt
        proxy_txt_content = file.read()

    proxy_txt_content_base64 = base64.b64encode(proxy_txt_content.encode()).decode()

    get_sha_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{proxy_txt_file_name}"  # 修改文件名为 proxy.txt
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

        upload_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{proxy_txt_file_name}"  # 修改文件名为 proxy.txt

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
