import os
import sys
import uvicorn
import logging
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

if __name__ == "__main__":
    logger.info("ZION SYSTEM STARTING ON PORT 8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
