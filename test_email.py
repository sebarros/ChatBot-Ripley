from email_sender import enviar_promocion, generar_email_ripley
from dotenv import load_dotenv
load_dotenv()

html = generar_email_ripley(
    cliente="Sebastián",
    clima={"city": "Puerto Montt", "temperature": 12, "windspeed": 20},
    productos=[
        {"title": "Chaqueta Impermeable", "price": 39990},
        {"title": "Parka Invierno", "price": 59990}
    ]
)

resultado = enviar_promocion(
    asunto="🛍️ Test Ripley - Ofertas para ti",
    cuerpo_html=html,
    destinatario="TU_CORREO_REAL@gmail.com"
)

print(resultado)