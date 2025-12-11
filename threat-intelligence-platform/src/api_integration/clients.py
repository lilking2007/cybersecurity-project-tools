import requests
import logging

logger = logging.getLogger(__name__)

class VirusTotalClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"

    def get_ip_report(self, ip_address):
        if not self.api_key:
            return {}
        headers = {"x-apikey": self.api_key}
        try:
            response = requests.get(f"{self.base_url}/ip_addresses/{ip_address}", headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching VT report for {ip_address}: {e}")
        return {}

class AbuseIPDBClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.abuseipdb.com/api/v2"

    def check_ip(self, ip_address):
        if not self.api_key:
            return {}
        headers = {
            "Key": self.api_key,
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip_address,
            "maxAgeInDays": 90
        }
        try:
            response = requests.get(f"{self.base_url}/check", headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching AbuseIPDB report for {ip_address}: {e}")
        return {}
