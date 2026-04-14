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
# DISCORD BOT
# =========================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

TAX = 0.10

# Converter valores
# k = mil
# m = milhão
# b = bilhão
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

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Farmly online!")

# =========================
# /tax
# =========================
@bot.tree.command(name="tax", description="Calculate 10% transaction tax")
@app_commands.describe(valor="Example: 10m, 500k, 1b")
async def tax(interaction: discord.Interaction, valor: str):

    try:
        amount = convert(valor)

        # Se enviar esse valor
        receive = int(amount * (1 - TAX))
        tax_taken = amount - receive

        # Se quiser receber esse valor
        send_needed = math.ceil(amount / (1 - TAX))
        tax_needed = send_needed - amount

        msg = f"""🌾 Calculating 10% transaction tax for {amount:,}

📤 If you SEND this amount:
Receiver gets: {receive:,}
(Tax taken: {tax_taken:,})

📥 If you want to RECEIVE this amount:
Sender must send: {send_needed:,}
(Tax taken: {tax_needed:,})"""

        await interaction.response.send_message(msg)

    except:
        await interaction.response.send_message(
            "❌ Invalid value. Use examples: 10m, 500k, 1b",
            ephemeral=True
        )

# =========================
# RUN
# =========================
threading.Thread(target=run_web).start()
bot.run(TOKEN)