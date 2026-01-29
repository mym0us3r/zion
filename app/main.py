import os
import sys
import uvicorn
import logging
import ipaddress
from urllib.parse import urlparse
import httpx
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ZION-CORE")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.analyzer import AttackSurfaceAnalyzer
from app.core.ransomware_client import RansomwareLiveClient
from app.core.phishstats_client import phish_stats_monitor

app = FastAPI(title="ZION - External Attack Surface")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

analyzer = AttackSurfaceAnalyzer()
ransom_client = RansomwareLiveClient()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/check")
async def check_target(ipAddress: str = Query(...)):
    try:
        # A análise interna usa a inteligência de IP, mas o frontend cuidará dos links
        return await analyzer.full_scan(ipAddress)
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        return {"error": str(e), "status": "failed"}

@app.get("/api/ransomware-stats")
async def get_ransomware_stats():
    stats = await ransom_client.get_global_stats()
    return stats if stats else {"groups": 313, "victims_this_year": 481, "total_victims": 25126}

@app.get("/api/phishing-stats")
async def get_phishing_stats():
    try:
        stats = await phish_stats_monitor.get_stats()
        if stats and stats.get("top_ips"):
            return {
                "top_ips": stats["top_ips"],
                "top_hosts": stats["top_hosts"]
            }
        return {
            "top_ips": ["186.225.21.10", "177.105.14.2", "191.243.55.8", "201.48.11.90"],
            "top_hosts": ["TELEFONICA-BR", "CLARO-BR", "INTERNET-PF", "ALGAR-BR"]
        }
    except Exception:
        return {"top_ips": ["OFFLINE"], "top_hosts": ["OFFLINE"]}

def _normalize_target(raw_target: str) -> str:
    target = (raw_target or "").strip()
    if "://" in target:
        parsed = urlparse(target)
        target = parsed.netloc or parsed.path
    if "/" in target:
        target = target.split("/")[0]
    if ":" in target:
        target = target.split(":")[0]
    return target

def _is_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False

@app.get("/api/rdap")
async def rdap_lookup(target: str = Query(...)):
    normalized = _normalize_target(target)
    if not normalized:
        return {"error": "invalid_target"}

    query_type = "ip" if _is_ip(normalized) else "domain"
    rdap_url = f"https://rdap.org/{query_type}/{normalized}"

    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            response = await client.get(rdap_url, headers={"accept": "application/json"})
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        logger.error(f"RDAP lookup failed: {e}")
        return {"error": "rdap_lookup_failed", "query": normalized, "type": query_type}

    summary = {
        "name": data.get("name"),
        "handle": data.get("handle"),
        "country": data.get("country"),
        "status": data.get("status"),
        "startAddress": data.get("startAddress"),
        "endAddress": data.get("endAddress"),
        "ldhName": data.get("ldhName"),
        "entities": []
    }

    for ent in data.get("entities", []):
        roles = ent.get("roles") or []
        vcard = ent.get("vcardArray")
        org = None
        if vcard and isinstance(vcard, list) and len(vcard) > 1:
            for item in vcard[1]:
                if item and item[0] == "fn":
                    org = item[3]
                    break
        summary["entities"].append({
            "handle": ent.get("handle"),
            "roles": roles,
            "name": org
        })

    return {
        "query": normalized,
        "type": query_type,
        "source": "rdap.org",
        "summary": summary,
        "raw": data
    }

if __name__ == "__main__":
    logger.info("ZION SYSTEM STARTING ON PORT 8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
