from fastapi import APIRouter
from config.database import db

router = APIRouter(
    prefix="/dashboard",
    tags=["threat-dashboard"]
)

@router.get("/stats")
async def get_dashboard_stats():
    # Aggregate stats from Elasticsearch
    log_count = 0
    if db.es:
        try:
            res = db.es.count(index="sentinel_system_logs")
            log_count = res['count']
        except:
            pass
            
    return {
        "system_status": "Operational",
        "total_logs_processed": log_count,
        "active_investigations": 5, # Mock
        "threat_level": "Low",
        "recent_alerts": []
    }
