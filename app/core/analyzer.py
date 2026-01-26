import socket
import os
import requests
import sys
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from core.abuse_client import get_abuse_data
from core.vt_client import get_vt_data
from core.otx_client import get_otx_data

class AttackSurfaceAnalyzer:
    def __init__(self):
        self.config = Config

    def get_ipinfo_data(self, ip):
        try:
            # Adicionado parâmetro para forçar resposta detalhada se disponível
            url = f"https://ipinfo.io/{ip}?token={self.config.IPINFO_TOKEN}"
            res = requests.get(url, timeout=5).json()
            full_org = res.get("org", "N/A")
            
            # O IPInfo pode não retornar o nome completo por padrão em todas as instâncias.
            # Aqui garantimos que, se não houver o campo country_name, usamos um fallback 
            # ou o sistema tratará no frontend.
            return {
                "ip": res.get("ip", ip),
                "asn": full_org.split(" ")[0] if " " in full_org else "N/A",
                "as_name": " ".join(full_org.split(" ")[1:]) if " " in full_org else "N/A",
                "country_code": res.get("country", "N/A"),
                "country_name": res.get("country_name") or res.get("country", "N/A"), # Fallback
                "city": res.get("city", "N/A"),
                "loc": res.get("loc", "0,0")
            }
        except:
            return {"ip": ip, "asn": "N/A", "as_name": "N/A", "country_name": "N/A", "city": "N/A", "loc": "0,0"}

    async def full_scan(self, target):
        target = target.lower().strip()
        is_ip = re.match(r"^\d{1,3}(\.\d{1,3}){3}$", target)

        try:
            resolved_ip = target if is_ip else socket.gethostbyname(target)
        except:
            resolved_ip = target

        geo = self.get_ipinfo_data(resolved_ip)
        otx_res = get_otx_data(target, resolved_ip)
        ot_pulses = otx_res.get('pulse_count', 0)

        vt_res = get_vt_data(target)
        vt_hits = vt_res.get('malicious', 0)
        if vt_hits == 0 and not is_ip:
            vt_res_www = get_vt_data(f"www.{target}")
            vt_hits = max(vt_hits, vt_res_www.get('malicious', 0))
        if vt_hits == 0:
            vt_res_ip = get_vt_data(resolved_ip)
            vt_hits = max(vt_hits, vt_res_ip.get('malicious', 0))

        abuse_res = get_abuse_data(resolved_ip)
        abuse_score = abuse_res.get('abuseConfidenceScore', 0)

        verdict = "CLEAN"
        if vt_hits > 0 or abuse_score > 50:
            verdict = "MALICIOUS"
        elif abuse_score > 0 or ot_pulses > 0:
            verdict = "SUSPICIOUS"

        return {
            "target": target,
            "resolved_ip": resolved_ip,
            "status": "success",
            "verdict": verdict,
            "geo": geo,
            "recon": {
                "abuseipdb": {"score": abuse_score},
                "virustotal": {"hits": vt_hits},
                "otx": {"pulse_count": ot_pulses}
            }
        }
