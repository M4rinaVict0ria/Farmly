import discord
from discord.ext import commands
from discord import app_commands
import math
import os
import threading
from flask import Flask

TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", 10000))

app = Flask(__name__)

@app.route("/")
def home():
    return "Farmly online!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Farmly online!")

@bot.tree.command(name="tax", description="Calculate 10% tax")
async def tax(interaction: discord.Interaction, valor: str):
    await interaction.response.send_message("Farmly funcionando!")

threading.Thread(target=run_web).start()

bot.run(TOKEN)