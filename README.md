#### Opción clásica: venv y pip

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
OPENAI_BASE_URL="https://models.inference.ai.azure.com"
GITHUB_BASE_URL="https://models.inference.ai.azure.com"
OPENAI_EMBEDDINGS_URL="https://models.github.ai/inference"
GITHUB_TOKEN="tu_github_token_aqui"
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY="tu_langsmith_api_key_aqui"
LANGSMITH_PROJECT="ingenieria_soluciones_con_ia"
```

**Cómo obtener tus tokens:**
- **GITHUB_TOKEN**: Ve a [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens) y crea un token con permisos de lectura. Asegúrate de tener acceso a [GitHub Models](https://github.com/marketplace/models).
- **LANGSMITH_API_KEY**: Crea una cuenta en [LangSmith](https://smith.langchain.com/) y genera una API key desde Settings.

> **IMPORTANTE:** Nunca subas tu archivo `.env` al repositorio. Ya está incluido en `.gitignore`.

### 4. Ejecutar Jupyter

Con el entorno activado:

```bash
jupyter lab
```

O sin activar el entorno (usa el `.venv` del proyecto):

```bash
uv run jupyter lab
```

Opcional: registrar el kernel de este entorno en Jupyter para elegirlo en la interfaz:

```bash
uv run python -m ipykernel install --user --name ingenieria-soluciones-ia --display-name "Python (ingenieria-soluciones-ia)"
```

---

## Estructura del Proyecto

```
RA1/  # Fundamentos de IA Generativa y Prompt Engineering
  IL1.1/  # Introducción a LLMs y conexión con APIs
  IL1.2/  # Técnicas de prompting (zero-shot, few-shot, chain-of-thought)
  IL1.3/  # Infraestructura RAG (Retrieval-Augmented Generation)
  IL1.4/  # Evaluación y optimización de LLMs

RA2/  # Desarrollo de Agentes Inteligentes con LLM
  IL2.1/  # Arquitectura y frameworks (LangChain, CrewAI)
  IL2.2/  # Memoria y herramientas externas (MCP)
  IL2.3/  # Planificación y orquestación de agentes
  IL2.4/  # Documentación técnica y diseño de arquitectura

RA3/  # Observabilidad, Seguridad y Ética en Agentes IA
  IL3.1/  # Herramientas de observabilidad y métricas
  IL3.2/  # Trazabilidad y procesamiento de logs
  IL3.3/  # Protocolos de seguridad y ética
  IL3.4/  # Escalabilidad y sostenibilidad
```

Cada subcarpeta IL contiene:
- **Notebooks (`.ipynb`)**: Prácticas guiadas paso a paso
- **Scripts Python (`.py`)**: Ejemplos ejecutables
- **Guías (`.md`)**: Teoría, patrones y mejores prácticas
- **README.md**: Objetivo y contexto de cada módulo

---

## Tecnologías y Librerías Principales

| Librería | Uso |
|----------|-----|
| `openai` | Cliente para APIs de modelos de lenguaje |
| `langchain` | Framework para construir aplicaciones con LLMs |
| `langchain-openai` | Integración LangChain con OpenAI |
| `langgraph` | Grafos de estado para agentes |
| `crewai` | Orquestación de sistemas multi-agente |
| `faiss-cpu` | Base de datos vectorial para RAG |
| `langsmith` | Observabilidad y evaluación de LLMs |
| `streamlit` | Interfaces web para demos |
| `pandas` / `numpy` | Procesamiento y análisis de datos |
| `matplotlib` / `plotly` | Visualización de datos |

---

## Navegación Recomendada

1. **Empieza por RA1** si eres nuevo en IA generativa y prompting
2. **RA2** para aprender a construir agentes inteligentes
3. **RA3** para llevar tus agentes a producción

Cada IL tiene ejemplos autocontenidos y README propio con explicaciones detalladas.

---

## Videotutoriales del Curso

Para un aprendizaje más visual, sigue la lista de reproducción completa:

[**Ver playlist en YouTube**](https://www.youtube.com/playlist?list=PL2gz3vdpKdfVHQqH39oPu4mxLrmAUd2eX)

---

## Evaluaciones y Entregables

| Tipo | Descripción | Peso |
|------|-------------|------|
| Quizzes | Evaluaciones formativas teóricas (1 por RA) | Variable |
| Proyectos Parciales | Proyectos prácticos con presentación (1 por RA) | Variable |
| Proyecto Final | Evaluación transversal integrando los 3 RA | 40% |

Los proyectos se desarrollan en parejas con presentación individual.

---

## Solución de Problemas Comunes

### Error de importación de módulos
```bash
# Asegúrate de tener el entorno virtual activado
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Error de API key
```bash
# Verifica que tu .env tenga las credenciales correctas
cat .env  # revisa que no estén vacías
```

### Problemas con Jupyter kernel
```bash
# Registrar el kernel del entorno virtual
python -m ipykernel install --user --name=curso-ia --display-name="Curso IA"
```

---

## Recursos Adicionales

- [LangChain Docs](https://python.langchain.com/)
- [CrewAI Docs](https://docs.crewai.com/)
- [OpenAI API](https://platform.openai.com/docs/)
- [LangSmith Docs](https://docs.smith.langchain.com/)
- [GitHub Models](https://github.com/marketplace/models)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## Contribuciones

Para dudas, sugerencias o mejoras, abre un issue o pull request.

Repositorio original del curso: [davila7/Ingenier-a-de-Soluciones-con-Inteligencia-Artificial](https://github.com/davila7/Ingenier-a-de-Soluciones-con-Inteligencia-Artificial)
