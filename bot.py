import discord
from discord.ext import commands
from discord import app_commands
from tokken_bot import token

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"connecté en tant que {bot.user.name}")
        print(f"{len(synced)} commandes synchronisées")
    except Exception as e:
        print(f"erreur de synchronisation: {e}")

@bot.command()
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author.display_name} !")

@bot.tree.command(name="dire", description="Le bot répète la phrase  donnée")
@app_commands.describe(message="Le message que le bot doit répéter")
async def dire(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@bot.tree.command(name="kick", description="POur expulser un membre")
@app_commands.describe(membre="le membre a expulser", raison="raison du kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, membre: discord.Member, raison: str="Aucune raison donnée"):
    try:
        await membre.kick(reason=raison)
        await interaction.response.send_message(f"Le membre {membre} a bien été expulsé")
    except Exception as e:
        await interaction.response.send_message("Le membre n'a pas pu etre expulsé")

@bot.tree.command(name="ban", description="Pour bannir un membre")
@app_commands.describe(membre="le membre a bannir", raison="raison du kick")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, membre: discord.Member, raison: str="Aucune raison donnée"):
    try:
        await membre.ban(reason=raison)
        await interaction.response.send_message(f"Le membre {membre} a bien été banni")
    except Exception as e:
        await interaction.response.send_message("Le membre n'a pas pu etre banni")

@bot.tree.command(name="embed")
@app_commands.describe(titre="Titre de l'embed", description="Contenu")
async def embed(interaction: discord.Interaction, titre: str, description: str):
    new_embed = discord.Embed(
        title = titre,
        description=description,
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=new_embed)

bot.run(token)
