import os
from dotenv import load_dotenv

# Carrega o .env do caminho absoluto
load_dotenv(dotenv_path="/opt/ZION/.env")

class Config:
    SHODAN_API = os.getenv("SHODAN_API", "")
    VT_API = os.getenv("VT_API", "")
    ABUSE_API = os.getenv("ABUSE_API", "")
    OTX_API = os.getenv("OTX_API", "")
    # Nova entrada para IPinfo
    IPINFO_TOKEN = os.getenv("IPINFO_TOKEN", "")

    @classmethod
    def validate(cls):
        """Valida as chaves e imprime o status no terminal"""
        keys_to_check = [
            "SHODAN_API", 
            "VT_API", 
            "ABUSE_API", 
            "OTX_API", 
            "IPINFO_TOKEN"
        ]

        print("\n--- ZION SYSTEM: KEY VALIDATION ---")
        for key in keys_to_check:
            value = getattr(cls, key, "")
            if not value:
                print(f"⚠️ ZION CONFIG: Chave {key} não encontrada no .env")
            else:
                # Exibe apenas os primeiros 4 caracteres por segurança
                print(f"✅ ZION CONFIG: Chave {key} carregada (Início: {str(value)[:4]}...)")
        print("-----------------------------------\n")

# Executa a validação ao carregar o arquivo
Config.validate()
