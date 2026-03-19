import discord 
from discord.ext import commands, tasks
import os
import asyncio
from mcstatus import JavaServer
from dotenv import load_dotenv
from discord import app_commands
import aiohttp
import random

load_dotenv()

print("Lancement du bot...")
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

# synchro des commandes
@bot.event
async def on_ready():
    try:
        sync = await bot.tree.sync()
        print(f"Synchro des commandes réussie: {len(sync)}")
    except Exception as error:
        print(f"Erreur lors de la synchro des commandes : {error}")

ROLE_AUTORISE_ID   = 1413220444139425863 
 
YOUTUBE_API_KEY    = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = "UCYzwcxDNFfjY-xv5v4pQBHg"  
 
TWITCH_CLIENT_ID     = os.getenv("TWITCH_CLIENT_ID")      
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")  
TWITCH_LOGIN         = "tachinosaure"                      
 
# embed bienvenue / au revoir
Bienvenue = discord.Embed(
    title="Bienvenue sur Le Nid ! <:TachiSalut:1413598803621187684>",
    description="Commence par aller checker le salon <#1234567890> \n Puis viens saluer la commu dans <#1234567890> \n Et enfin présente toi dans <#1234567890> \n \n Amuses toi bien sur Le Nid 🥰",
    color=discord.Color.yellow()
)

AuRevoir = discord.Embed(
    title="Un membre vient de partir… <:Crying_Tachi_2:1413908370645319811>",
    description="Tu vas nous manquer !",
    color=discord.Color.yellow()
)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1234567890)
    if channel:
        await channel.send(content=f"{member.mention}", embed=Bienvenue)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1234567890)
    if channel:
        await channel.send(content=f"{member.mention}", embed=AuRevoir)

# commandes
@bot.tree.command(name="youtube", description="Envoie le lien de la chaîne YouTube")
async def youtube_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("<:Youtube_logo:1427364412796440606> Voici le lien de la chaîne YouTube de Tachi : https://www.youtube.com/@Tachinosaure?sub_confirmation=1")

@bot.tree.command(name="twitch", description="Envoie le lien de la chaîne Twitch")
async def twitch_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Voici le lien de la chaîne Twitch de Tachi : https://www.twitch.tv/tachinosaure")

@bot.tree.command(name="dons", description="Envoie le lien pour les dons 🤑")
async def dons_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Pour donner de l'argent à Tachi 🤑: https://streamlabs.com/tachinosaure/tip \n(Oui, il est pauvre) ")

@bot.tree.command(name="site", description="Envoie le lien du site web de Tachi")
async def site_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Pour en apprendre plus sur Tachi <:Flex_Tachi:1438465028629200926> : https://tachinosaure.netlify.app/index%20tachi")

@bot.tree.command(name="clicker", description="Envoie le lien du Tachi Clicker")
async def clicker_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Voici le lien du Tachi Clicker <:Flex_Tachi:1438465028629200926> : https://tachi-clicker.netlify.app/")

@bot.tree.command(name="dino", description="Easter egg de dinov")
async def dino_cmd(interaction: discord.Interaction):
    message=[
        "https://tenor.com/view/dino-dancing-meme-2-gif-17614987387155457295",
        "https://tenor.com/view/dino-gif-1087655278955196117",
        "https://cdn.discordapp.com/attachments/1412874913294979182/1482385794563047444/Banniere_Discord.gif",
        "https://tenor.com/view/sml-t-rex-angry-mad-roar-gif-4206695623442034697",
        "https://tenor.com/view/t-rex-dinosaur-playing-guitar-gif-13148229006548549000",
        "https://tenor.com/view/dinofaurio-dinosaur-gif-12405026444729417661",
        "https://tenor.com/view/this-is-me-looking-at-the-tracker-gif-2845537589667322467",
        "https://tenor.com/view/dinosaur-meteorite-reverse-ratamotomami-gif-25442172",
        "https://tenor.com/view/flat-earth-meteorite-flat-earth-meteorite-dinosaurs-extinction-gif-23332390",
    ]
    await interaction.response.send_message(random.choice(message))

@bot.tree.command(name="statusmc", description="Affiche les informations du serveur Minecraft")
async def statusmc_cmd(interaction: discord.Interaction):
    ip = "huge-endorsement.gl.joinmc.link"
    await interaction.response.defer()

    try:
        status = await asyncio.wait_for(
            asyncio.to_thread(lambda: JavaServer.lookup(ip).status()),
            timeout=20.0  # temps plus généreux si le serveur est chargé
        )
    except asyncio.TimeoutError:
        # erreur de délai, le serveur met trop de temps à répondre
        await interaction.followup.send("La requête vers le serveur a expiré")
        return
    except Exception as e:
        # échec de connexion
        print(f"Erreur de connexion au serveur Minecraft: {e}")
        embed = discord.Embed(
            title="Serveur Minecraft <:logomc:1441345758539415602>",
            description="**Statut : Hors ligne** ❌\nLe serveur est hors ligne ou injoignable",
            color=discord.Color.red()
        )
        embed.add_field(name="IP", value=f"`{ip}`", inline=False)
        await interaction.followup.send(embed=embed)
        return
    # requête réussi
    embed = discord.Embed(
        title="Serveur Minecraft <:logomc:1441345758539415602>",
        description="**Statut : En ligne** ✅",
        color=discord.Color.green()
    )
    embed.add_field(name="IP", value=f"`{ip}`", inline=False)
    embed.add_field(name="Joueurs en ligne", value=f"{status.players.online}", inline=False)
    embed.add_field(
        name="Version",
        value=status.version.name if hasattr(status.version, 'name') else "Inconnue",
        inline=False,
    )
    await interaction.followup.send(embed=embed)

# commande pour lister les joueurs en ligne sur le serveur minecraft
@bot.tree.command(name="joueursmc", description="Affiche les joueurs en ligne sur le serveur Minecraft")
async def joueurs_cmd(interaction: discord.Interaction):
    ip = "duck.trollcraft.com" #this ip doesnt work
    await interaction.response.defer()
    try:
        status = await asyncio.wait_for(
            asyncio.to_thread(lambda: JavaServer.lookup(ip).status()),
            timeout=20.0
        )
    except asyncio.TimeoutError:
        await interaction.followup.send("La requête au serveur Minecraft a expiré, réessayez plus tard.")
        return
    except Exception as exc:
        print(f"Erreur lors de la récupération des joueurs : {exc}")
        await interaction.followup.send("Impossible de récupérer la liste des joueurs, le serveur semble hors ligne.")
        return

    # réponse valide
    online_count = status.players.online if status.players else 0
    samples = []
    if status.players and hasattr(status.players, 'sample') and status.players.sample:
        samples = status.players.sample
    if not samples:
        # pas d'infos des noms
        if online_count == 0:
            embed_empty = discord.Embed(
                title="Joueurs en ligne sur le serveur Minecraft <:logomc:1441345758539415602>",
                description="Aucun joueur n'est actuellement connecté.",
                color=discord.Color.blue()
            )
            embed_empty.add_field(name="IP", value=f"`{ip}`", inline=False)
            await interaction.followup.send(embed=embed_empty)
        else:
            embed_partial = discord.Embed(
                title="Joueurs en ligne",
                description=f"{online_count} joueur(s) sont en ligne, leurs pseudos ne sont pas disponibles.",
                color=discord.Color.blue()
            )
            embed_partial.add_field(name="IP", value=f"`{ip}`", inline=False)
            await interaction.followup.send(embed=embed_partial)
        return
    names = [
        (p.get('name', 'inconnu') if isinstance(p, dict) else getattr(p, 'name', 'inconnu'))
        for p in samples
    ]

    #envoyer un embed par joueur avec le skin.
    max_embeds_with_heads = 10
    if len(names) <= max_embeds_with_heads:
        embeds = []
        for name in names:
            embed_p = discord.Embed(
                title=f"{name}",
                description=f"En ligne sur le serveur Minecraft <:logomc:1441345758539415602>",
                color=discord.Color.blue()
            )
            if name and name != 'inconnu':
                avatar_url = f"https://minotar.net/avatar/{name}/64"
                embed_p.set_thumbnail(url=avatar_url)
            embeds.append(embed_p)
        await interaction.followup.send(embeds=embeds)

# commande pour afficher les statistiques du serveur Discord
@bot.tree.command(name="stats", description="Affiche les statistiques du serveur Discord")
async def stats_cmd(interaction: discord.Interaction):
    guild = interaction.guild
    
    if not guild:
        await interaction.response.send_message("<:bonk:1430833665818234900> Cette commande ne peut être utilisée que dans un serveur... <:bonk:1430833665818234900>")
        return
    # Nombres salons
    text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
    voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
    # Stats de membres
    members = guild.member_count
    online = sum(1 for m in guild.members if m.status != discord.Status.offline)
    # Nombre de boosts
    boosts = guild.premium_subscription_count
    #boosters
    boosters = [member.display_name for member in guild.premium_subscribers]
    boosters_text = "\n".join(boosters) if boosters else "Aucun booster"

    owner_name = guild.owner.display_name if guild.owner else "Inconnu"

    embed = discord.Embed(
        title=f"Statistiques du Nid de Tachi",
        description=f"Informations complètes du serveur Discord",
        color=discord.Color.blue()
    )
    # Ajouter la bannière du serveur 
    banner_path = os.path.join(os.path.dirname(__file__), "Bannière_Discord.gif")
    file_to_send = None
    if os.path.exists(banner_path):
        embed.set_image(url="attachment://Bannière_Discord.gif")
        file_to_send = discord.File(banner_path, filename="Bannière_Discord.gif")
    elif guild.banner:
        embed.set_image(url=guild.banner.url)
    embed.add_field(name="\n<:TachiSalut:1413598803621187684> Membres:", value=f"Total: {members}   •   🟢 En ligne: {online}", inline=False)
    embed.add_field(name="\n<:sigma_chill:1430753352270217256> Salons:", value=f"\nTextuels: {text_channels}\nVocaux: {voice_channels}", inline=False)
    embed.add_field(name="\n<:radiant:1450584396435423407> Boosts:", value=f"   **{boosts}** de: {boosters_text}", inline=False)
    embed.add_field(name="\n<:Sage:1413600218913439915> Dictateur:", value=f"{owner_name}", inline=False)
    embed.add_field(name="\n<:what_bob:1413908760962797662> Date de Création:", value=f"<t:{int(guild.created_at.timestamp())}:d>", inline=False)
    if file_to_send:
        await interaction.response.send_message(embed=embed, file=file_to_send)
    else:
        await interaction.response.send_message(embed=embed)

# commande pour afficher toutes les commandes existantes
@bot.tree.command(name="commandes", description="Affiche la liste de toutes les commandes disponibles")
async def commandes_cmd(interaction: discord.Interaction):
    commands_list = bot.tree.get_commands()
    embed = discord.Embed(
        title="<:Disturb_Tachi:1413908400286208010> Commandes disponibles",
        description=f"**Total: {len(commands_list)} commande(s)**",
        color=discord.Color.blue()
    )
    for cmd in commands_list:
        embed.add_field(
            name=f"/{cmd.name}",
            value=cmd.description or "Pas de description",
            inline=False
        )
    await interaction.response.send_message(embed=embed)

''' #this part of the code is for vintage story but the server is currently down
@bot.tree.command(name="statusvs", description="Affiche les informations du serveur Vintage Story")
async def statusvs_cmd(interaction: discord.Interaction):
    ip = "duck.trollcraft.com" #this ip doesnt work
    port = 8080
    url = f"http://{ip}:{port}/"
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
        embed.add_field(name="IP", value=f"`{ip}`", inline=False)
        await interaction.followup.send(embed=embed)
        return

    # Requête réussie
    embed = discord.Embed(
        title="Serveur Vintage Story",
        description="**Statut : En ligne** ✅",
        color=discord.Color.green()
    )
    embed.add_field(name="IP", value=f"`{ip}`", inline=False)
    embed.add_field(
        name="Joueurs en ligne",
        value=f"{data.get('Players', 0)}",
        inline=False
    )
    embed.add_field(name="Version", value=data.get("GameVersion", "Inconnue"), inline=False)
    embed.add_field(name="Mode de jeu", value=data.get("GameMode", "Inconnu"), inline=False)
    embed.add_field(name="Nom du serveur", value=data.get("ServerName", "Inconnu"), inline=False)
    await interaction.followup.send(embed=embed)
'''
@bot.tree.command(name="userinfo", description="Affiche les informations d'un membre")
@app_commands.describe(membre="Le membre dont tu veux voir les infos")
async def userinfo_cmd(interaction: discord.Interaction, membre: discord.Member):
    role_autorise = interaction.guild.get_role(ROLE_AUTORISE_ID)
    if role_autorise not in interaction.user.roles:
        await interaction.response.send_message(
            "❌ Tu n'as pas la permission d'utiliser cette commande.",
            ephemeral=True  
        )
        return
 
    roles = [r.mention for r in reversed(membre.roles) if r.name != "@everyone"]
    roles_text = " ".join(roles) if roles else "Aucun rôle"
    status_map = {
        discord.Status.online:    "🟢 En ligne",
        discord.Status.idle:      "🌙 Absent",
        discord.Status.dnd:       "🔴 Ne pas déranger",
        discord.Status.offline:   "⚫ Hors ligne",
    }
    statut = status_map.get(membre.status, "❓ Inconnu")
 
    activite = "Aucune activité"
    if membre.activity:
        if isinstance(membre.activity, discord.Streaming):
            activite = f"🔴 En stream : [{membre.activity.name}]({membre.activity.url})"
        elif isinstance(membre.activity, discord.Game):
            activite = f"🎮 Joue à {membre.activity.name}"
        elif isinstance(membre.activity, discord.Spotify):
            activite = f"🎵 Écoute {membre.activity.title} — {membre.activity.artist}"
        else:
            activite = str(membre.activity.name)
 
    embed = discord.Embed(
        title=f"Infos de {membre.display_name}",
        color=membre.color if membre.color != discord.Color.default() else discord.Color.blurple()
    )
    embed.set_thumbnail(url=membre.display_avatar.url)
    embed.add_field(name="🏷️ Tag Discord",      value=str(membre),                                           inline=True)
    embed.add_field(name="📅 Compte créé le",   value=f"<t:{int(membre.created_at.timestamp())}:D>",         inline=True)
    embed.add_field(name="📥 A rejoint le",     value=f"<t:{int(membre.joined_at.timestamp())}:D>",          inline=True)
    embed.add_field(name="⚡ Statut",           value=statut,                                                inline=True)
    embed.add_field(name="🎯 Activité",         value=activite,                                              inline=False)
    embed.add_field(name=f"🎭 Rôles ({len(roles)})", value=roles_text,                                       inline=False)
    if membre.premium_since:
        embed.add_field(
            name="💎 Booste depuis",
            value=f"<t:{int(membre.premium_since.timestamp())}:D>",
            inline=False
        )
    embed.set_footer(text=f"Demandé par {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed)

 
async def get_twitch_token() -> str | None:
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id":     TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type":    "client_credentials",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as r:
            if r.status == 200:
                data = await r.json()
                return data.get("access_token")
    return None
 
async def get_youtube_stats() -> dict | None:
    """Retourne les stats de la chaîne YouTube via l'API Data v3."""
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part":  "statistics,snippet",
        "id":    YOUTUBE_CHANNEL_ID,
        "key":   YOUTUBE_API_KEY,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as r:
            if r.status == 200:
                data = await r.json()
                items = data.get("items", [])
                if items:
                    return {
                        "nom":        items[0]["snippet"]["title"],
                        "abonnes":    int(items[0]["statistics"]["subscriberCount"]),
                        "vues":       int(items[0]["statistics"]["viewCount"]),
                        "videos":     int(items[0]["statistics"]["videoCount"]),
                        "miniature":  items[0]["snippet"]["thumbnails"]["default"]["url"],
                    }
    return None
 
 
async def get_twitch_stats() -> dict | None:
    """Retourne les stats de la chaîne Twitch (followers + statut live)."""
    token = await get_twitch_token()
    if not token:
        return None
    headers = {
        "Client-ID":     TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }
    async with aiohttp.ClientSession() as session:
 
        # Infos de base du canal
        async with session.get(
            f"https://api.twitch.tv/helix/users?login={TWITCH_LOGIN}",
            headers=headers
        ) as r:
            if r.status != 200:
                return None
            user_data = await r.json()
            user = user_data["data"][0] if user_data["data"] else None
            if not user:
                return None
        user_id = user["id"]
        # Followers
        async with session.get(
            f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}",
            headers=headers
        ) as r:
            followers = 0
            if r.status == 200:
                fdata = await r.json()
                followers = fdata.get("total", 0)
        # Vérification si live en ce moment
        async with session.get(
            f"https://api.twitch.tv/helix/streams?user_id={user_id}",
            headers=headers
        ) as r:
            is_live       = False
            viewers       = 0
            stream_title  = ""
            if r.status == 200:
                sdata = await r.json()
                if sdata["data"]:
                    is_live      = True
                    viewers      = sdata["data"][0]["viewer_count"]
                    stream_title = sdata["data"][0]["title"]
    return {
        "nom":           user["display_name"],
        "followers":     followers,
        "is_live":       is_live,
        "viewers":       viewers,
        "stream_title":  stream_title,
        "avatar":        user["profile_image_url"],
        "url":           f"https://twitch.tv/{TWITCH_LOGIN}",
    }
 
@bot.tree.command(name="chaines", description="Affiche les statistiques YouTube et Twitch de Tachi")
async def stats_chaines_cmd(interaction: discord.Interaction):
    await interaction.response.defer()
    yt, tw = None, None
    # Récup
    import asyncio
    yt, tw = await asyncio.gather(
        get_youtube_stats(),
        get_twitch_stats(),
        return_exceptions=True
    )
    # Si les deux ont échoué
    if isinstance(yt, Exception): yt = None
    if isinstance(tw, Exception): tw = None
 
    if yt is None and tw is None:
        await interaction.followup.send("❌ Impossible de récupérer les stats pour le moment.")
        return
    embed = discord.Embed(
        title="📊 Stats des chaînes de Tachi",
        color=discord.Color.gold()
    )
    if yt:
        embed.add_field(
            name="<:Youtube_logo:1427364412796440606> YouTube",
            value=(
                f"👥 **Abonnés :** {yt['abonnes']:,}\n"
                f"👁️ **Vues totales :** {yt['vues']:,}\n"
                f"🎬 **Vidéos :** {yt['videos']:,}"
            ),
            inline=True
        )
    else:
        embed.add_field(name="<:Youtube_logo:1427364412796440606> YouTube", value="❌ Indisponible", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    if tw:
        live_status = (
            f"🔴 **EN LIVE** — {tw['viewers']:,} spectateurs\n"
            f"🎙️ *{tw['stream_title']}*"
            if tw["is_live"]
            else "⚫ Hors ligne"
        )
        embed.add_field(
            name="🟣 Twitch",
            value=(
                f"👥 **Followers :** {tw['followers']:,}\n"
                f"{live_status}"
            ),
            inline=True
        )
        if tw["avatar"]:
            embed.set_thumbnail(url=tw["avatar"])
    else:
        embed.add_field(name="🟣 Twitch", value="❌ Indisponible", inline=True)
    await interaction.followup.send(embed=embed)

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
