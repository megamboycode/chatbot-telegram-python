import requests
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
CHAVE_API_OPENROUTER = os.getenv("TOKEN_OPENROUTER")

bot = telebot.TeleBot(CHAVE_API_TELEGRAM)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "👋 Fala! Me manda algo 😄")

@bot.message_handler(func=lambda m: True)
def responder(msg):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {CHAVE_API_OPENROUTER}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": [
                    {"role": "system", "content": "Responda em português."},
                    {"role": "user", "content": msg.text}
                ]
            }
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        if response.status_code != 200:
            bot.reply_to(msg, f"⚠️ Erro HTTP {response.status_code}")
            return

        dados = response.json()

        if "choices" in dados:
            texto = dados["choices"][0]["message"]["content"]
            bot.reply_to(msg, texto)
        else:
            bot.reply_to(msg, f"⚠️ Erro da API:\n{dados}")

    except Exception as e:
        print("ERRO:", str(e))
        bot.reply_to(msg, "⚠️ Erro interno.")

print("🤖 rodando...")
bot.infinity_polling()