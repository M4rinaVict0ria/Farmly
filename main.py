import discord
from discord.ext import commands
from discord import app_commands
import math
import os
import threading
from flask import Flask
from values import vehicles

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

# =========================
# CONVERTER VALORES
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
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print("Sync error:", e)

    print("Farmly online!")

# =========================
# /tax
# =========================
@bot.tree.command(name="tax", description="Calcula taxa de 10%")
@app_commands.describe(valor="Exemplo: 10m, 500k, 1b")
async def tax(interaction: discord.Interaction, valor: str):

    try:
        amount = convert(valor)

        receive = int(amount * 0.9)
        send_needed = math.ceil(amount / 0.9)

        msg = f"""🌾 **Calculando taxa de 10% para 💰 {amount:,}**

📤 Se enviar:
Recebe: {receive:,}

📥 Para receber esse valor:
Enviar: {send_needed:,}

━━━━━━━━━━━━━━
Farmly™"""

        await interaction.response.send_message(msg)

    except Exception:
        await interaction.response.send_message(
            "❌ Valor inválido. Use exemplos: 10m, 500k, 1b",
            ephemeral=True
        )

# =========================
# /valor
# =========================
@bot.tree.command(name="valor", description="Mostra valor de veículos")
@app_commands.describe(nome="Nome do carro")
async def valor(interaction: discord.Interaction, nome: str):

    key = nome.lower().strip()

    if key not in vehicles:
        await interaction.response.send_message(
            "❌ Veículo não encontrado.",
            ephemeral=True
        )
        return

    car = vehicles[key]

    msg = f"""{car['nome']}
Obtainable:
{car['obtainable']}
📝 Note:
{car['note']}
Value:
:fafcoin: {car['value']}
Stability:
{car['stability']}
Demand:
{car['demand']}
Rarity:
{car['rarity']}
"""

    await interaction.response.send_message(msg)

# =========================
# START
# =========================
threading.Thread(target=run_web, daemon=True).start()
while True:
    try:
        bot.run(TOKEN)
    except Exception as e:
        print("Bot caiu:", e)