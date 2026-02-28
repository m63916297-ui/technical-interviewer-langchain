from enum import Enum

class Recommendation(str, Enum):
    """Recomendaciones posibles"""
    NO_CUMPLE = "No cumple"
    CUMPLE = "Cumple"
    SOBRECUALIFICADO = "Sobrecualificado"

class DifficultyLevel(str, Enum):
    """Niveles de dificultad"""
    BASICO = "Básico"
    INTERMEDIO = "Intermedio"
    AVANZADO = "Avanzado"

def calculate_recommendation(score: int, level: str) -> str:
    """
    Calcula recomendación basada en score y nivel solicitado
    
    Args:
        score: Puntuación total (0-100)
        level: Nivel solicitado (Junior/Mid/Senior)
        
    Returns:
        Recomendación: No cumple, Cumple o Sobrecualificado
    """
    from config.settings import settings
    
    if score < settings.THRESHOLD_NO_CUMPLE:
        return Recommendation.NO_CUMPLE.value
    elif score < settings.THRESHOLD_CUMPLE:
        return Recommendation.CUMPLE.value
    else:
        return Recommendation.SOBRECUALIFICADO.value