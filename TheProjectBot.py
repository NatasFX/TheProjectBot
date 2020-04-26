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
import tracemalloc                                  #alguns tracebacks não funcionam sem isso
tracemalloc.start()                                 #^
import traceback                                    #nem lembro mais
import asyncio                                      #TimeOutError
import youtube_dl                                   #player de música
from nudity import Checker                          #pra fazer checks de nudez nas imagens de pessoas com cargo2pontos
import multiprocessing
import quantumrandom                               #real random generator
#-----------------


#logger de eventos do discord.py, é para debugging.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)




#especficar ID's
emoji = ':like:547068425067954196'                  #id do emoji customizado, foi pego usando \:like:
clube_id = 674680642583134209                       #id do texto para ser reagido no clube do livro
jamesid = 567835811123560478                        #id do james
grupo_id = 674679746919006240                       #id do canal de mensagem do grupo de estudos
regras = 542690955405426698                         #id do canal de regras
registro = 675819847128711182                       #id do canal registros
natasid = 283345376231292929                        #id do meu user para estreitar funções ao meu user. (debbugging)
willid = 258775759324184586                         #id do will
bate_papo_mirror = 701184727796940910               #dentadura
natasaltid = 536984029564764162                     #id Natas'     
#-------------- 

#todo list:
#james gado - done
#log - done
#games -talvez em outra vida
#ativos n precisar de 1 msgs só pra continuar ativos. -DEPRECATED
#persistence no cargo de .. - DONE
#não apagar mensagens contento ass que sejam do tenor - DONE
#persistence nos mutados - DONE
#organização dos comandos que estavam dentro do on_message - DONE
#não precisar pegar variáveis em todo on_message (fazer global) - DONE
#corrigir o rich presence que estava atualizando errado - DONE
#atualizar para dev e usar AllowedMentions - DONE
#pseudo-random menos random para o dice - DONE
#whitelist para counterar falsos positivos dos links contendo ass e tal 
#persistence no bom dia
#um único save para salvar todos os tipos de listas/dicionários
#USAR COGS



#iniciando variáveis úteis
entradasdeuserstempo = []                                                               #salva o tempo de entrada de users novos
entradasmembros = []                                                                    #salva os membros novo
newmembernumber = -1                                                                    #membro número
imageextensions = ['.png', '.jpg', '.webp', '.jpeg', '.mp4', '.3gp', 
    '.mov', '.webm', '.torrent', '.zip', '.rar']                                        #extensões para reconhecer imagens para mutar usuários com CPI
blacklist = ['pornhub', 'xvideos', 'xxx', 'xnxx', 'xhamster', 'porn',                   #sinalizar como porn
     'boobs', 'ass', 'pussy', 'dick', 'asshole', 'sex', 'discord.gg']
redirects = ['bit.ly', 'goo.gl', 'adf.ly', 'tinyurl', 'ow.ly']                          #sinalizar redirects
whitelist = ['tenor.com', '']
mensagemflood = 300                                                                     #número de caracteres antes de ser considerado mensagem como spam
membrosativos = []                                                                      #inicia lista de ativos, aqui vão os objetos membros
membrosativosvalores = []                                                               #inicia a lista onde ficam o nº de mensagens, correspondente ao index do membrosativos
membrosativostimes = []                                                                 #inicia a lista onde ficam a hora da última mensagem do index correspondente ao membro
ativothreshold = 100                                                                    #nº de mensagens pra se considerar ativo
tempmember = ''                                                                         #inicia a lista para guardar o membro que se faz checagem ao deletar mensagens
started = datetime.datetime.now()                                                       #pega a hora em que o bot foi iniciado, para cálculo de $uptime depois
initialtime = round(time.time()/86400, 0)                                               #inicia a variável de checks pra reset da lista membrosativosvalores
lastplayingchange = 0                                                                   #inica a variável pra
spam = 120                                                                              #120 é o número para se checar se em 15 minutos de entrada de servidor forem enviadas 120 mensagens, dar mute.
bomdiacooldown = {}                                                                     #aqui ficam temporariamente usuários impedidos de receberem a resposta do bot referente ao bom dia
logging.basicConfig(filename='botlog.log', filemode='w', format='%(levelname)s - %(message)s')
eventofilme = False                                                                     #especifica se tem evento de filme ou não.
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
    '**$dice**':'Joga dados.',
    '**$github**':'Link para o repositório GitHub do bot.',
    '**ping**':'ping.'
    }
natasmember = ''                                                                        #aqui abaixo iniciam variáveis que são globais. é pra economizar ficar pegando coisas a cada evento.
lastuserjoin = ''
lastlastuserjoin = ''
attachmentsApagados = {}
discordget = discord.utils.get                                                          #usar . pra pegar atributos muitas vezes é mais lento.
roles = ['Centro-Oeste','Sudeste', 'Sul','Nordeste','Norte']
roles_emoji = ['🌿','🍞','🧉','🌴','🧭']
voicechannel = ''
cargospegos = False
guild = ''
member = ''
ademir = ''
mutedrole = ''
cargo2pontos = ''
cargocaveira = ''
reg_tp = ''
mirrorchannel = ''
lasttimedonecommand = ''
limiter1dia = {}
raidcontrol = False
mutadosroles = {}
saudações = {'bom dia': [], 'boa tarde':[], 'boa noite': []}
#-------------------------


class attachment:                                                                      #útilidade pública
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

def daypass():                              #esta função retorna True na primeira vez executada, e True somente uma vez a cada 24 horas.
    global initialtime                                                                  #pega a variável que definimos globalmente, pois local não se aplica a eventos (ex. on_message não requer chamar a variável como global, mas def sim)
    if round(time.time()/86400, 0) > initialtime:                                       #pega o tempo atual e compara com o initial time, que é na primeira vez 0, e depois o tempo antes de ser feito qualquer comparação.
        initialtime = round(time.time()/86400, 0)
        return True
    else:
        initialtime = round(time.time()/86400, 0)
        return False
    
def log(information):                       #função experimental ainda não implementada
    '''
    with open(str(lista)+'.txt', 'w') as f:                                             #objetivo é ao pressionar combinação de tecla, salvar a lista de ativos para depois ler ao pressionar a mesma ou combinação diferente.
        for item in lista:
            f.write("%s\n" % item)
    '''
    logging.info(information)

def aprovarsugestão(member, message):       #usado por staff para aprovar sugestões (dã)
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

def savemutadosroles():
    global mutadosroles
    with open('mutadosroles.txt', 'wb') as f:
        pickle.dump(mutadosroles, f)



def loadmutadosroles():
    global mutadosroles
    try:
        with open('mutadosroles.txt', 'rb') as f:
            mutadosroles = pickle.load(f)
    except:
        with open('mutadosroles.txt', 'wb') as f:
            pickle.dump(mutadosroles, f)

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
    """n=1000
    for i in membrosativosvalores:
        if i !=0:
            n -= 1"""
        
    
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
    #loadativos()
    #loadtimes()
    #loadvalores()
    loadmutadosroles()
    if eventofilme:
        loadeventofilmelista()
        loadlistasugestãofilme()

    """
        n=1000
    for i in membrosativosvalores:
        if i !=0:
            n -= 1"""

    #print('Listas iniciadas\nslots restantes:')#, membrosativos, membrosativostimes, membrosativosvalores)
    
def resetlista():                       #aqui resetamos a lista, a lista na qual pertence os valores, já que não é necessário reiniciar tudo.
    global membrosativosvalores
    membrosativosvalores = []
    n = 0
    while n < 1000:
        membrosativosvalores.append(0)
        n += 1
    print('Lista de ativos valores foi RESET!')


resetativo()                            #inicia as listas, desligado pois as listas de ativos foram desabilitadas, religado pois tem mais coisa do que lista de ativos dentro da func


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
        if datetime.datetime.now() - bomdiacooldown[member] >= datetime.timedelta(seconds=50):
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
        'ECDSA',
        'The Project',
        'money to hoes',
        'NATAS LINDOOOOOO',
        'The Project',
        'The Project',
        'nada, to estudando.',
        'The Project',
        'The Project',
        'Python',
        'The Project',
        'Sou Open-Source! Digite o comando $github.',
        'The Project',
        '$help',
        '$help',
        '$help',
        '$help',
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
        'b͓̽u͓̽g͓̽s͓̽ ͓̽p͓̽r͓̽o͓̽ ͓̽a͓̽l͓̽t͓̽o͓̽',
        'pra esquecer a morena 😔'
        ]
    
    a = random.randint(0, 9)
    global lastplayingchange
    if a > 4:
        try:
            if datetime.datetime.now() - lastplayingchange[0] > datetime.timedelta(minutes=2):
                lastplayingchange = [datetime.datetime.now(), random.choice(lista)]
                return lastplayingchange[1]
            else:
                return lastplayingchange[1]
        except:
            lastplayingchange = [datetime.datetime.now(), 'The Project']
    else:
        try:
            return lastplayingchange[1]
        except:
            return 'The Project'


async def waiting(seconds, ctx, text):
    await asyncio.sleep(seconds)
    await ctx.channel.send(text)





#client = discord.Client()                                  #nem sei pq isso existe, HOJE EU SEI
#client.allowed_mentions(everyone = False)
client = commands.Bot(command_prefix = '$', help_command=None, allowed_mentions=discord.AllowedMentions(everyone=False))                 #isso eu sei         





@client.event
async def on_ready():
    print(f'[{currenttime()}]Logged on as {client.user}!')






@client.event
async def on_raw_reaction_remove(event):
    #raw pq se não for raw, ele não escuta os reacts em mensagens que foram enviadas antes de iniciar o bot
    userid = event.user_id                                  #pega o id de quem reagiu
    guild = client.get_guild(id=event.guild_id)             #pega a guild
    member = guild.get_member(userid)                           #procura o objeto membro correspondente ao id dentro da guild
    memberroles = member.roles
    guildroles = member.guild.roles
    reg_tp = guild.get_channel(registro)
    if event.channel_id != 697863869707845682:
        livro = discordget(member.guild.roles, name="Clube do Livro") #encontra a role de clube do livro, mesma coisa em baixo
        estudos = discordget(member.guild.roles, name="Grupo de Estudos")
        id = event.message_id                                   #pega o id a mensagem reagida e verifica se a mensagem reagida é a mesma do clube do livro ou estudos
        if id == clube_id:
            if str(event.emoji) == '\U0001F4DA':
                await discord.Member.remove_roles(member, livro)#tira a role
                await reg_tp.send(content='❌ [{}] Removido de {.mention} Grupo de Estudos'.format(currenttime(), member)) #escreve no log
        
        if id == grupo_id:
            if str(event.emoji) == '\U0001F4DA':
                await discord.Member.remove_roles(member, estudos)
                await reg_tp.send(content='❌ [{}] Removido de {.mention} Grupo de Estudos'.format(currenttime(), member))
    

    #referente à tag região
    global roles
    global roles_emoji

    if event.channel_id == 697863869707845682:                  #se o canal é o certo
        for item in roles:                                      #itera sobre todas as roles
            if hash(event.emoji.name) == hash(roles_emoji[roles.index(item)]) and item in str(memberroles): #verifica se o emoji removido está dentro da lista
                await member.remove_roles(discordget(guildroles, name=item)) #se sim, ele retira a role
                reg = await client.fetch_channel(registro)      #e envia no reg_tp as infos
                await reg.send(f'Removido role \"{item}\" ao usuário {member.mention}')
                return






@client.event
async def on_message(message):                          #aqui ficam todos os comandos relacionados a mensagens enviadas


    if message.author.bot:                              #não escutar mensagens de bot. é um boolean.
        return


    global cargospegos, guild, member, ademir, mutedrole, cargo2pontos, cargocaveira, reg_tp, mirrorchannel, saudações
    if message.guild != None and cargospegos == False:

        guild = message.guild                           #pega a guild
        #define o message.author como member direto pra poupar espaço
        member = message.author
        #--- parte de detecção de raids.
        ademir = discordget(message.guild.roles, name="Administrador")
        mutedrole = discordget(message.guild.roles, name="Muted")
        cargo2pontos = discordget(message.guild.roles, name="..")
        cargocaveira = discordget(message.guild.roles, name="\U0001F480")
        reg_tp = guild.get_channel(registro)
        mirrorchannel = await client.fetch_channel(bate_papo_mirror)
        cargospegos = True
        
        #--- cargos pegos
    
    
    messagecontentlower = message.content.lower()       #performance reasons

    global limiter1dia

    if daypass():
        limiter1dia.clear()
        saudações = {'bom dia': [], 'boa tarde':[], 'boa noite': []}




    if message.author.id == natasid:                    #verifica se quem manda mensagem sou eu
        if 'acordar' in message.content:
            send_magic_packet(secret.mac)               #envia o magic packet para o compiuter
            await message.channel.send('Magic packet enviado.')
            return                                      #retorna

        if messagecontentlower.startswith('status'):
            await message.author.send('**Server Status:**\n\n'+str(getsysinfo()))
            i=0
            await message.author.send('\n\n**Listas:**\n\n**Ativos:**\n')
            while i<=len(membrosativos)/2000:           #usamos o while aqui pra enviar mensagens maiores do que 2000 caracteres de maneira segmentada
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

        if messagecontentlower.startswith('command'):
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

    if 'Direct Message' in str(message.channel):
        print(f'Received DM with {message.author} message=\'{message.content}\'')
        directmessages.update({
            message.author.id:f'[{currenttime()}], \"{message.content}\"'
        })
        savedirectmessages()
        await message.author.send('O bot não suporta envio de mensagens por mensagem direta, por favor, utilize o canal de #bots em um servidor para seu uso!')
        return


    if 'obrigado' in messagecontentlower and client.user.mentioned_in(message=message): #se agradecer o bot, responder com uma mensagem legal
        await message.channel.send(f'Disponha, {message.author.mention} {str(gettplove(message))}')

    if random.choice([0,1,2]) == 0:
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(coolactivity())) #seta o 'jogando'
    
    

    if str(message.channel) == 'apresentações-introdução':  #mensagens aqui serão reagidas com like
        await message.add_reaction(emoji); await message.add_reaction(gettplove(message))               #emoji personalido :like:
        await reg_tp.send(content='✅ [{}] Nova apresentação de {.mention}'.format(currenttime(), message.author))
        await message.author.add_roles(discordget(message.guild.roles, name='Apresentado'))
        return



    if 'dias sem bater uma' in messagecontentlower or 'não bati uma faz' in messagecontentlower or 'sem bater uma por' in messagecontentlower:  #ideia do james, blz?
        number = ''
        if message.mentions:
            for x in messagecontentlower.replace(messagecontentlower[messagecontentlower.index("<"):messagecontentlower.index(">")+1], ''):
                if x.isdigit() and 'dias' in messagecontentlower[message.content.find(x):]:
                    number = number+str(x)
        else:
            for x in messagecontentlower:
                if x.isdigit() and 'dias' in messagecontentlower[message.content.find(x):]:
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
        
    if 'dias sem estudar' in messagecontentlower or 'não estudei por' in messagecontentlower or 'não estudei faz' in messagecontentlower:
        number = ''
        for x in message.content:
            if x.isdigit() and 'dias' in messagecontentlower[message.content.find(x):]:
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
    if 'não estudei hoje' in messagecontentlower:
        await message.channel.send(content=f'{message.author.mention}, VOCÊ NÃO ESTUDOU HOJE?????????!!!!!11 \n||eu estarei te observando enquanto procrastina||')
        return
    
    global natasmember
    if not natasmember and not 'direct' in message.channel.name.lower():
        natasmember = discordget(message.guild.members, id=natasid)



    #JULGAMENTO
    member = message.author
    if str(member.roles).find('..') != -1:                      #detecta se o user tem o cargo ..
        if message.channel.name != 'apresentações-introdução':  #pra não escutar introduções
            if len(message.content) > mensagemflood:            #se a mensagem é spam, contendo mais de 300 caracteres
                if member.top_role == cargocaveira:
                #mute nele, e embaixo faz um log no registro
                    global tempmember
                    tempmember = message.author
                    try:
                        await avisomuteDM(message)
                    except:
                        print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                    await member.add_roles(mutedrole)
                    lista = []
                    for role in member.roles:
                        lista.append(role.name)
                    mutadosroles.update({member.id: lista})
                    savemutadosroles()
                    await message.channel.purge(limit=15, check=is_troller)
                    await reg_tp.send(content='❌ [{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(mensagem grande)_ no canal {.mention}\n\nMensagem enviada: {} \n\ntamanho: {}\\{} \n\n '.format(currenttime(), ademir, message.author, message.channel, message.content[:1750], len(message.content), mensagemflood))
                    await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=60)

                    
                
                if member.top_role != cargocaveira:
                    await reg_tp.send(content='❌ [{}] \n\nusuário {.mention} cometeu infração _mensagem longa_ no canal {.mention}.\nconteúdo:{}'.format(currenttime(), member, message.channel, message.content[0:1850]))
                    await message.delete()
                    await message.channel.send(f'{message.author.mention}, não envie mensagens grandes!', delete_after=15)
                    await member.add_roles(cargocaveira)
                    lista = []
                    for role in message.author.roles:
                        lista.append(role.name)
                    mutadosroles.update({message.author.id: lista})
                    savemutadosroles()


            for i in imageextensions:                       #apaga mensagens contendo imagens como attachments
                if message.channel.name == 'shitpost':
                    return
                if str(message.attachments).lower().find(i) != -1:  #procura se a mensagem tem imagem.
                    if member.top_role == cargocaveira:
                        files = []                              #define a lista
                        filename = message.attachments[0].filename #define o nome de arquivo
                        os.system('wget –-quiet {} -O {}'.format(message.attachments[0].url, filename)) #baixa a imagem, precisa ter o wget dentro do path sistema
                        await member.add_roles(mutedrole)       #dá mute, e salva no registro
                        lista = []
                        for role in message.author.roles:
                            lista.append(role.name)
                        mutadosroles.update({message.author.id: lista})
                        savemutadosroles()

                        try:
                            await avisomuteDM(message)
                        except:
                            print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                        files = discord.File("{}".format(filename), filename="/home/natas/bot/{}".format(filename))
                        await reg_tp.send(file=files, content='❌ [{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(envio de imagem)_ no canal {.mention} \n\ntrigger: {} \n\nMensagem enviada:\n\n'.format(currenttime(), ademir, message.author, message.channel, i))
                        tempmember = message.author
                        await message.channel.purge(limit=15, check=is_troller)
                        await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=60)

                    if member.top_role != cargocaveira:
                        await reg_tp.send(content='❌ [{}] \n\nusuário {.mention} cometeu infração _envio de imagem não verificada_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                        await message.channel.send(f'{message.author.mention}, não envie imagens!', delete_after=15)
                        await member.add_roles(cargocaveira)
                        lista = []
                        for role in message.author.roles:
                            lista.append(role.name)
                        mutadosroles.update({message.author.id: lista})
                        savemutadosroles()

            for i in imageextensions:                       #apaga mensagens contendo link de imagens
                if messagecontentlower.find(i) != -1:
                    if member.top_role == cargocaveira:
                        await member.add_roles(mutedrole)
                        lista = []
                        for role in message.author.roles:
                            lista.append(role.name)
                        mutadosroles.update({message.author.id: lista})
                        savemutadosroles()
                        try:
                            await avisomuteDM(message)
                        except:
                            print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                        log(f'Usuário {tempmember} foi mutado por envio de imagem. (link)')
                        await reg_tp.send(content='❌ [{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(envio de link de imagem)_ no canal {.channel} \n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                        #global tempmember
                        tempmember = message.author
                        await message.channel.purge(limit=15, check=is_troller)

                    if member.top_role != cargocaveira:
                        await reg_tp.send(content='❌ [{}] \n\nusuário {.mention} cometeu infração _mensagem longa_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                    await member.add_roles(cargocaveira)
                    lista = []
                    for role in message.author.roles:
                        lista.append(role.name)
                    mutadosroles.update({message.author.id: lista})
                    savemutadosroles()
                    await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)

        #remover cargo 2 pontos se o usuário tiver dentro do server por mais de 24h
        if (datetime.datetime.now() - member.joined_at) > datetime.timedelta(hours=24):
            if member.top_role == cargo2pontos:
                await member.remove_roles(cargo2pontos)
                await reg_tp.send(content='❌ [{}] Usuário {.mention} removido do watchdog por tempo de servidor > 24h'.format(currenttime(), message.author))
    
    for i in redirects:                             #apaga mensagens contendo redirecionadores
        if messagecontentlower.find(i) != -1:
            if extractor.has_urls(message.content):
                await member.add_roles(mutedrole)
                lista = []
                for role in message.author.roles:
                    lista.append(role.name)
                mutadosroles.update({message.author.id: lista})
                savemutadosroles()
                log(f'Usuário {tempmember} foi mutado por envio link de redirecionador ({i}), \"{message.content}\"')
                try:
                    await avisomuteDM(message)
                except:
                    print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                await reg_tp.send(content='❌ [{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(link com redirect)_ no canal {.mention}\n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                tempmember = message.author
                await message.delete()
                await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)
    if extractor.has_urls(message.content):
        for link in extractor.find_urls(message.content):
            if 'http://' not in link and 'https://' not in link:
                link = 'http://'+link
            site = requests.get(link)
            if site.text.lower().find('block this site') != -1 or 'http://www.rtalabel.org/index.php?content=parents' in site.text:
                    await member.add_roles(mutedrole)
                    lista = []
                    for role in message.author.roles:
                        lista.append(role.name)
                    mutadosroles.update({message.author.id: lista})
                    savemutadosroles()
                    await reg_tp.send(content='❌ [{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(link de site contendo string adulta)_ no canal {.mention}\n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, message.content))
                    try:
                        await avisomuteDM(message)
                    except:
                        print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                    await message.delete(); await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)

            for i in blacklist:                             #apaga mensagens contendo links apra sites pornográficos
                if link.lower().find(i) != -1:
                    for i in whitelist:
                        if i in link: return
                    await member.add_roles(mutedrole)
                    lista = []
                    for role in message.author.roles:
                        lista.append(role.name)
                    mutadosroles.update({message.author.id: lista})
                    savemutadosroles()
                    await reg_tp.send(content='❌ [{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(link de site dentro do blacklist)_ no canal {.mention}\n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                    try:
                        await avisomuteDM(message)
                    except:
                        print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                    await message.delete(); await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)

                   
    #----fim seção mutar/avisar/registrar
    if extractor.has_urls(str(message.attachments)):
        for x in imageextensions:
            if x in message.attachments[0].filename.lower():
                for i in message.attachments:
                    time = currenttime()
                    os.system('wget -q {} -O \"/home/natas/bot/attachments/{}\"'.format(i.url, f'{time} {message.author.id} {message.channel.name} {message.author.name} filename:{i.filename}{x}')) #baixa a imagem, precisa ter o wget dentro do path sistema
                    print(f'file {i.filename} from {message.author.name} sent on {message.channel.name} downloaded.')
                    attachmentsApagados.update({message.id:attachment(time, message.author.id, message.channel.name, message.author.name, i.filename, x, f'{time} {message.author.id} {message.channel.name} {message.author.name} filename:{i.filename}{x}')})


        """
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=Checker, args=(f"/home/natas/bot/attachments/{attachmentsApagados[message.id].nomearquivo}",))
        
        p.start()
        print(f'get aqui: \n ------------{q.get()}')
        if q.get():
            await message.channel.send(f'{message.author.mention}, não envie pornografia!', delete_after=60)
            await message.delete()"""
                


                        



    if str(message.channel) == 'sugestões':                 #verifica se essa msg foi enviada no sugestões, etc
        await message.add_reaction('\U0001F44D')        #thumbsup
        await message.add_reaction('\U0001F44E')        #thumbsdown
        await reg_tp.send(content='<:like:547068425067954196> [{}] Nova sugestão de {.mention}'.format(currenttime(), message.author))


    if message.content.startswith('$meutico'):          #sei la fds
        pass#await message.channel.send('**grande**')
        


    if message.channel == 'clube-do-livro' or message.channel == 'grupo-de-estudos':
        await message.add_reaction('\U0001F4DA')#books  #mensagens aqui serão reagidas com livros

    if message.author.id == jamesid:                    #verifica se quem mandou foi o james
        #await message.author.edit(nick='')
        #await message.add_reaction(random.choice([':tpjames:626957423634022421',':tpjames:659586056466857984']))

        if message.content.find('madame') != -1 or message.content.find('senhorita') != -1 or message.content.find('donzela') != -1 or message.content.find('dama') != -1:
            await message.add_reaction('🇬');await message.add_reaction('🇦');await message.add_reaction('🇩');await message.add_reaction('🇴')

    if str(message.channel) == 'aprovações':            #reações no aprovações
        await message.add_reaction('\U0001F942');await message.add_reaction('\U0001F389')#champanhe e :tada:
        #await message.add_reaction('\U0001F3C6')       #troféu

    if client.user.mentioned_in(message=message) and message.mention_everyone is False:
        if not spammerdebomdialimiter(message.author): return
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
        if not spammerdebomdialimiter(message.author): return
        await message.add_reaction('\U0001F440')

    if spammerdebomdia and message.channel.name == 'bate-papo':
        if messagecontentlower.startswith('bom dia') and message.author.id not in saudações['bom dia']:#bomdia' in messagecontentlower.replace(' ', '') and spammerdebomdialimiter(message.author):
            saudações['bom dia'].append(message.author.id)
            if message.mentions and client.user not in message.mentions or not spammerdebomdialimiter(message.author): return
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
            

        if messagecontentlower.startswith('boa tarde') and message.author.id not in saudações['boa tarde']:#'boatarde' in messagecontentlower.replace(' ', '') and spammerdebomdialimiter(message.author):
            saudações['boa tarde'].append(message.author.id)
            if message.mentions and client.user not in message.mentions or not spammerdebomdialimiter(message.author): return
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
            

        if messagecontentlower.startswith('boa noite') and message.author.id not in saudações['boa noite']:#'boanoite' in messagecontentlower.replace(' ', '') and spammerdebomdialimiter(message.author):
            saudações['boa noite'].append(message.author.id)
            if message.mentions and client.user not in message.mentions or not spammerdebomdialimiter(message.author): return

            if 17 <= datetime.datetime.now().hour <= 23 or 0 <= datetime.datetime.now().hour <= 6:
                await message.channel.send(content='Boa noite, {}.'.format(message.author.name[0].upper()+message.author.name[1:]))
                return
            else:
                kekw = await message.author.guild.fetch_emoji(emoji_id=633527255993417768)
                await message.channel.send(content='Tu tá fora né? O cara manda um boa noite essas horas {}'.format(str(kekw)))
                return


    if messagecontentlower.startswith('ola bot') or messagecontentlower.startswith('olá bot') or messagecontentlower.startswith('oi bot') or messagecontentlower.startswith('oi <') and message.mentions[0] == message.guild.me:
        if message.channel.name != 'bate-papo' or not spammerdebomdialimiter(message.author): return
        await message.channel.send(content=f'Olá, {message.author.mention}.')

    if messagecontentlower.startswith('alguém sabe ') or messagecontentlower.startswith('alguém conhece ') or messagecontentlower.startswith('alguém já viu ') or messagecontentlower.startswith('alguém já ') or messagecontentlower.startswith('alguém tentou '):
        if not '?' in message.content or message.channel.name != 'bate-papo': return
        await message.guild.me.edit(nick="Alguém")
        await message.channel.send(f'{message.author.mention} Não.\nespero ter ajudado')
        await message.guild.me.edit(nick="")

    if False is True: #len(message.content) >= 7:                       #registrar mensagens para cargo ativo
        if daypass() == True:
            resetlista()
        try:
            global reloadativostime
            #global membrosativos
            #global membrosativostimes
            #global membrosativosvalores
            ###global tempvalue
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
                try:
                    await avisomuteDM(message)
                except:
                    print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                tempmember = member
                await message.channel.purge(limit=500, check=is_troller)
                await member.add_roles(mutedrole)
                await reg_tp.send(content='❌ [{}] Usuário {.mention} mutado por passar de 500 mensagens em 15 minutos dentro do servidor.'.format(currenttime(), member))


        
        #global membrosativosvalores
        if membrosativosvalores[membrosativos.index(member.name)] > ativothreshold:
            if 'Muted' in str(member.roles):
                return
                
            if str(member.roles).find('Ativo') == -1:
                await member.add_roles(discordget(member.guild.roles, name='Ativo'))
                await reg_tp.send(content='[{}] Usuário {.mention} adicionado cargo Ativo.'.format(currenttime(), message.author))
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
                        await reg_tp.send(content='[{}] Usuário {.mention} removido do cargo Ativo por inatividade dentre 1 dia.'.format(currenttime(), member1))
                        membrosativos.pop(membrosativostimes.index(i))                        #remove o registro dele
                        membrosativosvalores.pop(membrosativostimes.index(i))                 #listas
                        membrosativostimes.pop(membrosativostimes.index(i))                   #nas 3
                    else:
                        c = await client.fetch_channel(registro)
                        await c.send(f'Usuário {membrosativos[membrosativostimes.index(i)]} removido da lista pois não mandou mensagens em 1 dia.')
                        membrosativos.pop(membrosativostimes.index(i)); membrosativosvalores.pop(membrosativostimes.index(i))
                        membrosativostimes.pop(membrosativostimes.index(i))
                        



    if message.content.startswith('$resetlista') and message.author.id == natasid and False is True:
        resetlista()
        await message.channel.send(f'{message.author.mention}, lista resetada com sucesso!');return


    if messagecontentlower.startswith("a benção") and spammerdebomdialimiter(message.author) or messagecontentlower.startswith("bença") and spammerdebomdialimiter(message.author):
        if message.channel.name != 'bate-papo': return
        await message.channel.send(f'{message.author.mention} Deus te abençoe.')

    """ #isso aqui foi criado pra o bot enviar a mensagem no canal.
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

    """

    if messagecontentlower.startswith('to indo dormir') or messagecontentlower.startswith('vou dormir') or messagecontentlower.startswith('vou indo dormir') or messagecontentlower.startswith('eu vou ir dormir') or messagecontentlower.startswith('eu vou indo dormir') or messagecontentlower.startswith('eu to indo dormir'):
        if message.channel.name != 'bate-papo': return
        if not spammerdebomdialimiter(message.author): return
        if random.choice([0,1]) == 0:
            await message.channel.send(f'{message.author.mention}, já vai tarde.')
        else:
            await message.channel.send(f'{message.author.mention}, durma bem.')


    #bate papo mirror
    
    if message.channel.name == 'bate-papo':
        await mirrorchannel.send(content=f'[Mensagem de {message.author.mention}]\n{message.content}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
        
        
        if message.attachments:
            files = discord.File(f"/home/natas/bot/attachments/{attachmentsApagados[message.id].nomearquivo}")
            await mirrorchannel.send(file=files)








    await client.process_commands(message)              #isso sempre fica no final do on_message.






@client.event                                           #quando o user entra, mostrar uma mensagem de boas vindas.
async def on_member_join(member):
    global reg_tp, mutadosroles

    if member.id in mutadosroles:
        print(f'mutadosroles: {mutadosroles}')
            #for roles in mutadosroles[member.id]:
        i=1
        while i < len(mutadosroles[member.id]):
            print(f'trying to add {str(mutadosroles[member.id][i])}')
            await member.add_roles(discordget(member.guild.roles, name=mutadosroles[member.id][i]))
            i+=1
        await reg_tp.send(f'\n<:tpthink:522461647588294679> [{currenttime()}] usuário {member.mention} tinha {i-1} roles anteriores ao sair do servidor. Adicionadas de volta.\n\x0b')

    if member.bot: return
    if member.id == natasaltid: await member.add_roles(discordget(member.guild.roles, name='Bumper')) #pra facilitar minha vida
    global newmembernumber
    newmembernumber += 1
    #BOAS VINDAS
    channel = member.guild.get_channel(regras)          #procura o canal com id regras, pra mencionar nas DM's depois
    embed = getboasvindasembed(member)
    #reg_tp = member.guild.get_channel(registro)
    try:
        await member.send(embed=embed)                      #envia o embed
        await reg_tp.send(content='☺️ [{}] Dado boas-vindas ao {.mention}'.format(currenttime(), member))
    except:
        await reg_tp.send(content='😦 [{}] Não foi possível dar boas-vindas ao {.mention}.'.format(currenttime(), member))
    #--------fim boas vindas



    #começo do check de veracidade.
    tempodeexistencia = datetime.timedelta.total_seconds(datetime.datetime.now() - member.created_at)/86400 #resposta dada em dias
    #print(datetime.timedelta.total_seconds(tempodeexistencia)/86400)

    if tempodeexistencia < 1:
        global cargo2pontos
        await member.add_roles(cargo2pontos)
        lista = []
        for role in member.roles:
            lista.append(role.name)
        mutadosroles.update({member.id: lista})
        savemutadosroles()
        await reg_tp.send('❗ [{}] Usuário {.mention} com menos de 1 dia de conta no Discord entrou no servidor. watchdog adicionado.'.format(currenttime(), member))


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
            print('NMN:', newmembernumber+1, 'User:', member)

            lastuserjoin = entradasdeuserstempo[1]
            lastlastuserjoin = entradasdeuserstempo[0]
            #print('lastuserjoin:', lastuserjoin, 'datetime:', datetime.datetime.now())
            #print('entre users:', datetime.datetime.now() - lastuserjoin)
            if lastuserjoin - lastlastuserjoin <= datetime.timedelta(minutes=4.5):
                #print('assigning roles')
                cargo2pontos = discordget(member.guild.roles, name="..")
                await member.add_roles(cargo2pontos)
                try:
                    for role in member.roles:
                        mutadosroles.update({member.id, []})
                        mutadosroles[member.id].append(role.name)
                    savemutadosroles()
                except:
                    pass
                try:
                    oldmember = entradasmembros[0]
                    await oldmember.add_roles(cargo2pontos)
                    

                    
                    lista = []
                    for role in oldmember.roles:
                        lista.append(role.name)
                    print(lista)
                    mutadosroles.update({oldmember.id: lista})
                    savemutadosroles()

                    await reg_tp.send(content='❗ [{}] Cargo watchdog adicionado ao {.mention} e {.mention}, entraram em menos de {} minutos'.format(currenttime(), member, oldmember, round(datetime.timedelta.total_seconds(lastuserjoin - lastlastuserjoin)/60, 2)))
                    
                    global raidcontrol

                    if not raidcontrol:
                        raidcontrol = {}
                        raidcontrol.update({datetime.datetime.now():[oldmember, member]})
                        #print(raidcontrol)
                    else:
                        time=next(iter(raidcontrol.keys()))
                        if datetime.datetime.now() - time > datetime.timedelta(minutes=1.25):
                            raidcontrol = False
                            return

                        
                        global cargocaveira
                        for x in raidcontrol.values():
                            for raideiros in x+[member]:
                                if '💀' not in str(raideiros.roles):
                                    #print(raideiros.roles)
                                    await raideiros.add_roles(cargocaveira)
                                    lista = []
                                    for role in oldmember.roles:
                                        lista.append(role.name)
                                    mutadosroles.update({oldmember.id: lista})
                                    savemutadosroles()
                                    await reg_tp.send(f'Adicionado cargocaveira (intolerância) ao user {member.mention} pois entraram muitos ao mesmo tempo.')
                            
                    #print(raidcontrol)



                except Exception as e:
                    print(f"Tem algo de errado na atribuição de cargo ao oldmember\n{traceback.format_exc()}")
                
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
    reg_tp = member.guild.get_channel(registro)

    if event.message_id == clube_id:                    #verifica se a msg é a certa
        if str(event.emoji) == '\U0001F4DA':            #isso aqui é pra somente se o emoji for os livros
            await discord.Member.add_roles(member, livro) #add role
            await reg_tp.send(content='✅ [{}] Adicionado ao {.mention} Clube do Livro'.format(currenttime(), member))
    if event.message_id == grupo_id:
        if str(event.emoji) == '\U0001F4DA':
            await discord.Member.add_roles(member, estudos)
            await reg_tp.send(content='✅ [{}] Adicionado ao {.mention} Grupo de Estudos'.format(currenttime(), member))


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
        global roles_emoji
        remove_roles = member.remove_roles
        memberroles = member.roles
        c = await client.fetch_channel(697863869707845682)
        guildroles = member.guild.roles
        msg = await c.fetch_message(event.message_id)

        if not spammerdebomdialimiter(member):
            await event.member.send(f"{event.member.mention}\ncalma lá meu parceiro, vá mais com calma nas reações aí! Espere 1 minuto antes de tentar novamente.")
            for react in msg.reactions:
                await react.remove(member)
            return
        #print(msg.reactions)
        remove_reaction = msg.remove_reaction

        if any(i in str(memberroles) for i in roles):
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
                reg = await client.fetch_channel(registro)
                await reg.send(f'Adicionado role \"{item}\" ao usuário {member.mention}')
                return
                





@client.event
async def on_raw_message_delete(event):

    try:
        if event.cached_message.author.bot: return
    except:
        print(f'mensagem apagada porém não estava no cache.')

    canal = await client.fetch_channel(event.channel_id)
    reg_tp = await client.fetch_channel(registro)

    try:
        if event.cached_message.content == '': await reg_tp.send(f'🛑 [{currenttime()}] uma mensagem de {event.cached_message.author.mention} foi apagada no canal {canal.mention}. Não havia texto, somente um attachment. Segue abaixo.', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
        if event.cached_message.content != '': await reg_tp.send(content=f'🛑 [{currenttime()}] uma mensagem de {event.cached_message.author.mention} foi apagada no canal {canal.mention}. \n> {event.cached_message.content}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
    except:
        pass

    if event.message_id in attachmentsApagados:
        files = discord.File(f"/home/natas/bot/attachments/{attachmentsApagados[event.message_id].nomearquivo}")
        chn = await client.fetch_channel(registro)
        await chn.send(file=files)






@client.event
async def on_message_edit(b, a):

    if a.content == b.content: return

    try:
        await reg_tp.send(content=f'✏️ [{currenttime()}] uma mensagem de {a.author.mention} foi editada no canal {a.channel.mention}. link: http://discordapp.com/channels/{a.guild.id}/{a.channel.id}/{a.id} \nantes\n> {b.content}\ndepois\n> {a.content}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
    except Exception as e:
        print(f"some error. on_message_edit {e}")





@client.command()
async def join(ctx):
    if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    with ctx.message.channel.typing():
        if ctx.channel.name != 'bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, use este comando no chat de bots!')
        
        global voicechannel
        channel = ctx.message.author.voice.channel
        voicechannel = await channel.connect(reconnect=True)
        await ctx.send(f'Conectado ao canal {voicechannel.name}!')


@client.command()
async def leave(ctx):
    if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    with ctx.message.channel.typing():
        global voicechannel
        await voicechannel.disconnect(force=True)
        await ctx.send(f'{ctx.message.author.mention}, desconectado do canal {voicechannel.name}!')


@client.command()
async def play(ctx, url: str):
    pass
    '''
    global voicechannel
    with ctx.message.channel.typing():
        if os.path.isfile("Song.mp3"):
            os.remove("Song.mp3")
            print("removed file")
            return
        
        await ctx.send(f"going do download the music file")

        voice = discordget(client.voice_clients, guild=ctx.guild)

        YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
        }

        with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
            print("yeah we've got there")
            ydl.download([url])


        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f'renamed file: {file}')
                os.rename(file, "Song.mp3")

        
        voicechannel.play(discord.FFmpegPCMAudio("Song.mp3"), after=None)

        voicechannel.source = discord.PCMVolumeTransformer(voice.source)
        voicechannel.source.volume = 0.07


        await ctx.send(f'playing {name}')
        print('playing')
        '''


@client.command()
async def digitando(ctx, second: int):
    if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    if not "Administrador" in str(ctx.message.author.roles): return
    with ctx.channel.typing():
        if second > 99: return
        await waiting(second, ctx, ctx.message.content[12+len(str(second)):])


@client.command()
async def grupodeestudos(ctx):
    
    global limiter1dia

    author = ctx.message.author
    channel = ctx.message.channel

    if author.id in limiter1dia:
        await ctx.message.channel.send(f'{author.mention}, aguarde para usar este comando novamente!'); return

    limiter1dia.update({author.id: datetime.datetime.now()})

    if '..' in str(author.roles) or datetime.datetime.now() - author.joined_at < datetime.timedelta(days=7) or 'Grupo de Estudos' not in str(author.roles): 
        await ctx.channel.send(f'{ctx.message.author.mention}, você não tem permissão para usar este comando!')
        return
    else:
        await ctx.message.channel.send(f'{discordget(ctx.message.guild.roles, name="Grupo de Estudos").mention}, {author.mention} mencionou vocês para estudar!'); 


@client.command()
async def dice(ctx):
    
    message = ctx.message
    channelsend = message.channel.send
    author = message.author

    #RPG stuff
    if True:

        global lasttimedonecommand

        with message.channel.typing():
            if not 'd' in message.content[6:]: await channelsend(f'{author.mention}, por favor use no formato **X**d**Y**, onde X é o número de dados, e Y é o número de lados de cada dado.'); return
            if message.content[6:].count('d') > 1: await channelsend(f'{author.mention}, por favor use meu comando corretamente.'); return
            numeroDeDados, lados = message.content[6:].split('d')
            #if any(i in invalidCharacters for i in numeroDeDados.lower()) or any(i in invalidCharacters for i in lados.lower()): await channelsend(f'{message.author.mention}, use números por favor.'); return
            try:
                if int(numeroDeDados) < 1 or int(lados) < 1: await channelsend(f'{author.mention}, use números válidos por favor.'); return
            except:
                await channelsend(f'{author.mention}, use números por favor.'); return
            tip = '\nDica: só é suportado até 5 dados jogados.' if int(numeroDeDados) >= 6 else ''
            if int(numeroDeDados) >= 6 or len(lados) > 4: await channelsend(f'{author.mention}, use números menores. {tip}'); return
            
            #after verified its valid input:

            try:
                if datetime.datetime.now() - lasttimedonecommand < datetime.timedelta(seconds=20):
                    await channelsend(f"Aguarde antes de emitir um novo comando Dice.")
                    return
                else:
                    lasttimedonecommand = datetime.datetime.now()
            except:
                lasttimedonecommand = datetime.datetime.now()

            #do the math:
            i=1#;ladosList = []
            """
            while i <= int(lados): #never do this. never.
                ladosList.append(i)
                i+=1
            """; sum = 0
            
            i=1
            with message.channel.typing():
                await channelsend(f"Jogando **{numeroDeDados}** dados de **{lados}** lados {author.mention}!")
                while i <= int(numeroDeDados):
                    result = round(quantumrandom.randint(1, int(lados)))
                    await channelsend(f'Dado {i} jogado, valor: **{result}**!', delete_after=10)
                    sum += result
                    i+=1
            await channelsend(f"{i} dados foram jogados! Soma resultou em **{sum}**!")


@client.command()
async def uptime(ctx):
    if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    await ctx.message.channel.send(f'`Bot uptime is {datetime.datetime.now() - started}`')


@client.command()
async def ping(ctx):
    if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    await ctx.message.channel.send(f'Ping: {round(client.latency*1000)}ms')


@client.command(aliases=['ajuda'])
async def help(ctx):
    global setorajuda
    if True:                                        #comando de ajuda #procura o canal com id regras, pra mencionar nas DM's depois

        embed = discord.Embed(                      #aqui a gente escreve o embed (texto com formatação top q vai ser enviada nas DM's de quem entra)
            title = '⇝ **Ajuda: The Project!** ⇜',
            colour = discord.Color.blue()
        )

        for x in setorajuda:
            embed.add_field(name='**'+x+'**', value=setorajuda[x], inline=False)
        embed.set_footer(text='Criado por Natas#9686 e Will#1687')
        await ctx.message.channel.send(embed=embed)


@client.command()
async def mostrarboasvindas(ctx):
    embed = getboasvindasembed(ctx.message.author)
    await ctx.message.channel.send(embed=embed)
    

@client.command()
async def mensagemDM(ctx):
    if 'Administrador' not in str(ctx.message.author.roles): await ctx.message.channel.send(f'{ctx.message.author.mention}, este comando só pode ser usado por administradores!'); return
    if not ctx.message.mentions: await ctx.message.channel.send(f'{ctx.message.author.mention}, você precisa mencionar alguém para enviar a mensagem!'); return
    await ctx.message.mentions[0].send(ctx.message.content[34:])


@client.command()
async def github(ctx):
    await ctx.message.channel.send(f"{ctx.message.author.mention}, aqui está o repositório:\n https://github.com/NatasFX/TheProjectBot ")


@client.command()
async def sugerirfilme(ctx):

    message = ctx.message
    author = message.author
    channelsend = message.channel.send


    if message.channel.name == 'bots': #comando $sugerirfilme é ativo quando eventofilme for True
        global eventofilmelista
        global listasugestãofilme
        if eventofilme:                                                     #se o evento de filme esstiver ativo
            if eventofilmelista.get(message.author.id) is None or len(eventofilmelista.get(message.author.id)) <= 2:
                if not extractor.has_urls(message.content):                 #se conter links ele não vai escutar
                    if message.author.id in eventofilmelista.keys():#verifica se o cara já fez alguma sugestão
                        eventofilmelista.get(message.author.id).append(message.content[14:])
                    else:
                        eventofilmelista.update({
                            message.author.id:[message.content[14:]]
                        })
                    

                    staff = discordget(message.guild.channels, name='staff')#pega o canal para envio da solicitação de aprovação
                    
                    msg = await staff.send(content=f'Nova sugestão de filme de {author.mention}: \n\"{message.content[14:]}\"\nDeseja aprovar essa sugestão?')
                    await msg.add_reaction(':like:547068425067954196')
                    await msg.add_reaction('\U0001F44E')                    #envia a solicitação junto das reações para aprovação ou n
                    listasugestãofilme.update({                             #atualiza a lista com id da mensagem de solicitação e o filme escolhido
                        msg.id:[message.content[14:],author.id]
                    })
                    savelistasugestãofilme()                                #salva a lista no txt
                    await channelsend(f'{author.mention}, sua sugestão foi enviada, muito obrigado! {str(gettplove(message))}')
                    await channelsend(f'Você tem mais {3-len(eventofilmelista[message.author.id])} sugestões de filme')
                    saveeventofilmelista()                                  #mostra quantas sugestões de filme ainda podem ser feitas
                    return                                                  #sempre bom ter
                else:
                    await channelsend(f'{author.mention}, ops! aconteceu um erro.')
                    return
            else:
                await channelsend(content=f'{author.mention}, você não pode fazer mais que 3 sugestões!')
        else:
            await channelsend(f'{author.mention}, o evento de filme não está ativo no momento ou você já fez uma sugestão.')
            return
    else:
        await channelsend(f'{author.mention}, use o canal de #bots por favor!', delete_after=5)


@client.command(aliases=['versugestões'])
async def versugestão(ctx):

    message = ctx.message
    author = message.author
    channelsend = message.channel.send

    if message.channel.name == 'bots' and eventofilme: #'$versugestão' in message.content[0:13] and message.channel.name in ['bots'] or '$versugestões' in message.content[0:14] and message.channel.name in ['bots']:
        if not message.mentions:                            #se o user não mencionou ninguém, mostrar as sugestões dele
            if author.id in eventofilmelista:               #verifica se ele já fez sugestão
                try:                                        #aqui abaixo envia as sugestões referente ao user que pede
                    await channelsend(content=f'{author.mention}, segue sua(s) sugestão(ões) de filme(s):\n{eventofilmelista[author.id][0]}')
                    await channelsend(content=f'{eventofilmelista[author.id][1]}')
                    await channelsend(content=f'{eventofilmelista[author.id][2]}')
                except:
                    await message.channel.send(f'Você ainda pode fazer mais {3-len(eventofilmelista[author.id])} sugestão(ões).')
            if message.author.id not in eventofilmelista:
                await message.channel.send(f'Você não fez uma sugestão ainda {author.mention}, faça uma usando o comando $sugerirfilme')
                return
        
        if message.mentions:                                #se ele mencionou alguém, mostrar sugestões de quem foi mencionado
            try:
                if message.mentions[0].id in eventofilmelista:
                    try:                                    #aqui abaixo envia as sugestões
                        await channelsend(content=f'{message.author.mention}, essas são as sugestões do {message.mentions[0].mention}:')
                        await channelsend(content=f'{eventofilmelista[message.mentions[0].id][0]}')
                        await channelsend(content=f'{eventofilmelista[message.mentions[0].id][1]}')
                        await channelsend(content=f'{eventofilmelista[message.mentions[0].id][2]}')
                    except:
                        pass
                else:
                    await channelsend(f'{author.mention}, usuário {message.metions[0].mention} não sugeriu filme.')

            except:
                return
    else:
        await channelsend(f'{author.mention}, use este comando no chat de bots!', delte_after=10)


@client.command(aliases=['apagarsugestões'])
async def apagarsugestão(ctx):

    message = ctx.message
    author = message.author
    channelsend = message.channel.send

    if message.channel.name == 'bots' and eventofilme:  #comando para apagar as sugestões previamente feitas para realizar novas.
        msg = await channelsend(f'{author.mention}, você deseja apagar suas sugestões de filme?', delete_after=60)
        await msg.add_reaction('\U0001F44D')
        await msg.add_reaction('\U0001F44E')
        
        def check(reaction, user):
            if str(reaction.emoji) != '👍':
                return
            return user == author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            pass#await channel.send('Você demorou muito para responder, operação cancelada!', delete_after=5)
        else:
            del eventofilmelista[author.id]
            await channelsend('Sugestões de filmes apagados com sucesso!')


client.run(secret.key)