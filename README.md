# technical-interviewer-langchain
Technical Interviewer Agent with LangChain

## Descripción

**Technical Interviewer Agent** es una aplicación diseñada para simular entrevistas técnicas de manera automatizada. Utiliza LangChain como framework principal para orquestar modelos de lenguaje que generan preguntas técnicas adaptadas a diferentes niveles y áreas de conocimiento, además de evaluar las respuestas proporcionadas por los candidatos.

El sistema está diseñado para ser extensible, permitiendo la personalización de categorías de preguntas, criterios de evaluación y formatos de entrevista. La arquitectura modular facilita la integración con diferentes proveedores de modelos de lenguaje y bases de datos.

## Características Principales

- **Generación Inteligente de Preguntas**: Crea preguntas técnicas adaptadas al nivel de experiencia y área de especialización del candidato.
- **Evaluación Automatizada**: Analiza respuestas utilizando modelos de lenguaje para proporcionar feedback detallado y puntuaciones objetivas.
- **Múltiples Categorías**: Soporte para diversas áreas técnicas como desarrollo de software, bases de datos, arquitectura de sistemas, DevOps, entre otras.
- **Sistema de Puntuación**: Motor de puntuación configurable que considera múltiples criterios de evaluación.
- **Interfaz Interactiva**: Aplicación Streamlit que proporciona una experiencia de usuario intuitiva y amigable.
- **Extensible**: Arquitectura modular que permite agregar nuevas funcionalidades y personalizar las existentes.

## Arquitectura del Sistema

El sistema sigue un patrón arquitectónico de **capas** que garantiza la separación de responsabilidades y facilita el mantenimiento:

```
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE PRESENTACIÓN                       │
│                        app.py                                │
│              (Interfaz de Usuario - Streamlit)               │
├─────────────────────────────────────────────────────────────┤
│                   CAPA DE ORQUESTACIÓN                       │
│                     orchestrator/                            │
│            (Coordina el flujo de ejecución)                  │
├─────────────────────────────────────────────────────────────┤
│                 CAPA DE NEGOCIO/LÓGICA                       │
│                       engines/                               │
│      (Procesamiento principal y reglas de negocio)          │
├─────────────────────────────────────────────────────────────┤
│                     CAPA DE DATOS                            │
│                       models/                                │
│            (Definición de estructuras de datos)             │
├─────────────────────────────────────────────────────────────┤
│                  CAPA DE CONFIGURACIÓN                       │
│                       config/                                │
│          (Parámetros y ajustes del sistema)                  │
├─────────────────────────────────────────────────────────────┤
│                    CAPA DE SOPORTE                           │
│                        utils/                                │
│          (Funciones auxiliares y utilidades)                 │
├─────────────────────────────────────────────────────────────┤
│                   CAPA DE PROMPTS                            │
│                       prompts/                               │
│        (Plantillas de texto para el LLM)                     │
└─────────────────────────────────────────────────────────────┘
```

### Descripción de las Capas

| Capa | Responsabilidad | Directorio/Archivo |
|------|-----------------|-------------------|
| Presentación | Interfaz de usuario y visualización | `app.py` |
| Orquestación | Coordinación del flujo de ejecución | `orchestrator/` |
| Negocio/Lógica | Procesamiento principal y reglas de negocio | `engines/` |
| Datos | Definición de estructuras y modelos de datos | `models/` |
| Configuración | Parámetros y ajustes del sistema | `config/` |
| Soporte | Funciones auxiliares y utilidades | `utils/` |
| Prompts | Plantillas de texto para modelos de lenguaje | `prompts/` |

## Estructura del Proyecto

```
technical-interviewer-agent/
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuración del sistema
├── models/
│   ├── __init__.py
│   ├── schemas.py               # Esquemas de datos (Pydantic)
│   └── evaluation_models.py     # Modelos de evaluación
├── prompts/
│   ├── __init__.py
│   └── templates.py             # Plantillas de prompts
├── engines/
│   ├── __init__.py
│   ├── question_generator.py    # Motor de generación de preguntas
│   ├── answer_evaluator.py      # Motor de evaluación de respuestas
│   └── scoring_engine.py        # Motor de puntuación
├── orchestrator/
│   ├── __init__.py
│   └── agent_orchestrator.py    # Orquestador principal del agente
├── utils/
│   ├── __init__.py
│   ├── logging.py               # Configuración de logging
│   └── validators.py            # Validadores auxiliares
├── app.py                       # Aplicación Streamlit
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Documentación principal
└── TECHNICAL_JUSTIFICATION.md   # Justificación técnica del diseño
```

## Instalación

### Requisitos Previos

- Python 3.10 o superior
- pip o poetry para gestión de dependencias
- Cuenta de API para el proveedor de LLM (OpenAI, Anthropic, etc.)

### Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/technical-interviewer-langchain.git
   cd technical-interviewer-langchain
   ```

2. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno**:
   ```bash
   cp .env.example .env
   # Editar el archivo .env con tus credenciales
   ```


### Archivo de Configuración

El archivo `config/settings.py` contiene parámetros adicionales que pueden ser personalizados:

- Categorías de preguntas disponibles
- Criterios de evaluación por defecto
- Pesos para el sistema de puntuación
- Configuración de la interfaz Streamlit

## Uso

### Ejecutar la Aplicación

Para iniciar la aplicación Streamlit:

```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`.

### Flujo de Uso

1. **Configuración de la Entrevista**: Selecciona el área técnica, nivel de dificultad y número de preguntas.
2. **Inicio de la Entrevista**: El sistema genera la primera pregunta automáticamente.
3. **Respuesta del Candidato**: El candidato escribe su respuesta en la interfaz.
4. **Evaluación**: El sistema evalúa la respuesta y proporciona feedback inmediato.
5. **Siguiente Pregunta**: Se genera la siguiente pregunta adaptada al rendimiento.
6. **Informe Final**: Al finalizar, se genera un reporte con el desempeño general.

## Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| langchain | ^0.1.0 | Framework para aplicaciones con LLM |
| langchain-openai | ^0.0.5 | Integración con OpenAI |
| streamlit | ^1.30.0 | Interfaz de usuario web |
| pydantic | ^2.0.0 | Validación de datos |
| python-dotenv | ^1.0.0 | Gestión de variables de entorno |

## Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y asegúrate de que los tests pasen
4. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Abre un Pull Request

### Guías de Contribución

- Sigue el estilo de código PEP 8
- Añade tests para nuevas funcionalidades
- Actualiza la documentación cuando sea necesario
- Mantén la compatibilidad con versiones anteriores

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**Autor**: Tu Nombre  
**Repositorio**: [technical-interviewer-langchain](https://github.com/tu-usuario/technical-interviewer-langchain)  
**Documentación Técnica**: Ver [TECHNICAL_JUSTIFICATION.md](TECHNICAL_JUSTIFICATION.md) para detalles sobre las decisiones de diseño.
