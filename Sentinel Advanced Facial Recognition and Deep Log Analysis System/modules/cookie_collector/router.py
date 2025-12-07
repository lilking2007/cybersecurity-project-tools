from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from modules.cookie_collector.collector import cookie_collector

router = APIRouter(
    prefix="/cookies",
    tags=["cookie-collector"]
)

class CookieRequest(BaseModel):
    url: HttpUrl

@router.post("/inspect")
async def inspect_cookies(request: CookieRequest):
    return cookie_collector.collect(str(request.url))
