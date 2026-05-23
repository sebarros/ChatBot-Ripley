# 🛍️ Ripley Agent - Asistente Inteligente de Compras y Clima

Sistema de agente inteligente conversacional que actúa como asistente de compras para Ripley Chile, capaz de consultar clima, recomendar ropa y buscar productos utilizando herramientas externas, memoria y planificación de intenciones.

---

## 📌 Descripción General

Este proyecto implementa un **agente autónomo basado en LLM (GPT-4.1-mini)** que:

- Interpreta mensajes del usuario
- Decide qué herramienta usar (clima, productos, catálogo)
- Mantiene memoria corta y larga del usuario
- Genera respuestas naturales con contexto
- Recomienda productos según clima o intención de compra

---

## 🧠 Arquitectura del Sistema

El sistema está compuesto por 5 módulos principales:

### 1. `ripley_agent.py` (Agente principal)
- Orquesta todo el flujo del sistema
- Maneja memoria, planner y herramientas
- Construye el prompt final para el LLM
- Ejecuta el loop conversacional

### 2. `planner.py` (Clasificador de intención)
- Detecta la intención del usuario usando regex
- Decide qué herramienta usar:
  - 🌤️ clima
  - 🛍️ búsqueda de productos
  - 📦 listado de productos

### 3. `api_clients.py` (Integraciones externas)
- `WeatherAPIClient`: obtiene clima desde Open-Meteo
- `ProductAPIClient`: obtiene productos desde FakeStore API

### 4. `tools.py` (Herramientas del agente)
Implementa funciones reutilizables:

- 🌤️ `weather_tool`: consulta clima por ciudad
- 🔎 `search_product_tool`: busca productos por texto
- 📋 `list_products_tool`: muestra catálogo

Todas están registradas en `TOOL_MAP`.

### 5. `memory.py` (Sistema de memoria)
- 🧠 Memoria corta (últimos 15 mensajes)
- 🧠 Memoria larga (perfil del usuario)
- 📌 Estado conversacional (ej: recomendación post-clima)
- 🔎 Recuperación semántica simple con similitud de texto

---

## 🔄 Flujo del Agente

1. Usuario envía mensaje  
2. Se guarda en memoria corta  
3. Planner detecta intención  
4. Se ejecuta herramienta correspondiente:
   - Clima → API Open-Meteo
   - Productos → FakeStore API  
5. Se construye contexto + perfil + resultado tool  
6. LLM genera respuesta final  
7. Se guarda en memoria  

---

## 🌤️ Funcionalidad de Clima + Recomendación

Cuando el usuario consulta el clima:

1. Se obtiene ciudad (default: Puerto Montt)
2. Se consulta API meteorológica
3. El agente activa estado `SHOW_PRODUCTS`
4. En el siguiente mensaje afirmativo del usuario:
   - Recomienda ropa automáticamente

---

## 🛍️ Funcionalidades de Productos

El agente puede:

- Buscar productos por texto
- Listar catálogo completo
- Recomendar productos si el clima lo sugiere

📦 Fuente de datos: https://fakestoreapi.com