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
# MODELO OPTIMIZADO (MENOS COSTO)
# =========================
llm = ChatOpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY,
    model="gpt-4.1-mini",   
    temperature=0.2,
    streaming=True,
    max_tokens=150        
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
# BASE DE CONOCIMIENTO (RIPLEY)
# =========================
documents = [
    "Las devoluciones en Ripley se pueden realizar dentro de 10 días con boleta y producto en buen estado.",
    "Los despachos demoran entre 2 y 5 días hábiles dependiendo de la región.",
    "Las compras online pueden ser retiradas en tienda sin costo adicional.",
    "Los productos cuentan con garantía legal de 6 meses.",
    "Puedes pagar con tarjeta Ripley, tarjetas de crédito y débito.",
    "Para seguimiento de pedidos debes ingresar a tu cuenta en ripley.cl.",
    "Los cambios de productos están sujetos a disponibilidad de stock."
]

vector_db = FAISS.from_texts(documents, embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 1})  # 🔥 menos tokens

# =========================
# MEMORIA POR CHAT
# =========================
def get_chat_memory(chat_id):
    return st.session_state.chats[chat_id]

# =========================
# RESPUESTA CON STREAMING
# =========================
def responder_stream(pregunta, chat_history):

    docs = retriever.invoke(pregunta)
    context = "\n".join([d.page_content for d in docs])

    # 🔥 solo últimos mensajes (reduce tokens)
    memoria = "\n".join(
        [f"{m['role']}: {m['content']}" for m in chat_history[-4:]]
    )

    system_prompt = """
Eres un asistente oficial de Ripley Chile.

REGLAS:
- SOLO puedes responder usando el contexto entregado.
- Si no está en el contexto, responde: 
  "No tengo esa información en los documentos de Ripley."
- Puedes recordar el nombre del usuario si aparece en la conversación.
- Responde natural, breve y amable.
- NO inventes información externa.
"""

    prompt = f"""
CONTEXTO:
{context}

MEMORIA:
{memoria}

USUARIO:
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
            time.sleep(0.02)  # streaming más suave

# =========================
# SESSION STATE (MULTI CHAT)
# =========================
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
    st.session_state.chats["Chat 1"] = []

# =========================
# SIDEBAR
# =========================
st.sidebar.title("💬 Chats")

if st.sidebar.button("➕ Nuevo chat"):
    new_chat = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat] = []
    st.session_state.current_chat = new_chat
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