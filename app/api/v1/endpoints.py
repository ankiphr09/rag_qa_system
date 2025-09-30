from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Dict, Any
from ...services.rag_service import RAGService
from ...core.security import get_current_user
import tempfile
import os

router = APIRouter()
rag_service = RAGService()

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    metadata: Dict[str, Any] = {},
    current_user: Dict = Depends(get_current_user)
):
    """Upload and process a document"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Add user metadata
        metadata.update({
            "uploaded_by": current_user["username"],
            "original_name": file.filename
        })
        
        # Process document
        success = await rag_service.process_document(temp_file_path, metadata)
        
        # Clean up temp file
        os.unlink(temp_file_path)
        
        if success:
            return {"message": "Document processed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to process document")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_documents(
    question: str,
    current_user: Dict = Depends(get_current_user)
):
    """Query the document base"""
    try:
        result = await rag_service.query(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))