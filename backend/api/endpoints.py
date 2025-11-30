from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from backend.models.models import (
    DocumentUploadResponse, 
    KnowledgeBaseStatus, 
    TestCaseRequest, 
    TestPlan, 
    ScriptGenerationRequest, 
    ScriptGenerationResponse
)

router = APIRouter()

@router.post("/ingest/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    from backend.services.ingestion import ingestion_service
    try:
        file_path = ingestion_service.save_file(file, file.filename)
        num_chunks = ingestion_service.process_document(file_path)
        return DocumentUploadResponse(
            filename=file.filename,
            message=f"Successfully uploaded and ingested {num_chunks} chunks."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest/reset", response_model=DocumentUploadResponse)
async def reset_knowledge_base():
    from backend.services.ingestion import ingestion_service
    try:
        ingestion_service.clear_knowledge_base()
        return DocumentUploadResponse(
            filename="ALL",
            message="Knowledge base cleared."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/test-cases", response_model=TestPlan)
async def generate_test_cases(request: TestCaseRequest):
    from backend.services.rag import rag_service
    try:
        test_plan = rag_service.generate_test_cases(request.feature)
        return test_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/script", response_model=ScriptGenerationResponse)
async def generate_script(request: ScriptGenerationRequest):
    from backend.services.script_gen import script_gen_service
    try:
        script = script_gen_service.generate_script(request.test_case)
        return ScriptGenerationResponse(script_code=script)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
