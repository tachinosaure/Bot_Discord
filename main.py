import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

print("Lancement du bot...")
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

#embeds de bienvenue et d'au revoir

Bienvenue = discord.Embed(
    title="Bienvenue sur Le Nid ! <:TachiSalut:1413598803621187684>",
    description=(
        "Commence par aller checker le salon <#1413233587888586833> \n"
        "Puis viens saluer la commu dans <#1412869316759781406> \n"
        "Et enfin présente toi dans <#1413239378687561728> \n \n"
        "Amuses toi bien sur Le Nid 🥰"
    ),
    color=discord.Color.yellow()
)

AuRevoir = discord.Embed(
    title="Un membre vient de partir… <:Crying_Tachi_2:1413908370645319811>",
    description="Tu vas nous manquer !",
    color=discord.Color.yellow()
)
#événements
@bot.event
async def on_ready():
    try:
        sync = await bot.tree.sync()
        print(f"Synchro des commandes réussie : {len(sync)} commande(s)")
    except Exception as error:
        print(f"Erreur lors de la synchro des commandes : {error}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1412868706765242408)
    if channel:
        await channel.send(content=f"{member.mention}", embed=Bienvenue)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1412874827605217421)
    if channel:
        await channel.send(content=f"{member.mention}", embed=AuRevoir)

#chargement des cogs

COGS = [
    "cogs.reseaux",   # YouTube, Twitch, stats chaînes, dernière vidéo
    "cogs.jeux",      # Minecraft, Vintage Story
    "cogs.general",   # contact, dons, site, clicker, dino, stats Discord, userinfo…
]

async def main():
    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
            print(f"✅ {cog} chargé")
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())