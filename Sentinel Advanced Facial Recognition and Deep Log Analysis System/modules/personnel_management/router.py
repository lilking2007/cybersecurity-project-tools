from fastapi import APIRouter, Depends, HTTPException
from typing import List
from modules.system_management.auth import get_current_user
from modules.personnel_management.models import PersonnelProfile, AuditLogEntry
from modules.personnel_management.audit import audit_service

router = APIRouter(
    prefix="/personnel",
    tags=["personnel"]
)

@router.get("/audit-logs", response_model=List[dict])
async def view_audit_logs(current_user: dict = Depends(get_current_user)):
    # In a real app, check if current_user has 'admin' role
    logs = audit_service.get_logs()
    return logs

@router.post("/profile")
async def update_profile(profile: PersonnelProfile, current_user: dict = Depends(get_current_user)):
    # Mock update - in reality, save to Neo4j
    audit_service.log_action(
        user_id=current_user.username,
        action="UPDATE_PROFILE",
        resource="PersonnelProfile",
        details=f"Updated profile for {profile.full_name}"
    )
    return {"status": "Updated", "profile": profile}
