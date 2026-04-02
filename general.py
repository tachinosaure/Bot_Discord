import discord
from discord.ext import commands
from discord import app_commands
import os
import random

ROLE_AUTORISE_ID = 1413220444139425863


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="contact", description="Affiche le contact de Tachi")
    async def contacts_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Voici le contact de Tachi : \n Email: **Tachinosaure@gmail.com**"
        )

    @app_commands.command(name="dons", description="Envoie le lien pour les dons 🤑")
    async def dons_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Pour donner de l'argent à Tachi 🤑: \n"
            "**https://streamlabs.com/tachinosaure/tip** \n(Oui, il est pauvre) "
        )

    @app_commands.command(name="site", description="Envoie le lien du site web de Tachi")
    async def site_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Pour en apprendre plus sur Tachi <:Flex_Tachi:1438465028629200926> : \n"
            "**https://tachinosaure.netlify.app/index%20tachi**"
        )

    @app_commands.command(name="clicker", description="Envoie le lien du Tachi Clicker")
    async def clicker_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Voici le lien du Tachi Clicker <:Flex_Tachi:1438465028629200926> : \n"
            "**https://tachi-clicker.netlify.app/**"
        )

    @app_commands.command(name="jeu-nul", description="Envoie le lien d'un jeu nul fait avec un tuto YouTube")
    async def jeu_nul_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Voici le lien du jeu nul de Tachi fais avec un tuto : \n"
            "**https://jeu-nul.netlify.app/a**"
        )

    @app_commands.command(name="dino", description="Easter egg de dino")
    async def dino_cmd(self, interaction: discord.Interaction):
        gifs = [
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
        await interaction.response.send_message(random.choice(gifs))

    @app_commands.command(name="stats", description="Affiche les statistiques du serveur Discord")
    async def stats_cmd(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message(
                "<:bonk:1430833665818234900> Cette commande ne peut être utilisée que dans un serveur... <:bonk:1430833665818234900>"
            )
            return

        text_channels  = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
        voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
        members        = guild.member_count
        online         = sum(1 for m in guild.members if m.status != discord.Status.offline)
        boosts         = guild.premium_subscription_count
        boosters       = [member.display_name for member in guild.premium_subscribers]
        boosters_text  = "\n".join(boosters) if boosters else "Aucun booster"
        owner_name     = guild.owner.display_name if guild.owner else "Inconnu"

        embed = discord.Embed(
            title="Statistiques du Nid de Tachi",
            description="Informations complètes du serveur Discord",
            color=discord.Color.blue()
        )
        banner_path  = os.path.join(os.path.dirname(__file__), "..", "Bannière_Discord.gif")
        file_to_send = None
        if os.path.exists(banner_path):
            embed.set_image(url="attachment://Bannière_Discord.gif")
            file_to_send = discord.File(banner_path, filename="Bannière_Discord.gif")
        elif guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.add_field(name="\n<:TachiSalut:1413598803621187684> Membres:",          value=f"Total: {members}   •   🟢 En ligne: {online}",         inline=False)
        embed.add_field(name="\n<:sigma_chill:1430753352270217256> Salons:",           value=f"\nTextuels: {text_channels}\nVocaux: {voice_channels}",  inline=False)
        embed.add_field(name="\n<:radiant:1450584396435423407> Boosts:",               value=f"   **{boosts}** de: {boosters_text}",                    inline=False)
        embed.add_field(name="\n<:Sage:1413600218913439915> Dictateur:",               value=owner_name,                                                inline=False)
        embed.add_field(name="\n<:what_bob:1413908760962797662> Date de Création:",    value=f"<t:{int(guild.created_at.timestamp())}:d>",               inline=False)

        if file_to_send:
            await interaction.response.send_message(embed=embed, file=file_to_send)
        else:
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="commandes", description="Affiche la liste de toutes les commandes disponibles")
    async def commandes_cmd(self, interaction: discord.Interaction):
        commands_list = self.bot.tree.get_commands()
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

    @app_commands.command(name="userinfo", description="Affiche les informations d'un membre")
    @app_commands.describe(membre="Le membre dont tu veux voir les infos")
    async def userinfo_cmd(self, interaction: discord.Interaction, membre: discord.Member):
        role_autorise = interaction.guild.get_role(ROLE_AUTORISE_ID)
        if role_autorise not in interaction.user.roles:
            await interaction.response.send_message(
                "❌ Tu n'as pas la permission d'utiliser cette commande.",
                ephemeral=True
            )
            return

        roles      = [r.mention for r in reversed(membre.roles) if r.name != "@everyone"]
        roles_text = " ".join(roles) if roles else "Aucun rôle"
        status_map = {
            discord.Status.online:  "🟢 En ligne",
            discord.Status.idle:    "🌙 Absent",
            discord.Status.dnd:     "🔴 Ne pas déranger",
            discord.Status.offline: "⚫ Hors ligne",
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
        embed.add_field(name="🏷️ Tag Discord",           value=str(membre),                                      inline=True)
        embed.add_field(name="📅 Compte créé le",        value=f"<t:{int(membre.created_at.timestamp())}:D>",     inline=True)
        embed.add_field(name="📥 A rejoint le",          value=f"<t:{int(membre.joined_at.timestamp())}:D>",      inline=True)
        embed.add_field(name="⚡ Statut",                value=statut,                                            inline=True)
        embed.add_field(name="🎯 Activité",              value=activite,                                          inline=False)
        embed.add_field(name=f"🎭 Rôles ({len(roles)})", value=roles_text,                                        inline=False)
        if membre.premium_since:
            embed.add_field(
                name="💎 Booste depuis",
                value=f"<t:{int(membre.premium_since.timestamp())}:D>",
                inline=False
            )
        embed.set_footer(text=f"Demandé par {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
