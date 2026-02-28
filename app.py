import json
import time
import streamlit as st
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== MODELOS ====================

class CandidateInput(BaseModel):
    role: str = Field(..., description="Rol solicitado")
    level: str = Field(..., description="Nivel solicitado")
    tech_stack: List[str] = Field(..., description="Stack tecnológico")

class TechnicalQuestion(BaseModel):
    id: int
    question: str
    category: str
    difficulty: str
    expected_topics: List[str]

class CandidateAnswer(BaseModel):
    question_id: int
    answer: str

class EvaluationResult(BaseModel):
    question_id: int
    question_text: str
    answer_text: str
    score: int
    feedback: str
    criteria_met: List[str]

class FinalReport(BaseModel):
    candidate_info: CandidateInput
    questions_generated: List[TechnicalQuestion]
    answers_evaluation: List[EvaluationResult]
    total_score: int
    average_score: float
    recommendation: str
    strengths: List[str]
    weaknesses: List[str]
    execution_time_seconds: float
    agent_version: str = "1.0"

# ==================== CONFIGURACIÓN ====================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SUPPORTED_ROLES = [
    "Backend Engineer",
    "Frontend Engineer",
    "Full Stack Engineer",
    "Data Scientist",
    "DevOps Engineer"
]
SUPPORTED_LEVELS = ["Junior", "Mid", "Senior"]
THRESHOLD_NO_CUMPLE = 50
THRESHOLD_CUMPLE = 75

# ==================== PROMPTS ====================

QUESTION_GENERATION_PROMPT = """
Eres un entrevistador técnico experto evaluando un candidato para el rol de {role} en nivel {level}.

Stack tecnológico a evaluar: {tech_stack}

Genera exactamente 5 preguntas técnicas relevantes para este rol y nivel. 
Las preguntas deben:
1. Estar directamente relacionadas con el stack tecnológico
2. Ser progresivas en dificultad (de básica a avanzada)
3. Evaluar tanto conocimiento teórico como práctico
4. Ser específicas y sin ambigüedades

Responde con este formato JSON exacto:
{{
    "questions": [
        {{
            "id": 1,
            "question": "pregunta aquí",
            "category": "Fundamentals|Architecture|Best Practices|Performance|Security",
            "difficulty": "Básico|Intermedio|Avanzado",
            "expected_topics": ["topic1", "topic2", "topic3"]
        }},
        {{
            "id": 2,
            "question": "pregunta aquí",
            "category": "Fundamentals|Architecture|Best Practices|Performance|Security",
            "difficulty": "Básico|Intermedio|Avanzado",
            "expected_topics": ["topic1", "topic2", "topic3"]
        }},
        {{
            "id": 3,
            "question": "pregunta aquí",
            "category": "Fundamentals|Architecture|Best Practices|Performance|Security",
            "difficulty": "Básico|Intermedio|Avanzado",
            "expected_topics": ["topic1", "topic2", "topic3"]
        }},
        {{
            "id": 4,
            "question": "pregunta aquí",
            "category": "Fundamentals|Architecture|Best Practices|Performance|Security",
            "difficulty": "Básico|Intermedio|Avanzado",
            "expected_topics": ["topic1", "topic2", "topic3"]
        }},
        {{
            "id": 5,
            "question": "pregunta aquí",
            "category": "Fundamentals|Architecture|Best Practices|Performance|Security",
            "difficulty": "Básico|Intermedio|Avanzado",
            "expected_topics": ["topic1", "topic2", "topic3"]
        }}
    ]
}}

SOLO JSON, sin explicaciones adicionales.
"""

ANSWER_EVALUATION_PROMPT = """
Eres un evaluador técnico experto. Evalúa esta respuesta.

Contexto:
- Rol: {role}
- Nivel: {level}
- Stack: {tech_stack}

Pregunta:
"{question_text}"

Respuesta:
"{candidate_answer}"

Evalúa en 0-100 considerando exactitud, completitud, profundidad, claridad y relevancia.

Responde con JSON:
{{
    "score": <número 0-100>,
    "feedback": "explicación breve",
    "criteria_met": ["criterio1", "criterio2", "criterio3"]
}}

SOLO JSON, sin explicaciones.
"""

# ==================== GENERADOR DE PREGUNTAS ====================

def generate_questions(role: str, level: str, tech_stack: List[str]) -> List[TechnicalQuestion]:
    """Genera preguntas usando LangChain + OpenAI"""
    try:
        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        
        prompt = PromptTemplate(
            input_variables=["role", "level", "tech_stack"],
            template=QUESTION_GENERATION_PROMPT
        )
        
        formatted_prompt = prompt.format(
            role=role,
            level=level,
            tech_stack=", ".join(tech_stack)
        )
        
        response = llm.invoke(formatted_prompt)
        response_text = response.content
        
        # Extraer JSON
        response_json = json.loads(response_text)
        
        questions = [
            TechnicalQuestion(**q) 
            for q in response_json["questions"]
        ]
        
        return questions
        
    except Exception as e:
        st.error(f"Error generando preguntas: {str(e)}")
        return []

# ==================== EVALUADOR DE RESPUESTAS ====================

def evaluate_answer(question: TechnicalQuestion, answer: str, role: str, level: str, tech_stack: List[str]) -> EvaluationResult:
    """Evalúa una respuesta usando LangChain + OpenAI"""
    try:
        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=0.5
        )
        
        prompt = PromptTemplate(
            input_variables=["role", "level", "tech_stack", "question_text", "candidate_answer"],
            template=ANSWER_EVALUATION_PROMPT
        )
        
        formatted_prompt = prompt.format(
            role=role,
            level=level,
            tech_stack=", ".join(tech_stack),
            question_text=question.question,
            candidate_answer=answer
        )
        
        response = llm.invoke(formatted_prompt)
        response_text = response.content
        
        evaluation_json = json.loads(response_text)
        
        result = EvaluationResult(
            question_id=question.id,
            question_text=question.question,
            answer_text=answer,
            score=int(evaluation_json["score"]),
            feedback=evaluation_json["feedback"],
            criteria_met=evaluation_json["criteria_met"]
        )
        
        return result
        
    except Exception as e:
        st.error(f"Error evaluando respuesta: {str(e)}")
        return None

# ==================== MOTOR DE SCORING ====================

def calculate_final_score(evaluations: List[EvaluationResult]) -> tuple:
    """Calcula score final y métricas"""
    if not evaluations:
        return 0, 0, "No cumple", [], []
    
    scores = [e.score for e in evaluations]
    total_score = int(sum(scores) / len(scores))
    
    # Recomendación
    if total_score < THRESHOLD_NO_CUMPLE:
        recommendation = "No cumple"
    elif total_score < THRESHOLD_CUMPLE:
        recommendation = "Cumple"
    else:
        recommendation = "Sobrecualificado"
    
    # Fortalezas (scores altos)
    strengths = [
        e.criteria_met[0] if e.criteria_met else "N/A"
        for e in evaluations if e.score >= 75
    ][:3]
    
    # Debilidades (scores bajos)
    weaknesses = [
        f"Q{e.question_id}: {e.feedback}"
        for e in evaluations if e.score < 60
    ][:3]
    
    return total_score, float(total_score), recommendation, strengths, weaknesses

# ==================== UI - STREAMLIT ====================

st.set_page_config(
    page_title="Technical Interviewer Agent",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
    .main { padding: 2rem; }
    .stTitle { color: #1f77b4; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Technical Interviewer Agent")
st.markdown("**Evaluador técnico automatizado con LangChain + OpenAI**")
st.divider()

# Verificar API Key
if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY no configurada. Configura la variable de entorno.")
    st.info("Para desarrollo local: crea un archivo `.env` con tu API key")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    role = st.selectbox("Rol solicitado", SUPPORTED_ROLES)
    level = st.selectbox("Nivel solicitado", SUPPORTED_LEVELS)
    
    tech_stack = st.multiselect(
        "Stack tecnológico",
        options=[
            "Python", "JavaScript", "Java", "C#", "Go",
            "FastAPI", "Django", "Flask", "Node.js", "React",
            "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes",
            "AWS", "GCP", "Azure", "Git", "REST API"
        ],
        default=["Python"]
    )
    
    st.divider()
    st.info(f"""
    **Umbrales de evaluación:**
    - No cumple: < {THRESHOLD_NO_CUMPLE}
    - Cumple: {THRESHOLD_NO_CUMPLE}-{THRESHOLD_CUMPLE}
    - Sobrecualificado: ≥ {THRESHOLD_CUMPLE}
    """)

# Tabs principales
tab1, tab2, tab3 = st.tabs(["🎬 Ejecutar Entrevista", "📊 Ejemplo de Salida", "📖 Documentación"])

with tab1:
    st.header("Ejecutar Entrevista Técnica")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Paso 1: Generar Preguntas")
        
        if st.button("🚀 Generar Preguntas Técnicas", key="generate_btn", use_container_width=True):
            with st.spinner("⏳ Generando preguntas con IA..."):
                start_time = time.time()
                questions = generate_questions(role, level, tech_stack)
                generation_time = time.time() - start_time
                
                if questions:
                    st.session_state.questions = questions
                    st.success(f"✓ {len(questions)} preguntas generadas en {generation_time:.2f}s")
                    
                    st.markdown("### 📋 Preguntas Generadas:")
                    for q in questions:
                        with st.expander(f"Q{q.id}: {q.question[:60]}...", expanded=True):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Categoría:** {q.category}")
                                st.markdown(f"**Dificultad:** {q.difficulty}")
                            with col2:
                                st.markdown(f"**Tópicos esperados:**")
                                for topic in q.expected_topics:
                                    st.write(f"• {topic}")
    
    with col2:
        st.info("📌 Genera preguntas basadas en rol y stack")
    
    st.divider()
    
    # Paso 2: Respuestas
    if "questions" in st.session_state:
        st.subheader("Paso 2: Ingresar Respuestas del Candidato")
        
        answers_dict = {}
        
        for q in st.session_state.questions:
            with st.expander(f"Respuesta Q{q.id}"):
                answer_text = st.text_area(
                    f"Respuesta a: {q.question}",
                    value="",
                    height=100,
                    key=f"answer_{q.id}",
                    label_visibility="collapsed"
                )
                answers_dict[q.id] = answer_text
        
        st.session_state.answers_dict = answers_dict
        
        st.divider()
        
        # Paso 3: Evaluar
        st.subheader("Paso 3: Evaluar Respuestas")
        
        if st.button("📊 Ejecutar Evaluación Completa", key="evaluate_btn", use_container_width=True):
            
            # Validar respuestas
            if not all(answers_dict.values()):
                st.error("❌ Todas las respuestas deben estar completas")
            else:
                with st.spinner("⏳ Evaluando respuestas con IA... esto puede tardar 1-2 minutos"):
                    start_time = time.time()
                    
                    evaluations = []
                    progress_bar = st.progress(0)
                    
                    for idx, q in enumerate(st.session_state.questions):
                        answer_text = answers_dict[q.id]
                        
                        eval_result = evaluate_answer(
                            q, answer_text, role, level, tech_stack
                        )
                        
                        if eval_result:
                            evaluations.append(eval_result)
                        
                        progress_bar.progress((idx + 1) / len(st.session_state.questions))
                    
                    execution_time = time.time() - start_time
                    
                    # Calcular métricas finales
                    total_score, avg_score, recommendation, strengths, weaknesses = \
                        calculate_final_score(evaluations)
                    
                    # Crear reporte
                    report = FinalReport(
                        candidate_info=CandidateInput(
                            role=role,
                            level=level,
                            tech_stack=tech_stack
                        ),
                        questions_generated=st.session_state.questions,
                        answers_evaluation=evaluations,
                        total_score=total_score,
                        average_score=avg_score,
                        recommendation=recommendation,
                        strengths=strengths,
                        weaknesses=weaknesses,
                        execution_time_seconds=execution_time
                    )
                    
                    st.session_state.report = report
                    st.success(f"✓ Evaluación completada en {execution_time:.2f}s")

# Mostrar reporte si existe
if "report" in st.session_state:
    st.divider()
    st.markdown("## 📈 Reporte Final de Evaluación")
    
    report = st.session_state.report
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Score Total", f"{report.total_score}/100")
    
    with col2:
        st.metric("Promedio", f"{report.average_score:.1f}")
    
    with col3:
        st.metric("Recomendación", report.recommendation)
    
    with col4:
        st.metric("Tiempo", f"{report.execution_time_seconds:.1f}s")
    
    st.divider()
    
    # Detalles de evaluación
    st.markdown("### 📋 Detalles de Evaluación")
    
    for eval_result in report.answers_evaluation:
        with st.expander(f"Q{eval_result.question_id}: {eval_result.question_text[:50]}... [{eval_result.score}/100]"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"### Score: **{eval_result.score}/100**")
            
            with col2:
                st.markdown("**Respuesta:**")
                st.text(eval_result.answer_text)
                st.markdown("**Feedback:**")
                st.info(eval_result.feedback)
                st.markdown("**Criterios cumplidos:**")
                for criterion in eval_result.criteria_met:
                    st.write(f"✓ {criterion}")
    
    st.divider()
    
    # Fortalezas y debilidades
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💪 Fortalezas")
        if report.strengths:
            for strength in report.strengths:
                st.success(f"✓ {strength}")
        else:
            st.info("Sin fortalezas destacadas")
    
    with col2:
        st.markdown("### ⚠️ Debilidades")
        if report.weaknesses:
            for weakness in report.weaknesses:
                st.warning(f"✗ {weakness}")
        else:
            st.info("Sin debilidades identificadas")
    
    st.divider()
    
    # Exportar
    st.markdown("### 📥 Descargar Resultados")
    
    json_report = report.model_dump_json(indent=2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 Descargar JSON",
            data=json_report,
            file_name=f"interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        summary_text = f"""
REPORTE TÉCNICO - ENTREVISTADOR AUTOMÁTICO
==========================================
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CANDIDATO
---------
Rol: {report.candidate_info.role}
Nivel: {report.candidate_info.level}
Stack: {', '.join(report.candidate_info.tech_stack)}

RESULTADO
---------
Score Total: {report.total_score}/100
Promedio: {report.average_score:.1f}
Recomendación: {report.recommendation}
Tiempo: {report.execution_time_seconds:.1f}s

FORTALEZAS
----------
{chr(10).join([f"• {s}" for s in report.strengths]) if report.strengths else "N/A"}

DEBILIDADES
-----------
{chr(10).join([f"• {w}" for w in report.weaknesses]) if report.weaknesses else "N/A"}
        """
        
        st.download_button(
            label="📋 Descargar Resumen",
            data=summary_text,
            file_name=f"interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

with tab2:
    st.header("Ejemplo de Salida JSON")
    st.markdown("Aquí se muestra un ejemplo de la estructura de respuesta:")
    
    example_output = {
        "candidate_info": {
            "role": "Backend Engineer",
            "level": "Mid",
            "tech_stack": ["Python", "FastAPI", "PostgreSQL"]
        },
        "total_score": 78,
        "average_score": 78.0,
        "recommendation": "Cumple",
        "strengths": ["Async programming", "Database design", "API Design"],
        "weaknesses": ["Docker best practices", "Performance optimization"],
        "execution_time_seconds": 45.23,
        "agent_version": "1.0"
    }
    
    st.json(example_output)

with tab3:
    st.header("📖 Documentación")
    
    st.markdown("""
    ### 🏗️ Arquitectura
    
    Este agente implementa un flujo de 3 fases:
    
    1. **Generación de Preguntas** (LangChain + GPT-3.5)
       - Recibe: rol, nivel, stack tecnológico
       - Genera: 5 preguntas técnicas relevantes
       - Output: Lista de preguntas tipadas
    
    2. **Evaluación de Respuestas** (LangChain + GPT-3.5)
       - Recibe: pregunta + respuesta del candidato
       - Evalúa: score 0-100 + feedback
       - Output: Resultado detallado de evaluación
    
    3. **Cálculo de Métricas** (Python puro)
       - Calcula: promedio, fortalezas, debilidades
       - Genera: recomendación final
       - Output: Reporte JSON estructurado
    
    ### 🔧 Stack Tecnológico
    
    - **Frontend:** Streamlit
    - **LLM:** OpenAI GPT-3.5-turbo vía LangChain
    - **Tipado:** Pydantic v2
    - **Lenguaje:** Python 3.9+
    
    ### 📊 Estructura de Evaluación
    
    - **No cumple:** Score < 50
    - **Cumple:** Score 50-75
    - **Sobrecualificado:** Score ≥ 75
    
    ### ⚡ Mejores Prácticas
    
    ✅ Prompts estructurados con formato JSON esperado
    ✅ Outputs tipados con Pydantic BaseModel
    ✅ Separación clara de responsabilidades
    ✅ Manejo robusto de errores
    ✅ UI intuitiva con Streamlit
    ✅ Trazabilidad del flujo de ejecución
    
    ### 🔐 Seguridad
    
    ⚠️ La API key se configura mediante variable de entorno
    ⚠️ Nunca hardcodees secrets en el código
    ⚠️ Usa `.env` local durante desarrollo
    """)

st.divider()
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: gray;">
    <small>Technical Interviewer Agent v1.0 | Powered by LangChain + OpenAI</small>
</div>
""", unsafe_allow_html=True)
