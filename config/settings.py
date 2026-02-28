import logging
from models.schemas import CandidateInput
from config.settings import settings

logger = logging.getLogger(__name__)

def validate_input(candidate_input: CandidateInput) -> None:
    """
    Valida la entrada del candidato
    
    Args:
        candidate_input: Datos a validar
        
    Raises:
        ValueError: Si la validación falla
    """
    # Validar rol
    if candidate_input.role not in settings.SUPPORTED_ROLES:
        raise ValueError(
            f"Rol '{candidate_input.role}' no soportado. "
            f"Opciones: {settings.SUPPORTED_ROLES}"
        )
    
    # Validar nivel
    if candidate_input.level not in settings.SUPPORTED_LEVELS:
        raise ValueError(
            f"Nivel '{candidate_input.level}' no soportado. "
            f"Opciones: {settings.SUPPORTED_LEVELS}"
        )
    
    # Validar stack tecnológico
    if not candidate_input.tech_stack or len(candidate_input.tech_stack) == 0:
        raise ValueError("El stack tecnológico no puede estar vacío")
    
    if len(candidate_input.tech_stack) > 10:
        raise ValueError("El stack tecnológico no puede exceder 10 elementos")
    
    logger.info("✓ Validación completada exitosamente")
