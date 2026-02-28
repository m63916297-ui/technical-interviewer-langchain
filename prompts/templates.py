
QUESTION_GENERATION_PROMPT = """
Eres un entrevistador técnico experto evaluando un candidato para el rol de {role} en nivel {level}.

Stack tecnológico a evaluar: {tech_stack}

Genera exactamente 5 preguntas técnicas relevantes para este rol y nivel. 
Las preguntas deben:
1. Estar directamente relacionadas con el stack tecnológico mencionado
2. Ser progresivas en dificultad (de básica a avanzada)
3. Evaluar tanto conocimiento teórico como práctico
4. Ser específicas y sin ambigüedades

Formato de respuesta (JSON):
{{
    "questions": [
        {{
            "id": 1,
            "question": "pregunta aquí",
            "category": "categoría (e.g., Fundamentals, Architecture, Best Practices)",
            "difficulty": "Básico|Intermedio|Avanzado",
            "expected_topics": ["topic1", "topic2"]
        }},
        ...
    ]
}}

IMPORTANTE: Responde SOLO con JSON válido, sin explicaciones adicionales.
"""

ANSWER_EVALUATION_PROMPT = """
Eres un evaluador técnico experto. Tu tarea es evaluar la respuesta de un candidato.

Contexto:
- Rol solicitado: {role}
- Nivel: {level}
- Stack tecnológico: {tech_stack}

Pregunta técnica #{question_id}:
"{question_text}"

Respuesta del candidato:
"{candidate_answer}"

Evalúa esta respuesta en una escala 0-100 considerando:
1. Exactitud técnica
2. Completitud de la respuesta
3. Demostración de entendimiento profundo
4. Claridad y estructura
5. Relevancia para el rol/nivel

Proporciona:
- Score (0-100)
- Feedback constructivo
- Lista de criterios cumplidos

Formato de respuesta (JSON):
{{
    "score": <0-100>,
    "feedback": "explicación del score",
    "criteria_met": ["criterio1", "criterio2"]
}}

IMPORTANTE: Responde SOLO con JSON válido.
"""

SCORING_SUMMARY_PROMPT = """
Resume la evaluación técnica de un candidato para {role} en nivel {level}.

Preguntas y puntuaciones:
{evaluation_summary}

Proporciona:
1. Puntuación total
2. Puntuación promedio
3. Fortalezas identificadas (máximo 3)
4. Debilidades identificadas (máximo 3)
5. Recomendación final

Formato de respuesta (JSON):
{{
    "total_score": <0-100>,
    "average_score": <0-100>,
    "strengths": ["fortaleza1", "fortaleza2", "fortaleza3"],
    "weaknesses": ["debilidad1", "debilidad2", "debilidad3"]
}}

IMPORTANTE: Responde SOLO con JSON válido.
"""