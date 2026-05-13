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

@bot.tree.command(name="sondage", description="Créer un sondage")
@app_commands.describe(question="La question a poser", choix="Les options (séparées d'une virgule)")
async def sondage(interaction: discord.Interaction, question: str, choix: str):
    liste_choix = [c.strip for c in choix.split(",")]
    if len(liste_choix) > 15:
        await interaction.response.send_message("Le sondage ne peut pas dépasser 15 options", ephemeral=True)
        return
    
    embed = discord.Embed(title="📊 Sondage", description=f"**{question}**", color=discord.Color.blue())
    embed.set_footer(text=f"proposé par {interaction.user.display_name}")

    view = discord.ui.View(timeout=None)

    for option in liste_choix:
        bouton = discord.ui.Button(label=option, style=discord.ButtonStyle.secondary)

        def create_callback(label):
            async def callback(inter: discord.Interaction):
                await inter.response.send_message(f"Vous avez voté pour {label}", ephemeral=True)
            return callback
        
        bouton.callback = create_callback(option)
        view.add_item(bouton)

    await interaction.response.send_message(embed=embed, view=view)

bot.run(token)