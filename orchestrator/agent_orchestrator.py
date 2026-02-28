import time
import logging
from typing import List
from models.schemas import (
    CandidateInput, TechnicalQuestion, CandidateAnswer, 
    EvaluationResult, FinalReport
)
from engines.question_generator import QuestionGenerator
from engines.answer_evaluator import AnswerEvaluator
from engines.scoring_engine import ScoringEngine
from utils.validators import validate_input
from utils.logging import setup_logging

logger = logging.getLogger(__name__)

class TechnicalInterviewerAgent:
    """Orquestador principal del agente entrevistador técnico"""
    
    def __init__(self):
        setup_logging()
        self.question_generator = QuestionGenerator()
        self.answer_evaluator = AnswerEvaluator()
        self.scoring_engine = ScoringEngine()
        
    def conduct_interview(
        self,
        candidate_input: CandidateInput,
        candidate_answers: List[CandidateAnswer]
    ) -> FinalReport:
        """
        Ejecuta el flujo completo de entrevista técnica
        
        Args:
            candidate_input: Datos del candidato
            candidate_answers: Respuestas del candidato
            
        Returns:
            Reporte final tipado en JSON
        """
        start_time = time.time()
        
        try:
            # 1. VALIDACIÓN
            logger.info("="*60)
            logger.info("INICIANDO ENTREVISTA TÉCNICA")
            logger.info("="*60)
            logger.info(f"Validando entrada: {candidate_input.role} ({candidate_input.level})")
            
            validate_input(candidate_input)
            logger.info("✓ Entrada validada correctamente")
            
            # 2. GENERACIÓN DE PREGUNTAS
            logger.info("\n[FASE 1] GENERACIÓN DE PREGUNTAS")
            logger.info("-"*60)
            questions = self.question_generator.generate_questions(
                role=candidate_input.role,
                level=candidate_input.level,
                tech_stack=candidate_input.tech_stack
            )
            logger.info(f"✓ {len(questions)} preguntas generadas")
            
            # 3. EVALUACIÓN DE RESPUESTAS
            logger.info("\n[FASE 2] EVALUACIÓN DE RESPUESTAS")
            logger.info("-"*60)
            evaluations = self.answer_evaluator.evaluate_batch(
                questions=questions,
                answers=candidate_answers,
                role=candidate_input.role,
                level=candidate_input.level,
                tech_stack=candidate_input.tech_stack
            )
            logger.info(f"✓ {len(evaluations)} respuestas evaluadas")
            
            # 4. CÁLCULO DE PUNTUACIONES
            logger.info("\n[FASE 3] CÁLCULO DE PUNTUACIONES")
            logger.info("-"*60)
            total_score, avg_score, recommendation, strengths, weaknesses = \
                self.scoring_engine.generate_summary(
                    evaluations=evaluations,
                    level=candidate_input.level
                )
            
            # 5. GENERACIÓN DE REPORTE
            logger.info("\n[FASE 4] GENERACIÓN DE REPORTE FINAL")
            logger.info("-"*60)
            
            execution_time = time.time() - start_time
            
            report = FinalReport(
                candidate_info=candidate_input,
                questions_generated=questions,
                answers_evaluation=evaluations,
                total_score=total_score,
                average_score=avg_score,
                recommendation=recommendation,
                strengths=strengths,
                weaknesses=weaknesses,
                execution_time_seconds=round(execution_time, 2),
                agent_version="1.0"
            )
            
            logger.info(f"✓ Reporte generado en {execution_time:.2f}s")
            logger.info("="*60)
            logger.info(f"RESULTADO FINAL: {recommendation} ({total_score}/100)")
            logger.info("="*60)
            
            return report
            
        except Exception as e:
            logger.error(f"Error crítico en flujo de entrevista: {e}", exc_info=True)
            raise