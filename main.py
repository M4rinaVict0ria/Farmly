import discord
from discord.ext import commands
from discord import app_commands
import math
import os
import threading
from flask import Flask
from values import vehicles

# =========================
# CONFIG
# =========================
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", 10000))

if not TOKEN:
    raise ValueError("TOKEN não encontrado nas variáveis de ambiente")

TAX = 0.10

CANAL_TAX = 1493431079464603668
CANAL_VALOR = 1493433809264185344

# =========================
# FLASK (Render keep alive)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Farmly online!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)

threading.Thread(target=run_web, daemon=True).start()

# =========================
# DISCORD BOT
# =========================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

synced = False

# =========================
# CONVERSOR DE VALORES
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

# normaliza vehicles (evita erro de "não encontrado")
vehicles_normalized = {k.lower(): v for k, v in vehicles.items()}

# =========================
# ON READY
# =========================
@bot.event
async def on_ready():
    global synced

    if not synced:
        await bot.tree.sync()
        synced = True

    print("🚜 Farmly online!")

# =========================
# /tax
# =========================
@bot.tree.command(name="tax", description="Calcula taxa de 10%")
@app_commands.describe(valor="Exemplo: 10m, 500k, 1b")
async def tax(interaction: discord.Interaction, valor: str):

    if interaction.channel.id != CANAL_TAX:
        await interaction.response.send_message(
            "❌ Use o comando de TAX no canal #🏧││calcular .",
            ephemeral=True
        )
        return

    try:
        amount = convert(valor)

        receive = int(amount * 0.9)
        tax_taken = amount - receive

        send_needed = math.ceil(amount / 0.9)
        tax_needed = send_needed - amount

        msg = f"""🌾 **Calculando taxa de 10% para 💰 {amount:,}**

📤 **Se você ENVIAR esse valor:**
Recebedor recebe: 💰 {receive:,}
(Taxa cobrada: {tax_taken:,})

📥 **Se você quiser RECEBER esse valor:**
Remetente precisa enviar: 💰 {send_needed:,}
(Taxa cobrada: {tax_needed:,})

━━━━━━━━━━━━━━━━━━
💰 Farmly™ Calculadora"""

        await interaction.response.send_message(msg)

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Valor inválido: {valor}",
            ephemeral=True
        )

# =========================
# /valor
# =========================
@bot.tree.command(name="valor", description="Ver valor de veículo")
@app_commands.describe(nome="Nome do veículo")
async def valor(interaction: discord.Interaction, nome: str):

    if interaction.channel.id != CANAL_VALOR:
        await interaction.response.send_message(
            "❌ Use o comando de VALOR no canal #💸│checar-valor .",
            ephemeral=True
        )
        return

    nome = nome.lower().strip()

    if nome in vehicles_normalized:
        v = vehicles_normalized[nome]

        msg = f"""🚜 **{v['nome']}**

📦 Obtenção:
{v['obtainable']}

📝 Nota:
{v['nota']}

💰 Valor:
💰 {v['valor']}

📈 Estabilidade:
{v['stability']}

🔥 Demanda:
{v['demand']}

💎 Raridade:
{v['rarity']}

━━━━━━━━━━━━━━━━━━
🌾 Farmly™ Valores FAF"""

    else:
        msg = "❌ Veículo não encontrado."

    await interaction.response.send_message(msg)

# =========================
# START BOT
# =========================
bot.run(TOKEN)