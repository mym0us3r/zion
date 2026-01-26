import httpx
import asyncio

class RansomwareLiveClient:
    def __init__(self):
        self.url = "https://api.ransomware.live/v2/stats"
        # Headers para simular um navegador e evitar bloqueios
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # Dados iniciais de segurança (Fallback)
        self.cache = {
            "groups": 313,
            "victims_this_year": 481,
            "total_victims": 25126
        }

    async def get_global_stats(self):
        try:
            async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
                response = await client.get(self.url)
                
                if response.status_code == 200:
                    data = response.json()
                    self.cache = {
                        "groups": data.get("groups", self.cache["groups"]),
                        "victims_this_year": data.get("victims_this_year", self.cache["victims_this_year"]),
                        "total_victims": data.get("total_victims", self.cache["total_victims"])
                    }
                else:
                    print(f"[!] Ransomware.live instável (Status {response.status_code}). Usando Cache.")
                    
                return self.cache
        except Exception as e:
            # Em caso de erro (como o que vimos no log), o sistema não para, ele retorna o cache
            print(f"[!] Erro silencioso tratado: {e}")
            return self.cache
