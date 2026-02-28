import json
import logging
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.schemas import TechnicalQuestion
from prompts.templates import QUESTION_GENERATION_PROMPT
from config.settings import settings

logger = logging.getLogger(__name__)

class QuestionGenerator:
    """Motor de generación de preguntas técnicas usando LangChain"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.7
        )
        self.parser = JsonOutputParser()
        
    def generate_questions(
        self, 
        role: str, 
        level: str, 
        tech_stack: List[str]
    ) -> List[TechnicalQuestion]:
        """
        Genera preguntas técnicas usando LangChain
        
        Args:
            role: Rol solicitado
            level: Nivel solicitado
            tech_stack: Stack tecnológico
            
        Returns:
            Lista de preguntas técnicas tipadas
        """
        try:
            # Crear prompt
            prompt = PromptTemplate(
                input_variables=["role", "level", "tech_stack"],
                template=QUESTION_GENERATION_PROMPT
            )
            
            # Formatear entrada
            formatted_prompt = prompt.format(
                role=role,
                level=level,
                tech_stack=", ".join(tech_stack)
            )
            
            logger.info(f"Generando preguntas para {role} ({level})")
            
            # Invocar LLM
            response = self.llm.invoke(formatted_prompt)
            response_text = response.content
            
            # Parsear JSON
            response_json = json.loads(response_text)
            
            # Convertir a modelos tipados
            questions = [
                TechnicalQuestion(**q) 
                for q in response_json["questions"]
            ]
            
            logger.info(f"✓ {len(questions)} preguntas generadas exitosamente")
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Error en generación de preguntas: {e}")
            raise