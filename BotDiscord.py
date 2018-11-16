import discord
from discord.ext import commands
from discord.ext.commands import Bot

BOT_PREFIX=("!")
bot = commands.Bot(command_prefix=BOT_PREFIX)
TOKEN = 'NTEyNTUxMTEwODIxODA2MDkw.Ds8C5g.zp5IWS1aggsfQpI6mfJRK2rRGjc'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        #msg = 'Hello {0.author.mention}'.format(message)
        helpmsg = 'The purpose of this Bot is to insult freely ' + message.server.get_member_named('darksoutofar').mention
        await client.send_message(message.channel, helpmsg)

    if message.content.startswith('!WhoIsBG'):
        member_objectbg = message.server.get_member_named('Strategychess')
        await client.send_message(message.channel, member_objectbg.mention + 'est beaucoup trop BG !')

    if message.content.startswith('!WhoIsPD'):
        member_object = message.server.get_member_named('darksoutofar')
        await client.send_message(message.channel, member_object.mention + 'est un pd!')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------')

client.run(TOKEN)