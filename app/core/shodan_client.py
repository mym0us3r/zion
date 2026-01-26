import requests

class ShodanClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.shodan.io/shodan/host"

    def get_facet_data(self, target, is_ip=False):
        if not self.api_key or target in ["Error", "127.0.0.1", "N/A"]:
            return self._empty_response()

        try:
            if is_ip:
                url = f"{self.base_url}/{target}?key={self.api_key}"
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    d = r.json()
                    return {
                        "top_ports": [{"key": str(p), "count": 1} for p in d.get('ports', [])][:5],
                        "top_orgs": [{"key": d.get('org', 'N/A'), "count": 1}],
                        "top_products": [{"key": "N/A", "count": 0}]
                    }
            else:
                facets = "port,org,product"
                params = {"key": self.api_key, "query": f"hostname:{target}", "facets": facets}
                r = requests.get("https://api.shodan.io/shodan/host/count", params=params, timeout=15)
                if r.status_code == 200:
                    f_data = r.json().get('facets', {})
                    return {
                        "top_ports": [{"key": str(x['value']), "count": x['count']} for x in f_data.get('port', [])[:5]],
                        "top_orgs": [{"key": x['value'], "count": x['count']} for x in f_data.get('org', [])[:5]],
                        "top_products": [{"key": x['value'], "count": x['count']} for x in f_data.get('product', [])[:5]]
                    }
            return self._empty_response()
        except Exception as e:
            print(f"❌ Shodan Error: {e}")
            return self._empty_response()

    def _empty_response(self):
        return {"top_ports": [], "top_orgs": [], "top_products": []}
