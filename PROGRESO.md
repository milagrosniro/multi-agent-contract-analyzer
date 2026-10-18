# PROGRESO — Proyecto Integrador LegalMove

## Estado actual
- [x] Fase 0 — Análisis de la consigna
- [ ] Fase 1 — Diseño (arquitectura + estructura de carpetas)
  - [x] Estructura de carpetas y archivos vacíos creada por Claude (excepción: tarea mecánica), incl. `.gitignore` y `.env.example`
  - [x] Paso 1 respondido. D1 (SDK OpenAI para visión), D2 (structured output + except ValidationError), D3 (spans manuales) ACEPTADAS
- [x] Paso 2 — Entorno: venv, pip install, git init. Versiones: langchain 1.4.6, langchain-openai 1.7.2,
  langfuse **5.0.2** (≠ v3 del curso → verificar API de spans en Paso 10), openai 3.35.1, pydantic 2.14.1
  - [x] requirements.txt regenerado en ASCII
- [ ] Paso 3 — Imágenes de prueba (falta solo `data/test_contracts/README.md`, lo escribe el estudiante)
  - [x] 8 PNG (150 dpi, A4) en `data/test_contracts/` generados por Claude (excepción: tarea mecánica): `documento_{1,2,3}__{original,enmienda}.png` (del docx) + `documento_4` = par simple propio (Mantenimiento: solo cláusula 3, USD 2.500→2.800 y vencimiento día 10→5)
  - [x] PDFs convertidos a PNG y eliminados
- [ ] Fase 2..N — Construcción
- [ ] Fase final — Preparación de la defensa

## Checklist de requisitos (con puntaje de la rúbrica)

### Obligatorios — código
| # | Requisito | Archivo | Pts | Hecho |
|---|-----------|---------|-----|-------|
| R1 | `parse_contract_image(path)`: valida JPEG/PNG → base64 → GPT-4o Vision → texto fiel respetando jerarquía (cláusulas/secciones) | `src/image_parser.py` | 15 | [ ] |
| R2 | `ContextualizationAgent`: recibe 2 textos → mapa de estructura comparada (NO extrae cambios). System prompt propio ("Analista Senior") | `src/agents/contextualization_agent.py` | 15 | [ ] |
| R3 | `ExtractionAgent`: recibe mapa + 2 textos → cambios (adición / eliminación / modificación) en JSON. System prompt propio ("Auditor") | `src/agents/extraction_agent.py` | (R2) + 15 prompting | [ ] |
| R4 | `ContractChangeOutput` (Pydantic): `sections_changed: List[str]`, `topics_touched: List[str]`, `summary_of_the_change: str` + descripciones de campo; validar con `model_validate()` o structured output; manejar `ValidationError` con mensajes claros | `src/models.py` | 10 | [ ] |
| R5 | Langfuse: span raíz `contract-analysis` + hijos `parse_original_contract`, `parse_amendment_contract`, `contextualization_agent`, `extraction_agent`, con input/output/latencia/tokens/metadata | `src/main.py` | 15 | [ ] |
| R6 | Manejo de errores: timeouts, rate limits, límite de tokens, archivo inexistente/formato inválido, encoding; nada hardcodeado | todos | 10 | [ ] |
| R7 | `main.py` acepta 2 paths por argumento y corre todo el pipeline | `src/main.py` | — | [ ] |

### Obligatorios — entregables
| # | Entregable | Hecho |
|---|-----------|-------|
| E1 | Repo público en GitHub | [ ] |
| E2 | `data/test_contracts/`: mínimo 2 pares (4 imágenes) + README (par simple + par complejo) | [ ] |
| E3 | `README.md`: diagrama, arquitectura, setup, uso, decisiones técnicas | [ ] (10 pts) |
| E4 | `requirements.txt` con versiones FIJADAS (`==`) + `.env.example` | [ ] |

### Defensa en vivo (10 pts + todo lo demás se valida ahí)
- [ ] Contar contexto LegalMove y problema
- [ ] Demo en vivo con 2 pares (simple y complejo)
- [ ] Explicar traza en Langfuse: spans, inputs/outputs de cada agente, tokens, latencia
- [ ] Responder: ¿por qué 2 agentes y no 1? ¿por qué GPT-4o para parsing? ¿cómo diseñaste los prompts? ¿cómo manejás errores de validación?

## Mapa requisito → material del curso
| Requisito | Dónde se ve en el curso | Nota |
|-----------|------------------------|------|
| R1 Visión + base64 | **M4** `M4/lectures/video-sh-m4l1-main/extract_form_data.py` (`encode_image` + `image_url` con `data:...;base64` + `detail: "high"` + GPT-4o) | Ojo: hardcodea `image/jpeg` aunque sea PNG → nosotros elegimos el MIME según la extensión. Usa `except Exception` genérico (= "Satisfactorio" en rúbrica 2.2). |
| R4 Pydantic avanzado | **M4** `henry-m4-multimodal-architecture/src/henry_m4/schemas.py` (`Field(description=...)`, `@field_validator`, `@model_validator`), `M4/lectures/.../extract_form_data.py` (`response_format=FormFields`), `validation_script.py` (`except ValidationError` + `e.json()`) | La rúbrica pide descripciones de campo → patrón de `schemas.py`. |
| R6 Errores / self-healing | **M4** `henry-m4-multimodal-architecture/src/henry_m4/vision_engine.py` (`PipelineVisionAutoreparable`: reintenta pasándole al LLM el error de Pydantic) | Candidato a "manejo elegante de errores de validación". |
| R6 Config sin hardcodear | **M4** `henry-m4-multimodal-architecture/src/henry_m4/config.py` (`Settings` dataclass + `os.getenv` con defaults) | Sus modelos default son ficticios; nosotros usamos `gpt-4o` (lo exige la consigna). |
| Modo offline (opcional) | **M4** `ModeloGuionadoVision` en `vision_engine.py` | Idea: desarrollar/testear sin gastar API. Decisión de diseño tuya. |
| R2/R3 Agentes y handoff | `M3/L3/lectures/.../collaboration_patterns.py` (clase Agent, handoff), `M3/henry-ai-engineering/clases/02_langchain_rag.py` (LangChain), `M3/L1/02_workflows_vs_agentes.ipynb` | Clave para la defensa: ¿esto es "agente" o "workflow"? |
| R4 Pydantic | `clases/03_multiagente_langgraph.py:469` (`with_structured_output`), `clases/02_langchain_rag.py:202` (`model_validate`) | Las dos vías que acepta la rúbrica. |
| R5 Langfuse | `M3/L4/lectures/video-2-langfuse/multi_agent_langfuse.py` (span raíz + hijos), `clases/04_produccion_llmops.py`, `M3/henry-ai-engineering/src/henry_agents/operations.py` (`CallbackHandler`: captura tokens de LangChain automáticamente) | Ojo: verificar API según versión instalada de langfuse. |
| R6 dotenv | mismo archivo de L4 (`load_dotenv()` + `os.getenv`) | |

## Contratos de prueba (Recursos adicionales)
Archivos: `Contratos y Enmiendas de ejemplo.docx` (texto de 3 pares) y
`Diferencias entre Contratos y Enmiendas de ejemplo.docx` (cambios esperados = "respuesta correcta").
- **Faltan las imágenes** `documento_{1,2,3}__{original,enmienda}.jpg` que nombra el doc de diferencias.
- Par 1 Licencia de Software: plazo, pago, soporte, terminación + cláusula 7 nueva.
  ⚠️ **Cambio NO listado en el doc oficial**: cláusula 1 elimina "intransferible" y cambia
  "únicamente para fines internos de la empresa" → "para operaciones internas de negocio".
  Prueba de fidelidad: el sistema debería detectarlo (argumento fuerte en la defensa).
- Par 2 Consultoría: alcance, duración, honorarios, entregables + cláusula 7 nueva.
- Par 3 SaaS: precio, disponibilidad, soporte. Título dice "VERSIÓN ACTUALIZADA" (no "Enmienda"):
  es un contrato re-expresado completo, no una adenda parcial.
- Consigna pide un caso "simple (una cláusula)": ninguno lo es estrictamente; el par 3 es el más simple.
  Evaluar crear un par propio de 1 cambio.

## Decisiones de diseño (y por qué)
_(se completa en Fase 1)_

## Conceptos aprendidos
- **Mapa vs textos (Paso 1):** el mapa es el ÍNDICE (dónde mirar), los textos son la EVIDENCIA
  (qué dice literalmente). El resumen pierde detalle → el Agente 2 necesita ambos (ej. "intransferible").
- **Por qué 2 agentes:** responsabilidad única, prompts especializados, depurabilidad por span en Langfuse;
  la rúbrica penaliza solapamiento.
- **base64:** codifica bytes binarios como texto para viajar dentro del JSON de la API.
  ⚠️ Pesa ~33% MÁS, no menos (error corregido). Alternativa: URL pública.
- **Repaso pendiente:** reforzar base64 en el simulacro de defensa.

## Pendientes / preguntas abiertas
- ~~Falta M4~~ → revisado (solo trae L1: visión + Pydantic + self-healing; L4/L5 del README no están incluidos).
- Nivel de Python del estudiante
- Fecha de entrega / defensa
- ¿Tenemos los contratos de "Recursos adicionales" o hay que generarlos?
- ¿Cuenta de GitHub, API key de OpenAI con crédito y cuenta en Langfuse listas?
