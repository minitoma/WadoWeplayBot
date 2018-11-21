import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

BOT_PREFIX = "!"
bot = commands.Bot(command_prefix=BOT_PREFIX)
TOKEN = config['config']['token']

client = discord.Client()

list_who_play_yes = []
list_who_play_no = []
msg_ask_sure = "⚠ Tu es vraiment sûr de vouloir reset le vote maintenant ? ⚠"
reaction_check = '✅'
reaction_uncheck = '❌'


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        help_msg = 'Voici la liste des commandes utilisables pour ce bot :'
        help_who_play = '!whoPlay permet de lancer un vote et ainsi de ' \
                        'savoir qui sera disponible pour jouer avec ' \
                        'les copains ce soir !'
        help_list = '!list affiche les différent votant à la question de !whoPlay'
        help_invocation = '!invocation permet de mentionner tout les votant qui ont répondu positivement ' \
                          'à la question de !whoPlay'
        help_reset = '!reset permet de remettre à zéro le vote, et vide la liste des copains qui ' \
                     'se sont enregistré'
        await client.send_message(message.channel, help_msg)
        await client.send_message(message.channel, help_who_play)
        await client.send_message(message.channel, help_list)
        await client.send_message(message.channel, help_invocation)
        await client.send_message(message.channel, help_reset)

    if message.content.startswith('ROCK AND STONES'):
        drg = 'TO THE BONES !!'
        await client.send_message(message.channel, drg)

    if message.content.startswith('!WhoIsBG'):
        member_objectbg = message.server.get_member_named('Strategychess')
        await client.send_message(message.channel, member_objectbg.mention + 'est beaucoup trop BG !')

    if message.content.startswith('!WhoIsPD'):
        member_object = message.server.get_member_named('darksoutofar')
        await client.send_message(message.channel, member_object.mention + ' est un pd !')

    if message.content.startswith('!whoPlay'):
        msg_who = 'Qui est chaud pour jouer avec les copains aujourd\'hui ? (pour voter, réagir avec 👍 ou 👎)'
        msg_react = await client.send_message(message.channel, msg_who)
        reaction_yes = '👍'
        reaction_no = '👎'
        await client.add_reaction(msg_react, reaction_yes)
        await client.add_reaction(msg_react, reaction_no)

        @client.event
        async def on_reaction_add(reaction, user):
            if user != client.user:
                # On vérifie que le message sur lequel on réagit est bien la question envoyé par le bot
                if reaction.message.content == msg_react.content:
                    # On test si la réaction de l'utilisateur est positive
                    if reaction.emoji == reaction_yes:
                        # On vérifie si l'utilisateur n'est pas dans la list des négations
                        if user not in list_who_play_no:
                            # Dans ce cas on l'ajoute dans la liste positive et on informe le chat
                            if user not in list_who_play_yes:
                                list_who_play_yes.append(user)
                        # Sinon, il est dans la liste des négations
                        else:
                            # Donc on l'enlève de la liste Non et on l'ajoute dans la liste Oui
                            list_who_play_no.remove(user)
                            if user not in list_who_play_yes:
                                list_who_play_yes.append(user)
                            await client.remove_reaction(msg_react, reaction_no, user)
                    # Sinon, si la réaction est non
                    elif reaction.emoji == reaction_no:
                        # On vérifie qu'il n'est pas aussi dans la liste oui
                        if user not in list_who_play_yes:
                            # si il n'y est pas alors on l'ajoute dans la liste non et on informe dans le chat
                            if user not in list_who_play_no:
                                list_who_play_no.append(user)
                        # Sinon, il est dans la liste Oui
                        else:
                            # Dans ce cas on l'enlève de la liste oui, et on l'ajoute à la liste non, en prenant soin
                            #   d'enlever l'emoji oui déjà coché si il est coché
                            list_who_play_yes.remove(user)
                            if user not in list_who_play_no:
                                list_who_play_no.append(user)
                            await client.remove_reaction(msg_react, reaction_yes, user)
                    else:
                        await client.send_message(message.channel, 'Bah qu\'est ce que tu fais {} ?? {} C\'est '
                                                                   'pas un emoji '
                                                                   'valide pour voter '
                                                                   'ça...'.format(user.mention, reaction.emoji))
                elif reaction.message.content == msg_ask_sure:
                    if reaction.emoji == reaction_check:
                        list_who_play_yes.clear()
                        list_who_play_no.clear()
                        await client.send_message(message.channel, 'Le vote a bien été reset ! Tu peux relancer un'
                                                                   ' vote avec la commande !whoPlay ou retourner voter '
                                                                   'sur l\'ancien message')
                else:
                    raise ValueError('Reaction sur un mauvais message')
            else:
                raise ValueError('Reaction du bot a ne pas réagir')

        @client.event
        async def on_reaction_remove(reaction, user):
            if reaction.message.content == msg_react.content:
                if reaction.emoji == reaction_yes:
                    if user in list_who_play_yes:
                        list_who_play_yes.remove(user)
                elif reaction.emoji == reaction_no:
                    if user in list_who_play_no:
                        list_who_play_no.remove(user)
                else:
                    raise ValueError('Mauvaise réaction')
            else:
                raise ValueError('Reaction sur un mauvais')

    if message.content.startswith('!list'):
        affiche_list_yes = ""
        affiche_list_no = ""
        for x in list_who_play_yes:
            affiche_list_yes += " {}".format(x.name)
        for y in list_who_play_no:
            affiche_list_no += " {}".format(y.name)
        await client.send_message(message.channel, 'Voici la liste des copains qui souhaitent '
                                                   'jouer 😍 : ' + affiche_list_yes)

        await client.send_message(message.channel, 'Voici la liste des copains qui sont '
                                                   'pas marrant... 😢 : ' + affiche_list_no)

    if message.content.startswith('!invocation'):
        affiche_list_yes = ""
        if len(list_who_play_yes) != 0:
            for x in list_who_play_yes:
                affiche_list_yes += " {}".format(x.mention)
            await client.send_message(message.channel, 'Allez les copains !! c\'est parti ! On joue !! 😍')
            await client.send_message(message.channel, affiche_list_yes)

    if message.content.startswith('!reset'):
        if len(list_who_play_yes) == 0 and len(list_who_play_no) == 0:
            await client.send_message(message.channel, "La liste est déjà vide.")
        else:
            msg_sure = await client.send_message(message.channel, msg_ask_sure)
            await client.add_reaction(msg_sure, reaction_check)
            await client.add_reaction(msg_sure, reaction_uncheck)

'''@client.event
async def on_reaction_add(reaction, user,):
    channel = reaction.message.channel
    if reaction.emoji == '':
        await client.send_message(channel, '{} has added {} to the message: {}'.format(user.mention, reaction.emoji,                                                                                 reaction.message.content))
'''


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------')

client.run(TOKEN)