from fastapi import APIRouter, UploadFile, File, HTTPException
from modules.facial_recognition.engine import face_engine

router = APIRouter(
    prefix="/facial-recognition",
    tags=["facial-recognition"]
)

@router.post("/identify")
async def identify_face(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    content = await file.read()
    try:
        img = face_engine.process_image(content)
        results = face_engine.get_embeddings(img)
        
        # In a real system, we would now query Elasticsearch/Neo4j 
        # to find the closest matching vector to 'results[0]["embedding"]'
        
        return {
            "status": "success",
            "faces_detected": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
