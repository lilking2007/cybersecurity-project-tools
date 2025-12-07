from fastapi import APIRouter
from modules.external_empowerment.connector import external_connector

router = APIRouter(
    prefix="/external",
    tags=["external-empowerment"]
)

@router.get("/search")
async def search_external(q: str, source: str = "generic"):
    return external_connector.search_database(q, source)
