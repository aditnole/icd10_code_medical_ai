from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union
from enum import Enum

class MedicalEntity(BaseModel):
    text: str
    label: str

class ICD10Code(BaseModel):
    code: str
    code_type: Literal["Primary", "Secondary"]
    description: str
    confidence: float 
    supporting_keyword_evidence: str  


class ICD10Response(BaseModel):
    identified_codes: List[ICD10Code]

class SummaryResponse(BaseModel):
    summary: str
