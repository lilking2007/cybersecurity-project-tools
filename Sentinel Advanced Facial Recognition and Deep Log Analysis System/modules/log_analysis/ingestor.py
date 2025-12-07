from config.database import db
from datetime import datetime
import json

class LogIngestor:
    INDEX_NAME = "sentinel_system_logs"

    def __init__(self):
        if db.es and not db.es.indices.exists(index=self.INDEX_NAME):
            db.es.indices.create(index=self.INDEX_NAME)

    def ingest_line(self, line: str, source: str):
        # Basic parsing - in production use grok or regex
        doc = {
            "raw_message": line,
            "source": source,
            "timestamp": datetime.now(),
            "level": "INFO" # Default
        }
        
        # Simple heuristic for demo
        if "error" in line.lower():
            doc["level"] = "ERROR"
        elif "warning" in line.lower():
            doc["level"] = "WARNING"
            
        if db.es:
            db.es.index(index=self.INDEX_NAME, document=doc)
    
    def search_logs(self, query_string: str):
        if not db.es: return []
        q = {
            "query": {
                "multi_match": {
                    "query": query_string,
                    "fields": ["raw_message", "source"]
                }
            }
        }
        res = db.es.search(index=self.INDEX_NAME, body=q)
        return [hit["_source"] for hit in res["hits"]["hits"]]

log_ingestor = LogIngestor()
