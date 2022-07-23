from discord import Intents
from discord.ext.commands import Bot

class InfiniteBot(Bot):
    def __init__(self):
        super().__init__(
            command_prefix='.',
            help_command=None,
            description='N/A',
            intents=Intents.all()
        )
    
    async def setup_hook(self) -> None:
        await self.load_extension('core.extensions')
        await self.load_extension('core.games.cointoss')