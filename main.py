import discord
from discord.ext import commands
from discord import app_commands
import math
import os
import threading
from flask import Flask

TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", 10000))

# =========================
# WEB SERVER (Render)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Farmly online!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)

# =========================
# BOT DISCORD
# =========================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

TAX = 0.10

# =========================
# CONVERTER VALORES
# k = mil
# m = milhão
# b = bilhão
# =========================
def convert(v):
    v = v.lower().replace(",", "").strip()

    if v.endswith("k"):
        return int(float(v[:-1]) * 1_000)
    elif v.endswith("m"):
        return int(float(v[:-1]) * 1_000_000)
    elif v.endswith("b"):
        return int(float(v[:-1]) * 1_000_000_000)
    else:
        return int(v)

# =========================
# BOT ONLINE
# =========================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Farmly online!")

# =========================
# COMANDO /tax
# =========================
@bot.tree.command(name="tax", description="Calcula taxa de 10%")
@app_commands.describe(valor="Exemplo: 10m, 500k, 1b")
async def tax(interaction: discord.Interaction, valor: str):

    try:
        amount = convert(valor)

        # Se enviar esse valor
        receive = int(amount * 0.9)
        tax_taken = amount - receive

        # Se quiser receber esse valor
        send_needed = math.ceil(amount / 0.9)
        tax_needed = send_needed - amount

        msg = f"""🌾 **Calculando taxa de 10% para :coin: {amount:,}**

📤 **Se você ENVIAR esse valor:**
Recebedor recebe: :coin: {receive:,}
(Taxa cobrada: {tax_taken:,})

📥 **Se você quiser RECEBER esse valor:**
Remetente precisa enviar: :coin: {send_needed:,}
(Taxa cobrada: {tax_needed:,})

━━━━━━━━━━━━━━━━━━
💰 **Farmly™ Calculadora de Trocas**"""

        await interaction.response.send_message(msg)

    except:
        await interaction.response.send_message(
            "❌ Valor inválido. Use exemplos: 10m, 500k, 1b",
            ephemeral=True
        )

# =========================
# INICIAR
# =========================
threading.Thread(target=run_web).start()
print("TOKEN:", TOKEN)
bot.run(TOKEN)