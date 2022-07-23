from infinite import InfiniteBot
from discord.ext.commands import (
    Cog, 
    group, 
    Context
)
from discord.ext.commands.errors import (
    ExtensionAlreadyLoaded, 
    ExtensionNotLoaded, 
    NoEntryPointError, 
    ExtensionFailed, 
    ExtensionNotFound
)
from typing import (
    NamedTuple, 
    Optional
)
from string import Template
from enum import Enum
from functools import partial


BUSY = ':warning: Another extension action is already in progress, please try again later.'
IN_PROGESS = Template(':hourglass: Extension **$verb** is now in progress, please wait...')
COMPLETED = Template(':checkered_flag: Extension **$verb** has just finished.\n$codeblock')


class CompletedAction(NamedTuple):
    extension: str
    error_message: Optional[str]    


class Action(Enum):
    LOAD = partial(InfiniteBot.load_extension)
    RELOAD = partial(InfiniteBot.reload_extension)
    UNLOAD = partial(InfiniteBot.unload_extension)


class Extensions(Cog, name='extensions'):
    def __init__(self, bot: InfiniteBot) -> None:
        self.bot = bot
        self.aip = False

    @group(name='extensions', aliases=['extension', 'exts', 'ext'], invoke_without_command=True)
    async def ext(self, ctx: Context) -> None:
        await ctx.send('This command has not been implemented yet!')

    @ext.command(name='load', aliases=['l'])
    async def load(self, ctx: Context, *extensions: str) -> None:
        await self.manage_action_on_extensions(ctx, Action.LOAD, *extensions)
    
    @ext.command(name='reload', aliases=['r'])
    async def reload(self, ctx: Context, *extensions: str) -> None:
        await self.manage_action_on_extensions(ctx, Action.RELOAD, *extensions)
    
    @ext.command(name='unload', aliases=['u'])
    async def unload(self, ctx: Context, *extensions: str) -> None:
        await self.manage_action_on_extensions(ctx, Action.UNLOAD, *extensions)
    
    async def build_codeblock(self, *cas: CompletedAction) -> str:
        codeblock = '```diff'
        
        for ca in cas:
            codeblock = codeblock + f'\n{"-" if ca.error_message else "+"} {ca.extension}'
            
            if ca.error_message:
                codeblock = codeblock + f'\n--- {ca.error_message}'
        
        return codeblock + '```'
    
    async def manage_action_on_extensions(self, ctx: Context, action: Action, *extensions: str) -> None:
        if self.aip:
            await ctx.send(content=BUSY)
            return
        
        self.aip = True
        sent_msg = await ctx.send(content=IN_PROGESS.safe_substitute(verb=action.name))
        
        if len(extensions) == 1:
            ca = await self.run_action_on_extension(action, extensions[0])
            cb = await self.build_codeblock(ca)
            await sent_msg.edit(content=COMPLETED.safe_substitute(verb=action.name, codeblock=cb))
            self.aip = False
        else:
            cas = []
            
            for extension in extensions:
                ca = await self.run_action_on_extension(action, extension)
                cas.append(ca)
            
            cb = await self.build_codeblock(*cas)
            await sent_msg.edit(content=COMPLETED.safe_substitute(verb=action.name, codeblock=cb))
            self.aip = False

    async def run_action_on_extension(self, action: Action, extension: str) -> CompletedAction:        
        try:
            await action.value(self.bot, extension)
        except ExtensionAlreadyLoaded as e:
            error_message = 'Extension is already loaded.'
        except ExtensionNotLoaded as e:
            if action is Action.RELOAD:
                return await self.run_action_on_extension(Action.LOAD, extension)
            else:
                error_message = 'Extension is not currently loaded.'
        except NoEntryPointError as e:
            error_message = 'Extension does not have a setup entry point.'
        except ExtensionFailed as e:
            error_message = 'Extension failed to load during execution of the module or setup entry point.'
        except ExtensionNotFound as e:
            error_message = 'Extension could not be found.'
        except Exception as e:
            error_message = str(e)
        else:
            error_message = None
    
        return CompletedAction(extension, error_message)


async def setup(bot: InfiniteBot) -> None:
    await bot.add_cog(Extensions(bot))