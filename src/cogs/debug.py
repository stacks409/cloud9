import discord
from discord.ext import commands
from discord.ext.commands.context import Context

class Debug(commands.Cog):
    def __init__(self, cloud9) -> None:
        self.cloud9 = cloud9
        
    @commands.command(name='ping')
    async def ping(self, ctx: Context):
        async with ctx.typing():
            message = await ctx.send(':ping_pong: Pong!')
            ping = (message.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000
            await message.edit(content=f':ping_pong: Pong!\nTook {int(ping)}ms\nLatency: {int(self.cloud9.latency * 1000)}ms')
        
def setup(cloud9):
    cloud9.add_cog(Debug(cloud9))