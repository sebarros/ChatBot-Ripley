import streamlit as st
import os
import time
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage

# =========================
# CONFIG API
# =========================
OPENAI_API_KEY = os.getenv("GITHUB_TOKEN")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

if not OPENAI_API_KEY:
    st.error("Falta GITHUB_TOKEN en variables de entorno")
    st.stop()

# =========================
# MODELO
# =========================
llm = ChatOpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY,
    model="gpt-4.1-mini",
    temperature=0.2,
    streaming=True,
    max_tokens=250
)

# =========================
# EMBEDDINGS
# =========================
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY,
    openai_api_base=OPENAI_BASE_URL
)

# =========================
# BASE DE CONOCIMIENTO
# =========================
documents = [
    # COMPRAS
    "Para comprar en Ripley puedes ingresar a ripley.cl, buscar el producto que deseas y agregarlo al carrito. Luego debes completar el proceso de pago.",
    "Puedes comprar productos en Ripley tanto en tiendas físicas como a través de su sitio web.",
    "Para realizar una compra online debes seleccionar el producto, elegir talla o modelo, agregar al carrito y pagar.",
    "Ripley ofrece productos como ropa, tecnología, electrodomésticos y más.",
    
    # PAGOS
    "Puedes pagar con tarjeta Ripley, tarjetas de crédito y débito.",
    "Al comprar online puedes elegir diferentes medios de pago disponibles en la plataforma.",
    
    # DESPACHO
    "Los despachos demoran entre 2 y 5 días hábiles dependiendo de la región.",
    "Las compras online pueden ser enviadas a domicilio o retiradas en tienda.",
    "Las compras online pueden ser retiradas en tienda sin costo adicional.",
    
    # DEVOLUCIONES
    "Las devoluciones en Ripley se pueden realizar dentro de 10 días con boleta y producto en buen estado.",
    "Los cambios de productos están sujetos a disponibilidad de stock.",
    
    # GARANTÍA
    "Los productos cuentan con garantía legal de 6 meses.",
    
    # SEGUIMIENTO
    "Para seguimiento de pedidos debes ingresar a tu cuenta en ripley.cl.",
    
    # GENERAL
    "Ripley es una tienda por departamento que vende ropa, tecnología, calzado y artículos para el hogar."
]

vector_db = FAISS.from_texts(documents, embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 1})

# =========================
# MEMORIA: EXTRAER NOMBRE
# =========================
def extraer_nombre(texto):
    texto = texto.lower()
    if "me llamo" in texto:
        return texto.split("me llamo")[-1].strip().split()[0]
    return None

# =========================
# RESPUESTA CON STREAMING
# =========================
def responder_stream(pregunta, chat_history):

    docs = retriever.invoke(pregunta)
    context = "\n".join([d.page_content for d in docs])

    memoria = "\n".join(
        [f"{m['role']}: {m['content']}" for m in chat_history[-6:]]
    )

    nombre = st.session_state.get("user_name", "")

    system_prompt = """
Eres un asistente oficial de Ripley Chile.

REGLAS IMPORTANTES:

1. Para preguntas sobre Ripley (compras, devoluciones, despacho, etc):
   - SOLO usa el CONTEXTO entregado
   - Si no está en el contexto:
     "No tengo esa información en los documentos de Ripley."

2. Para preguntas sobre el usuario (nombre, datos personales, conversación):
   - USA la MEMORIA de la conversación
   - NO respondas con la frase de "no tengo información"

3. Si el usuario pregunta algo como:
   - "¿cómo me llamo?"
   - "¿recuerdas mi nombre?"
   → debes responder usando la memoria

4. Responde de forma natural, breve y amable.
"""

    prompt = f"""
CONTEXTO (Ripley):
{context}

MEMORIA CONVERSACIÓN:
{memoria}

NOMBRE USUARIO:
{nombre}

PREGUNTA:
{pregunta}
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]

    full = ""

    for chunk in llm.stream(messages):
        if chunk.content:
            full += chunk.content
            yield full
            time.sleep(0.02)

# =========================
# SESSION STATE
# =========================
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
    st.session_state.chats["Chat 1"] = []

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# =========================
# SIDEBAR
# =========================
st.sidebar.title("💬 Chats")

if st.sidebar.button("➕ Nuevo chat"):
    new_chat = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat] = []
    st.session_state.current_chat = new_chat
    st.session_state.user_name = ""  # reset nombre
    st.rerun()

selected = st.sidebar.radio(
    "Selecciona chat",
    list(st.session_state.chats.keys()),
    index=list(st.session_state.chats.keys()).index(st.session_state.current_chat)
)

st.session_state.current_chat = selected

# =========================
# UI PRINCIPAL
# =========================
st.title("🤖 Chatbot Ripley")

messages = st.session_state.chats[selected]

# historial
for m in messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# =========================
# INPUT
# =========================
if prompt := st.chat_input("Escribe tu mensaje..."):

    nombre_detectado = extraer_nombre(prompt)
    if nombre_detectado:
        st.session_state.user_name = nombre_detectado

    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        final = ""

        for partial in responder_stream(prompt, messages):
            placeholder.markdown(partial)
            final = partial

    messages.append({"role": "assistant", "content": final})