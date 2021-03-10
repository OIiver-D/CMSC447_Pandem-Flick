import discord
from discord.ext import commands 
from discord.utils import get

class help(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("help cog online.")

    @commands.command(pass_context=True)    
    async def help(self,ctx):
        embed = discord.Embed(title="Pandem-Flick: ", color=0xAC1ADC)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(help(client))