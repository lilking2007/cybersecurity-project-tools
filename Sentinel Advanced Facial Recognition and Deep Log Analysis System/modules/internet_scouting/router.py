from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from modules.internet_scouting.scout import scout

router = APIRouter(
    prefix="/scout",
    tags=["internet-scouting"]
)

class ScoutRequest(BaseModel):
    url: HttpUrl

@router.post("/analyze")
async def analyze_website(request: ScoutRequest):
    result = scout.scout_url(str(request.url))
    return result
