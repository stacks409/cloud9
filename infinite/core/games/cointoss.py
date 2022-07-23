from infinite import InfiniteBot
from discord import (
    Embed, 
    ButtonStyle, 
    Interaction
)
from discord.ui import (
    View, 
    Button, 
    button
)
from discord.ext.commands import (
    Cog, 
    command, 
    Context
)
import random


class CoinTossView(View):
    def __init__(self):
        super().__init__(timeout=10)
        self.dealer_choice = random.choice(['Heads', 'Tails'])
        self.user_choice = None
        self.user_won = False

    async def on_timeout(self) -> None:
        self.clear_items()

    async def on_user_choice(self, choice: str) -> None:
        self.user_choice = choice
        self.user_won = self.dealer_choice == self.user_choice
        self.stop()

    @button(style=ButtonStyle.green, label='Heads')
    async def on_user_clicked_heads(self, btn: Button, ctx: Interaction) -> None:
        await self.on_user_choice('Heads')
    
    @button(style=ButtonStyle.red, label='Tails')
    async def on_user_clicked_tails(self, btn: Button, ctx: Interaction) -> None:
        await self.on_user_choice('Tails')


class CoinToss(Cog, name='cointoss'):
    def __init__(self, bot: InfiniteBot) -> None:
        self.bot = bot
    
    @command(name='cointoss', aliases=['ct', 'coinflip', 'cf'])
    async def cointoss(self, ctx: Context) -> None:
        embed = Embed(description='The dealer has flipped a coin!\n**Please select a choice as your guess**', color=0xFFF5BA)
        embed.set_author(name=f'{ctx.author.display_name} - Coin Toss', icon_url=ctx.author.display_avatar.url)

        ctv = CoinTossView()
        message = await ctx.send(embed=embed, view=ctv)
        timeout = await ctv.wait()
        
        if timeout:
            embed.description = 'The dealer got tired and dropped the coin thus losing the coin result.'
            embed.color = 0x000000
            await message.edit(embed=embed, view=None)
        else:
            embed.description = f'**\tYou have {"won" if ctv.user_won else "lost"}!**'
            embed.color = 0xBFFCC6 if ctv.user_won else 0xFFABAB
            embed.add_field(name='You Guessed', value=ctv.user_choice, inline=True)
            embed.add_field(name='Dealer Had', value=ctv.dealer_choice, inline=True)
            await message.edit(embed=embed, view=None)


async def setup(bot: InfiniteBot) -> None:
    await bot.add_cog(CoinToss(bot))