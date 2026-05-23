import streamlit as st
import re
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# =========================
# CONFIG LLM
# =========================
llm = ChatOpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),  # cambia si usas Azure
    model="gpt-4o-mini",
    temperature=0.3
)

# =========================
# FUNCIONES DE CHUNKING (DEL PROFE)
# =========================
def chunking_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []

    if overlap >= chunk_size:
        overlap = chunk_size - 1

    step = max(1, chunk_size - overlap)

    for i in range(0, len(words), step):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)

        if i + chunk_size >= len(words):
            break

    return chunks

def chunking_by_sentences(text, max_sentences=5, overlap_sentences=1):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []

    if overlap_sentences >= max_sentences:
        overlap_sentences = max_sentences - 1

    step = max(1, max_sentences - overlap_sentences)

    for i in range(0, len(sentences), step):
        chunk_sentences = sentences[i:i + max_sentences]
        chunk = '. '.join(chunk_sentences) + '.'
        chunks.append(chunk)

        if i + max_sentences >= len(sentences):
            break

    return chunks

def chunking_by_paragraphs(text):
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]

def chunking_by_characters(text, chunk_size=500, overlap=100):
    chunks = []

    if overlap >= chunk_size:
        overlap = chunk_size - 1

    step = max(1, chunk_size - overlap)

    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

        if i + chunk_size >= len(text):
            break

    return chunks

# =========================
# INTENCIÓN
# =========================
def clasificar_intencion(mensaje):
    prompt = f"""
    Clasifica en una palabra:
    compra, reclamo, seguimiento, informacion

    Mensaje: {mensaje}
    """
    try:
        return llm.invoke(prompt).content.strip().lower()
    except:
        return "informacion"

def obtener_system_prompt(intencion):
    if "reclamo" in intencion:
        return "Eres soporte Ripley, responde con empatia y solución."
    elif "compra" in intencion:
        return "Eres vendedor Ripley, recomienda productos."
    elif "seguimiento" in intencion:
        return "Eres asistente de pedidos, informa estado de envíos."
    else:
        return "Eres asistente general de Ripley."

# =========================
# UI
# =========================
st.set_page_config(page_title="RipleyBot + Chunking", layout="wide")

st.title("🤖 CHATBOT RIPLEY CHILE")

# Sidebar
st.sidebar.header("⚙️ Configuración")

chunking_method = st.sidebar.selectbox(
    "Método de chunking:",
    ["Por palabras", "Por oraciones", "Por párrafos", "Por caracteres"]
)

if chunking_method == "Por palabras":
    chunk_size = st.sidebar.slider("Tamaño chunk", 50, 500, 150)
    overlap = st.sidebar.slider("Overlap", 0, 100, 20)

elif chunking_method == "Por oraciones":
    max_sentences = st.sidebar.slider("Oraciones por chunk", 1, 10, 5)
    overlap_sentences = st.sidebar.slider("Overlap oraciones", 0, 3, 1)

elif chunking_method == "Por caracteres":
    chunk_size = st.sidebar.slider("Tamaño caracteres", 100, 2000, 500)
    overlap = st.sidebar.slider("Overlap caracteres", 0, 500, 100)

# =========================
# BASE DE CONOCIMIENTO
# =========================
st.header("📚 Base de conocimiento")

input_method = st.radio(
    "Fuente:",
    ["Texto manual", "Texto de ejemplo"]
)

example_texts = {
    "Políticas Ripley": """Las devoluciones se pueden realizar dentro de 10 días con boleta.
Los despachos demoran entre 2 y 5 días hábiles.
Puedes retirar en tienda sin costo.
Garantía legal de 6 meses.
Pagos con tarjeta crédito, débito y Ripley.
Seguimiento en ripley.cl.""",

    "FAQ Ecommerce": """¿Cuánto demora el despacho? Entre 2 y 5 días hábiles.
¿Cómo devuelvo un producto? Con boleta dentro de 10 días.
¿Puedo retirar en tienda? Sí, sin costo adicional.
¿Qué pasa si el producto falla? Tiene garantía legal de 6 meses.""",

    "Texto IA": """La inteligencia artificial es una rama de la informática que permite a las máquinas aprender.
El aprendizaje automático permite mejorar con datos.
Las redes neuronales imitan el cerebro humano."""
}

if input_method == "Texto manual":
    text_input = st.text_area("Ingresa texto:", height=200)
else:
    selected = st.selectbox("Selecciona ejemplo:", list(example_texts.keys()))
    text_input = example_texts[selected]
    st.text_area("Contenido:", value=text_input, height=200, disabled=True)

procesar = st.button("🔄 Procesar conocimiento")

# =========================
# PROCESAMIENTO + RAG
# =========================
if procesar and text_input.strip():

    if chunking_method == "Por palabras":
        chunks = chunking_text(text_input, chunk_size, overlap)

    elif chunking_method == "Por oraciones":
        chunks = chunking_by_sentences(text_input, max_sentences, overlap_sentences)

    elif chunking_method == "Por párrafos":
        chunks = chunking_by_paragraphs(text_input)

    else:
        chunks = chunking_by_characters(text_input, chunk_size, overlap)

    st.success(f"{len(chunks)} chunks creados")

    # Mostrar chunks
    for i, c in enumerate(chunks):
        with st.expander(f"Chunk {i+1}"):
            st.write(c)

    # Crear embeddings + FAISS
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("GITHUB_TOKEN")
    )

    vector_db = FAISS.from_texts(chunks, embeddings)
    st.session_state["retriever"] = vector_db.as_retriever()

# =========================
# CHATBOT
# =========================
st.header("💬 Chat con RipleyBot")

user_input = st.text_input("Escribe tu pregunta:")

if user_input and "retriever" in st.session_state:

    retriever = st.session_state["retriever"]

    docs = retriever.invoke(user_input)
    context = "\n".join([d.page_content for d in docs])

    # 🔥 filtro opcional
    if not docs or len(context.strip()) < 20:
        st.write("🤖 Respuesta")
        st.write("Lo siento, solo puedo ayudarte con información relacionada a Ripley.")
    
    else:
        intencion = clasificar_intencion(user_input)
        system_prompt = obtener_system_prompt(intencion)

        # ✅ AQUÍ defines prompt SIEMPRE
        prompt = f"""
        {system_prompt}

        Contexto:
        {context}

        Pregunta del usuario:
        {user_input}

        Instrucciones:
        - Responde SOLO con información del contexto
        - Si no está en el contexto, di:
          "Lo siento, solo puedo ayudarte con información relacionada a Ripley."
        """

        response = llm.invoke(prompt)

        st.write("🤖 Respuesta")
        st.write(response.content)

elif user_input:
    st.warning("Primero procesa la base de conocimiento 👆")