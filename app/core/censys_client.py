import requests
import os
from typing import Optional, Dict, Any

def get_censys_data(ip: str) -> Optional[Dict[str, Any]]:
    """Busca informações no Censys v3 Platform API"""
    token = os.getenv("CENSYS_API_TOKEN")
    if not token:
        return None

    # URL da API v3 conforme sua pesquisa
    url = f"https://api.platform.censys.io/v3/global/asset/host/{ip}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.censys.api.v3.host.v1+json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            resource = data.get('result', {}).get('resource', {})
            
            # Formata para o padrão esperado pelo ZION
            return {
                "organization": resource.get('autonomous_system', {}).get('name', 'N/A'),
                "asn": resource.get('autonomous_system', {}).get('asn', 'N/A'),
                "services_count": len(resource.get('services', [])),
                "location": resource.get('location', {}),
                "dns_names": resource.get('dns', {}).get('names', [])
            }
        else:
            print(f"[CENSYS] Erro {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"[CENSYS] Erro de conexão: {str(e)}")
        return None
