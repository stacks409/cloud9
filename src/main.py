import discord
from discord.ext import commands

cloud9 = commands.Bot(command_prefix=commands.when_mentioned_or('.'), description='N/A', intents=discord.Intents.all(), case_insensitive=True)
cloud9.remove_command('help')

@cloud9.event
async def on_ready():
    print(f'Logged in as {cloud9.user} ({cloud9.user.id})')
    
    # Load all of the cogs
    modules = ['debug']
    
    try:
        for module in modules:
            cloud9.load_extension(f'cogs.{module}')
            print(f'Loaded: {module}')
    except Exception as e:
        print(f'Error loading {module}: {e}')
        
    await cloud9.change_presence(status=discord.Status.idle)

@cloud9.event
async def on_member_join(member):
    pass

@cloud9.event
async def on_member_remove(member):
    pass

print('Starting up Cloud 9')
cloud9.run('TOKEN')