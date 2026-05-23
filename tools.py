from langchain_core.tools import Tool
from api_clients import WeatherAPIClient, ProductAPIClient

weather_client = WeatherAPIClient()
product_client = ProductAPIClient()


# =========================
# WEATHER TOOL
# =========================
def weather_tool(city: str):
    data = weather_client.get_weather(city)

    if not data or "error" in data:
        return f"No encontré el clima en {city}"

    return f"{data['city']} → {data['temperature']}°C, viento {data['windspeed']} km/h"


# =========================
# PRODUCT SEARCH
# =========================
def search_product_tool(query: str):
    products = product_client.get_products()

    results = [
        p for p in products
        if query.lower() in p["title"].lower()
    ]

    if not results:
        results = products[:5]

    out = "🛍️ Productos:\n"
    for p in results:
        out += f"- {p['title']} | ${p['price']}\n"

    return out

def send_email_tool(data: dict):
    html = generar_email_ripley(
        cliente=data.get("nombre", "cliente"),
        clima=data.get("clima"),
        productos=data.get("productos")
    )

    return enviar_promocion(
        asunto="🛍️ Ofertas personalizadas Ripley para ti",
        cuerpo_html=html,
        destinatario=data.get("email")
    )


# =========================
# LIST PRODUCTS
# =========================
def list_products_tool(_):
    products = product_client.get_products()

    out = "🛍️ Catálogo:\n"
    for p in products[:10]:
        out += f"- {p['title']} | ${p['price']}\n"

    return out


# =========================
# TOOL REGISTRY
# =========================
TOOL_LIST = [
    Tool(name="weather", func=weather_tool, description="Clima"),
    Tool(name="search_product", func=search_product_tool, description="Buscar productos"),
    Tool(name="list_products", func=list_products_tool, description="Listar productos")
]

TOOL_MAP = {t.name: t for t in TOOL_LIST}