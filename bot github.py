#Bot do Servidor The Project
#Autoria: Natas#9686 e Will#1687

#importar recursos
import discord
from discord.ext import commands
import datetime
import random
import string
import requests
import os
import time
from urlextract import URLExtract
extractor = URLExtract()
import threading
from sysinfo import getsysinfo
#from daypass import daypass
#-----------------

#especficar ID's
emoji = ':like:547068425067954196'              #id do emoji customizado, foi pego usando \:like:
clube_id = 674680642583134209                   #id do texto para ser reagido no clube do livro
jamesid = 567835811123560478                    #id do james
grupo_id = 674679746919006240                   #id da mensagem do grupo de estudos
regras = 542690955405426698                     #id do canal de regras
registro = 675819847128711182                   #id canal registros
natasid = 283345376231292929                    #meu id para estreitar funções ao meu user. (debbugging)
willid = 258775759324184586
#--------------

#todo list:
#james gado - done
#log - done
#


#iniciando variáveis úteis
entradasdeuserstempo = []                                                               #salva o tempo de entrada de users novos
entradasmembros = []                                                                    #salva os membros novo
newmembernumber = -1                                                                    #membro número
imageextensions = ['.png', '.jpg', '.webp']                                             #extensões para reconhecer imagens para mutar usuários com CPI
pornsites = ['pornhub', 'xvideos', 'xxx', 'xnxx', 'xhamster', 'porn',                   #sinalizar como porn
     'boobs', 'ass', 'pussy', 'dick', 'asshole', 'sex']
redirects = ['bit.ly', 'goo.gl', 'adf.ly', 'tinyurl', 'ow.ly']                          #sinalizar redirects
mensagemflood = 300                                                                     #número de caracteres antes de ser considerado mensagem como spam
membrosativos = []                                                                      #inicia lista de ativos, aqui vão os objetos membros
membrosativosvalores = []                                                               #inicia a lista onde ficam o nº de mensagens, correspondente ao index do membrosativos
membrosativostimes = []                                                                 #inicia a lista onde ficam a hora da última mensagem do index correspondente ao membro
ativothreshold = 100                                                                    #nº de mensagens pra se considerar ativo
tempmember = ''                                                                         #inicia a lista para guardar o membro que se faz checagem ao deletar mensagens
started = datetime.datetime.now()                                                       #pega a hora em que o bot foi iniciado, para cálculo de $uptime depois
initialtime = 0                                                                         #inicia a variável de checks pra reset da lista membrosativosvalores
lastplayingchange = datetime.datetime.now()                                             #inica a variável pra
spam = 120                                                                              #120 é o número para se checar se em 15 minutos de entrada de servidor forem enviadas 120 mensagens, dar mute.
bomdiacooldown = {}                                                                     #aqui ficam temporariamente usuários impedidos de receberem a resposta do bot referente ao bom dia
#-------------------------

def gettplove(message):
    return discord.utils.get(message.guild.emojis, id=522462442366828574)      #representa o emoji tplove, para mostrar, usa-se str(tplove)



def getboasvindasembed(member):
    channel = member.guild.get_channel(regras)
    embed = discord.Embed(              #aqui a gente escreve o embed (texto com formatação top q vai ser enviada nas DM's de quem entra)
        title = '⇝ **Seja bem-vindo(a) ao The Project!** ⇜',
        description = '• O The Project é uma comunidade focada na troca de conhecimento. Todos devem ter acesso a ele, portanto deve ser compartilhado com o próximo. \n \n • Aqui discutimos sobre quaisquer temas, ajudamos uns aos outros em vestibulares, idiomas, ENEM, concursos, entre outros. Somos uma comunidade amigável, sempre ajudando no desenvolvimento pessoal de cada um. Sinta-se a vontade para juntar-se a nós para uma conversa sadia, respeitosa e muito mais! \n \n ⇝ **Lembre-se de ler as {a}, para evitar qualquer transtorno.**'.format(a=channel.mention),
        colour = discord.Color.magenta()
        )
    embed.set_image(url='https://cdn.discordapp.com/attachments/605248064181108767/674644426035036160/unknown.png') #aqui vai a imagem que fica no final da msg, #não funcionam gifs.

    return embed


def daypass():                          #esta função retorna True na primeira vez executada, e True somente uma vez a cada 24 horas.
    global initialtime                                                                  #pega a variável que definimos globalmente, pois local não se aplica a eventos (ex. on_message não requer chamar a variável como global, mas def sim)
    if round(time.time()/86400, 0) > initialtime:                                       #pega o tempo atual e compara com o initial time, que é na primeira vez 0, e depois o tempo antes de ser feito qualquer comparação.
        initialtime = round(time.time()/86400, 0)
        return True
    else:
        initialtime = round(time.time()/86400, 0)
        return False
    

def writelog(lista):                    #função experimental ainda não implementada
    with open(str(lista)+'.txt', 'w') as f:                                             #objetivo é ao pressionar combinação de tecla, salvar a lista de ativos para depois ler ao pressionar a mesma ou combinação diferente.
        for item in lista:
            f.write("%s\n" % item)


def is_troller(m):                      #aqui usamos a variável tempmember para checar nas mensagens que serão apagadas pertecem ao membro desordeiro, retorna True se a mensagem será apagada.
    global tempmember
    return m.author == tempmember


def resetativo():                       #resetativo é o primeiro reset inicial que damos, é onde as listas são definidas com seus "placeholders"
    global membrosativos
    global membrosativosvalores
    global membrosativostimes
    membrosativos = []
    membrosativosvalores = []
    membrosativostimes = []    
    n = 0
    while n < 100:
        membrosativosvalores.append(0)                                                  #enche de zero, pra dar pop e insert, append coloca no fim da lista e não queremos isso
        n += 1
    n = 0
    while n < 100:
        membrosativostimes.append(0)
        n += 1
    #print('Lista de ativos foi RESET!\n\n', membrosativosvalores, membrosativos)


def resetlista():                       #aqui resetamos a lista, a lista na qual pertence os valores, já que não é necessário reiniciar tudo.
    global membrosativosvalores
    membrosativosvalores = []
    n = 0
    while n < 100:
        membrosativosvalores.append(0)
        n += 1
    print('Lista de ativos valores foi RESET!\n\n', membrosativosvalores)


resetativo()                            #inicia as listas


def getadmincargos(member):
    cargoadministrador = discord.utils.get(member.guild.roles, name="Administrador")    #seta o cargo ademiro
    cargomoderador = discord.utils.get(member.guild.roles, name="Moderador")            #seta o cargo moderador
    return cargoadministrador, cargomoderador


def avisomuteDM(message):               #aqui é enviado a mensagem de aviso para o usuário que tomou mute automaticamente
    #will = discord.utils.get(message.guild.members, id=willid)
    natas = discord.utils.get(message.guild.members, id=natasid)
    return message.author.send(content='{.mention}\n*Esta é uma mensagem automática* \n\nOlá, você fui mutado temporariamente no servidor The Project por comportamento potencialmente indesejado, suas mensagens foram salvas e serão posteriormente avaliadas por um moderador.\nSe você acredita que isso é um erro, informe a staff (preferencialmente {.mention}) por favor.\n\nAtenciosamente, equipe The Project.'.format(message.author, natas))


def currenttime():                      #retorna uma string com a data e hora atual com precisão de segundos e não aqueles microsegundos quebrados.
    return str(datetime.datetime.now())[:-7]


spammerdebomdia = True                  #boolean pra responder qlqr um com bom dias e tal.

def spammerdebomdialimiter(member):
    global bomdiacooldown
    try:
        bomdiacooldown[member]
        if datetime.datetime.now() - bomdiacooldown[member] >= datetime.timedelta(seconds=30):
            del bomdiacooldown[member]
            return True
        else:
            return False
    except KeyError:
        bomdiacooldown.update({
            member:datetime.datetime.now()
        })
        return True
        
setorajuda = {                          #aqui é invocado quando alguém usa o $help para obter ajuda.

    '**$ajuda**':'Mostra essa mensagem.',
    '**$mostrarboasvindas**':'Mostra a mensagem de boas-vindas.',
    '**$uptime**':'Retorna o tempo de execução ininterupta do bot.',
    '**teste**':'isso é um teste'}

def coolactivity():                     #randomicamente escolhe dentro dessa lista alguma atividade pro bot mostrar, 10% de chance dele pegar alguma da lista em cada mensagem.
    lista = [

        'The Project',
        'The Project',
        'nada, to estudando.',
        'trying to solve a hard equation. 1+1=?',
        'The Project',
        'The Project',
        'nada, to estudando.',
        'James gado',
        'The Project',
        'The Project',
        'throwing money to hoes',
        'NATAS LINDOOOOOO',
        'The Project',
        'The Project',
        'nada, to estudando.',
        'The Project',
        'The Project',
        'Python',
        'The Project',
        'The Project',
        'nada, to estudando.',
        'Prefixo: $',
        'The Project',
        'The Project',
        'nada, to estudando.',
        'nada, to estudando.',
        'The Project',
        '𝕓𝕦𝕘𝕤 𝕡𝕣𝕠 𝕒𝕝𝕥𝕠',
        '[̲̅b][̲̅u][̲̅g][̲̅s] [̲̅p][̲̅r][̲̅o] [̲̅a][̲̅l][̲̅t][̲̅o]',
        'b̸͇͕͕̱̜͔̓͐͜u̴̦͇͂͐͋̓̽͌̅͑̕g̴̠̾̽̆͑s̶̘͎͙͍͒̉̀̐͘ͅ ̷̘̘̦͛͛̍̄̀̇̆͋͠ṗ̵̖̗̎͐͝ṟ̶̼̳͚̬̣͉̓̒̀̈́̑̑̓͑̽ơ̵̢̻͍̤͎͎̾͆͊̉̔̔̀̈́ ̶̨͇̲̜͉̼͌̏́͊͛a̵̤̹̪̿̆̔l̸̡̧͓̜͚͓̖̣̆̽̄͋̐̿̌t̶̪͓̣̬̟̹̹̺͓͖͊̏͋̈́̾̂̕͠o̴͖̗̝̞̣̩͖̣͛͛͊͗',
        'b͓̽u͓̽g͓̽s͓̽ ͓̽p͓̽r͓̽o͓̽ ͓̽a͓̽l͓̽t͓̽o͓̽'
        ]
    
    a = ''.join(random.sample(string.digits, 1))
    global lastplayingchange
    if int(a) > 4:
        if datetime.datetime.now() - lastplayingchange > datetime.timedelta(minutes=1):
            lastplayingchange = datetime.datetime.now()
            return random.choice(lista)
        else:
            return 'The Project'
    else:
        return 'The Project'






#vc coloca as funções que usam self dentro dessa buceta aqui
class MyClient(discord.Client):


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    #raw pq se não for raw, ele não escuta os reacts em mensagens que foram enviadas antes de iniciar o bot


    async def on_raw_reaction_remove(self, event):
        userid = event.user_id                          #pega o id de quem reagiu
        guild = discord.Client.get_guild(self, id=event.guild_id) #pega a guild
        member = guild.get_member(userid)               #procura o objeto membro correspondente ao id dentro da guild
        #print(event.channel_id, userid, member)
        livro = discord.utils.get(member.guild.roles, name="Clube do Livro") #encontra a role de clube do livro, mesma coisa em baixo
        estudos = discord.utils.get(member.guild.roles, name="Grupo de Estudos")
        id = event.message_id                           #pega o id a mensagem reagida e verifica se a mensagem reagida é a mesma do clube do livro ou estudos
        if id == clube_id:
            if str(event.emoji) == '\U0001F4DA':
                await discord.Member.remove_roles(member, livro) #tira a role
                await member.guild.get_channel(registro).send(content='[{}] Removido de {.mention} Grupo de Estudos'.format(currenttime(), member)) #escreve no log
        if id == grupo_id:
            if str(event.emoji) == '\U0001F4DA':
                await discord.Member.remove_roles(member, estudos)
                await member.guild.get_channel(registro).send(content='[{}] Removido de {.mention} Grupo de Estudos'.format(currenttime(), member))
                #writelog(member, 'Removido de {} Grupo de Estudos'.format(member))
                #print('[{}] Removido de {} Grupo de Estudos'.format(currenttime(), member))
        #clube_id = event.channel_id
client = MyClient()                                     #nem sei pq isso existe



@client.event
async def on_message(message):                          #aqui ficam todos os comandos relacionados a mensagens enviadas


    if message.guild != None:

        guild = message.guild                           #pega a guild
        #define o message.author como member direto pra poupar espaço
        member = message.author
        #--- parte de detecção de raids.
        ademir = discord.utils.get(message.guild.roles, name="Administrador")
        mutedrole = discord.utils.get(message.guild.roles, name="Muted")
        cargo2pontos = discord.utils.get(message.guild.roles, name="..")
        cargocaveira = discord.utils.get(message.guild.roles, name="\U0001F480")
        #--- cargos pegos


    if message.author.bot:                              #não escutar mensagens de bot. é um boolean.
        return


    if message.author.id == natasid and str(message.channel) == 'Direct Message with Natas#9686':                    #verifica se quem manda mensagem sou eu
        print(message.channel)                      #depois de verificado
        await message.author.send('Olá, Natas, aqui está seu pedido.')
        await message.author.send('**Server Status:**\n\n'+str(getsysinfo()))     #enviar o system information de volta no DM
        return


    if 'Direct Message with' in str(message.channel):
        await message.author.send('O bot não suporta envio de mensagens por mensagem direta, por favor, utilize o canal de #bots em um servidor para seu uso!')
        return


    if 'obrigado' in message.content.lower() and client.user.mentioned_in(message=message): #se agradecer o bot, responder com uma mensagem legal
        await message.channel.send('Disponha, {.mention} {}'.format(message.author, str(gettplove(message))))


    await client.change_presence(status=discord.Status.idle, activity=discord.Game(coolactivity())) #seta o 'jogando'


    if str(message.channel) == 'apresentações-introdução':  #mensagens aqui serão reagidas com like
        await message.add_reaction(emoji); await message.add_reaction(gettplove(message))               #emoji personalido :like:
        await guild.get_channel(registro).send(content='[{}] Nova apresentação de {.mention}'.format(currenttime(), message.author))
        await message.author.add_roles(discord.utils.get(message.guild.roles, name='Apresentado'))
        return


    #JULGAMENTO
    if str(member.roles).find('..') != -1:                  #detecta se o user tem o cargo ..
        if message.channel.name != 'apresentações-introdução':#pra não escutar introduções
            if len(message.content) > mensagemflood:        #se a mensagem é spam, contendo mais de 300 caracteres
                if member.top_role == cargocaveira:
                #mute nele, e embaixo faz um log no registro
                    global tempmember
                    tempmember = message.author
                    await avisomuteDM(message)
                    await member.add_roles(mutedrole)
                    await member.guild.get_channel(registro).send(content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(mensagem grande)_ no canal {.mention}\n\nMensagem enviada: {} \n\ntamanho: {}\\{} \n\n '.format(currenttime(), ademir, message.author, message.channel, message.content, len(message.content), mensagemflood))
                    await message.channel.purge(limit=15, check=is_troller)
                
                if member.top_role != cargocaveira:
                    await member.guild.get_channel(registro).send(content='[{}] \n\nusuário {.mention} cometeu infração _mensagem longa_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                await member.add_roles(cargocaveira)

            for i in imageextensions:                       #apaga mensagens contendo imagens como attachments
                if str(message.attachments).find(i) != -1:  #procura se a mensagem tem imagem.
                    if member.top_role == cargocaveira:
                        files = []                              #define a lista
                        filename = message.attachments[0].filename #define o nome de arquivo
                        os.system('wget –-quiet {} -O {}'.format(message.attachments[0].url, filename)) #baixa a imagem, precisa ter o wget dentro do path sistema
                        await member.add_roles(mutedrole)       #dá mute, e salva no registro
                        await avisomuteDM(message)
                        files = discord.File("{}".format(filename), filename="/home/natas/bot/{}".format(filename))
                        await member.guild.get_channel(registro).send(file=files, content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(envio de imagem)_ no canal {.mention} \n\ntrigger: {} \n\nMensagem enviada:\n\n'.format(currenttime(), ademir, message.author, message.channel, i))
                        #try:
                        #global tempmember
                        tempmember = message.author
                        await message.channel.purge(limit=15, check=is_troller)
                        #except:
                        #    raise Exception('Erro: Mensagem Já Deletada')
                        #    break

                    if member.top_role != cargocaveira:
                        await member.guild.get_channel(registro).send(content='[{}] \n\nusuário {.mention} cometeu infração _envio de imagem não verificada_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                    await member.add_roles(cargocaveira)

            for i in imageextensions:                       #apaga mensagens contendo link de imagens
                if message.content.find(i) != -1:
                    if member.top_role == cargocaveira:
                        await member.add_roles(mutedrole)
                        await avisomuteDM(message)
                        await member.guild.get_channel(registro).send(content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(envio de link de imagem)_ no canal {.channel} \n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                        #global tempmember
                        tempmember = message.author
                        await message.channel.purge(limit=15, check=is_troller)

                    if member.top_role != cargocaveira:
                        await member.guild.get_channel(registro).send(content='[{}] \n\nusuário {.mention} cometeu infração _mensagem longa_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                    await member.add_roles(cargocaveira)

            for i in pornsites:                             #apaga mensagens contendo links apra sites pornográficos
                if message.content.find(i) != -1:
                    if member.top_role == cargocaveira:
                        if extractor.has_urls(message.content):
                            await member.add_roles(mutedrole)
                            await avisomuteDM(message)
                            #global tempmember
                            tempmember = message.author
                            await message.channel.purge(limit=15, check=is_troller)

                    if member.top_role != cargocaveira:
                        await member.guild.get_channel(registro).send(content='[{}] \n\nusuário {.mention} cometeu infração _mensagem longa_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                    await member.add_roles(cargocaveira)

            for i in redirects:                             #apaga mensagens contendo redirecionadores
                if message.content.find(i) != -1:
                    if extractor.has_urls(message.content):
                        if member.top_role == cargocaveira:
                            await member.add_roles(mutedrole)
                            await avisomuteDM(message)
                            await member.guild.get_channel(registro).send(content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(link com redirect)_ no canal {.mention}\n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                            #global tempmember
                            tempmember = message.author
                            await message.channel.purge(limit=15, check=is_troller)

                        if member.top_role != cargocaveira:
                            await member.guild.get_channel(registro).send(content='[{}] \n\nusuário {.mention} cometeu infração _mensagem longa_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                        await member.add_roles(cargocaveira)
        #remover cargo 2 pontos se o usuário tiver dentro do server por mais de 24h

        if (datetime.datetime.now() - member.joined_at) > datetime.timedelta(hours=24):
            if member.top_role == cargo2pontos:
                await member.remove_roles(cargo2pontos)
                await member.guild.get_channel(registro).send(content='[{}] Usuário {.mention} removido do watchdog por tempo de servidor > 24h'.format(currenttime(), message.author))
    #----fim seção mutar/avisar/registrar


    if str(message.channel) == 'sugestões':                 #verifica se essa msg foi enviada no sugestões, etc
        await message.add_reaction('\U0001F44D')        #thumbsup
        await message.add_reaction('\U0001F44E')        #thumbsdown
        await guild.get_channel(registro).send(content='[{}] Nova sugestão de {.mention}'.format(currenttime(), message.author))

    if message.content.startswith('$help') or message.content.startswith('$ajuda'):             #comando de ajuda #procura o canal com id regras, pra mencionar nas DM's depois

        embed = discord.Embed( #aqui a gente escreve o embed (texto com formatação top q vai ser enviada nas DM's de quem entra)
            title = '⇝ **Ajuda: The Project!** ⇜',
            #description = '• O The Project é uma comunidade focada na troca de conhecimento. Todos devem ter acesso a ele, portanto deve ser compartilhado com o próximo. \n \n • Aqui discutimos sobre quaisquer temas, ajudamos uns aos outros em vestibulares, idiomas, ENEM, concursos, entre outros. Somos uma comunidade amigável, sempre ajudando no desenvolvimento pessoal de cada um. Sinta-se a vontade para juntar-se a nós para uma conversa sadia, respeitosa e muito mais! \n \n ⇝ **Lembre-se de ler as, para evitar qualquer transtorno.**',
            colour = discord.Color.blue()
        )

        for x in setorajuda:
            embed.add_field(name='**'+x+'**', value=setorajuda[x], inline=False)
        embed.set_footer(text='Criado por Natas#9686 e Will#1687')
        await message.channel.send(embed=embed)

    if message.content.startswith('$meutico'):          #sei la fds
        await message.channel.send('**grande**')
    if message.content.startswith('$uptime'):
        await message.channel.send('`Bot uptime is {}`'.format(datetime.datetime.now() - started))

    if message.channel == 'clube-do-livro' or message.channel == 'grupo-de-estudos':
        await message.add_reaction('\U0001F4DA')#books  #mensagens aqui serão reagidas com livros

    if message.author.id == jamesid:                    #verifica se quem mandou foi o james

        if len(message.content) > 15:
            await message.add_reaction(':tpjames:626957423634022421')
        else:
            await message.add_reaction(':tpjames:659586056466857984')

        if message.content.find('madame') != -1 or message.content.find('senhorita') != -1:
            await message.add_reaction('🇬');await message.add_reaction('🇦');await message.add_reaction('🇩');await message.add_reaction('🇴')

    if str(message.channel) == 'aprovações':            #reações no aprovações
        await message.add_reaction('\U0001F942');await message.add_reaction('\U0001F389')#champanhe e :tada:
        #await message.add_reaction('\U0001F3C6')       #troféu

    if client.user.mentioned_in(message=message) and message.mention_everyone is False:
        if 'ajuda' in message.content or 'help' in message.content:
            await message.channel.send('eae gay, tá com medo porque?')
        else:
            await message.add_reaction('\U0001F440')


    if spammerdebomdia:

        if message.content.lower().startswith('bom dia') and spammerdebomdialimiter(message.author) is True:
            if 18 >= datetime.datetime.now().hour >= 12:
                await message.channel.send(content='Não sei você mas aqui já é boa tarde {.mention}.'.format(message.author))
            else:
                if 6 <= datetime.datetime.now().hour < 12:
                    await message.channel.send(content='Bom dia, {}.'.format(message.author.name[0].upper()+message.author.name[1:]))
                else:                
                    await message.channel.send(content='Acordou agora bela adormecida? Já é de noite {.mention}.'.format(message.author))

        if message.content.lower().startswith('boa tarde') and spammerdebomdialimiter(message.author) is True:
            if datetime.datetime.now().hour > 18:
                await message.channel.send(content='Não sei você mas aqui já é boa noite {.mention}.'.format(message.author))
            else:
                if datetime.datetime.now().hour >= 12:
                    await message.channel.send(content='Boa tarde, {}.'.format(message.author.name[0].upper()+message.author.name[1:]))
                if datetime.datetime.now().hour < 12:
                    await message.channel.send(content='Boa tarde? Cê tá maluco meu, é de manhã ainda {.mention}'.format(message.author))
                
        if message.content.lower().startswith('boa noite') and spammerdebomdialimiter(message.author) is True:
            if 18 <= datetime.datetime.now().hour <= 23:
                await message.channel.send(content='Boa noite, {}.'.format(message.author.name[0].upper()+message.author.name[1:]))
            elif 0 <= datetime.datetime.now().hour <= 6:
                await message.channel.send(content='Boa noite, {}.'.format(message.author.name[0].upper()+message.author.name[1:]))
            else:
                kekw = await message.author.guild.fetch_emoji(emoji_id=633527255993417768)
                await message.channel.send(content='Tu tá fora né? O cara manda um boa noite essas horas {}'.format(str(kekw)))


    if message.content.startswith('$mostrarboasvindas'):
        embed = getboasvindasembed(message.author)
        await message.channel.send(embed=embed)
    

    #registrar mensagens para cargo ativo
    if len(message.content) >= 7:
        if daypass() == True:
            resetlista()
        try:
            if membrosativos.index(member)+1:
                #print('membrosativos.index(member):', membrosativos.index(member)) #read at index, +=1, pop, insert at index


                tempvalue = membrosativosvalores[membrosativos.index(member)]
                tempvalue += 1
                membrosativosvalores.pop(membrosativos.index(member))
                membrosativosvalores.insert(membrosativos.index(member), tempvalue)

                membrosativostimes.pop(membrosativos.index(member))
                membrosativostimes.insert(membrosativos.index(member), datetime.datetime.now())


                #print(membrosativostimes)
                #print('membrosativosvalores', membrosativosvalores)
                print('[{}] membro {} nº {} total de mensagens: {}'.format(currenttime() , member, membrosativos.index(member), tempvalue))
        except ValueError:
            membrosativos.append(member)
            print('adicionado {} na lista de ativos para computação de dados'.format(member))


        if membrosativosvalores[membrosativos.index(member)] >= spam:
            if datetime.datetime.now() - member.joined_at <= datetime.timedelta(minutes=15):
                await avisomuteDM(message)
                tempmember = member
                await message.channel.purge(limit=500, check=is_troller)
                await member.add_roles(mutedrole)

        
        #global membrosativosvalores
        if membrosativosvalores[membrosativos.index(member)] > ativothreshold:
            
            if str(member.roles).find('Ativo') == -1:
                await member.add_roles(discord.utils.get(member.guild.roles, name='Ativo'))
                await member.guild.get_channel(registro).send(content='[{}] Usuário {.mention} adicionado cargo Ativo.'.format(currenttime(), message.author))
                #print('Dado cargo ativo ao {}'.format(member))


    for i in membrosativostimes:
        try:
            if datetime.datetime.now() - i > datetime.timedelta(days=2):
                member1 = membrosativos[membrosativostimes.index(i)]                #pega o membro referente, e não o atual

                membrosativos.pop(membrosativostimes.index(i))                      #remove o registro dele
                membrosativostimes.pop(membrosativostimes.index(i))                 #nas 3
                membrosativosvalores.pop(membrosativostimes.index(i))               #listas

                if str(member1.roles).find('Ativo') != -1:                          #se encontrar a tag ativo nele
                    await member1.remove_roles(discord.utils.get(member.guild.roles, name='Ativo')) #remove
                    await member1.guild.get_channel(registro).send(content='[{}] Usuário {.mention} removido do cargo Ativo por inatividade dentre 2 dias.'.format(currenttime(), member1))
        except TypeError:
            pass
    '''
    writelog(membrosativos)
    writelog(membrosativostimes)
    writelog(membrosativosvalores)
    '''

    

@client.event                                           #quando o user entra, mostrar uma mensagem de boas vindas.
async def on_member_join(member):
    global newmembernumber
    newmembernumber += 1
    #BOAS VINDAS
    channel = member.guild.get_channel(regras)          #procura o canal com id regras, pra mencionar nas DM's depois
    embed = getboasvindasembed(member)
    await member.send(embed=embed)                      #envia o embed
    await member.guild.get_channel(registro).send(content='[{}] Dado boas-vindas ao {.mention}'.format(currenttime(), member))
    #--------fim boas vindas



    #começo do check de veracidade.
    tempodeexistencia = datetime.timedelta.total_seconds(datetime.datetime.now() - member.created_at)/86400 #resposta dada em dias
    #print(datetime.timedelta.total_seconds(tempodeexistencia)/86400)

    if tempodeexistencia < 1:
        channel = member.guild.get_channel(registro)
        cargo2pontos = discord.utils.get(member.guild.roles, name="..")
        await member.add_roles(cargo2pontos)
        await channel.send('[{}] Usuário {.mention} com menos de 1 dia de conta no Discord entrou no servidor. watchdog adicionado.'.format(currenttime(), member))
        #print('Novo usuário conta nova.')


    #entradasdeuserstempo.update( {str(member): member.joined_at} )
    entradasdeuserstempo.append(member.joined_at - datetime.timedelta(hours=3))
    entradasmembros.append(member)
    #print('entradastempo:',entradasdeuserstempo, '\n\n', 'entradasmembro:',entradasmembros)


    if entradasdeuserstempo[1]:
        #print('entradasdeuserstempo is true')
        print('NMN:', newmembernumber)

        lastuserjoin = entradasdeuserstempo[newmembernumber]
        lastlastuserjoin = entradasdeuserstempo[-1+newmembernumber]
        #print('lastuserjoin:', lastuserjoin, 'datetime:', datetime.datetime.now())
        #print('entre users:', datetime.datetime.now() - lastuserjoin)
        if lastuserjoin - lastlastuserjoin <= datetime.timedelta(minutes=4.5):
            #print('assigning roles')
            cargo2pontos = discord.utils.get(member.guild.roles, name="..")
            try:
                oldmember = entradasmembros[-1+newmembernumber]
                await oldmember.add_roles(cargo2pontos)
                await member.guild.get_channel(registro).send(content='[{}] Cargo watchdog adicionado ao {.mention} e {.mention}, entraram em menos de {} minutos'.format(currenttime(), member, oldmember, round(datetime.timedelta.total_seconds(lastuserjoin - lastlastuserjoin)/60, 2)))
            except:
                raise Exception('exception at try: line 369')
            await member.add_roles(cargo2pontos)
            


@client.event                                           #add a role Clube do Livro/Grupode Estudos
async def on_raw_reaction_add(event):
    #id = event.user_id                                 #pega id de quem reagiu
    member = event.member                               #aqui não precisa procurar dentro da guild pra pegar o objeto membro
    livro = discord.utils.get(member.guild.roles, name="Clube do Livro")
    estudos = discord.utils.get(member.guild.roles, name="Grupo de Estudos")
    #print(test)
    if event.message_id == clube_id:                    #verifica se a msg é a certa
        if str(event.emoji) == '\U0001F4DA':            #isso aqui é pra somente se o emoji for os livros
            await discord.Member.add_roles(member, livro) #add role
            await member.guild.get_channel(registro).send(content='[{}] Adicionado ao {.mention} Clube do Livro'.format(currenttime(), member))
    if event.message_id == grupo_id:
        if str(event.emoji) == '\U0001F4DA':
            await discord.Member.add_roles(member, estudos)
            await member.guild.get_channel(registro).send(content='[{}] Adicionado ao {.mention} Grupo de Estudos'.format(currenttime(), member))


    

client.run('<censored>') #especificar o token para executar o bot