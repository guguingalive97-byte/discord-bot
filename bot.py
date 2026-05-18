import discord
from discord.ext import commands
from discord import app_commands

import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# BOTÕES
class ContratoView(discord.ui.View):

    def __init__(self, equipe, dono_id, canal_id):
        super().__init__(timeout=None)

        self.equipe = equipe
        self.dono_id = dono_id
        self.canal_id = canal_id

    @discord.ui.button(
        label="Aceitar",
        style=discord.ButtonStyle.green
    )
    async def aceitar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            f"Você aceitou o contrato da {self.equipe}.",
            ephemeral=True
        )

        canal = bot.get_channel(self.canal_id)

        if canal:
            await canal.send(
                f"{interaction.user.display_name} aceitou o contrato da equipe {self.equipe}."
            )

    @discord.ui.button(
        label="Recusar",
        style=discord.ButtonStyle.red
    )
    async def recusar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            f"Você recusou o contrato da {self.equipe}.",
            ephemeral=True
        )

        canal = bot.get_channel(self.canal_id)

        if canal:
            await canal.send(
                f"{interaction.user.display_name} recusou o contrato da equipe {self.equipe}."
            )


# COMANDO
@bot.tree.command(
    name="contrato",
    description="Enviar contrato"
)

@app_commands.describe(
    jogador="Jogador",
    equipe="Equipe",
    salario="Salário",
    multa="Multa rescisória",
    duracao="Duração"
)

async def contrato(
    interaction: discord.Interaction,
    jogador: discord.Member,
    equipe: str,
    salario: str,
    multa: str,
    duracao: str
):

    embed = discord.Embed(
        title="📄 CONTRATO",
        color=discord.Color.red()
    )

    embed.add_field(
        name="Equipe",
        value=equipe,
        inline=False
    )

    embed.add_field(
        name="Salário",
        value=salario,
        inline=False
    )

    embed.add_field(
        name="Multa Rescisória",
        value=multa,
        inline=False
    )

    embed.add_field(
        name="Duração",
        value=duracao,
        inline=False
    )

    embed.add_field(
        name="Enviado por",
        value=interaction.user.name,
        inline=False
    )

    view = ContratoView(
        equipe,
        interaction.user.id,
        interaction.channel.id
    )

    try:

        await jogador.send(
            embed=embed,
            view=view
        )

        await interaction.response.send_message(
            f"Contrato enviado para {jogador.mention}.",
            ephemeral=True
        )

    except Exception as e:
        print(e)

        await interaction.response.send_message(
            "Não consegui enviar mensagem privada.",
            ephemeral=True
        )

@bot.event
async def on_ready():

    await bot.tree.sync()

print(f"Bot online como {bot.user}")
print("Slash commands sincronizados")

bot.run(TOKEN)
