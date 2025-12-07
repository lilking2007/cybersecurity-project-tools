from config.database import db
from modules.personnel_management.models import AuditLogEntry
from datetime import datetime

class AuditService:
    INDEX_NAME = "sentinel_audit_logs"

    def __init__(self):
        # Ensure index exists
        if db.es and not db.es.indices.exists(index=self.INDEX_NAME):
            db.es.indices.create(index=self.INDEX_NAME)

    def log_action(self, user_id: str, action: str, resource: str, details: str = None):
        if not db.es:
            print("Elasticsearch not connected, cannot log audit trail.")
            return

        entry = {
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "timestamp": datetime.now(),
            "details": details
        }
        
        try:
            db.es.index(index=self.INDEX_NAME, document=entry)
        except Exception as e:
            print(f"Failed to write audit log: {e}")

    def get_logs(self, user_id: str = None, limit: int = 50):
        if not db.es: 
            return []
            
        query = {"match_all": {}}
        if user_id:
            query = {"match": {"user_id": user_id}}
            
        res = db.es.search(index=self.INDEX_NAME, query=query, size=limit, sort=[{"timestamp": "desc"}])
        return [hit["_source"] for hit in res["hits"]["hits"]]

audit_service = AuditService()
