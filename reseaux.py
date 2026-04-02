import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import asyncio
import os
import re

YOUTUBE_API_KEY    = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = "UCYzwcxDNFfjY-xv5v4pQBHg"

TWITCH_CLIENT_ID     = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_LOGIN         = "tachinosaure"


class Reseaux(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot          

    async def _get_twitch_token(self) -> str | None:
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

    async def _get_youtube_stats(self) -> dict | None:
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "statistics,snippet",
            "id":   YOUTUBE_CHANNEL_ID,
            "key":  YOUTUBE_API_KEY,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                if r.status == 200:
                    data = await r.json()
                    items = data.get("items", [])
                    if items:
                        return {
                            "nom":       items[0]["snippet"]["title"],
                            "abonnes":   int(items[0]["statistics"]["subscriberCount"]),
                            "vues":      int(items[0]["statistics"]["viewCount"]),
                            "videos":    int(items[0]["statistics"]["videoCount"]),
                            "miniature": items[0]["snippet"]["thumbnails"]["default"]["url"],
                        }
        return None

    async def _get_twitch_stats(self) -> dict | None:
        token = await self._get_twitch_token()
        if not token:
            return None
        headers = {
            "Client-ID":     TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {token}",
        }
        async with aiohttp.ClientSession() as session:
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

            async with session.get(
                f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}",
                headers=headers
            ) as r:
                followers = 0
                if r.status == 200:
                    fdata = await r.json()
                    followers = fdata.get("total", 0)

            async with session.get(
                f"https://api.twitch.tv/helix/streams?user_id={user_id}",
                headers=headers
            ) as r:
                is_live, viewers, stream_title = False, 0, ""
                if r.status == 200:
                    sdata = await r.json()
                    if sdata["data"]:
                        is_live      = True
                        viewers      = sdata["data"][0]["viewer_count"]
                        stream_title = sdata["data"][0]["title"]

        return {
            "nom":          user["display_name"],
            "followers":    followers,
            "is_live":      is_live,
            "viewers":      viewers,
            "stream_title": stream_title,
            "avatar":       user["profile_image_url"],
            "url":          f"https://twitch.tv/{TWITCH_LOGIN}",
        }

    #commandes 

    @app_commands.command(name="youtube", description="Envoie le lien de la chaîne YouTube")
    async def youtube_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "<:Youtube_logo:1427364412796440606> Voici le lien de la chaîne YouTube de Tachi : \n"
            "**https://www.youtube.com/@Tachinosaure?sub_confirmation=1**"
        )

    @app_commands.command(name="twitch", description="Envoie le lien de la chaîne Twitch")
    async def twitch_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Voici le lien de la chaîne Twitch de Tachi : \n"
            "**https://www.twitch.tv/tachinosaure**"
        )

    @app_commands.command(name="chaines", description="Affiche les statistiques YouTube et Twitch de Tachi")
    async def stats_chaines_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        yt, tw = await asyncio.gather(
            self._get_youtube_stats(),
            self._get_twitch_stats(),
            return_exceptions=True
        )
        if isinstance(yt, Exception): yt = None
        if isinstance(tw, Exception): tw = None

        if yt is None and tw is None:
            await interaction.followup.send("❌ Impossible de récupérer les stats pour le moment.")
            return

        embed = discord.Embed(title="📊 Stats des chaînes de Tachi", color=discord.Color.gold())

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
                f"🔴 **EN LIVE** — {tw['viewers']:,} spectateurs\n🎙️ *{tw['stream_title']}*"
                if tw["is_live"] else "⚫ Hors ligne"
            )
            embed.add_field(
                name="🟣 Twitch",
                value=f"👥 **Followers :** {tw['followers']:,}\n{live_status}",
                inline=True
            )
            if tw["avatar"]:
                embed.set_thumbnail(url=tw["avatar"])
        else:
            embed.add_field(name="🟣 Twitch", value="❌ Indisponible", inline=True)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="lastvideo", description="Affiche la dernière vidéo YouTube de Tachi")
    async def lastvideo_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.googleapis.com/youtube/v3/channels", params={
                "part": "contentDetails,snippet",
                "id":   YOUTUBE_CHANNEL_ID,
                "key":  YOUTUBE_API_KEY,
            }) as r:
                data = await r.json()
                if not data.get("items"):
                    await interaction.followup.send("❌ Impossible de récupérer la chaîne.")
                    return
                uploads_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            async with session.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
                "part":       "snippet,contentDetails",
                "playlistId": uploads_id,
                "maxResults": 1,
                "key":        YOUTUBE_API_KEY,
            }) as r:
                data = await r.json()
                if not data.get("items"):
                    await interaction.followup.send("❌ Aucune vidéo trouvée.")
                    return
                item    = data["items"][0]
                snippet = item["snippet"]

            video_id = item["contentDetails"]["videoId"]
            async with session.get("https://www.googleapis.com/youtube/v3/videos", params={
                "part": "statistics,contentDetails",
                "id":   video_id,
                "key":  YOUTUBE_API_KEY,
            }) as r:
                video_data    = await r.json()
                video_stats   = video_data["items"][0]["statistics"]
                video_details = video_data["items"][0]["contentDetails"]

        duree_raw = video_details.get("duration", "PT0S")
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duree_raw)
        h, m, s = (int(match.group(i) or 0) for i in (1, 2, 3))
        duree = f"{h}h {m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

        published_ts = int(discord.utils.parse_time(snippet["publishedAt"]).timestamp())

        embed = discord.Embed(
            title=snippet["title"],
            url=f"https://www.youtube.com/watch?v={video_id}",
            color=discord.Color.red()
        )
        embed.set_author(name="📺 Dernière vidéo de Tachi")
        embed.set_image(url=snippet["thumbnails"].get("maxres", snippet["thumbnails"]["high"])["url"])
        embed.add_field(name="👁️ Vues",    value=f"{int(video_stats.get('viewCount', 0)):,}",  inline=True)
        embed.add_field(name="👍 Likes",   value=f"{int(video_stats.get('likeCount', 0)):,}",  inline=True)
        embed.add_field(name="⏱️ Durée",   value=duree,                                         inline=True)
        embed.add_field(name="📅 Publiée", value=f"<t:{published_ts}:R>",                       inline=True)

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Reseaux(bot))