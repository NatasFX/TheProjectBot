#Bot do Servidor The Project
#Autoria: Natas#9686 e Will#1687

#importar módulos
from secret import secret
import discord                                      #Importando API do discord
from discord.ext import commands                    #Facilitar pra criar comandos
import datetime                                     #datetime, melhor módulo pra manejamento de tempo
import random                                       #random é pra fazer random.
import string                                       #importar strings padronizadas
import requests                                     #requests pra baixar as imagens
import os                                           #pra usar com os.system ou os.popen
import time                                         #time né
from urlextract import URLExtract                   #extrator de URL's
extractor = URLExtract()                            #definindo o extrator pra ficar com menos texto
import threading                                    #threading que por enquanto n estou usando
from sysinfo import getsysinfo                      #meu módulo pra retornar a informação de sistema
from wakeonlan import send_magic_packet             #pra acordar meu pc
import pyscreenshot as ImageGrab                    #imagegrab pra tirar screenshots
import logging                                      #meio que inútil
import pickle                                       #fazer os salvamentos das listas
import tracemalloc
tracemalloc.start()
import traceback
#-----------------          

#especficar ID's
emoji = ':like:547068425067954196'                  #id do emoji customizado, foi pego usando \:like:
clube_id = 674680642583134209                       #id do texto para ser reagido no clube do livro
jamesid = 567835811123560478                        #id do james
grupo_id = 674679746919006240                       #id do canal de mensagem do grupo de estudos
regras = 542690955405426698                         #id do canal de regras
registro = 675819847128711182                       #id do canal registros
natasid = 283345376231292929                        #id do meu user para estreitar funções ao meu user. (debbugging)
willid = 258775759324184586                         #id do will
#-------------- 

#todo list:
#james gado - done
#log - done
#games
#ativos n precisar de 1 msgs só pra continuar ativos.
#persistence no cargo de ..
#não apagar mensagens contento ass que sejam do tenor


#iniciando variáveis úteis
entradasdeuserstempo = []                                                               #salva o tempo de entrada de users novos
entradasmembros = []                                                                    #salva os membros novo
newmembernumber = -1                                                                    #membro número
imageextensions = ['.png', '.jpg', '.webp', '.jpeg', '.mp4', '.3gp', 
    '.mov', '.webm', '.torrent', '.zip', '.rar']                                             #extensões para reconhecer imagens para mutar usuários com CPI
pornsites = ['pornhub', 'xvideos', 'xxx', 'xnxx', 'xhamster', 'porn',                   #sinalizar como porn
     'boobs', 'ass', 'pussy', 'dick', 'asshole', 'sex', 'discord.gg']
redirects = ['bit.ly', 'goo.gl', 'adf.ly', 'tinyurl', 'ow.ly']                          #sinalizar redirects
mensagemflood = 300                                                                     #número de caracteres antes de ser considerado mensagem como spam
membrosativos = []                                                                      #inicia lista de ativos, aqui vão os objetos membros
membrosativosvalores = []                                                               #inicia a lista onde ficam o nº de mensagens, correspondente ao index do membrosativos
membrosativostimes = []                                                                 #inicia a lista onde ficam a hora da última mensagem do index correspondente ao membro
ativothreshold = 100                                                                    #nº de mensagens pra se considerar ativo
tempmember = ''                                                                         #inicia a lista para guardar o membro que se faz checagem ao deletar mensagens
started = datetime.datetime.now()                                                       #pega a hora em que o bot foi iniciado, para cálculo de $uptime depois
initialtime = round(time.time()/86400, 0)                                               #inicia a variável de checks pra reset da lista membrosativosvalores
lastplayingchange = datetime.datetime.now()                                             #inica a variável pra
spam = 120                                                                              #120 é o número para se checar se em 15 minutos de entrada de servidor forem enviadas 120 mensagens, dar mute.
bomdiacooldown = {}                                                                     #aqui ficam temporariamente usuários impedidos de receberem a resposta do bot referente ao bom dia
logging.basicConfig(filename='botlog.log', filemode='w', format='%(levelname)s - %(message)s')
eventofilme = False                                                                      #especifica se tem evento de filme ou não.
spammerdebomdia = True                                                                  #boolean pra responder qlqr um com bom dias e tal.
eventofilmelista = {}                                                                   #inicia a variável para armazenas quem e o que sugeriu no evento de filme.
listasugestãofilme = {}                                                                 #inicia a variável que faz alguma coisa q n lembro.
reloadativostime = 0                                                                    #ainda  n to usando isso
directmessages = {}                                                                     #pra salvar as mensagens que os locos me enviam por direct no bot.
setorajuda = {                                                                          #aqui é invocado quando alguém usa o $help para obter ajuda.

    '**$ajuda**':'Mostra essa mensagem.',
    '**$mostrarboasvindas**':'Mostra a mensagem de boas-vindas.',
    '**$uptime**':'Retorna o tempo de execução ininterupta do bot.',
    '**$sugerirfilme**':'Usado para sugerir nomes de filmes quando acontecerá um evento de filme.',
    '**$versugestão**':'Usado para ver as sugestões de filme suas ou de outros usuários',
    '**$apagarsugestão**':'Usado para apagar suas sugestões.',
    '**$dice**':'Joga dados.'
    }
natasmember = ''
lastuserjoin = ''
lastlastuserjoin = ''
attachmentsApagados = {}
discordget = discord.utils.get
roles = ['Centro-Oeste','Sudeste', 'Sul','Nordeste','Norte']
roles_emoji = ['🌿','🍞','🧉','🌴','🧭']
#-------------------------


class attachment:
    def __init__(self, time, message_id, channel_name, author, filename, fileformat, nomearquivo):
        self.time = time
        self.message_id = message_id
        self.channel_name = channel_name
        self.author = author
        self.filename = filename
        self.fileformat = fileformat
        self.nomearquivo = nomearquivo



def gettplove(message):
    return discordget(message.guild.emojis, id=522462442366828574)      #representa o emoji tplove, para mostrar, usa-se str(tplove)


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
    

def log(information):                    #função experimental ainda não implementada
    '''
    with open(str(lista)+'.txt', 'w') as f:                                             #objetivo é ao pressionar combinação de tecla, salvar a lista de ativos para depois ler ao pressionar a mesma ou combinação diferente.
        for item in lista:
            f.write("%s\n" % item)
    '''
    logging.info(information)


def aprovarsugestão(member, message):
    channel = discordget(member.guild.channels, name='sugestões-de-filmes')
    return channel.send(content=str(message))


def is_troller(m):                      #aqui usamos a variável tempmember para checar nas mensagens que serão apagadas pertecem ao membro desordeiro, retorna True se a mensagem será apagada.
    global tempmember
    return m.author == tempmember



def savelistasugestãofilme():
    global listasugestãofilme
    with open('listasugestãofilme.txt', 'wb') as f:
        pickle.dump(listasugestãofilme, f)

def saveativos():
    with open("ativos.txt", "wb") as fp:   #Pickling
        pickle.dump(membrosativos, fp)

def savetimes():
    with open("times.txt", "wb") as fp:   #Pickling
        pickle.dump(membrosativostimes, fp)

def savevalores():
    with open("valores.txt", "wb") as fp:   #Pickling
        pickle.dump(membrosativosvalores, fp)

def saveeventofilmelista():
    global eventofilmelista
    with open('eventofilmelista.txt', 'wb') as f:
        pickle.dump(eventofilmelista, f)

def savedirectmessages():
    global directmessages
    with open('directmessages.txt', 'wb') as f:
        pickle.dump(directmessages, f)



def loadlistasugestãofilme():
    global listasugestãofilme
    try:
        with open('listasugestãofilme.txt', 'rb') as f:
            listasugestãofilme = pickle.load(f)
    except:
        with open('listasugestãofilme.txt', 'wb') as f:
            pickle.dump(listasugestãofilme, f)

def loadativos():
    global membrosativos
    try:
        with open("ativos.txt", "rb") as fp:   # Unpickling
            membrosativos = pickle.load(fp)
    except:
        with open("ativos.txt", "wb") as fp:   # Unpickling
            pickle.dump(membrosativos, fp)

def loadtimes():
    global membrosativostimes  
    try:
        with open("times.txt", "rb") as fp:   # Unpickling
            membrosativostimes = pickle.load(fp)
    except:
        n = 0
        while n < 1000:
            membrosativostimes.append(0)                                                  #enche de zero, pra dar pop e insert, append coloca no fim da lista e não queremos isso
            n += 1
        with open("times.txt", "wb") as fp:   # Unpickling
            pickle.dump(membrosativostimes, fp)

def loadvalores():
    global membrosativosvalores
    try:
        with open("valores.txt", "rb") as fp:   # Unpickling
            membrosativosvalores = pickle.load(fp)
    except:
        n = 0
        while n < 1000:
            membrosativosvalores.append(0)                                                  #enche de zero, pra dar pop e insert, append coloca no fim da lista e não queremos isso
            n += 1
        with open("valores.txt", "wb") as fp:   # Unpickling
            pickle.dump(membrosativosvalores, fp)

def loadeventofilmelista():
    global eventofilmelista
    try:
        with open('eventofilmelista.txt', 'rb') as f:
            eventofilmelista = pickle.load(f)
    except:
        with open('eventofilmelista.txt', 'wb') as f:
            pickle.dump(eventofilmelista, f)

def resetativo():                       #resetativo é o primeiro reset inicial que damos, é onde as listas são definidas com seus "placeholders"
    n=1000
    for i in membrosativosvalores:
        if i !=0:
            n -= 1
        
    
    '''
    global membrosativos
    global membrosativosvalores
    global membrosativostimes
    membrosativos = []
    membrosativosvalores = []
    membrosativostimes = []    
    n = 0
    while n < 1000:
        membrosativosvalores.append(0)                                                  #enche de zero, pra dar pop e insert, append coloca no fim da lista e não queremos isso
        n += 1
    n = 0
    while n < 1000:
        membrosativostimes.append(0)
        n += 1
    
    saveativos()
    savetimes()
    savevalores()
    '''
    loadativos()
    loadtimes()
    loadvalores()
    if eventofilme:
        loadeventofilmelista()
        loadlistasugestãofilme()

    n=1000
    for i in membrosativosvalores:
        if i !=0:
            n -= 1

    print('Listas iniciadas\nslots restantes:', n)#, membrosativos, membrosativostimes, membrosativosvalores)
    
def resetlista():                       #aqui resetamos a lista, a lista na qual pertence os valores, já que não é necessário reiniciar tudo.
    global membrosativosvalores
    membrosativosvalores = []
    n = 0
    while n < 1000:
        membrosativosvalores.append(0)
        n += 1
    print('Lista de ativos valores foi RESET!')


resetativo()                            #inicia as listas


def getadmincargos(member):
    cargoadministrador = discordget(member.guild.roles, name="Administrador")    #seta o cargo ademiro
    cargomoderador = discordget(member.guild.roles, name="Moderador")            #seta o cargo moderador
    return cargoadministrador, cargomoderador


def avisomuteDM(message):               #aqui é enviado a mensagem de aviso para o usuário que tomou mute automaticamente
    #will = discordget(message.guild.members, id=willid)
    natas = discordget(message.guild.members, id=natasid)
    return message.author.send(content='{.mention}\n*Esta é uma mensagem automática* \n\nOlá, você fui mutado temporariamente no servidor The Project por comportamento potencialmente indesejado, suas mensagens foram salvas e serão posteriormente avaliadas por um moderador.\nSe você acredita que isso é um erro, informe a staff (preferencialmente {.mention}) por favor.\n\nAtenciosamente, equipe The Project.'.format(message.author, natas))


def currenttime():                      #retorna uma string com a data e hora atual com precisão de segundos e não aqueles microsegundos quebrados.
    return datetime.datetime.now().strftime('%d.%h.%Y %H:%M:%S')


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





client = discord.Client()                                  #nem sei pq isso existe
#client.allowed_mentions(everyone = False)
client = commands.Bot(command_prefix = '$')                 #isso eu sei

#


@client.event
async def on_raw_reaction_remove(event):
    global roles
    global roles_emojis
    userid = event.user_id                                  #pega o id de quem reagiu
    guild = client.get_guild(id=event.guild_id)             #pega a guild
    member = guild.get_member(userid)                       #procura o objeto membro correspondente ao id dentro da guild
    memberroles = member.roles
    guildroles = member.guild.roles
    if event.channel_id != 697863869707845682:
        livro = discordget(member.guild.roles, name="Clube do Livro") #encontra a role de clube do livro, mesma coisa em baixo
        estudos = discordget(member.guild.roles, name="Grupo de Estudos")
        id = event.message_id                                   #pega o id a mensagem reagida e verifica se a mensagem reagida é a mesma do clube do livro ou estudos
        if id == clube_id:
            if str(event.emoji) == '\U0001F4DA':
                await discord.Member.remove_roles(member, livro)#tira a role
                await member.guild.get_channel(registro).send(content='[{}] Removido de {.mention} Grupo de Estudos'.format(currenttime(), member)) #escreve no log
        
        if id == grupo_id:
            if str(event.emoji) == '\U0001F4DA':
                await discord.Member.remove_roles(member, estudos)
                await member.guild.get_channel(registro).send(content='[{}] Removido de {.mention} Grupo de Estudos'.format(currenttime(), member))


    
    if event.channel_id == 697863869707845682:
        for item in roles:
            if event.emoji.name == roles_emoji[roles.index(item)] and item not in str(memberroles):
                if not any(i in str(memberroles) for i in roles):
                    await member.remove_roles(discordget(guildroles, name=item))
                    return




@client.command()
async def ping(ctx):
    await ctx.send('pinto')





@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    #raw pq se não for raw, ele não escuta os reacts em mensagens que foram enviadas antes de iniciar o bot


@client.event
async def on_message(message):                          #aqui ficam todos os comandos relacionados a mensagens enviadas


    if message.guild != None:

        guild = message.guild                           #pega a guild
        #define o message.author como member direto pra poupar espaço
        member = message.author
        #--- parte de detecção de raids.
        ademir = discordget(message.guild.roles, name="Administrador")
        mutedrole = discordget(message.guild.roles, name="Muted")
        cargo2pontos = discordget(message.guild.roles, name="..")
        cargocaveira = discordget(message.guild.roles, name="\U0001F480")
        #--- cargos pegos


    if message.author.bot:                              #não escutar mensagens de bot. é um boolean.
        return


    if message.author.id == natasid and str(message.channel) == 'Direct Message with Natas#9686':                        #verifica se quem manda mensagem sou eu
        if 'acordar' in message.content:
            send_magic_packet(secret.mac)      #envia o magic packet para o compiuter
            await message.channel.send('Magic packet enviado.')
            return                                      #retorna pra não enviar o negócio

        if 'status' in message.content and not 'command' in message.content:
            await message.author.send('**Server Status:**\n\n'+str(getsysinfo()))
            i=0
            await message.author.send('\n\n**Listas:**\n\n**Ativos:**\n')
            while i<=len(membrosativos)/2000:
                await message.author.send(f'`{str(membrosativos)[(2000*i):1950+(2000*i)]}`')
                i+=1
            i=0
            await message.author.send('\n**Times:**\n')
            while i<=len(str(membrosativostimes))/1980:
                await message.author.send(f'`{str(membrosativostimes)[((1980*i)):1980+(1980*i)]}`')
                i+=1
            i=0

            await message.author.send('\n**Valores:**\n')
            await message.author.send(f'`{membrosativosvalores[:100]}`')

            await message.author.send(f'\n**NMN:**\n`{newmembernumber}`\n**lastuserjoin:**\n`{lastuserjoin}`\n**lastlastuserjoin:**\n`{lastlastuserjoin}`')
            await message.author.send(f'\n**entradasdeuserstempo:**\n`{entradasdeuserstempo}`')
            await message.author.send(f'\n**entradasmembros:**\n`{entradasmembros}`')
            return

        if 'command' in message.content:
            output = os.popen(message.content[message.content.find('command')+8:]).read()
            if not output:
                output = 'Done.'
            await message.author.send(output)
            return

        ''' deprecated, using ssh to view program output
        if ['screenshot','screen','prntsc'] in message.content:
            im = ImageGrab.grab()
            im.save('Screenshot.jpg')
            files = discord.File('Screenshot.jpg')#, filename="c:/users/natas/documents/Screenshot.jpg")
            await message.channel.send(file=files)
            return
        '''

    if 'Direct Message with' in str(message.channel) and 'Natas' not in str(message.channel):
        print('Received DM with {} message=\'{}\''.format(message.author, message.content))
        directmessages.update({
            message.author.id:f'[{currenttime()}], \"{message.content}\"'
        })
        savedirectmessages()
        await message.author.send('O bot não suporta envio de mensagens por mensagem direta, por favor, utilize o canal de #bots em um servidor para seu uso!')
        return


    if 'obrigado' in message.content.lower() and client.user.mentioned_in(message=message): #se agradecer o bot, responder com uma mensagem legal
        await message.channel.send('Disponha, {.mention} {}'.format(message.author, str(gettplove(message))))


    await client.change_presence(status=discord.Status.idle, activity=discord.Game(coolactivity())) #seta o 'jogando'


    if str(message.channel) == 'apresentações-introdução':  #mensagens aqui serão reagidas com like
        await message.add_reaction(emoji); await message.add_reaction(gettplove(message))               #emoji personalido :like:
        await guild.get_channel(registro).send(content='[{}] Nova apresentação de {.mention}'.format(currenttime(), message.author))
        await message.author.add_roles(discordget(message.guild.roles, name='Apresentado'))
        return



    if message.content.startswith('$sugerirfilme') and 200 > len(message.content) > 13 and message.channel.name in ['bots']: #comando $sugerirfilme é ativo quando eventofilme for True
        global eventofilmelista
        global listasugestãofilme
        if eventofilme:                                     #se o evento de filme esstiver ativo
            if eventofilmelista.get(message.author.id) is None or len(eventofilmelista.get(message.author.id)) <= 2:
                if not extractor.has_urls(message.content): #se conter links ele não vai escutar
                    if message.author.id in eventofilmelista.keys():#verifica se o cara já fez alguma sugestão
                        eventofilmelista.get(message.author.id).append(message.content[14:])
                    else:
                        eventofilmelista.update({
                            message.author.id:[message.content[14:]]
                        })
                    

                    staff = discordget(message.guild.channels, name='staff')#pega o canal para envio da solicitação de aprovação
                    
                    msg = await staff.send(content=f'Nova sugestão de filme de {message.author.mention}: \n\"{message.content[14:]}\"\nDeseja aprovar essa sugestão?')
                    await msg.add_reaction(':like:547068425067954196')
                    await msg.add_reaction('\U0001F44E')    #envia a solicitação junto das reações para aprovação ou n
                    listasugestãofilme.update({             #atualiza a lista com id da mensagem de solicitação e o filme escolhido
                        msg.id:[message.content[14:],message.author.id]
                    })
                    savelistasugestãofilme()                #salva a lista no txt
                    await message.channel.send(f'{message.author.mention}, sua sugestão foi enviada, muito obrigado! {str(gettplove(message))}')
                    await message.channel.send(f'Você tem mais {3-len(eventofilmelista[message.author.id])} sugestões de filme')
                    saveeventofilmelista()                  #mostra quantas sugestões de filme ainda podem ser feitas
                    return                                  #sempre bom ter
                else:
                    await message.channel.send(f'{message.author.mention}, ops! aconteceu um erro.')
                    return
            else:
                await message.channel.send(content=f'{message.author.mention}, você não pode fazer mais que 3 sugestões!')
        else:
            await message.channel.send(f'{message.author.mention}, o evento de filme não está ativo no momento ou você já fez uma sugestão.')
            return

    if '$versugestão' in message.content[0:13] and message.channel.name in ['bots'] or '$versugestões' in message.content[0:14] and message.channel.name in ['bots']:
        if not message.mentions:                            #se o user não mencionou ninguém, mostrar as sugestões dele
            if message.author.id in eventofilmelista:       #verifica se ele já fez sugestão
                try:                                        #aqui abaixo envia as sugestões referente ao user que pede
                    await message.channel.send(content=f'{message.author.mention}, segue sua(s) sugestão(ões) de filme(s):\n{eventofilmelista[message.author.id][0]}')
                    await message.channel.send(content=f'{eventofilmelista[message.author.id][1]}')
                    await message.channel.send(content=f'{eventofilmelista[message.author.id][2]}')
                except:
                    await message.channel.send(f'Você ainda pode fazer mais {3-len(eventofilmelista[message.author.id])} sugestão(ões).')
            if message.author.id not in eventofilmelista:
                await message.channel.send(f'Você não fez uma sugestão ainda {message.author.mention}, faça uma usando o comando $sugerirfilme')
                return
        
        if message.mentions:                                #se ele mencionou alguém, mostrar sugestões de quem foi mencionado
            try:
                if message.mentions[0].id in eventofilmelista:
                    try:                                    #aqui abaixo envia as sugestões
                        await message.channel.send(content=f'{message.author.mention}, essas são as sugestões do {message.mentions[0].mention}:')
                        await message.channel.send(content=f'{eventofilmelista[message.mentions[0].id][0]}')
                        await message.channel.send(content=f'{eventofilmelista[message.mentions[0].id][1]}')
                        await message.channel.send(content=f'{eventofilmelista[message.mentions[0].id][2]}')
                    except:
                        pass
                else:
                    await message.channel.send(f'{message.author.mention}, usuário {message.metions[0].mention} não sugeriu filme.')

            except:
                return

    if '$apagarsugestão' in message.content[0:16] and message.channel.name in ['bots'] or '$apagarsugestões' in message.content[0:17] and message.channel.name in ['bots']:#comando para apagar as sugestões previamente feitas para realizar novas.
        msg = await message.channel.send(f'{message.author.mention}, você deseja apagar suas sugestões de filme?')
        await msg.add_reaction('\U0001F44D')
        await msg.add_reaction('\U0001F44E')
        
        channel = message.channel
        def check(reaction, user):
            if str(reaction.emoji) != '👍':
                return
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            pass#await channel.send('Você demorou muito para responder, operação cancelada!', delete_after=5)
        else:
            del eventofilmelista[message.author.id]
            await channel.send('Sugestões de filmes apagados com sucesso!')

    if 'dias sem bater uma' in message.content.lower() or 'não bati uma faz' in message.content.lower() or 'sem bater uma por' in message.content.lower():
        number = ''
        for x in message.content:
            if x.isdigit() and 'dias' in message.content.lower()[message.content.find(x):]:
                number = number+str(x)
        try:
            if len(number) > 10:
                await message.channel.send(content='vou pegar esse monte de dígito ({} aliás) que vc escreveu e enfiar no seu cu seu fdp {}'.format(len(number), message.author.mention))
                return
            if int(number) > 3:
                await message.channel.send(content='{.mention} ficou {} dias sem bater uma? Quem segura leite é vaca porra ta maluco'.format(message.author, number))
                return
        except ValueError:
            pass
        
    if 'dias sem estudar' in message.content.lower() or 'não estudei por' in message.content.lower() or 'não estudei faz' in message.content.lower() or 'não estudei hoje' in message.content:
        number = ''
        for x in message.content:
            if x.isdigit() and 'dias' in message.content.lower()[message.content.find(x):]:
                number = number+str(x)
        try:
            if len(number) > 10:
                await message.channel.send(content='vou pegar esse monte de dígito ({} aliás) que vc escreveu e enfiar no seu cu seu fdp {}'.format(len(number), message.author.mention))
                return
            if int(number) > 1:
                await message.channel.send(content='{.mention} ficou {} dias sem estudar? Desse jeito nunca vai passar no vestibular seu burro'.format(message.author, number))
                return
        except ValueError:
            pass
        if 'não estudei hoje' in message.content:
            message.channel.send(content=f'{message.author.mention}, VOCÊ NÃO ESTUDOU HOJE?????????!!!!!11 \n||eu estarei te observando enquanto procrastina||')
            return
    global natasmember
    if not natasmember and not 'direct' in message.channel.name.lower():
        natasmember = discordget(message.guild.members, id=natasid)

    #JULGAMENTO
    member = message.author
    if str(member.roles).find('..') != -1:                  #detecta se o user tem o cargo ..
        if message.channel.name != 'apresentações-introdução':#pra não escutar introduções
            if len(message.content) > mensagemflood:        #se a mensagem é spam, contendo mais de 300 caracteres
                if member.top_role == cargocaveira:
                #mute nele, e embaixo faz um log no registro
                    global tempmember
                    tempmember = message.author
                    await avisomuteDM(message)
                    await member.add_roles(mutedrole)
                    log(f'Usuário {tempmember} foi mutado por flood.')
                    await message.channel.purge(limit=15, check=is_troller)
                    await member.guild.get_channel(registro).send(content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(mensagem grande)_ no canal {.mention}\n\nMensagem enviada: {} \n\ntamanho: {}\\{} \n\n '.format(currenttime(), ademir, message.author, message.channel, message.content[:1750], len(message.content), mensagemflood))
                    await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)
                    
                
                if member.top_role != cargocaveira:
                    await member.guild.get_channel(registro).send(content='[{}] \n\nusuário {.mention} cometeu infração _mensagem longa_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                await member.add_roles(cargocaveira)

            for i in imageextensions:                       #apaga mensagens contendo imagens como attachments
                if message.channel.name == 'shitpost':
                    return
                if str(message.attachments).lower().find(i) != -1:  #procura se a mensagem tem imagem.
                    if member.top_role == cargocaveira:
                        files = []                              #define a lista
                        filename = message.attachments[0].filename #define o nome de arquivo
                        os.system('wget –-quiet {} -O {}'.format(message.attachments[0].url, filename)) #baixa a imagem, precisa ter o wget dentro do path sistema
                        await member.add_roles(mutedrole)       #dá mute, e salva no registro
                        log(f'Usuário {tempmember} foi mutado por envio de imagem.')
                        await avisomuteDM(message)
                        files = discord.File("{}".format(filename), filename="/home/natas/bot/{}".format(filename))
                        await member.guild.get_channel(registro).send(file=files, content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(envio de imagem)_ no canal {.mention} \n\ntrigger: {} \n\nMensagem enviada:\n\n'.format(currenttime(), ademir, message.author, message.channel, i))
                        tempmember = message.author
                        await message.channel.purge(limit=15, check=is_troller)
                        await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)

                    if member.top_role != cargocaveira:
                        await member.guild.get_channel(registro).send(content='[{}] \n\nusuário {.mention} cometeu infração _envio de imagem não verificada_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                    await member.add_roles(cargocaveira)

            for i in imageextensions:                       #apaga mensagens contendo link de imagens
                if message.content.lower().find(i) != -1:
                    if member.top_role == cargocaveira:
                        await member.add_roles(mutedrole)
                        await avisomuteDM(message)
                        log(f'Usuário {tempmember} foi mutado por envio de imagem. (link)')
                        await member.guild.get_channel(registro).send(content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(envio de link de imagem)_ no canal {.channel} \n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                        #global tempmember
                        tempmember = message.author
                        await message.channel.purge(limit=15, check=is_troller)

                    if member.top_role != cargocaveira:
                        await member.guild.get_channel(registro).send(content='[{}] \n\nusuário {.mention} cometeu infração _mensagem longa_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                    await member.add_roles(cargocaveira)
                    await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)

        #remover cargo 2 pontos se o usuário tiver dentro do server por mais de 24h
        if (datetime.datetime.now() - member.joined_at) > datetime.timedelta(hours=24):
            if member.top_role == cargo2pontos:
                await member.remove_roles(cargo2pontos)
                await member.guild.get_channel(registro).send(content='[{}] Usuário {.mention} removido do watchdog por tempo de servidor > 24h'.format(currenttime(), message.author))
    
    for i in redirects:                             #apaga mensagens contendo redirecionadores
        if message.content.lower().find(i) != -1:
            if extractor.has_urls(message.content):
                await member.add_roles(mutedrole)
                log(f'Usuário {tempmember} foi mutado por envio link de redirecionador ({i}), \"{message.content}\"')
                await avisomuteDM(message)
                await member.guild.get_channel(registro).send(content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(link com redirect)_ no canal {.mention}\n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                tempmember = message.author
                await message.delete()
                await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)
    if extractor.has_urls(message.content):
        for i in pornsites:                             #apaga mensagens contendo links apra sites pornográficos
            if str(extractor.find_urls(message.content)).lower().find(i) != -1:
                if message.content.startswith('https://tenor.com'): return
                await member.add_roles(mutedrole)
                log(f'Usuário {tempmember} foi mutado por envio de site pornográfico.')
                await member.guild.get_channel(registro).send(content='[{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(link de site dentro do blacklist)_ no canal {.mention}\n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                await avisomuteDM(message)
                await message.delete()
                await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)

    #----fim seção mutar/avisar/registrar
    if extractor.has_urls(str(message.attachments)):
        for x in imageextensions:
            if x in message.attachments[0].filename.lower():
                for i in message.attachments:
                    time = currenttime()
                    os.system('wget -q {} -O \"/home/natas/bot/attachments/{}\"'.format(i.url, f'{time} {message.author.id} {message.channel.name} {message.author.name} filename:{i.filename}{x}')) #baixa a imagem, precisa ter o wget dentro do path sistema
                    print(f'file {i.filename} from {message.author.name} sent on {message.channel.name} downloaded.')
                    attachmentsApagados.update({message.id:attachment(time, message.author.id, message.channel.name, message.author.name, i.filename, x, f'{time} {message.author.id} {message.channel.name} {message.author.name} filename:{i.filename}{x}')})
            



    if str(message.channel) == 'sugestões':                 #verifica se essa msg foi enviada no sugestões, etc
        await message.add_reaction('\U0001F44D')        #thumbsup
        await message.add_reaction('\U0001F44E')        #thumbsdown
        await guild.get_channel(registro).send(content='[{}] Nova sugestão de {.mention}'.format(currenttime(), message.author))

    if message.content.startswith('$help') or message.content.startswith('$ajuda'):             #comando de ajuda #procura o canal com id regras, pra mencionar nas DM's depois

        embed = discord.Embed( #aqui a gente escreve o embed (texto com formatação top q vai ser enviada nas DM's de quem entra)
            title = '⇝ **Ajuda: The Project!** ⇜',
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

        await message.add_reaction(random.choice([':tpjames:626957423634022421',':tpjames:659586056466857984']))

        if message.content.find('madame') != -1 or message.content.find('senhorita') != -1 or message.content.find('donzela') != -1 or message.content.find('dama') != -1:
            await message.add_reaction('🇬');await message.add_reaction('🇦');await message.add_reaction('🇩');await message.add_reaction('🇴')

    if str(message.channel) == 'aprovações':            #reações no aprovações
        await message.add_reaction('\U0001F942');await message.add_reaction('\U0001F389')#champanhe e :tada:
        #await message.add_reaction('\U0001F3C6')       #troféu

    if client.user.mentioned_in(message=message) and message.mention_everyone is False:
        if 'ajuda' in message.content or 'help' in message.content or message.content == '<@!668640272573399041>':
            await message.channel.send(content=f'Precisa de ajuda {message.author.mention}?\nAqui estão meus comandos!\n\n')
            embed = discord.Embed( #aqui a gente escreve o embed (texto com formatação top q vai ser enviada nas DM's de quem entra)
                title = '⇝ **Ajuda: The Project!** ⇜',
                colour = discord.Color.blue()
            )
            for x in setorajuda:
                embed.add_field(name='**'+x+'**', value=setorajuda[x], inline=False)
            embed.set_footer(text='Criado por Natas#9686 e Will#1687')
            await message.channel.send(embed=embed)
        else:
            await message.add_reaction('\U0001F440')

    if ' bot ' in message.content or ' bot,' in message.content or 'bot ' in message.content or 'bot' in message.content[-3:]:
        await message.add_reaction('\U0001F440')

    if spammerdebomdia and message.channel.name in ['bate-papo', 'shitpost']:
        if 'bomdia' in message.content.lower().replace(' ', '') and spammerdebomdialimiter(message.author):
            if message.mentions and client.user not in message.mentions: return
            if 18 >= datetime.datetime.now().hour >= 12:
                await message.channel.send(content='Não sei você mas aqui já é boa tarde {.mention}.'.format(message.author))
                return
            else:
                if 6 <= datetime.datetime.now().hour < 12:
                    await message.channel.send(content='Bom dia, {}.'.format(message.author.name[0].upper()+message.author.name[1:]))
                    return
                else:                
                    await message.channel.send(content='Acordou agora bela adormecida? Já é de noite {.mention}.'.format(message.author))
                    return

        if 'boatarde' in message.content.lower().replace(' ', '') and spammerdebomdialimiter(message.author):
            
            if message.mentions and client.user not in message.mentions: return
            if datetime.datetime.now().hour > 18:
                await message.channel.send(content='Não sei você mas aqui já é boa noite {.mention}.'.format(message.author))
                return
            else:
                if datetime.datetime.now().hour >= 12:
                    await message.channel.send(content='Boa tarde, {}.'.format(message.author.name[0].upper()+message.author.name[1:]))
                    return
                if datetime.datetime.now().hour < 12:
                    await message.channel.send(content='Boa tarde? Cê tá maluco meu, é de manhã ainda {.mention}'.format(message.author))
                    return
                
        if 'boanoite' in message.content.lower().replace(' ', '') and spammerdebomdialimiter(message.author):
            if message.mentions and client.user not in message.mentions: return

            if 18 <= datetime.datetime.now().hour <= 23 or 0 <= datetime.datetime.now().hour <= 6:
                await message.channel.send(content='Boa noite, {}.'.format(message.author.name[0].upper()+message.author.name[1:]))
                return
            else:
                kekw = await message.author.guild.fetch_emoji(emoji_id=633527255993417768)
                await message.channel.send(content='Tu tá fora né? O cara manda um boa noite essas horas {}'.format(str(kekw)))
                return

    if message.content.lower().startswith('ola bot') or message.content.lower().startswith('olá bot') and spammerdebomdialimiter(message.author) and message.channel.name == 'bate-papo':
        await message.channel.send(content=f'Olá, {message.author.mention}.')

    if message.content.startswith('$mostrarboasvindas'):
        embed = getboasvindasembed(message.author)
        await message.channel.send(embed=embed)
    
    if message.content.startswith('$mensagemDM') and message.mentions[0]:
        if 'Administrador' not in str(message.author.roles): await message.channel.send(f'{message.author.mention}, este comando só pode ser usado por administradores!'); return
        await message.mentions[0].send(message.content[len('<@258775759324184586>')+len('$mensagemDM')+2:])


    if False is True: #len(message.content) >= 7:                       #registrar mensagens para cargo ativo
        if daypass() == True:
            resetlista()
        try:
            global reloadativostime
            #global membrosativos
            #global membrosativostimes
            #global membrosativosvalores
            global tempvalue
            #print('membrosativos', membrosativos)
            if membrosativos.index(member.name)+1:
                #print('membrosativos.index(member.name):', membrosativos.index(member.name)) #read at index, +=1, pop, insert at index


                tempvalue = membrosativosvalores[membrosativos.index(member.name)]
                tempvalue += 1
                membrosativosvalores.pop(membrosativos.index(member.name))
                membrosativosvalores.insert(membrosativos.index(member.name), tempvalue)

                membrosativostimes.pop(membrosativos.index(member.name))
                membrosativostimes.insert(membrosativos.index(member.name), datetime.datetime.now())

                saveativos();savetimes();savevalores()

                print(f'[{currenttime()}] membro {member} nº {membrosativos.index(member.name)} total de mensagens: {tempvalue}')
                
        except ValueError:
            membrosativos.append(member.name)
            saveativos()
            print('adicionado {} na lista de ativos para computação de dados'.format(member))


        if membrosativosvalores[membrosativos.index(member.name)] >= spam:
            
            if datetime.datetime.now() - member.joined_at <= datetime.timedelta(minutes=15):
                await avisomuteDM(message)
                tempmember = member
                await message.channel.purge(limit=500, check=is_troller)
                await member.add_roles(mutedrole)
                await message.guild.get_channel(registro).send(content='[{}] Usuário {.mention} mutado por passar de 500 mensagens em 15 minutos dentro do servidor.'.format(currenttime(), member1))


        
        #global membrosativosvalores
        if membrosativosvalores[membrosativos.index(member.name)] > ativothreshold:
            if 'Muted' in str(member.roles):
                return
                
            if str(member.roles).find('Ativo') == -1:
                await member.add_roles(discordget(member.guild.roles, name='Ativo'))
                await member.guild.get_channel(registro).send(content='[{}] Usuário {.mention} adicionado cargo Ativo.'.format(currenttime(), message.author))
                '''
                if 'Muted' or 'Silenciado' in str(member.roles):        #se o cara tá mutado e falar ele n ganha o cargokkkkk
                    await remove_roles(discordget(member.guild.roles, name='Ativo'))
                    '''

    if False is True:
        for i in membrosativostimes:
            if i != 0:
                
                #print(datetime.datetime.now() - i)
                if datetime.datetime.now() - i > datetime.timedelta(days=1):
                    member1 = discordget(message.guild.members, name=membrosativos[membrosativostimes.index(i)])     #pega o membro referente, e não o atual
                    c = await client.fetch_channel(registro)
                    if member1 == None: await c.send(f"Não foi possível encontrar o user de nome {membrosativos[membrosativostimes.index(i)]}, talvez ele saiu do servidor?"); membrosativos.pop(membrosativostimes.index(i)); membrosativosvalores.pop(membrosativostimes.index(i)); membrosativostimes.pop(membrosativostimes.index(i)); return
                    
                    if str(member1.roles).find('Ativo') != -1:                          #se encontrar a tag ativo nele
                        await member1.remove_roles(discordget(member.guild.roles, name='Ativo')) #remove
                        await member1.guild.get_channel(registro).send(content='[{}] Usuário {.mention} removido do cargo Ativo por inatividade dentre 1 dia.'.format(currenttime(), member1))
                        membrosativos.pop(membrosativostimes.index(i))                        #remove o registro dele
                        membrosativosvalores.pop(membrosativostimes.index(i))                 #listas
                        membrosativostimes.pop(membrosativostimes.index(i))                   #nas 3
                    else:
                        c = await client.fetch_channel(registro)
                        await c.send(f'Usuário {membrosativos[membrosativostimes.index(i)]} removido da lista pois não mandou mensagens em 1 dia.')
                        membrosativos.pop(membrosativostimes.index(i)); membrosativosvalores.pop(membrosativostimes.index(i))
                        membrosativostimes.pop(membrosativostimes.index(i))
                        

    #RPG stuff
    if message.content.startswith('$dice '): # and message.author == jamesid:
        with message.channel.typing():
            if not 'd' in message.content[6:]: await message.channel.send(f'{message.author.mention}, por favor use no formato **X**d**Y**, onde X é o número de dados, e Y é o número de lados dos x dados.'); return
            if message.content[6:].count('d') > 1: await message.channel.send(f'{message.author.mention}, por favor use meu comando corretamente.'); return
            numeroDeDados, lados = message.content[6:].split('d')
            #if any(i in invalidCharacters for i in numeroDeDados.lower()) or any(i in invalidCharacters for i in lados.lower()): await message.channel.send(f'{message.author.mention}, use números por favor.'); return
            try:
                if int(numeroDeDados) < 1 or int(lados) < 1: await message.channel.send(f'{message.author.mention}, use números válidos por favor.'); return
            except:
                await message.channel.send(f'{message.author.mention}, use números por favor.'); return
            if len(numeroDeDados) > 3 or len(lados) > 3: await message.channel.send(f'{message.author.mention}, tu tá maluco? Oxe eu não vou calcular tanta coisa assim não'); return
            await message.channel.send(f"Jogando **{numeroDeDados}** dados de **{lados}** lados {message.author.mention}!")
            i=1;ladosList = []
            while i <= int(lados):
                ladosList.append(i)
                i+=1
            sum = 0;i=0
            while i < int(numeroDeDados):
                sum += random.choice(ladosList)
                i+=1
            await message.channel.send(f"Dados jogados! Soma dos dados jogados é **{sum}**!")

    if message.content.startswith('$resetlista') and message.author.id == natasid and False is True:
        resetlista()
        await message.channel.send(f'{message.author.mention}, lista resetada com sucesso!');return


    if message.content.lower().startswith("a benção") and spammerdebomdialimiter(message.author) or message.content.lower().startswith("bença") and spammerdebomdialimiter(message.author):
        await message.channel.send(f'{message.author.mention} Deus te abençoe.')

    if message.channel.id == 697863869707845682:

        embed = discord.Embed(

            title = 'Para ganhar a tag referente a região em que você vive, clique nas reações correspondentes abaixo:',
            description = '\n:herb:\t\t \t\t**Centro-Oeste**\n\n:bread: :cheese:\t**Sudeste**\n\n:mate:\t\t \t\t**Sul**\n\n:palm_tree:\t\t \t\t**Nordeste**\n\n:compass:\t\t \t\t**Norte**',
            color = discord.Color.purple()
        )

        msg = await message.channel.send(embed=embed)
        await msg.add_reaction('🌿')
        await msg.add_reaction('🍞')
        await msg.add_reaction('🧉')
        await msg.add_reaction('🌴')
        await msg.add_reaction('🧭')







@client.event                                           #quando o user entra, mostrar uma mensagem de boas vindas.
async def on_member_join(member):
    log(f'membro {member} entrou no servidor.')
    if member.bot: return
    if member.name == 'Natas\'': await member.add_roles(discordget(member.guild.roles, name='Bumper'))
    global newmembernumber
    newmembernumber += 1
    #BOAS VINDAS
    channel = member.guild.get_channel(regras)          #procura o canal com id regras, pra mencionar nas DM's depois
    embed = getboasvindasembed(member)
    try:
        await member.send(embed=embed)                      #envia o embed
        await member.guild.get_channel(registro).send(content='[{}] Dado boas-vindas ao {.mention}'.format(currenttime(), member))
    except:
        await member.guild.get_channel(registro).send(content='[{}] Não foi possível dar boas-vindas ao {.mention}.'.format(currenttime(), member))
    #--------fim boas vindas



    #começo do check de veracidade.
    tempodeexistencia = datetime.timedelta.total_seconds(datetime.datetime.now() - member.created_at)/86400 #resposta dada em dias
    #print(datetime.timedelta.total_seconds(tempodeexistencia)/86400)

    if tempodeexistencia < 1:
        channel = member.guild.get_channel(registro)
        cargo2pontos = discordget(member.guild.roles, name="..")
        await member.add_roles(cargo2pontos)
        await channel.send('[{}] Usuário {.mention} com menos de 1 dia de conta no Discord entrou no servidor. watchdog adicionado.'.format(currenttime(), member))
        #print('Novo usuário conta nova.')


    #entradasdeuserstempo.update( {str(member): member.joined_at} )
    
    entradasdeuserstempo.append(datetime.datetime.now())# - datetime.timedelta(hours=3))
    if len(entradasdeuserstempo) > 2: entradasdeuserstempo.pop(0)
    
    entradasmembros.append(member)
    if len(entradasmembros) > 2: entradasmembros.pop(0)
    #print('entradastempo:',entradasdeuserstempo, '\n\n', 'entradasmembro:',entradasmembros)

    try:

        if entradasdeuserstempo[1]:
            #print('entradasdeuserstempo is true')
            global lastuserjoin
            global lastlastuserjoin
            print('NMN:', newmembernumber, 'User:', member)

            lastuserjoin = entradasdeuserstempo[1]
            lastlastuserjoin = entradasdeuserstempo[0]
            #print('lastuserjoin:', lastuserjoin, 'datetime:', datetime.datetime.now())
            #print('entre users:', datetime.datetime.now() - lastuserjoin)
            if lastuserjoin - lastlastuserjoin <= datetime.timedelta(minutes=4.5):
                #print('assigning roles')
                cargo2pontos = discordget(member.guild.roles, name="..")
                await member.add_roles(cargo2pontos)
                try:
                    oldmember = entradasmembros[0]
                    await oldmember.add_roles(cargo2pontos)
                    await member.guild.get_channel(registro).send(content='[{}] Cargo watchdog adicionado ao {.mention} e {.mention}, entraram em menos de {} minutos'.format(currenttime(), member, oldmember, round(datetime.timedelta.total_seconds(lastuserjoin - lastlastuserjoin)/60, 2)))
                except:
                    print("Tem algo de errado na atribuição de cargo ao oldmember")
                
    except Exception as error:
        global natasmember
        if newmembernumber != 0:
            await natasmember.send(f"[{currenttime()}] {natasmember.mention}\nException at newmembernumber. \n`{traceback.format_exc()}`\nTime to reset.")
            




@client.event
async def on_member_leave(member):
    c = await client.fetch_channel(registro)
    await c.send(f'[{currenttime()}] {member.mention} saiu do servidor.')





@client.event                                           #add a role Clube do Livro/Grupode Estudos
async def on_raw_reaction_add(event):
    

    if event.member.bot:
        return


    member = event.member                               #aqui não precisa procurar dentro da guild pra pegar o objeto membro
    livro = discordget(member.guild.roles, name="Clube do Livro")
    estudos = discordget(member.guild.roles, name="Grupo de Estudos")

    if event.message_id == clube_id:                    #verifica se a msg é a certa
        if str(event.emoji) == '\U0001F4DA':            #isso aqui é pra somente se o emoji for os livros
            await discord.Member.add_roles(member, livro) #add role
            await member.guild.get_channel(registro).send(content='[{}] Adicionado ao {.mention} Clube do Livro'.format(currenttime(), member))
    if event.message_id == grupo_id:
        if str(event.emoji) == '\U0001F4DA':
            await discord.Member.add_roles(member, estudos)
            await member.guild.get_channel(registro).send(content='[{}] Adicionado ao {.mention} Grupo de Estudos'.format(currenttime(), member))


    #parte que faz o bgl de aprovação da sugestão de filme
    if event.message_id in listasugestãofilme and event.emoji.id == 547068425067954196:
        channel = discordget(event.member.guild.channels, id=event.channel_id)
        await channel.send('Sugestão aprovada!')

        msg = await aprovarsugestão(event.member, f'Sugestão de filme de <@{listasugestãofilme[event.message_id][1]}>:\n{listasugestãofilme[event.message_id][0]}')
        await msg.add_reaction('\U0001F44D')
        await msg.add_reaction('\U0001F44E')
    
    #regiões do país

    
    if event.channel_id == 697863869707845682:
        global roles
        global roles_emojis
        remove_roles = member.remove_roles
        memberroles = member.roles
        c = await client.fetch_channel(697863869707845682)
        guildroles = member.guild.roles
        msg = await c.fetch_message(event.message_id)

        if not spammerdebomdialimiter(member):
            
            for react in msg.reactions:
                await react.remove(member)
            """
            await remove_roles(discordget(guildroles, name='Nordeste'))
            await remove_roles(discordget(guildroles, name='Sul'))
            await remove_roles(discordget(guildroles, name='Sudeste'))
            await remove_roles(discordget(guildroles, name='Centro-Oeste'))
            await remove_roles(discordget(guildroles, name='Norte'))"""
            return
        #print(msg.reactions)

        await c.send('reacted')

        remove_reaction = msg.remove_reaction

        if any(i in str(memberroles) for i in roles):
            await c.send(f'found role')
            if 'Sul' in str(member.roles):
                await remove_roles(discordget(guildroles, name='Sul'))
                await remove_reaction(roles_emoji[2],member)
            if 'Nordeste' in str(member.roles):
                await remove_roles(discordget(guildroles, name='Nordeste'))
                await remove_reaction(roles_emoji[3],member)
            if 'Sudeste' in str(member.roles):
                await remove_roles(discordget(guildroles, name='Sudeste'))
                await remove_reaction(roles_emoji[1],member)
            if 'Centro-Oeste' in str(member.roles):
                await remove_roles(discordget(guildroles, name='Centro-Oeste'))
                await remove_reaction(roles_emoji[0],member)
            if 'Norte' in str(member.roles):
                await remove_roles(discordget(guildroles, name='Norte'))
                await remove_reaction(roles_emoji[4],member)


        for item in roles:
            if event.emoji.name == roles_emoji[roles.index(item)] and item not in str(memberroles):

                await event.member.add_roles(discordget(guildroles, name=item))
                await c.send(f'Adicionado 1 role {item}')
                return
                





@client.event
async def on_raw_message_delete(event):

    if event.cached_message.author.bot: return

    canal = await client.fetch_channel(event.channel_id)
    try:
        if event.cached_message.content == '': c = await client.fetch_channel(registro); await c.send(f'[{currenttime()}] uma mensagem de {event.cached_message.author.mention} foi apagada no canal {canal.mention}. Não havia texto, somente um attachment. Segue abaixo.')
        if event.cached_message.content != '': await event.cached_message.author.guild.get_channel(registro).send(content=f'[{currenttime()}] uma mensagem de {event.cached_message.author.mention} foi apagada no canal {canal.mention}. \n> {event.cached_message.content}')
    except:
        pass

    if event.message_id in attachmentsApagados:
        files = discord.File(f"/home/natas/bot/attachments/{attachmentsApagados[event.message_id].nomearquivo}")
        chn = await client.fetch_channel(registro)
        await chn.send(file=files)





client.run(secret.key)