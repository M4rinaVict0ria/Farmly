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
# FLASK (KEEP ALIVE)
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
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

synced = False

# =========================
# CONVERSOR
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

# normaliza vehicles
vehicles_normalized = {k.lower().strip(): v for k, v in vehicles.items()}

# =========================
# ON READY
# =========================
@bot.event
async def on_ready():
    global synced

    if not synced:
        await bot.tree.sync()
        synced = True

    print(f"🚜 Farmly online como {bot.user}")

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

        receive = int(amount * (1 - TAX))
        tax_taken = amount - receive

        send_needed = math.ceil(amount / (1 - TAX))
        tax_needed = send_needed - amount

        msg = f"""🌾 **Calculando taxa de 10% 💰 {amount:,}**

📤 ENVIANDO:
Recebe: 💰 {receive:,}
Taxa: {tax_taken:,}

📥 RECEBENDO:
Precisa enviar: 💰 {send_needed:,}
Taxa: {tax_needed:,}

━━━━━━━━━━━━━━
Farmly™"""

        await interaction.response.send_message(msg)

    except Exception:
        await interaction.response.send_message(
            "❌ Valor inválido. Ex: 10m, 500k, 1b",
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
            "❌ Use o comando VALOR no canal #💸│checar-valor .",
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

━━━━━━━━━━━━━━
Farmly™ Valores"""

    else:
        msg = "❌ Veículo não encontrado."

    await interaction.response.send_message(msg)

# =========================
# START
# =========================
if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    print("TOKEN:", TOKEN)bot.run(TOKEN)