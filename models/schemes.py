from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class CandidateInput(BaseModel):
    """Entrada: datos del candidato a evaluar"""
    role: str = Field(..., description="Rol solicitado (e.g., Backend Engineer)")
    level: str = Field(..., description="Nivel solicitado (Junior/Mid/Senior)")
    tech_stack: List[str] = Field(..., description="Stack tecnológico (e.g., [Python, FastAPI, PostgreSQL])")

class TechnicalQuestion(BaseModel):
    """Pregunta técnica generada"""
    id: int = Field(..., ge=1, le=5)
    question: str
    category: str
    difficulty: str
    expected_topics: List[str]

class CandidateAnswer(BaseModel):
    """Respuesta del candidato"""
    question_id: int
    answer: str
    score_given: Optional[int] = Field(None, ge=0, le=100)

class EvaluationResult(BaseModel):
    """Resultado de evaluación para una pregunta"""
    question_id: int
    question_text: str
    answer_text: str
    score: int = Field(..., ge=0, le=100)
    feedback: str
    criteria_met: List[str]

class FinalReport(BaseModel):
    """Reporte final del agente entrevistador"""
    candidate_info: CandidateInput
    questions_generated: List[TechnicalQuestion]
    answers_evaluation: List[EvaluationResult]
    total_score: int = Field(..., ge=0, le=100)
    average_score: float
    recommendation: str = Field(..., description="No cumple / Cumple / Sobrecualificado")
    strengths: List[str]
    weaknesses: List[str]
    execution_time_seconds: float
    agent_version: str = "1.0"
