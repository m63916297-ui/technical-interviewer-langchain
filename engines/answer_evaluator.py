import json
import logging
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from models.schemas import EvaluationResult, TechnicalQuestion, CandidateAnswer
from prompts.templates import ANSWER_EVALUATION_PROMPT
from config.settings import settings

logger = logging.getLogger(__name__)

class AnswerEvaluator:
    """Motor de evaluación de respuestas usando LangChain"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.5
        )
        
    def evaluate_answer(
        self,
        question: TechnicalQuestion,
        answer: CandidateAnswer,
        role: str,
        level: str,
        tech_stack: List[str]
    ) -> EvaluationResult:
        """
        Evalúa una respuesta individual
        
        Args:
            question: Pregunta técnica
            answer: Respuesta del candidato
            role: Rol solicitado
            level: Nivel solicitado
            tech_stack: Stack tecnológico
            
        Returns:
            Resultado de evaluación tipado
        """
        try:
            # Crear prompt
            prompt = PromptTemplate(
                input_variables=[
                    "role", "level", "tech_stack", 
                    "question_id", "question_text", "candidate_answer"
                ],
                template=ANSWER_EVALUATION_PROMPT
            )
            
            # Formatear entrada
            formatted_prompt = prompt.format(
                role=role,
                level=level,
                tech_stack=", ".join(tech_stack),
                question_id=question.id,
                question_text=question.question,
                candidate_answer=answer.answer
            )
            
            logger.info(f"Evaluando respuesta para pregunta {question.id}")
            
            # Invocar LLM
            response = self.llm.invoke(formatted_prompt)
            response_text = response.content
            
            # Parsear JSON
            evaluation_json = json.loads(response_text)
            
            # Crear resultado tipado
            result = EvaluationResult(
                question_id=question.id,
                question_text=question.question,
                answer_text=answer.answer,
                score=evaluation_json["score"],
                feedback=evaluation_json["feedback"],
                criteria_met=evaluation_json["criteria_met"]
            )
            
            logger.info(f"✓ Pregunta {question.id}: {result.score}/100")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear evaluación: {e}")
            raise
        except Exception as e:
            logger.error(f"Error en evaluación: {e}")
            raise
    
    def evaluate_batch(
        self,
        questions: List[TechnicalQuestion],
        answers: List[CandidateAnswer],
        role: str,
        level: str,
        tech_stack: List[str]
    ) -> List[EvaluationResult]:
        """Evalúa un lote de respuestas"""
        results = []
        for question in questions:
            # Buscar respuesta correspondiente
            answer = next(
                (a for a in answers if a.question_id == question.id),
                None
            )
            if answer:
                result = self.evaluate_answer(
                    question, answer, role, level, tech_stack
                )
                results.append(result)
        return results