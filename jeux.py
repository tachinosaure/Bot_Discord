import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import aiohttp
from mcstatus import JavaServer

MC_IP = "huge-endorsement.gl.joinmc.link"


class Jeux(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #Minecraft

    @app_commands.command(name="ip_mc", description="Envoie l'IP du serveur Minecraft")
    async def ip_mc_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Voici l'IP du serveur Minecraft de Tachi : \n **{MC_IP}**"
        )

    @app_commands.command(name="statusmc", description="Affiche les informations du serveur Minecraft")
    async def statusmc_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            status = await asyncio.wait_for(
                asyncio.to_thread(lambda: JavaServer.lookup(MC_IP).status()),
                timeout=20.0
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("La requête vers le serveur a expiré.")
            return
        except Exception as e:
            print(f"Erreur de connexion au serveur Minecraft: {e}")
            embed = discord.Embed(
                title="Serveur Minecraft <:logomc:1441345758539415602>",
                description="**Statut : Hors ligne** ❌\nLe serveur est hors ligne ou injoignable",
                color=discord.Color.red()
            )
            embed.add_field(name="IP", value=f"`{MC_IP}`", inline=False)
            await interaction.followup.send(embed=embed)
            return

        embed = discord.Embed(
            title="Serveur Minecraft <:logomc:1441345758539415602>",
            description="**Statut : En ligne** ✅",
            color=discord.Color.green()
        )
        embed.add_field(name="IP", value=f"`{MC_IP}`", inline=False)
        embed.add_field(name="Joueurs en ligne", value=f"{status.players.online}", inline=False)
        embed.add_field(
            name="Version",
            value=status.version.name if hasattr(status.version, 'name') else "Inconnue",
            inline=False,
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="joueursmc", description="Affiche les joueurs en ligne sur le serveur Minecraft")
    async def joueurs_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            status = await asyncio.wait_for(
                asyncio.to_thread(lambda: JavaServer.lookup(MC_IP).status()),
                timeout=20.0
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("La requête au serveur Minecraft a expiré, réessayez plus tard.")
            return
        except Exception as exc:
            print(f"Erreur lors de la récupération des joueurs : {exc}")
            await interaction.followup.send("Impossible de récupérer la liste des joueurs, le serveur semble hors ligne.")
            return

        online_count = status.players.online if status.players else 0
        samples = []
        if status.players and hasattr(status.players, 'sample') and status.players.sample:
            samples = status.players.sample

        if not samples:
            if online_count == 0:
                embed = discord.Embed(
                    title="Joueurs en ligne sur le serveur Minecraft <:logomc:1441345758539415602>",
                    description="Aucun joueur n'est actuellement connecté.",
                    color=discord.Color.blue()
                )
            else:
                embed = discord.Embed(
                    title="Joueurs en ligne sur le serveur Minecraft <:logomc:1441345758539415602>",
                    description=f"{online_count} joueur(s) sont en ligne, leurs pseudos ne sont pas disponibles.",
                    color=discord.Color.blue()
                )
            embed.add_field(name="IP", value=f"`{MC_IP}`", inline=False)
            await interaction.followup.send(embed=embed)
            return

        names = [
            (p.get('name', 'inconnu') if isinstance(p, dict) else getattr(p, 'name', 'inconnu'))
            for p in samples
        ]
        if len(names) <= 10:
            embeds = []
            for name in names:
                embed_p = discord.Embed(
                    title=f"{name}",
                    description="En ligne sur le serveur Minecraft <:logomc:1441345758539415602>",
                    color=discord.Color.blue()
                )
                if name and name != 'inconnu':
                    embed_p.set_thumbnail(url=f"https://minotar.net/avatar/{name}/64")
                embeds.append(embed_p)
            await interaction.followup.send(embeds=embeds)

'''
Vintage Story
(commandes commentées dans le main d'origine — décommente quand tu as l'IP)

@app_commands.command(name="ip_vs", description="Envoie l'IP du serveur Vintage Story")
async def ip_vs_cmd(self, interaction: discord.Interaction):
    VS_IP = "TON_IP_ICI"
    await interaction.response.send_message(
        f"Voici l'IP du serveur Vintage Story de Tachi : \n **{VS_IP}**"
        )

@app_commands.command(name="statusvs", description="Affiche les informations du serveur Vintage Story")
async def statusvs_cmd(self, interaction: discord.Interaction):
    VS_IP   = "TON_IP_ICI"
    VS_PORT = 8080
    url     = f"http://{VS_IP}:{VS_PORT}/"
    await interaction.response.defer()
    try:
        async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status != 200:
            raise Exception(f"HTTP {response.status}")
            data = await response.json()
            except asyncio.TimeoutError:
            await interaction.followup.send("La requête vers le serveur a expiré.")
            return
            except Exception as e:
            print(f"Erreur de connexion au serveur Vintage Story: {e}")
            embed = discord.Embed(
            title="Serveur Vintage Story",
            description="**Statut : Hors ligne** ❌\nLe serveur est hors ligne ou injoignable",
            color=discord.Color.red()
        )
        embed.add_field(name="IP", value=f"`{VS_IP}`", inline=False)
        await interaction.followup.send(embed=embed)
        return
    embed = discord.Embed(
    title="Serveur Vintage Story",
    description="**Statut : En ligne** ✅",
    color=discord.Color.green()
)
embed.add_field(name="IP",             value=f"`{VS_IP}`",                          inline=False)
embed.add_field(name="Joueurs",        value=f"{data.get('Players', 0)}",            inline=False)
embed.add_field(name="Version",        value=data.get("GameVersion", "Inconnue"),    inline=False)
embed.add_field(name="Mode de jeu",    value=data.get("GameMode", "Inconnu"),        inline=False)
embed.add_field(name="Nom du serveur", value=data.get("ServerName", "Inconnu"),      inline=False)
await interaction.followup.send(embed=embed)
'''

async def setup(bot: commands.Bot):
    await bot.add_cog(Jeux(bot))
