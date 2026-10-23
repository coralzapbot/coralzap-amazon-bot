
import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=15,
    ).raise_for_status()

@app.get("/")
def home():
    return "CoralZap está funcionando."

@app.post("/webhook")
def webhook():
    data = request.get_json(silent=True) or {}
    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "").strip().lower()

    if not chat_id or not text:
        return {"ok": True}

    if text in ("/start", "/start@coralzap_bot"):
        reply = (
            "¡Hola! Soy CoralZap, tu cazachollos de Amazon España. "
            "Estoy en fase de configuración. "
            "Pronto prepararemos las alertas de descuentos del 70% o más."
        )
    elif text.startswith("/ayuda"):
        reply = "Comandos disponibles: /start y /ayuda"
    else:
        reply = "Todavía estoy aprendiendo. Prueba /ayuda."

    send_message(chat_id, reply)
    return {"ok": True}
