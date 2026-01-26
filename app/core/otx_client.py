import requests
import os
import re

def get_single_otx_resource(resource_type, indicator, api_key):
    """Consulta um único recurso no OTX e retorna o JSON."""
    url = f"https://otx.alienvault.com/api/v1/indicators/{resource_type}/{indicator}/general"
    headers = {"X-OTX-API-KEY": api_key, "User-Agent": "Zion-Monitor-V1"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

def get_otx_data(target, resolved_ip=None):
    """
    Realiza a soma cumulativa de Pulses:
    1. Domínio Raiz (ex: gov.br)
    2. Subdomínio WWW (ex: www.gov.br)
    3. IP da Infraestrutura (ex: 161.148.164.31)
    """
    api_key = os.getenv("OTX_API")
    if not api_key:
        return {"pulse_count": 0, "facts": [], "cves": []}

    total_pulses = 0
    all_data_text = ""
    
    # 1. Identifica se o alvo inicial é IP ou Domínio
    is_ip = all(c.isdigit() or c == '.' for c in target) and target.count('.') == 3
    
    # Lista de alvos para checagem cumulativa
    check_list = []
    if is_ip:
        check_list.append(("IPv4", target))
    else:
        check_list.append(("domain", target)) # Domínio Raiz
        if not target.startswith("www."):
            check_list.append(("domain", f"www.{target}")) # Variante WWW
        if resolved_ip:
            check_list.append(("IPv4", resolved_ip)) # IP da Infra

    # Executa as consultas e soma os resultados
    for r_type, indicator in check_list:
        data = get_single_otx_resource(r_type, indicator, api_key)
        if data:
            count = data.get('pulse_info', {}).get('count', 0)
            total_pulses += count
            all_data_text += str(data)

    # Extração de CVEs do bloco acumulado
    cve_pattern = re.compile(r'CVE-\d{4}-\d{4,}')
    found_cves = list(set(cve_pattern.findall(all_data_text)))

    return {
        "pulse_count": total_pulses,
        "facts": ["Cumulative Threat Analysis Enabled"] if total_pulses > 0 else [],
        "cves": found_cves if found_cves else ["N/A"]
    }
