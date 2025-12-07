from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from modules.log_analysis.ingestor import log_ingestor

router = APIRouter(
    prefix="/logs",
    tags=["log-analysis"]
)

def process_log_file(content: str, filename: str):
    lines = content.split('\n')
    for line in lines:
        if line.strip():
            log_ingestor.ingest_line(line, source=filename)

@router.post("/upload")
async def upload_log(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    content = await file.read()
    text_content = content.decode("utf-8")
    
    # Process in background to avoid blocking
    background_tasks.add_task(process_log_file, text_content, file.filename)
    
    return {"message": "Log file accepted for processing", "filename": file.filename}

@router.get("/search")
async def search_logs(q: str):
    results = log_ingestor.search_logs(q)
    return {"count": len(results), "results": results}
