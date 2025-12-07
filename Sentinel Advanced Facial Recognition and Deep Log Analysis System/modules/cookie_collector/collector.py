import requests
from typing import Dict, List

class CookieCollector:
    def collect(self, url: str) -> Dict:
        try:
            session = requests.Session()
            session.headers.update({"User-Agent": "Sentinel-CookieBot/1.0"})
            response = session.get(url, timeout=10)
            
            cookies = session.cookies.get_dict()
            
            # Basic analysis of cookies
            analysis = []
            for name, value in cookies.items():
                risk = "Low"
                if "session" in name.lower() or "id" in name.lower():
                    risk = "Medium"
                if "auth" in name.lower() or "token" in name.lower():
                    risk = "High"
                
                analysis.append({
                    "name": name,
                    "risk_level": risk,
                    "secure": False # Requests doesn't easily expose flags without deeper inspection
                })
                
            return {
                "url": url,
                "cookie_count": len(cookies),
                "cookies": analysis,
                "headers": dict(response.headers)
            }
        except Exception as e:
            return {"error": str(e)}

cookie_collector = CookieCollector()
