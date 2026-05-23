"""
email_sender.py - Envio de promociones Ripley
============================================
Envía correos promocionales personalizados con SMTP (Gmail)
basados en la sesión del agente Ripley (clima + productos).
"""

import os
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime


# =========================
# ENVIO DE EMAIL
# =========================
def enviar_promocion(asunto: str, cuerpo_html: str, destinatario: str = None):

    remitente = os.getenv("EMAIL_FROM", "ripley.bot@gmail.com")
    password = os.getenv("EMAIL_PASSWORD", "")
    destino_default = os.getenv("EMAIL_TO", "cliente@correo.com")
    destino = destinatario or destino_default

    if not password:
        return "[!] EMAIL_PASSWORD no configurado en .env"

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destino

    msg.set_content("Tu cliente de correo no soporta HTML.")

    msg.add_alternative(cuerpo_html, subtype="html")

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(remitente, password)
            server.send_message(msg)

        return f"[OK] Promoción enviada a {destino}"

    except smtplib.SMTPAuthenticationError:
        return (
            "[!] Error SMTP Gmail\n"
            "Activa verificación en 2 pasos y usa App Password:\n"
            "https://myaccount.google.com/security"
        )

    except Exception as e:
        return f"[!] Error enviando correo: {e}"


# =========================
# GENERADOR HTML PROMOCIONAL RIPLEY
# =========================
def generar_email_ripley(cliente: str, clima: dict = None, productos: list = None):

    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Clima formateado
    clima_html = ""
    if clima:
        clima_html = f"""
        <div style="background:#e3f2fd;padding:15px;border-radius:10px;margin-bottom:20px;">
            <h3 style="margin:0;color:#0d47a1;">🌤️ Clima actual</h3>
            <p style="margin:5px 0;">
                {clima.get('city','')} → {clima.get('temperature','?')}°C | Viento {clima.get('windspeed','?')} km/h
            </p>
        </div>
        """

    # Productos
    productos_html = ""
    if productos:
        cards = ""
        for p in productos[:5]:
            cards += f"""
            <div style="border:1px solid #eee;border-radius:10px;padding:10px;margin:10px 0;">
                <p style="margin:0;font-weight:bold;">{p.get('title','Producto')}</p>
                <p style="margin:5px 0;color:#d32f2f;">${p.get('price','')}</p>
            </div>
            """

        productos_html = f"""
        <div>
            <h3 style="color:#111;">🛍️ Recomendaciones para ti</h3>
            {cards}
        </div>
        """

    html = f"""
    <html>
    <head><meta charset="utf-8"></head>

    <body style="font-family:Arial;background:#f5f5f5;margin:0;padding:0;">

        <div style="max-width:650px;margin:20px auto;background:white;border-radius:12px;overflow:hidden;">

            <!-- HEADER -->
            <div style="background:linear-gradient(90deg,#e60012,#ff4d4d);color:white;padding:20px;text-align:center;">
                <h1 style="margin:0;">🛍️ Ripley Chile</h1>
                <p style="margin:5px 0;">Ofertas personalizadas para ti</p>
            </div>

            <!-- BODY -->
            <div style="padding:20px;">

                <p style="font-size:16px;">
                    Hola <strong>{cliente}</strong>, hemos preparado recomendaciones especiales para ti.
                </p>

                <p style="font-size:12px;color:#888;">
                    Generado el {ahora}
                </p>

                {clima_html}

                {productos_html}

                <!-- CTA -->
                <div style="text-align:center;margin-top:30px;">
                    <a href="https://www.ripley.cl"
                       style="background:#e60012;color:white;padding:12px 20px;
                       text-decoration:none;border-radius:8px;font-weight:bold;">
                        Ver más ofertas en Ripley
                    </a>
                </div>

            </div>

            <!-- FOOTER -->
            <div style="background:#111;color:#bbb;text-align:center;padding:15px;font-size:12px;">
                Ripley Chile © 2026 - Recomendaciones automáticas del asistente inteligente
            </div>

        </div>

    </body>
    </html>
    """

    return html