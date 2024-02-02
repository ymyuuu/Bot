import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

def get_ip_info(ip, session, output_path, asn_set):
    try:
        response = session.get(f"https://ipinfo.io/{ip}?token=6683ed526c919a", timeout=1)
        data = response.json()

        asn_match = re.match(r"AS(\d+)", data.get('org', 'N/A'))
        asn = asn_match.group(1) if asn_match else 'N/A'
        
        with open(os.path.join(output_path, f"ASN{asn}.txt"), 'a') as file:
            file.write(f"{ip}\n")

        asn_set.add(asn)
        
    except requests.RequestException:
        pass

def send_to_telegram(file_path):
    with open(file_path, 'rb') as file:
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendDocument", files={'document': file}, params={'chat_id': chat_id})

def clear_files():
    [os.remove(os.path.join(output_path, filename)) for filename in os.listdir(output_path) if filename.startswith(("ASN", "Best")) and filename.endswith(".txt")]

def send_notification(message_text):
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", params={'chat_id': chat_id, 'text': message_text, 'parse_mode': 'Markdown'})

proxy_url = "https://ipdb.api.030101.xyz/?type=proxy"
best_proxy_url = "https://ipdb.api.030101.xyz/?type=bestproxy"
best_cf_url = "https://ipdb.api.030101.xyz/?type=bestcf"
bot_token = os.environ.get('BOT_TOKEN')  # Read from environment variable
chat_id = os.environ.get('CHAT_ID')      # Read from environment variable

output_path = os.path.dirname(os.path.realpath(__file__))

try:
    start_time = datetime.now() + timedelta(hours=8)  # Add 8 hours for Beijing time
    send_notification(f"Scan start at *{start_time:%Y-%m-%d %H:%M}*")
    print(f"Scan start at {start_time:%Y-%m-%d %H:%M}")

    clear_files()

    unique_asns = set()
    proxy_data = requests.get(proxy_url).text.strip().split('\n')

    with requests.Session() as session, ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda ip: get_ip_info(ip, session, output_path, unique_asns), proxy_data)
    
    best_proxy_data = requests.get(best_proxy_url).text.strip().split('\n')
    with open(os.path.join(output_path, "BestProxy.txt"), 'w') as best_proxy_file:
        best_proxy_file.write("\n".join(best_proxy_data))

    best_cf_data = requests.get(best_cf_url).text.strip().split('\n')
    with open(os.path.join(output_path, "BestCF.txt"), 'w') as best_cf_file:
        best_cf_file.write("\n".join(best_cf_data))
        best_cf_file.write("\nBestCF.txt is ok")  # Add the description text

    [send_to_telegram(os.path.join(output_path, filename)) for filename in os.listdir(output_path) if filename.startswith(("ASN", "Best")) and filename.endswith(".txt")]

    end_time = datetime.now() + timedelta(hours=8)  # Add 8 hours for Beijing time
    duration = (end_time - start_time).total_seconds()
    send_notification(f"Scan over at *{end_time:%Y-%m-%d %H:%M}*\nIPs: {len(proxy_data)}, ASNs: {len(unique_asns)}, Lasted for {duration:.2f}s")
    print(f"Scan over at {end_time:%Y-%m-%d %H:%M}")
    send_to_telegram(os.path.join(output_path, "BestProxy.txt"))
    send_to_telegram(os.path.join(output_path, "BestCF.txt"))

except requests.RequestException:
    pass
