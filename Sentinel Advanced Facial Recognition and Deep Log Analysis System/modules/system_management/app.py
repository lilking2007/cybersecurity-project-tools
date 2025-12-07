from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import config

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    description="API for Sentinel Advanced Facial Recognition and Deep Log Analysis System"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from modules.system_management.routers import users
from modules.personnel_management import router as personnel
from modules.facial_recognition import router as facial
from modules.log_analysis import router as logs
from modules.internet_scouting import router as scout
from modules.cookie_collector import router as cookies
from modules.external_empowerment import router as external
from modules.threat_dashboard import router as dashboard
from config.database import db
from fastapi import Request
from modules.personnel_management.audit import audit_service
import time

app.include_router(users.router)
app.include_router(personnel.router)
app.include_router(facial.router)
app.include_router(logs.router)
app.include_router(scout.router)
app.include_router(cookies.router)
app.include_router(external.router)
app.include_router(dashboard.router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log every modification request
    if request.method in ["POST", "PUT", "DELETE"]:
        audit_service.log_action(
            user_id="system_middleware",
            action=f"HTTP_{request.method}",
            resource=str(request.url),
            details=f"Status: {response.status_code}"
        )
    return response

@app.on_event("startup")
async def startup_event():
    db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    db.close()

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": config.VERSION}

@app.get("/")
async def root():
    return {"message": "Sentinel System is running"}
