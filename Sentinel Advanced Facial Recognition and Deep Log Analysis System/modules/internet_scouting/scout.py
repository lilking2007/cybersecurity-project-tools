import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class InternetScout:
    def scout_url(self, url: str) -> Dict:
        try:
            headers = {"User-Agent": "Sentinel-Scout/1.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic metadata
            title = soup.title.string if soup.title else "No Title"
            links = [a['href'] for a in soup.find_all('a', href=True)]
            images = [img['src'] for img in soup.find_all('img', src=True)]
            
            return {
                "status": "success",
                "url": url,
                "title": title,
                "link_count": len(links),
                "image_count": len(images),
                "preview_links": links[:10],
                "preview_images": images[:5]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

scout = InternetScout()
