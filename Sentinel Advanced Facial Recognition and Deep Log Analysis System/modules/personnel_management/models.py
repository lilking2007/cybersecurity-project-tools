from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PersonnelProfile(BaseModel):
    user_id: str
    full_name: str
    rank: str
    department: str
    badge_number: str
    clearance_level: int
    certifications: List[str] = []
    
class AuditLogEntry(BaseModel):
    user_id: str
    action: str
    resource: str
    timestamp: datetime = datetime.now()
    details: Optional[str] = None
