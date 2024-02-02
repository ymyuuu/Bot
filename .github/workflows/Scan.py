import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

def get_ip_info(ip, session, output_path, asn_set):
    try:
        response = session.get(f"https://ipinfo.io/{ip}?token=8bedced47027a8", timeout=1)
        data = response.json()

        asn_match = re.match(r"AS(\d+)", data.get('org', 'N/A'))
        asn = asn_match.group(1) if asn_match else 'N/A'
        
        with open(os.path.join(output_path, f"ASN{asn}.txt"), 'a') as file:
            file.write(f"{ip}\n")

        asn_set.add(asn)
        
    except requests.RequestException:
        pass

def send_to_telegram(file_path, additional_text=None, parse_mode='MarkdownV2'):
    with open(file_path, 'rb') as file:
        files = {'document': (file_path, file, 'rb')}

        data = {'chat_id': chat_id, 'parse_mode': parse_mode}
        if additional_text:
            data['caption'] = additional_text

        requests.post(f"https://api.telegram.org/bot{bot_token}/sendDocument", files=files, data=data)

def clear_files():
    [os.remove(os.path.join(output_path, filename)) for filename in os.listdir(output_path) if filename.startswith(("ASN", "Best")) and filename.endswith(".txt")]

def send_notification(message_text, parse_mode='MarkdownV2'):
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", params={'chat_id': chat_id, 'text': message_text, 'parse_mode': parse_mode})

def scan_and_send_files(url, filename_prefix, additional_text=None, parse_mode='MarkdownV2'):
    data = requests.get(url).text.strip()
    with open(os.path.join(output_path, f"{filename_prefix}.txt"), 'w') as file:
        file.write(data)
    send_to_telegram(os.path.join(output_path, f"{filename_prefix}.txt"), additional_text=additional_text, parse_mode=parse_mode)

proxy_url = "https://ipdb.api.030101.xyz/?type=proxy"
best_proxy_url = "https://ipdb.api.030101.xyz/?type=bestproxy"
best_cf_url = "https://ipdb.api.030101.xyz/?type=bestcf"
bot_token = os.environ.get('BOT_TOKEN')  # Read from environment variable
chat_id = os.environ.get('CHAT_ID')      # Read from environment variable

output_path = os.path.dirname(os.path.realpath(__file__))

try:
    start_time = datetime.now() + timedelta(hours=8)  # Add 8 hours for Beijing time
    send_notification(f"Scan *start* at *{start_time:%Y-%m-%d %H:%M}*", parse_mode='Markdown')
    print(f"Scan start at {start_time:%Y-%m-%d %H:%M}")

    clear_files()

    unique_asns = set()
    proxy_data = requests.get(proxy_url).text.strip().split('\n')

    with requests.Session() as session, ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda ip: get_ip_info(ip, session, output_path, unique_asns), proxy_data)

    for asn in unique_asns:
        send_to_telegram(os.path.join(output_path, f"ASN{asn}.txt"))

    scan_and_send_files(best_cf_url, "BestCF", additional_text="`bestcf.onecf.eu.org`", parse_mode='MarkdownV2')
    scan_and_send_files(best_proxy_url, "BestProxy", additional_text="`bestproxy.onecf.eu.org`", parse_mode='MarkdownV2')

    end_time = datetime.now() + timedelta(hours=8)
    duration = (end_time - start_time).total_seconds()
    scan_message = f"Scan *over* at **{end_time:%Y-%m-%d %H:%M}**\nIPs: {len(proxy_data)}, ASNs: {len(unique_asns)}, Lasted for {duration:.2f}s\n[API](https://api.030101.xyz?disable_web_page_preview=true)\n[GitHub](https://github.com/ymyuuu?disable_web_page_preview=true)\n[Blog](https://onecn.eu.org?disable_web_page_preview=true)"
    send_notification(scan_message, parse_mode='Markdown')
    print(f"Scan over at {end_time:%Y-%m-%d %H:%M}")

except requests.RequestException:
    pass
