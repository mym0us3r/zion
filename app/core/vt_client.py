import requests
import os

def get_vt_data(ip):
    api_key = os.getenv("VT_API")
    if not api_key: return None
    
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            stats = response.json()['data']['attributes']['last_analysis_stats']
            return {
                "malicious": stats.get('malicious', 0),
                "suspicious": stats.get('suspicious', 0),
                "undetected": stats.get('undetected', 0)
            }
    except:
        pass
    return {"malicious": 0}
