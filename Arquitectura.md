┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND                       │
│  (Interfaz: rol, nivel, stack → input de candidato)        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│             AGENT ORCHESTRATOR (main.py)                    │
│  - Validación de inputs                                    │
│  - Coordinación de flujos                                  │
│  - Trazabilidad de ejecución                               │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ QUESTION     │ │ EVALUATION   │ │ SCORING      │
│ GENERATOR    │ │ ENGINE       │ │ ENGINE       │
│ (LangChain)  │ │ (LangChain)  │ │ (Logic)      │
└──────────────┘ └──────────────┘ └──────────────┘
        │            │               │
        └────────────┼───────────────┘
                     ▼
        ┌────────────────────────┐
        │  OUTPUT FORMATTER      │
        │  (TypedDict JSON)      │
        └────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   STREAMLIT RESULT     │
        │   (Display & Export)   │
        └────────────────────────┘
