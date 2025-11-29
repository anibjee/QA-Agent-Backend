from pydantic import BaseModel
from typing import List, Optional

class DocumentUploadResponse(BaseModel):
    filename: str
    message: str

class KnowledgeBaseStatus(BaseModel):
    document_count: int
    status: str

class TestCaseRequest(BaseModel):
    feature: str

class TestCase(BaseModel):
    test_id: str
    feature: str
    test_scenario: str
    expected_result: str
    grounded_in: str

class TestPlan(BaseModel):
    test_cases: List[TestCase]

class ScriptGenerationRequest(BaseModel):
    test_case: TestCase

class ScriptGenerationResponse(BaseModel):
    script_code: str
