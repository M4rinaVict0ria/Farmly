import discord
from discord.ext import commands
from discord import app_commands
import math
import os

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Farmly online!")

def convert(v):
    v = v.lower()

    if v.endswith("k"):
        return int(float(v[:-1]) * 1000)
    elif v.endswith("m"):
        return int(float(v[:-1]) * 1000000)
    elif v.endswith("b"):
        return int(float(v[:-1]) * 1000000000)
    return int(v)

@bot.tree.command(name="tax", description="Calculate 10% tax")
async def tax(interaction: discord.Interaction, valor: str):

    amount = convert(valor)

    receive = int(amount * 0.9)
    send_needed = math.ceil(amount / 0.9)

    await interaction.response.send_message(
f"""🌾 Farmly Tax Calculator

For {amount:,}

📤 If you SEND:
Receiver gets: {receive:,}

📥 If you want to RECEIVE:
Sender must send: {send_needed:,}
"""
)

bot.run(TOKEN)