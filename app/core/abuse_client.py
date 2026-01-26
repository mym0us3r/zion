import requests
import os

def get_abuse_data(ip: str) -> dict:
    """Retorna o JSON completo do AbuseIPDB para o analyzer."""
    api_key = os.getenv("ABUSE_API")
    if not api_key:
        return {}

    url = 'https://api.abuseipdb.com/api/v2/check'
    params = {'ipAddress': ip, 'maxAgeInDays': '90'}
    headers = {'Accept': 'application/json', 'Key': api_key}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('data', {})
        return {}
    except:
        return {}

def get_abuse_score(ip: str) -> int:
    """Extrai apenas o score para o main.py não quebrar."""
    data = get_abuse_data(ip)
    return data.get('abuseConfidenceScore', 0)
