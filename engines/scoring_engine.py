import logging
from typing import List, Tuple
from models.schemas import EvaluationResult
from models.evaluation_models import calculate_recommendation
from config.settings import settings

logger = logging.getLogger(__name__)

class ScoringEngine:
    """Motor de cálculo de puntuaciones y recomendaciones"""
    
    @staticmethod
    def calculate_total_score(evaluations: List[EvaluationResult]) -> int:
        """Calcula puntuación total (promedio ponderado)"""
        if not evaluations:
            return 0
        
        total = sum(e.score for e in evaluations)
        average = total / len(evaluations)
        
        logger.info(f"Score calculado: {average:.2f}")
        return int(round(average))
    
    @staticmethod
    def extract_strengths(evaluations: List[EvaluationResult]) -> List[str]:
        """Extrae fortalezas basadas en feedbacks positivos"""
        strengths = []
        
        for eval_result in evaluations:
            if eval_result.score >= 75:
                # Extraer categoría
                if eval_result.criteria_met:
                    strengths.extend(eval_result.criteria_met[:1])
        
        # Retornar top 3 únicas
        return list(set(strengths))[:3]
    
    @staticmethod
    def extract_weaknesses(evaluations: List[EvaluationResult]) -> List[str]:
        """Extrae debilidades de respuestas bajas"""
        weaknesses = []
        
        for eval_result in evaluations:
            if eval_result.score < 60:
                weaknesses.append(
                    f"Pregunta {eval_result.question_id}: {eval_result.feedback}"
                )
        
        return weaknesses[:3]
    
    @staticmethod
    def get_recommendation(score: int, level: str) -> str:
        """Genera recomendación final"""
        recommendation = calculate_recommendation(score, level)
        logger.info(f"Recomendación: {recommendation}")
        return recommendation
    
    @staticmethod
    def generate_summary(
        evaluations: List[EvaluationResult],
        level: str
    ) -> Tuple[int, float, str, List[str], List[str]]:
        """
        Genera resumen completo de evaluación
        
        Returns:
            (total_score, average_score, recommendation, strengths, weaknesses)
        """
        total_score = ScoringEngine.calculate_total_score(evaluations)
        average_score = total_score  # Mismo valor en este caso
        recommendation = ScoringEngine.get_recommendation(total_score, level)
        strengths = ScoringEngine.extract_strengths(evaluations)
        weaknesses = ScoringEngine.extract_weaknesses(evaluations)
        
        return total_score, float(average_score), recommendation, strengths, weaknesses