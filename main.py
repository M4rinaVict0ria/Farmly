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

TAX = 0.10

CANAL_TAX = 1493431079464603668
CANAL_VALOR = 1493433809264185344

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

    if interaction.channel.id != CANAL_TAX:
        await interaction.response.send_message(
            "❌ Use o comando de TAX no canal #🏧││calcular",
            ephemeral=True
        )
        return

    try:
        amount = convert(valor)

        receive = int(amount * 0.9)
        tax_taken = amount - receive

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
# COMANDO /valor
# =========================
@bot.tree.command(name="valor", description="Ver valor de veículo")
@app_commands.describe(nome="Nome do veículo")
async def valor(interaction: discord.Interaction, nome: str):
    
    if interaction.channel.id != CANAL_VALOR:
        await interaction.response.send_message(
            "❌ Use o comando de VALOR no canal #💸│checar-valor.",
            ephemeral=True
        )
        return

    nome = nome.lower()

    if nome in vehicles:
        v = vehicles[nome]

        msg = f"""🚜 **{v['nome']}**

📦 **Obtenção:**
{v['obtainable']}

📝 **Nota:**
{v['nota']}

💰 **Valor:**
:fafcoin: {v['valor']}

📈 **Estabilidade:**
{v['stability']}

🔥 **Demanda:**
{v['demand']}

💎 **Raridade:**
{v['rarity']}

━━━━━━━━━━━━━━━━━━
🌾 **Farmly™ Valores FAF**"""

    else:
        msg = "❌ Veículo não encontrado."

    await interaction.response.send_message(msg)

# =========================
# INICIAR
# =========================
threading.Thread(target=run_web).start()
bot.run(TOKEN)