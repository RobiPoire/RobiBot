import discord
from discord import app_commands
from discord.ext import commands
from .tools.fruits import random_fruit
from datetime import datetime
import logging

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="randomfruit")
    async def randomfruit(self, interaction: discord.Interaction) -> None:
        try:
            fruit = random_fruit("./res/fruits.csv")
            embed = discord.Embed(title=fruit.get_name(),
                                description=fruit.get_description())
            embed.set_image(url=fruit.get_image())
            embed.set_footer(text="Fruit aléatoire")
            embed.timestamp = datetime.now()
            embed.colour = discord.Colour.green()
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur est survenue : {e}")
            logging.error(f"Une erreur est survenue : {e}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
