import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from planner import Planner
from tools import TOOL_MAP
from memory import MemoryManager
from email_sender import enviar_promocion, generar_email_ripley

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.2
)

planner = Planner()
memory = MemoryManager()


# =========================
# HELPERS
# =========================
def is_yes(text: str):
    return text.lower().strip() in ["si", "sí", "ok", "dale", "yes", "claro"]


def extract_city(text: str):
    text = text.lower()

    text = text.replace("dime el clima en", "")
    text = text.replace("clima en", "")
    text = text.replace("temperatura en", "")
    text = text.replace("que clima hay en", "")

    text = text.strip()

    return text if text else "puerto montt"


def run_tool(tool_name, input_text):
    tool = TOOL_MAP.get(tool_name)
    if not tool:
        return None
    return tool.func(input_text)


# =========================
# AGENTE
# =========================
def agent(user_input: str):

    memory.store_short(user_input)

    semantic_context = memory.retrieve_semantic(user_input)
    profile = memory.get_profile()

    state = memory.get_state()
    tool_result = None

    # =========================
    # FLUJO ESTADO
    # =========================
    if is_yes(user_input) and state == "SHOW_PRODUCTS":

        tool_result = run_tool("search_product", "chaqueta suéter bufanda")
        memory.set_state(None)

    else:

        plan = planner.create_plan(user_input)
        tool_name = plan.get("tool")

        # 🌤️ WEATHER FIX COMPLETO
        if tool_name == "weather":

            city = extract_city(user_input)

            print("DEBUG CITY:", city)

            tool_result = run_tool("weather", city)

            print("DEBUG WEATHER:", tool_result)

            memory.set_state("SHOW_PRODUCTS")

        elif tool_name == "search_product":
            tool_result = run_tool("search_product", user_input)

        elif tool_name == "list_products":
            tool_result = run_tool("list_products", user_input)

        else:
            tool_result = None

    # =========================
    # PROMPT FINAL
    # =========================
    prompt = f"""
Eres un asistente de compras de Ripley Chile.

REGLAS:
- Usa SOLO TOOL RESULT si existe
- No inventes información
- Si hay clima, recomienda ropa
- Si hay productos, muéstralos
- Mantén conversación natural

CONTEXTO:
{semantic_context}

PERFIL:
{json.dumps(profile, ensure_ascii=False)}

TOOL RESULT:
{tool_result}

USUARIO:
{user_input}
"""

    response = llm.invoke(prompt).content

    memory.store_response(response)

    return response


if __name__ == "__main__":
    print("\n🛍️ RIPLEY AGENTE FINAL CORREGIDO\n")

    while True:
        msg = input("Usuario: ")

        if msg.lower() == "exit":
            break

        print("\n🤖:", agent(msg), "\n")