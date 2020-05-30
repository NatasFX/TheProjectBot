#Bot do Servidor The Project
#Autoria: Natas#9686

#importar módulos --------------------------------------
import asyncio                                          # TimeOutError
import datetime                                         # datetime, melhor módulo pra manejamento de tempo
import logging                                          # meio que inútil
import os                                               # pra usar com os.system ou os.popen
import pickle                                           # fazer os salvamentos das listas
import random                                           # random é pra fazer random.
import string                                           # importar strings padronizadas
import sys
import threading                                        # threading que por enquanto n estou usando
import time                                             # time né
import traceback                                        # nem lembro mais
import tracemalloc                                      # alguns tracebacks não funcionam sem isso
import discord                                          # Importando API do discord
import pyscreenshot as ImageGrab                        # imagegrab pra tirar screenshots
#from nudity import Checker                             #pra fazer checks de nudez nas imagens de pessoas com cargo2pontos
#import multiprocessing                                 #algum dia isso aqui vai funcionar
import quantumrandom                                    # real random generator
import requests                                         # requests pra baixar as imagens
import youtube_dl                                       # player de música
from discord.ext import commands                        # Facilitar pra criar comandos
from gtts import gTTS as gtts                           #google Text to Speech
from timeout_decorator import timeout                   #timeout decorator pra funções n demorarem
from urlextract import URLExtract                       # extrator de URL's
from wakeonlan import send_magic_packet                 # pra acordar meu pc (q n tenho mais)
from secret import secret                               # token e mac_addr
from sysinfo import getsysinfo                          # meu módulo pra retornar a informação de sistema
extractor = URLExtract()                                #definindo o extrator pra ficar com menos texto
tracemalloc.start()                                     #^
#-------------------------------------------------------



"""#logger de eventos do discord.py, é para debugging.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)"""



#especficar ID's------------------------------------
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
tomzinhoID = 253253452103286784                     #tomzinhoID, from clube do livro
#---------------------------------------------------



#todo list: ---------------------------------------------------------------------
#james gado - done
#log - done
#games -talvez em outra vida
#ativos n precisar de 1 msgs só pra continuar ativos. - DEPRECATED
#persistence no cargo de .. - DONE
#não apagar mensagens contento ass que sejam do tenor - DONE
#persistence nos mutados - DONE
#organização dos comandos que estavam dentro do on_message - DONE
#não precisar pegar variáveis em todo on_message (fazer global) - DONE
#corrigir o rich presence que estava atualizando errado - DONE
#atualizar para dev e usar AllowedMentions - DONE
#pseudo-random menos random para o dice - DONE
#whitelist para counterar falsos positivos dos links contendo ass e tal - DONE
#persistence no bom dia - DONE
#um único save para salvar todos os tipos de listas/dicionários - DONE
#USAR COGS
#reg_tp usando embeds
#algum comando que procure o significado de palavras, devem existir apis públicas pra dicionários em português.
#---------------------------------------------------------------------------------



#iniciando variáveis úteis -------------------------------------------------------------
entradasdeuserstempo = []                                                               #salva o tempo de entrada de users novos
entradasmembros = []                                                                    #salva os membros novo
newmembernumber = -1                                                                    #membro número
imageextensions = ['.png', '.jpg', '.webp', '.jpeg', '.mp4', '.3gp', 
    '.mov', '.webm', '.torrent', '.zip', '.rar']                                        #extensões para reconhecer imagens para mutar usuários com CPI
blacklist = ['pornhub', 'xvideos', 'xxx', 'xnxx', 'xhamster', 'porn',                   #sinalizar como porn
    'boobs', 'pussy', 'dick', 'asshole', 'sex', 'discord.gg', 'chat.whatsapp.com']
redirects = ['bit.ly', 'goo.gl', 'adf.ly', 'tinyurl', 'ow.ly']                          #sinalizar redirects
whitelist = ['tenor.com']
mensagemflood = 300                                                                     #número de caracteres antes de ser considerado mensagem como spam
membrosativos = []                                                                      #inicia lista de ativos, aqui vão os objetos membros
membrosativosvalores = []                                                               #inicia a lista onde ficam o nº de mensagens, correspondente ao index do membrosativos
membrosativostimes = []                                                                 #inicia a lista onde ficam a hora da última mensagem do index correspondente ao membro
ativothreshold = 100                                                                    #nº de mensagens pra se considerar ativo
tempmember = ''                                                                         #inicia a lista para guardar o membro que se faz checagem ao deletar mensagens
started = datetime.datetime.now()                                                       #pega a hora em que o bot foi iniciado, para cálculo de $uptime depois
initialtime = round((time.time()-761400)/86400, 0)                                      #inicia a variável de checks pra reset da lista membrosativosvalores
lastplayingchange = [datetime.datetime.now()-datetime.timedelta(minutes=5), 'The Project']#inica a variável pra
spam = 120                                                                              #120 é o número para se checar se em 15 minutos de entrada de servidor forem enviadas 120 mensagens, dar mute.
bomdiacooldown = {}                                                                     #aqui ficam temporariamente usuários impedidos de receberem a resposta do bot referente ao bom dia
logging.basicConfig(filename='botlog.log', filemode='w', format='%(levelname)s - %(message)s')
eventofilme = False                                                                     #especifica se tem evento de filme ou não.
spammerdebomdia = True                                                                  #boolean pra responder qlqr um com bom dias e tal.
eventofilmelista = {}                                                                   #inicia a variável para armazenas quem e o que sugeriu no evento de filme.
listasugestãofilme = {}                                                                 #inicia a variável que faz alguma coisa q n lembro.
reloadativostime = 0                                                                    #ainda  n to usando isso
direct_messages = {'testing':'my balls'}                                                #pra salvar as mensagens que os locos me enviam por direct no bot.
setorajuda = {                                                                          #aqui é invocado quando alguém usa o $help para obter ajuda.

    '**$ajuda**':'Mostra essa mensagem.',
    '**$mostrarboasvindas**':'Mostra a mensagem de boas-vindas.',
    '**$uptime**':'Retorna o tempo de execução ininterupta do bot.',
    '**$sugerirfilme**':'Usado para sugerir nomes de filmes quando acontecerá um evento de filme.',
    '**$versugestão**':'Usado para ver as sugestões de filme suas ou de outros usuários',
    '**$apagarsugestão**':'Usado para apagar suas sugestões.',
    '**$dice**':'Joga dados.',
    '**$github**':'Link para o repositório GitHub do bot.',
    '**ping**':'ping.',
    '**$tempmute**':'Muta usuários.',
    '**$unmute**':'Desmuta usuários.',
    '**$pomodoro**': 'Temporizador para pomodoro em voice chat.'
    }
natasmember = ''                                                                        #aqui abaixo iniciam variáveis que são globais. é pra economizar ficar pegando coisas a cada evento.
lastuserjoin = ''                                                                       #variáveis globais pra usar em outros eventos
lastlastuserjoin = ''                                                                   #^
attachmentsApagados = {}                                                                #armazena objetos que contem os atachments apagados
discordget = discord.utils.get                                                          #usar . pra pegar atributos muitas vezes é mais lento.
roles = ['Centro-Oeste','Sudeste', 'Sul','Nordeste','Norte']                            #mesma coisa
roles_emoji = ['🌿', '🍞', '🧉', '🌴', '🧭']                                            #global que n precisava ser global mas tá aí
voicechannel = ''                                                                       #eh... complicado
cargospegos = False                                                                     #inicializador de muitas variáveis. usado no on_message
guild = ''                                                                              #nem lembro
member = ''                                                                             #^
ademir = ''                                                                             #variável global para o cargo de Administrador
mutedrole = ''                                                                          #variável global para o cargo de mutado
cargo2pontos = ''                                                                       #variável global para o cargo2pontos
cargocaveira = ''                                                                       #variável global para o cargocaveira
reg_tp = ''                                                                             #variável global para enviar msg pro reg_tp
mirrorchannel = ''                                                                      #global variable representing the batepapo mirror channel
lasttimedonecommand = ''                                                                #dicelimiter
limiter1dia = {}                                                                        #limiter1dia é pro $grupodeestudos
raidcontrol = False                                                                     #inicialização do raidcontrol, para keep track dos que entram no sv mt rápido (1,5m)
userroles = {}                                                                          #importante variável, o nome é mutados mas é para todos os que o bot já givou cargo. salvado frequentemente no userroles.txt. dict.
saudações = {'bom dia': [], 'boa tarde':[], 'boa noite': []}                            #guardar quem já foi "saudado"
bate_papo_ids = {}                                                                      #keep track of sent messages and their respective parent
lastusersent = 0                                                                        #pra o bot não repetir o header em casa msg no bate papo mirror
mutadosMembers = {}                                                                     #usuários mutados ficam aqui, com seus respectivos datetimes
moderador = ''                                                                          #variável global....
supervisor = ''                                                                         #^
membrosQuePrecisaDesmutar = []                                                          #pra usar no on_voice_state_update
interromperLoop = False                                                                 #usado pra quebrar o loop do pomodoro
warnedMembers = {}                                                                      #do $tempwarn
warnRole = ''                                                                           #variável global..
pomodoroID = 0                                                                          #iniciando variável global do id de pomodoro
canalDePomodoro = ''                                                                    #guarda o author.voice.channel q o bot entrou
pomodoroMemberCommand = ''                                                              #id de quem iniciou pomodoro
#---------------------------------------------------------------------------------------



if not '3.8.2' in sys.version: print('Eu devo ser executado na versão 3.8.2 do Python seu burro!'); exit()



#definição de funções --------------------------

class obj:                                      #é possível atribuir a uma váriável vários atributos dentro de um objeto usando uma classe vazia.
    pass

class attachment:                               #útilidade pública
    def __init__(self, time, message_id, channel_name, author, filename, fileformat, nomearquivo):
        self.time = time
        self.message_id = message_id
        self.channel_name = channel_name
        self.author = author
        self.filename = filename
        self.fileformat = fileformat
        self.nomearquivo = nomearquivo

def cleanFileDirectory(dir):                    #limpa diretórios pois linux n salva /> corretamente
    notAllowed = ['>', '<', '/', '\\', '|', '&', ':']

    """
    def replaceAndSave(toReplace):
        global dir
        dir = dir.replace(toReplace, '')


    [replaceAndSave(item) for item in notAllowed] """
    for item in notAllowed:
        dir = dir.replace(item, '')

    return dir

def gettplove(message):                         #pra usar no send content de agradecimento
    return discordget(message.guild.emojis, id=522462442366828574)      #representa o emoji tplove, para mostrar, usa-se str(tplove)

def getboasvindasembed(member):                 #retorna o embed de boas vindas. usado no comando e no on_member_join
    channel = member.guild.get_channel(regras)
    embed = discord.Embed(              #aqui a gente escreve o embed (texto com formatação top q vai ser enviada nas DM's de quem entra)
        title = '⇝ **Seja bem-vindo(a) ao The Project!** ⇜',
        description = '• O The Project é uma comunidade focada na troca de conhecimento. Todos devem ter acesso a ele, portanto deve ser compartilhado com o próximo. \n \n • Aqui discutimos sobre quaisquer temas, ajudamos uns aos outros em vestibulares, idiomas, ENEM, concursos, entre outros. Somos uma comunidade amigável, sempre ajudando no desenvolvimento pessoal de cada um. Sinta-se a vontade para juntar-se a nós para uma conversa sadia, respeitosa e muito mais! \n \n ⇝ **Lembre-se de ler as {a}, para evitar qualquer transtorno.**'.format(a=channel.mention),
        colour = discord.Color.magenta()
        )
    embed.set_image(url='https://cdn.discordapp.com/attachments/605248064181108767/674644426035036160/unknown.png') #aqui vai a imagem que fica no final da msg, #não funcionam gifs.

    return embed

def daypass():                                  #esta função retorna False na primeira vez executada, e True somente uma vez a cada 24 horas.
    global initialtime                                                                  #pega a variável que definimos globalmente, pois local não se aplica a eventos (ex. on_message não requer chamar a variável como global, mas def sim)
    tempo = (time.time()/86400)-.625
    if round(tempo) > initialtime:                                       #pega o tempo atual e compara com o initial time, que é na primeira vez 0, e depois o tempo antes de ser feito qualquer comparação.
        initialtime = round((time.time()/86400)-.5)
        savelista(initialtime, 'initialtime')
        return True
    else:
        initialtime = round(tempo, 0)
        savelista(initialtime, 'initialtime')
        if random.randint(0,150) == 0:
            print(f'Restam {round((1-(((-time.time()/86400)-.625)%1))*1440)} minutos para próximo reset daypass')
        return False
    
def log(information):                           #função experimental ainda não implementada
    '''
    with open(str(lista)+'.txt', 'w') as f:                                             #objetivo é ao pressionar combinação de tecla, salvar a lista de ativos para depois ler ao pressionar a mesma ou combinação diferente.
        for item in lista:
            f.write("%s\n" % item)
    '''
    logging.info(information)

def aprovarsugestão(member, message):           #usado por staff para aprovar sugestões (dã)
    channel = discordget(member.guild.channels, name='sugestões-de-filmes')
    return channel.send(content=str(message))

def is_troller(m):                              #aqui usamos a variável tempmember para checar nas mensagens que serão apagadas pertecem ao membro desordeiro, retorna True se a mensagem será apagada.
    global tempmember
    return m.author == tempmember

def savelista(variable, variablename):          #apaguei umas 10 funções e criei só uma que foi essa
    try:
        with open(f'{variablename}.txt', 'wb') as file:
            pickle.dump(variable, file)
        return True
    except:
        return False

def loadlista(variable, variablename):          #apaguei umas 10 funções e criei só uma que foi essa
    if os.access(f"{variablename}.txt", os.R_OK):

        with open(f"{variablename}.txt", 'rb') as file:
            return pickle.load(file)
    else:
        savelista(variable, variablename)

def resetativo():                               #resetativo é o primeiro reset inicial que damos, é onde as listas são definidas com seus "placeholders"
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
    
    savelista(ativos, 'ativos')
    savetimes()
    savevalores()
    '''
    #loadativos()
    #loadtimes()
    #loadvalores()
    #loaduserroles()

    global userroles, direct_messages, saudações, initialtime, mutadosMembers, warnedMembers, membrosQuePrecisaDesmutar
    userroles = loadlista(userroles, 'userroles')
    os.system('clear')
    print(f'\nloaded {len(userroles.keys())} users and {sum([len(i)-1 for i in userroles.values()])} roles!\n')
    #direct_messages = loadlista(direct_messages, 'direct_messages')

    #direct_messages.update({'testing':'my balls'})
    #print(f'directs loadeds: {direct_messages}')

    loadlista(warnedMembers, 'warnedMembers')
    print(f'loaded {len(warnedMembers)} membros avisados.\n')

    saudações = loadlista(saudações, 'saudações')
    print(f'saudações loaded: {saudações}\n')

    initialtime = loadlista(initialtime, 'initialtime')
    print(f'initialtime loaded: {initialtime}\n')
    
    loadlista(membrosQuePrecisaDesmutar, 'membrosQuePrecisaDesmutar')
    print(f'Foram carregados {len(membrosQuePrecisaDesmutar)} membros que precisam ser desmutados\n')

    mutadosMembers = loadlista(mutadosMembers, 'mutadosMembers')
    #print(f'Os burrao mutados foram carregados {mutadosMembers}')
    print("Mutes agendados:")
    [print(f"{(time).strftime('%d/%h/%y %H:%M')}") for time in sorted(mutadosMembers.values())]
    #[print(f"{(datetime.datetime.now()-time).strftime('%D %T')}") for time in mutadosMembers.values()]

    if eventofilme:
        global eventofilmelista, listasugestãofilme
        eventofilmelista = loadlista(eventofilmelista, 'eventofilmelista')
        listasugestãofilme = loadlista(listasugestãofilme, 'listasugestãofilme')
        #loadeventofilmelista()
        #loadlistasugestãofilme()

    """
        n=1000
    for i in membrosativosvalores:
        if i !=0:
            n -= 1"""

    #print('Listas iniciadas\nslots restantes:')#, membrosativos, membrosativostimes, membrosativosvalores)
    
def resetlista():                               #aqui resetamos a lista, a lista na qual pertence os valores, já que não é necessário reiniciar tudo.
    global membrosativosvalores
    membrosativosvalores = []
    n = 0
    while n < 1000:
        membrosativosvalores.append(0)
        n += 1
    print('Lista de ativos valores foi RESET!')

def getadmincargos(member):                     #definir o cargo de adm, mas nem usamos mais pq os cargo agr é tudo global ent sla
    cargoadministrador = discordget(member.guild.roles, name="Administrador")    #seta o cargo ademiro
    cargomoderador = discordget(member.guild.roles, name="Moderador")            #seta o cargo moderador
    return cargoadministrador, cargomoderador

def avisomuteDM(message):                       #aqui é enviado a mensagem de aviso para o usuário que tomou mute automaticamente
    #will = discordget(message.guild.members, id=willid)
    natas = discordget(message.guild.members, id=natasid)
    return message.author.send(content=f'{message.author.mention}\n*Esta é uma mensagem automática* \n\nOlá, você fui mutado temporariamente no servidor The Project por comportamento potencialmente indesejado, suas mensagens foram salvas e serão posteriormente avaliadas por um moderador.\nSe você acredita que isso é um erro, informe a staff (preferencialmente {natas.mention}) por favor.\n\nAtenciosamente, equipe The Project.')

def currenttime():                              #retorna uma string com a data e hora atual com precisão de segundos e não aqueles microsegundos quebrados.
    return datetime.datetime.now().strftime('%d.%h.%Y %H:%M:%S')

def spammerdebomdialimiter(member):             #limitador de bom dia mas que eu uso em mts outros lugares tbm pra controle de fluxo aosdijasdoasd
    global bomdiacooldown
    try:
        bomdiacooldown[member]
        if datetime.datetime.now() - bomdiacooldown[member] >= datetime.timedelta(seconds=40):
            del bomdiacooldown[member]
            return True
        else:
            return False
    except KeyError:
        bomdiacooldown.update({
            member:datetime.datetime.now()
        })
        return True

def coolactivity():                             #randomicamente escolhe dentro dessa lista alguma atividade pro bot mostrar, 10% de chance dele pegar alguma da lista em cada mensagem.
    lista = [

        'trying to solve a hard equation. 1+1=?',
        'nada, to estudando.',
        'nada, to estudando.',
        'nada, to estudando.',
        'nada, to estudando.',
        'nada, to estudando.',
        'nada, to estudando.',
        'James gado',
        'ECDSA',
        'money to hoes',
        'NATAS LINDOOOOOO',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'The Project',
        'Python',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        'Sou Open-Source! Digite o comando $github.',
        '$help',
        '$help',
        '$help',
        '$help',
        'Prefixo: $',
        '𝕓𝕦𝕘𝕤 𝕡𝕣𝕠 𝕒𝕝𝕥𝕠',
        '[̲̅b][̲̅u][̲̅g][̲̅s] [̲̅p][̲̅r][̲̅o] [̲̅a][̲̅l][̲̅t][̲̅o]',
        'b̸͇͕͕̱̜͔̓͐͜u̴̦͇͂͐͋̓̽͌̅͑̕g̴̠̾̽̆͑s̶̘͎͙͍͒̉̀̐͘ͅ ̷̘̘̦͛͛̍̄̀̇̆͋͠ṗ̵̖̗̎͐͝ṟ̶̼̳͚̬̣͉̓̒̀̈́̑̑̓͑̽ơ̵̢̻͍̤͎͎̾͆͊̉̔̔̀̈́ ̶̨͇̲̜͉̼͌̏́͊͛a̵̤̹̪̿̆̔l̸̡̧͓̜͚͓̖̣̆̽̄͋̐̿̌t̶̪͓̣̬̟̹̹̺͓͖͊̏͋̈́̾̂̕͠o̴͖̗̝̞̣̩͖̣͛͛͊͗',
        'b͓̽u͓̽g͓̽s͓̽ ͓̽p͓̽r͓̽o͓̽ ͓̽a͓̽l͓̽t͓̽o͓̽',
        'pra esquecer a morena 😔',
        'pra esquecer a morena 😔',
        'pra esquecer a morena 😔'
        ]
    
    a = random.randint(0, 9)
    global lastplayingchange
    if a > 4:
        try:
            if datetime.datetime.now() - lastplayingchange[0] > datetime.timedelta(minutes=5):
                lastplayingchange = [datetime.datetime.now(), random.choice(lista)]
                return client.change_presence(status=discord.Status.idle, activity=discord.Game(lastplayingchange[1])) #seta o 'jogando'
            else:
                return client.change_presence(status=discord.Status.idle, activity=discord.Game(lastplayingchange[1])) #seta o 'jogando'
        except:
            lastplayingchange = [datetime.datetime.now()-datetime.timedelta(minutes=5), 'The Project']
    else:
        try:
            return client.change_presence(status=discord.Status.idle, activity=discord.Game(lastplayingchange[1])) #seta o 'jogando'
        except:
            return ''

async def waiting(seconds, ctx, text):          #usado no $digitando. bem inútil aodhaoshd
    await asyncio.sleep(seconds)
    await ctx.channel.send(text)

resetativo()                                    #inicia as listas, desligado pois as listas de ativos foram desabilitadas, religado pois tem mais coisa do que lista de ativos dentro da func
#-----------------------------------------------



#definição do cliente.
client = commands.Bot(command_prefix = '$', help_command=None, allowed_mentions=discord.AllowedMentions(everyone=False, roles=True, users=True))                 #isso eu sei         
#--------------------




@client.event
async def on_ready():                                                   #on_ready é chamado quando o bot está pronto
    print(f'[{currenttime()}]\tlogged on as {client.user}!')
    c = await client.fetch_channel(registro)
    await c.send('Bot has awaken!')                                     #esta mensagem usamos para chamar o on_message com nossa guild e atribuir os cargos usando o cargospegos.






@client.event
async def on_raw_reaction_remove(event):                                #on_raw_reaction_remove é chamado quando uma mensagem independente do cache teve uma reação removida.
    #raw pq se não for raw, ele não escuta os reacts em mensagens que foram enviadas antes de iniciar o bot

    userid = event.user_id                                              #pega o id de quem reagiu
    guild = client.get_guild(id=event.guild_id)                         #pega a guild
    member = guild.get_member(userid)                                   #procura o objeto membro correspondente ao id dentro da guild
    memberroles = member.roles
    guildroles = member.guild.roles
    global reg_tp#reg_tp = guild.get_channel(registro)

    if event.channel_id != 697863869707845682:
        livro = discordget(member.guild.roles, name="Clube do Livro")   #encontra a role de clube do livro, mesma coisa em baixo
        estudos = discordget(member.guild.roles, name="Grupo de Estudos")
        id = event.message_id                                           #pega o id a mensagem reagida e verifica se a mensagem reagida é a mesma do clube do livro ou estudos
        if id == clube_id:
            if str(event.emoji) == '\U0001F4DA':
                await discord.Member.remove_roles(member, livro)        #tira a role
                lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                await reg_tp.send(content=f'❌\t[{currenttime()}]\tRemovido e salvo {livro.mention} de {member.mention}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False)) #escreve no log
        
        if id == grupo_id:
            if str(event.emoji) == '\U0001F4DA':
                await discord.Member.remove_roles(member, estudos)
                await reg_tp.send(content=f'❌\t[{currenttime()}] Removido e salvo {estudos.mention} de {member.mention}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
    

    #referente à tag região
    global roles
    global roles_emoji

    if event.channel_id == 697863869707845682:                          #se o canal é o certo
        for item in roles:                                              #itera sobre todas as roles
            if hash(event.emoji.name) == hash(roles_emoji[roles.index(item)]) and item in str(memberroles): #verifica se o emoji removido está dentro da lista
                await member.remove_roles(discordget(guildroles, name=item)) #se sim, ele retira a role
                #reg = await client.fetch_channel(registro)              #e envia no reg_tp as infos
                lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                await reg_tp.send(f'✅\t[{currenttime()}]\tRemovido e salvo role {item} ao usuário {member.mention}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
                return






@client.event
async def on_message(message):                                          #aqui ficam todos os comandos relacionados a mensagens enviadas, é chamado sempre que o bot consegue ver que foi enviado uma mensagem na guild


    global cargospegos, guild, member, ademir, mutedrole, cargo2pontos, cargocaveira, reg_tp, mirrorchannel, saudações, bate_papo_ids, direct_messages, limiter1dia, mutadosMembers, moderador, supervisor, warnRole
    
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
        moderador = discordget(message.guild.roles, name="Moderador")
        supervisor = discordget(message.guild.roles, name="Supervisor")
        warnRole = discordget(message.guild.roles, name="Warned")
        cargospegos = True
        
        #--- cargos pegos
    try:
        await coolactivity()                                #for some reasomn the bot was crashing at this line. limited the times 'change_presence' is being called
    except:
        pass
    messagecontentlower = message.content.lower()       #performance reasons


    if 'obrigado' in messagecontentlower or 'obrigada' in messagecontentlower:                   #se agradecer o bot, responder com uma mensagem legal

        if 'Direct Message' in str(message.channel) and not 'The Project#8708' in str(message.channel):
            await message.channel.send(f'Disponha, {message.author.mention} <:tplove:522462442366828574>'); return
        elif not client.user.mentioned_in(message=message): return
        
        await message.channel.send(f'Disponha, {message.author.mention} {str("<:tplove:522462442366828574>")}'); return



    if 'Direct Message' in str(message.channel) and not message.author.bot:
        print(f'Received DM with {message.author} message=\'{message.content}\'')
        #time = currenttime()
        #savelista(direct_messages, 'direct_messages')
        #direct_messages.update({'testing':'my balls'})
        #savelista(direct_messages, 'direct_messages')
        try:
            await reg_tp.send(f'<:tpwat:522462810676920322>\t[{currenttime()}]\tusuário {message.author.mention} enviou mensagem no privado.\n`{message.content}`')
        except:
            await reg_tp.send(f'<:tpwat:522462810676920322>\t[{currenttime()}]\tusuário {message.author.mention} enviou mensagem no privado mas era muito grande.\n`{message.content[:1900]}``')
        await message.author.send('<:tpa:693622183532036166>')
        await message.author.send(f'O bot não suporta envio de mensagens por mensagem direta, por favor, utilize o canal de #bots em um servidor para seu uso!')
        return



    if extractor.has_urls(str(message.attachments)) and not message.author.bot:
        #for x in imageextensions:
        #    if x in message.attachments[0].filename.lower(): #coloquei pra baixar tudo mesmo, sendo até sla, .rar
        for i in message.attachments:
            time = currenttime(); x = ".everything"
            os.system(f'wget -q {i.url} -O \"/home/natas/bot/attachments/{cleanFileDirectory(f"{time} {message.author.id} {message.channel.name} {message.author.name} filename_{i.filename}")}\"') #baixa a imagem, precisa ter o wget dentro do path sistema
            attachmentsApagados.update({message.id:attachment(time, message.author.id, message.channel.name, message.author.name, i.filename, x, cleanFileDirectory(f'{time} {message.author.id} {message.channel.name} {message.author.name} filename_{i.filename}'))})
            print(f'[{currenttime()}] file {i.filename} from {message.author.name} sent on {str(message.channel)} downloaded.')
                

    #bate papo mirror
    if str(message.channel) == 'bate-papo' and not "mirror" in str(message.channel):
        global lastusersent

        if lastusersent != message.author.id:
            header = f'{message.author.mention}:'
            lastusersent = message.author.id
        else:
            header=''

        if message.attachments:
            #print(f"going after the file... [{currenttime()}]")
            files = discord.File(f"/home/natas/bot/attachments/{cleanFileDirectory(attachmentsApagados[message.id].nomearquivo)}")
            msg = await mirrorchannel.send(content=f'[Mensagem de {message.author.name}]', file=files, allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
            bate_papo_ids.update({message.id:msg.id})
        else:
            try:
                msg = await mirrorchannel.send(content=f'{header}\n{message.content}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
                bate_papo_ids.update({message.id:msg.id})
            except:
                pass
    
    
    if message.author.bot:                                              #não escutar mensagens de bot. é um boolean.
        return
        
    



    if str(message.channel) == 'apresentações-introdução':  #mensagens aqui serão reagidas com like
        await message.add_reaction(emoji); await message.add_reaction(gettplove(message))               #emoji personalido :like:
        await reg_tp.send(content=f'✅\t[{currenttime()}]\tNova apresentação de {message.author.mention}')
        return
        #await message.author.add_roles(discordget(message.guild.roles, name='Apresentado'))


    


    
    for i in mutadosMembers:
        if mutadosMembers[i] - datetime.datetime.now()  < datetime.timedelta(seconds=0):
            try:
                user = await guild.fetch_member(i)
                await user.remove_roles(mutedrole)
            except:
                await reg_tp.send(f'🕛\t[{currenttime()}]\tUsuário {i} saiu do servidor antes que seu tempo de mute acabasse.')
                del mutadosMembers[i]; savelista(mutadosMembers, 'mutadosMembers'); return
            del mutadosMembers[i]; savelista(mutadosMembers, 'mutadosMembers')
            await reg_tp.send(f'🕛\t[{currenttime()}]\tUsuário {user.mention} desmutado pois o tempo passou.')
            break

    for i in warnedMembers:
        if warnedMembers[i] - datetime.datetime.now()  < datetime.timedelta(seconds=0):
            try:
                user = await guild.fetch_member(i)
                await user.remove_roles(warnRole)
            except:
                await reg_tp.send(f'🕛\t[{currenttime()}]\tUsuário {i} saiu do servidor antes que seu tempo de mute acabasse.')
                del warnedMembers[i]; savelista(warnedMembers, 'warnedMembers'); return
            del warnedMembers[i]; savelista(warnedMembers, 'warnedMembers')
            await reg_tp.send(f'🕛\t[{currenttime()}]\tUsuário {user.mention} desavisado pois o tempo passou.')
            break

    

    if daypass():
        print(f'!!!!!!\n\n[{currenttime()}]Daypass returned true\n\n!!!!!!')
        limiter1dia.clear()
        saudações = {'bom dia': [], 'boa tarde':[], 'boa noite': []}; savelista(saudações, 'saudações')


    if message.author.id == natasid and 'Direct Message' in str(message.channel):                    #verifica se quem manda mensagem sou eu


        if 'acordar' in message.content:
            send_magic_packet(secret.mac)               #envia o magic packet para o compiuter
            await message.channel.send('Magic packet enviado.')
            return                                      #retorna

        elif messagecontentlower.startswith('status'):
            await message.author.send('**Server Status:**\n\n'+str(getsysinfo()))
            print(f'[{currenttime()}] Sent server info to {message.author}, id: {message.author.id}, canal: {message.channel}\n')
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

        elif messagecontentlower.startswith('command'):
            output = os.popen(message.content[message.content.find('command')+8:]).read()
            if not output:
                output = 'Done.'
            await message.author.send(output)
            return
        else:
            return
            
        ''' deprecated, using ssh to view program output
        if ['screenshot','screen','prntsc'] in message.content:
            im = ImageGrab.grab()
            im.save('Screenshot.jpg')
            files = discord.File('Screenshot.jpg')#, filename="c:/users/natas/documents/Screenshot.jpg")
            await message.channel.send(file=files)
            return
        '''


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
                await message.channel.send(content=f'vou pegar esse monte de dígito ({len(number)} aliás) que vc escreveu e enfiar no seu cu seu fdp {message.author.mention}')
                return
            if int(number) > 3:
                await message.channel.send(content=f'{message.author.mention} ficou {number} dias sem bater uma? Quem segura leite é vaca porra ta maluco')
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
                await message.channel.send(content=f'vou pegar esse monte de dígito ({len(number)} aliás) que vc escreveu e enfiar no seu cu seu fdp {message.author.mention}', delete_after=10)
                return
            if int(number) > 1:
                await message.channel.send(content=f'{message.author.mention} ficou {number} dias sem estudar? Desse jeito nunca vai passar no vestibular seu burro')
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
    if str(member.roles).find('..') != -1:                          #detecta se o user tem o cargo ..
        if message.channel.name != 'apresentações-introdução':      #pra não escutar introduções


            if len(message.content) > mensagemflood:                #se a mensagem é spam, contendo mais de 300 caracteres
                if member.top_role == cargocaveira:
                    await member.add_roles(mutedrole) #mute nele, e embaixo faz um log no registro

                    global tempmember; tempmember = message.author
                    
                    try:
                        await avisomuteDM(message)
                    except:
                        await reg_tp.send('<:tptapeado:607549256756101121>\tFoi tentado enviar uma mensagem de aviso mute para {message.author.mention} porém ele desabilitou tal opção.')
                    
                    lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                    await message.channel.purge(limit=15, check=is_troller)
                    await reg_tp.send(content=f'❌ [{currenttime()}] \n {ademir.mention}\n\nusuário {message.author.mention} mutado por comportamento potencialmente indesejado _(mensagem grande)_ no canal {message.channel.mention}\n\nMensagem enviada: {message.content[:1750]} \n\ntamanho: {len(message.content)}\\{mensagemflood} \n\n ')
                    await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=60)

                    
                
                if member.top_role != cargocaveira:
                    await reg_tp.send(content=f'❌ [{currenttime()}] \n\nusuário {member.mention} cometeu infração _mensagem longa_ no canal {message.channel.mention}.\nconteúdo:{message.content[0:1850]}')
                    await message.delete()
                    await message.channel.send(f'{message.author.mention}, não envie mensagens grandes!', delete_after=15)
                    await member.add_roles(cargocaveira)
                    lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                    for role in message.author.roles:
                        lista.append(role.name)
                    userroles.update({message.author.id: lista})
                    savelista(userroles, 'userroles')

            for i in imageextensions:                               #apaga mensagens contendo imagens como attachments
                if message.channel.name == 'shitpost':
                    return
                if str(message.attachments).lower().find(i) != -1:  #procura se a mensagem tem imagem.
                    if member.top_role == cargocaveira:
                        files = []                                  #define a lista
                        filename = message.attachments[0].filename #define o nome de arquivo
                        os.system('wget –-quiet {} -O {}'.format(message.attachments[0].url, filename)) #baixa a imagem, precisa ter o wget dentro do path sistema
                        await member.add_roles(mutedrole)           #dá mute, e salva no registro
                        lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                        try:
                            await avisomuteDM(message)
                        except:
                            print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                        files = discord.File("{}".format(cleanFileDirectory(filename)), filename="/home/natas/bot/{}".format(cleanFileDirectory(filename)))
                        await reg_tp.send(file=files, content='❌ [{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(envio de imagem)_ no canal {.mention} \n\ntrigger: {} \n\nMensagem enviada:\n\n'.format(currenttime(), ademir, message.author, message.channel, i))
                        tempmember = message.author
                        await message.channel.purge(limit=15, check=is_troller)
                        await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=60)

                    if member.top_role != cargocaveira:
                        await reg_tp.send(content='❌ [{}] \n\nusuário {.mention} cometeu infração _envio de imagem não verificada_ no canal {.mention}.'.format(currenttime(), member, message.channel))
                        await message.channel.send(f'{message.author.mention}, não envie imagens!', delete_after=15)
                        await member.add_roles(cargocaveira)
                        lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')

            for i in imageextensions:                               #apaga mensagens contendo link de imagens
                if messagecontentlower.find(i) != -1:
                    if member.top_role == cargocaveira:
                        await member.add_roles(mutedrole)
                        lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                        savelista(userroles, 'userroles')
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
                    lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                    await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)

        #remover cargo 2 pontos se o usuário tiver dentro do server por mais de 24h
        if (datetime.datetime.now() - member.joined_at) > datetime.timedelta(hours=24):
            if member.top_role == cargo2pontos:
                await member.remove_roles(cargo2pontos)
                await reg_tp.send(content='<:like:547068425067954196>\t[{}]\tUsuário {.mention} removido do watchdog por tempo de servidor > 24h'.format(currenttime(), message.author))
    
    for i in redirects:                             #apaga mensagens contendo redirecionadores
        if messagecontentlower.find(i) != -1:
            if extractor.has_urls(message.content):
                await member.add_roles(mutedrole)
                lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                log(f'Usuário {tempmember} foi mutado por envio link de redirecionador ({i}), \"{message.content}\"')
                try:
                    await avisomuteDM(message)
                except:
                    print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                await reg_tp.send(content='❌ [{}] \n {.mention}\n\n usuário {.mention} mutado por comportamento potencialmente indesejado _(link com redirect)_ no canal {.mention}\n\ntrigger: {} \n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, i, message.content))
                tempmember = message.author
                await message.delete()
                await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)



    if extractor.has_urls(message.content):                 #aqui verifica se os links enviador são verídicos, ou se tem problemas.
        for link in extractor.find_urls(message.content, check_dns=False, only_unique=True):

            for i in blacklist:                             #apaga mensagens contendo links apra sites pornográficos
                if link.lower().find(i) != -1:
                    for x in whitelist:
                        if x in link: return
                    await member.add_roles(mutedrole)
                    lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                    await reg_tp.send(content=f'❌ [{currenttime()}] \n {ademir.mention}\n\n usuário {message.author.mention} mutado por comportamento potencialmente indesejado _(link de site dentro do blacklist)_ no canal {message.channel.mention}\n\ntrigger: {i} \n\nMensagem enviada:\n\n{message.content}')
                    try:
                        await avisomuteDM(message)
                    except:
                        print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')

                    await message.delete(); await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)
                    return

            if 'http://' not in link and 'https://' not in link:
                link = f'http://{link}'
            try:
                @timeout(2)
                def foo():
                    global site
                    print(f"resolving {link}")
                    site = requests.get(link)
                foo()
            except:
                print("Link enviado deu timeout. Parando processo para não rolar exception no bot."); return
            if site.text.lower().find('block this site') != -1 or 'www.rtalabel.org/index.php?content=parents' in site.text:
                    await member.add_roles(mutedrole)
                    lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                    await reg_tp.send(content='❌ [{}] \n {.mention}\n\nUsuário {.mention} mutado por comportamento potencialmente indesejado _(link de site contendo string adulta)_ no canal {.mention}\n\nMensagem enviada:\n\n{}'.format(currenttime(), ademir, message.author, message.channel, message.content))
                    try:
                        await avisomuteDM(message)
                    except:
                        print('Foi tentado enviar uma mensagem de aviso mute para {message.author.name} porém ele desabilitou tal opção.')
                    await message.delete(); await message.channel.send(f'https://tenor.com/zH0p.gif', delete_after=30)
                    return


    
                   
    #----fim seção mutar/avisar/registrar


    """
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=Checker, args=(f"/home/natas/bot/attachments/{attachmentsApagados[message.id].nomearquivo}",))
    
    p.start()
    print(f'get aqui: \n ------------{q.get()}')
    if q.get():
        await message.channel.send(f'{message.author.mention}, não envie pornografia!', delete_after=60)
        await message.delete()"""
                


                        



    if str(message.channel) == 'sugestões':             #verifica se essa msg foi enviada no sugestões, etc
        await message.add_reaction('\U0001F44D')        #thumbsup
        await message.add_reaction('\U0001F44E')        #thumbsdown
        await reg_tp.send(content='<:like:547068425067954196>\t[{}]\tNova sugestão de {.mention}'.format(currenttime(), message.author))


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

    if spammerdebomdia and message.channel.name == 'bate-papo' and client.user.mentioned_in(message=message):
        if messagecontentlower.startswith('bom dia') and message.author.id not in saudações['bom dia']:#bomdia' in messagecontentlower.replace(' ', '') and spammerdebomdialimiter(message.author):
            saudações['bom dia'].append(message.author.id); savelista(saudações, "saudações")
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
            saudações['boa tarde'].append(message.author.id); savelista(saudações, "saudações")
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
            saudações['boa noite'].append(message.author.id); savelista(saudações, "saudações")

            if 17 <= datetime.datetime.now().hour <= 23 or 0 <= datetime.datetime.now().hour <= 6:
                await message.channel.send(content=f'Boa noite, {message.author.name[0].upper()+message.author.name[1:]}.')
                return
            else:
                kekw = await message.author.guild.fetch_emoji(emoji_id=633527255993417768)
                await message.channel.send(content=f'Tu tá fora né? O cara manda um boa noite essas horas {str(kekw)}')
                return


    if messagecontentlower.startswith('ola bot') or messagecontentlower.startswith('olá bot') or messagecontentlower.startswith('oi bot') or messagecontentlower.startswith('oi <') and message.mentions[0] == message.guild.me:
        if message.channel.name != 'bate-papo' or not spammerdebomdialimiter(message.author) : return
        await message.channel.send(content=f'Olá, {message.author.mention}.')

    """
    if messagecontentlower.startswith('alguém sabe ') or messagecontentlower.startswith('alguém conhece ') or messagecontentlower.startswith('alguém pode ') or messagecontentlower.startswith('alguém já ') or messagecontentlower.startswith('alguém tentou ') or messagecontentlower.startswith('alguém '):
        if not '?' in message.content or message.channel.name != 'bate-papo': return
        await message.guild.me.edit(nick="Alguém")
        await message.channel.trigger_typing(); await asyncio.sleep(.2)
        await message.channel.send(f'{message.author.mention} Não', delete_after=7)
        await message.channel.trigger_typing(); await asyncio.sleep(1)
        await message.channel.send(f'Espero ter ajudado', delete_after=6)
        await message.channel.trigger_typing(); await asyncio.sleep(.3)
        await message.channel.send(f'<:tprs:522461981433921570>', delete_after=6)
        await message.guild.me.edit(nick="")"""

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

                savelista(membrosativos, 'ativos');savelista(membrosativostimes, 'ativos');savelista(membrosativosvalores, 'ativos')

                print(f'[{currenttime()}]\tmembro {member} nº {membrosativos.index(member.name)} total de mensagens: {tempvalue}')
                
        except ValueError:
            membrosativos.append(member.name)
            savelista(membrosativos, 'ativos')
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


    if messagecontentlower.startswith("a benção") or messagecontentlower.startswith("bença"):
        if message.channel.name != 'bate-papo': return# or not spammerdebomdialimiter(message.author): 
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

    if messagecontentlower.startswith('to indo dormir') or messagecontentlower.startswith('vou dormir') or messagecontentlower.startswith('vou indo dormir') or messagecontentlower.startswith('eu vou ir dormir') or messagecontentlower.startswith('eu vou indo dormir') or messagecontentlower.startswith('eu to indo dormir') or messagecontentlower.startswith('vou ir dormir'):
        if message.channel.name != 'bate-papo': return
        if not spammerdebomdialimiter(message.author): return
        if random.choice([0,1,3,4,5,6,7,8,9]) == 0:
            await message.channel.send(f'{message.author.mention}, já vai tarde.')
        else:
            await message.channel.send(f'{message.author.mention}, durma bem.')


    



    await client.process_commands(message)              #isso sempre fica no final do on_message.






@client.event                                           
async def on_member_join(member):                                       #quando o user entra, mostrar uma mensagem de boas vindas.
    global reg_tp, userroles
    if member.bot: return

    if member.id in userroles:
        #print(f'userroles: {userroles}')
            #for roles in userroles[member.id]:
        i=1
        while i < len(userroles[member.id]):
            #print(f'trying to add {str(userroles[member.id][i])}')
            await member.add_roles(discordget(member.guild.roles, name=userroles[member.id][i]))
            i+=1
        del userroles[member.id]; savelista(userroles, 'userroles')
        await reg_tp.send(f'<:tpthink:522461647588294679>\t[{currenttime()}]\tusuário {member.mention} tinha {i-1} roles anteriores ao sair do servidor. Adicionadas de volta.')

    if member.id == natasaltid: await member.add_roles(discordget(member.guild.roles, name='Bumper')) #pra facilitar minha vida
    global newmembernumber
    newmembernumber += 1
    
    #BOAS VINDAS
    channel = member.guild.get_channel(regras)          #procura o canal com id regras, pra mencionar nas DM's depois
    embed = getboasvindasembed(member)
    #reg_tp = member.guild.get_channel(registro)
    try:
        await member.send(embed=embed)                      #envia o embed
        await reg_tp.send(content='☺️\t[{}]\tDado boas-vindas ao {.mention}'.format(currenttime(), member))
    except:
        await reg_tp.send(content='😦\t[{}]\tNão foi possível dar boas-vindas ao {.mention}.'.format(currenttime(), member))
    #--------fim boas vindas


    #começo do check de veracidade.
    tempodeexistencia = datetime.timedelta.total_seconds(datetime.datetime.now() - member.created_at)/86400 #resposta dada em dias
    #print(datetime.timedelta.total_seconds(tempodeexistencia)/86400)

    if tempodeexistencia < 1:
        global cargo2pontos
        await member.add_roles(cargo2pontos)
        lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
        await reg_tp.send('❗\t[{}]\tUsuário {.mention} com menos de 1 dia de conta no Discord entrou no servidor. watchdog adicionado.'.format(currenttime(), member))


    #entradasdeuserstempo.update( {str(member): member.joined_at} )
    
    entradasdeuserstempo.append(datetime.datetime.now())# - datetime.timedelta(hours=3))
    if len(entradasdeuserstempo) > 2: entradasdeuserstempo.pop(0)
    
    entradasmembros.append(member)
    if len(entradasmembros) > 2: entradasmembros.pop(0)
    #print('entradastempo:',entradasdeuserstempo, '\n\n', 'entradasmembro:',entradasmembros)

    try:
        global lastuserjoin,lastlastuserjoin

        print('NMN:', newmembernumber+1, 'User:', member)

        if entradasdeuserstempo[1]:
            
            lastuserjoin = entradasdeuserstempo[1]
            lastlastuserjoin = entradasdeuserstempo[0]

            #print('lastuserjoin:', lastuserjoin, 'datetime:', datetime.datetime.now())
            #print('entre users:', datetime.datetime.now() - lastuserjoin)
            if lastuserjoin - lastlastuserjoin <= datetime.timedelta(minutes=4.5):
                #print('assigning roles')
                cargo2pontos = discordget(member.guild.roles, name="..")
                await member.add_roles(cargo2pontos)
                try:
                    lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                except:
                    pass
                try:
                    oldmember = entradasmembros[0]
                    try:
                        await oldmember.add_roles(cargo2pontos)
                    except:
                        oldmember = member
                        await reg_tp.send(f'Membro que tinha entrado antes em pouco tempo não está mais no servidor.')


                    lista = []; [lista.append(role.name.replace('@everyone', f'{oldmember.name}')) for role in oldmember.roles]; userroles.update({oldmember.id: lista}); savelista(userroles, 'userroles')
                    await reg_tp.send(content='❗\t[{}]\tCargo watchdog adicionado ao {.mention} e {.mention}, entraram em menos de {} minutos'.format(currenttime(),oldmember, member, round(datetime.timedelta.total_seconds(lastuserjoin - lastlastuserjoin)/60, 2)))
                    

                    #controle de raid, adc cargo intolerância quando muita gente entra muito rápido.
                    global raidcontrol

                    if not raidcontrol:
                        raidcontrol = {}
                        raidcontrol.update({datetime.datetime.now():[oldmember, member]})
                        #print('atualizado lista')
                        #print(raidcontrol)
                    else:
                        time=next(iter(raidcontrol.keys()))
                        if datetime.datetime.now() - time > datetime.timedelta(minutes=1.5):
                            raidcontrol = False
                            return

                        global ademir, cargocaveira
                        for x in raidcontrol.values():
                            for raideiros in x+[member]:
                                if '💀' not in str(raideiros.roles):
                                    try:
                                        await raideiros.add_roles(cargocaveira)
                                        lista = []; [lista.append(role.name.replace('@everyone', f'{raideiros.name}')) for role in raideiros.roles]; userroles.update({raideiros.id: lista}); savelista(userroles, 'userroles')
                                        await reg_tp.send(f'❌\t**RAID ALERT**\t❌\t\t❌\t**RAID ALERT**\t❌\t\t❌\t**RAID ALERT**\t❌\t\t❌\t**RAID ALERT**\t❌\t\t\nIntolerância ao user {raideiros.mention} pois entraram muitos ao mesmo tempo.\n\n{ademir.mention}')
                                    except:
                                        reg_tp.send(f'Membro que tinha entrado antes em pouco tempo não está mais no servidor.')
                    #print(raidcontrol)



                except:
                    print(f"Tem algo de errado na atribuição de cargo ao oldmember\n{traceback.format_exc()}")
                
    except Exception as error:
        global natasmember
        if newmembernumber != 0:
            await natasmember.send(f"[{currenttime()}]\t{natasmember.mention}\nException at newmembernumber. \n`{traceback.format_exc()}`\nTime to reset.")
            





@client.event
async def on_member_remove(member):                                     #quando alguém sai do grupo
    global reg_tp
    
    if  [i for i in ['🤡', 'Grupo de Estudos', 'Clube do Livro', 'Muted', '..', '💀', 'Sul', 'Nordeste', 'Norte', 'Centro-oeste', 'Sudeste' ] if i in str(member.roles)] != []:
    #[item for item in bigList if item == someStuff]
        lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista})
        if savelista(userroles, 'userroles'):
            await reg_tp.send(f'<:tpthink:522461647588294679>\t[{currenttime()}]\t{member.mention} {member} saiu do servidor e seus cargos `{str(member.roles)}` foram salvos.')

    else:
        await reg_tp.send(f'<:tptaotane:531859246292402186>\t[{currenttime()}]\t{member.mention} {member} saiu do servidor. Cargos não salvos pois não eram importantes.')






@client.event                                          
async def on_raw_reaction_add(event):                                   #add a role Clube do Livro/Grupode Estudos
    

    if event.member.bot:
        return


    member = event.member                               #aqui não precisa procurar dentro da guild pra pegar o objeto membro
    livro = discordget(member.guild.roles, name="Clube do Livro")
    estudos = discordget(member.guild.roles, name="Grupo de Estudos")
    reg_tp = member.guild.get_channel(registro)

    if event.message_id == clube_id:                    #verifica se a msg é a certa
        if str(event.emoji) == '\U0001F4DA':            #isso aqui é pra somente se o emoji for os livros
            await discord.Member.add_roles(member, livro) #add role
            lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
            await reg_tp.send(content='✅\t[{}]\tAdicionado e salvo cargo {.mention} ao {.mention}.'.format(currenttime(), livro, member), allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
    if event.message_id == grupo_id:
        if str(event.emoji) == '\U0001F4DA':
            await discord.Member.add_roles(member, estudos)
            lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
            await reg_tp.send(content='✅\t[{}]\tAdicionado e salvo cargo {.mention} ao {.mention}.'.format(currenttime(), estudos, member), allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))


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
                lista = []; [lista.append(role.name.replace('@everyone', f'{member.name}')) for role in member.roles]; userroles.update({member.id: lista}); savelista(userroles, 'userroles')
                await reg.send(f'✅\t[{currenttime()}]\tAdicionado e salvo role \"{discordget(guildroles, name=item).mention}\" ao usuário {member.mention}', allowed_mentions=discord.AllowedMentions(users=False, roles=False))
                return
                





@client.event
async def on_raw_message_delete(event):                                 #pra recuperar mensagens que foram apagadas

    try:
        if event.cached_message.author.bot or "Direct Message" in str(event.cached_message.channel): return
    except:
        print('Mensagem apagada porém não estava no cache.'); return
    
    canal = await client.fetch_channel(event.channel_id)
    reg_tp = await client.fetch_channel(registro)
    global mirrorchannel, bate_papo_ids

    def findout():
        if not event.cached_message.content:
            return ' '
        else:
            return f' \n```\n{event.cached_message.content}\n```'

    def isbatepapo():
        if event.cached_message.channel.name == 'bate-papo':
            return f'\nLink em: {mirrorchannel.mention}: <https://discordapp.com/channels/439263663837151242/701184727796940910/{bate_papo_ids[event.cached_message.id]}>.'
        else:
            return ''


    if not event.cached_message.attachments:
        await reg_tp.send(f'🛑\t[{currenttime()}]\tUma mensagem de {event.cached_message.author.mention} foi apagada no canal {canal.mention}{isbatepapo()}{findout()}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
    else:
        await reg_tp.send(f'🛑\t[{currenttime()}]\tUma mensagem de {event.cached_message.author.mention} foi apagada no canal {canal.mention}{isbatepapo()}{findout()}Havia um attachment, segue abaixo:', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))

    if event.message_id in attachmentsApagados:
        files = discord.File(f"/home/natas/bot/attachments/{cleanFileDirectory(attachmentsApagados[event.message_id].nomearquivo)}")
        chn = await client.fetch_channel(registro)
        await chn.send(file=files)

    """    global bate_papo_ids
    try:
        await reg_tp.send(f'found corresponding message in https://discordapp.com/channels/439263663837151242/701184727796940910/{bate_papo_ids[event.cached_message.id]}')
    except:
        print('error')"""






@client.event
async def on_message_edit(b, a):                                        #keep track of edited messages

    if a.content == b.content or a.author.bot: return
    global mirrorchannel, bate_papo_ids
    
    def isbatepapo():
        if a.channel.name == 'bate-papo':
            return f'\nLink do original em: {mirrorchannel.mention}: <https://discordapp.com/channels/439263663837151242/701184727796940910/{bate_papo_ids[a.id]}>.'
        else:
            return ''

    try:
        await reg_tp.send(content=f'✏️\t[{currenttime()}]\tUma mensagem de {a.author.mention} foi editada no canal {a.channel.mention}.\nLink: <https://discordapp.com/channels/{a.guild.id}/{a.channel.id}/{a.id}>{isbatepapo()}', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
        await reg_tp.send(content=f'\nantes\n```\n{b.content}\n```', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
        await reg_tp.send(content=f'depois\n```\n{a.content}\n```', allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False))
    except Exception as e:
        print(f"some error. on_message_edit {e}")






@client.event
async def on_member_update(userbefore, userafter):
    global userroles, reg_tp
    if userbefore.roles != userafter.roles and [i for i in ['Grupo de Estudos', 'Clube do Livro', 'Muted', '..', '💀', 'Sul', 'Nordeste', 'Norte', 'Centro-oeste', 'Sudeste'] if i in str(userafter.roles)]:
        lista = []; [lista.append(role.name.replace('@everyone', f'{userafter.name}')) for role in userafter.roles]; userroles.update({userafter.id: lista}); savelista(userroles, 'userroles')
        await reg_tp.send(f'⚙️\t[{currenttime()}]\tFoi alterado os cargos de {userafter.mention}. Mudanças foram salvas no userroles.', allowed_mentions=discord.AllowedMentions(users=False))






@client.event
async def on_command_error(ctx, error):
    global reg_tp, natasmember
    if 'tempmute' in ctx.invoked_with:
        await ctx.message.channel.send(f'{ctx.message.author.mention}, uso:\n$tempmute @user número[**m**inutos/**h**oras/**d**ias] motivo', delete_after=10)
    elif 'pomodoro' in ctx.invoked_with:
        await ctx.message.channel.send(f'{ctx.message.author.mention}, uso:\n`$pomodoro (iniciar/parar) (minutosDeEstudo) (minutosDePausa)`\nEx: $pomodoro iniciar 25m 5m', delete_after=10); print(f'{error}')
    elif 'tempwarn' in ctx.invoked_with:
        await ctx.message.channel.send(f'{ctx.message.author.mention}, uso:\n$tempwarn @user número[**m**inutos/**h**oras/**d**ias] motivo', delete_after=10)
    else:
        await reg_tp.send(f'erro! {natasmember.mention}\n{error}\n{ctx.invoked_with}\n{traceback.format_exc()}')






@client.event
async def on_voice_state_update(member, before, after):
    global membrosQuePrecisaDesmutar, canalDePomodoro
        
    #ADICIONAR NA LISTA CASO SAIR
    if canalDePomodoro == before.channel and after.channel == None and member.id not in membrosQuePrecisaDesmutar and before.mute or canalDePomodoro == before.channel and after.channel != canalDePomodoro and member.id not in membrosQuePrecisaDesmutar and before.mute:
        print(f'adicionado {member} na lista pois saiu do canal de pomodoro'); membrosQuePrecisaDesmutar.append(member.id); savelista(membrosQuePrecisaDesmutar, 'membrosQuePrecisaDesmutar')
    
    #REMOVER O MUTE QUANDO ESTIVER NA LISTA E FOR ENTRAR EM OUTRA CALL
    if after.channel != None and member.id in membrosQuePrecisaDesmutar and member.voice.mute and not member.guild.me.id in map(lambda member: member.id, after.channel.members):
        await member.edit(mute=False); print(f'membro {member} desmutado pois saiu da call de pomodoro e entrou em outra.'); membrosQuePrecisaDesmutar.remove(member.id); savelista(membrosQuePrecisaDesmutar, 'membrosQuePrecisaDesmutar'); return






""" @client.command()
async def join(ctx):                                                    #comando de música que é mt complicado implementar
    if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    with ctx.message.channel.typing():
        if ctx.channel.name != 'bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, use este comando no chat de bots!')
        
        global voicechannel
        channel = ctx.message.author.voice.channel
        voicechannel = await channel.connect(reconnect=True)
        await ctx.send(f'Conectado ao canal {voicechannel.name}!') """


""" @client.command()
async def leave(ctx):                                                   #comando de música que é mt complicado implementar
    if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    with ctx.message.channel.typing():
        global voicechannel
        await voicechannel.disconnect(force=True)
        await ctx.send(f'{ctx.message.author.mention}, desconectado do canal {voicechannel.name}!')
 """

""" @client.command()
async def play(ctx, url: str):                                          #comando de música que é mt complicado implementar
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
        print('playing') """



@client.command()
async def digitando(ctx, second: int):                                  #pra zuar
    if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    if not "Administrador" in str(ctx.message.author.roles): return
    with ctx.channel.typing():
        if second > 99: return
        await waiting(second, ctx, ctx.message.content[12+len(str(second)):])


@client.command()
async def grupodeestudos(ctx):                                          #chamar galera do grupo de estudos
    
    global limiter1dia
    author = ctx.message.author;message=ctx.message;channel = ctx.message.channel;channelsend = message.channel.send
    

    if author.id in limiter1dia:
        await ctx.message.channel.send(f'{author.mention}, aguarde para usar este comando novamente!'); return
    limiter1dia.update({author.id: datetime.datetime.now()})


    if '..' in str(author.roles) or datetime.datetime.now() - author.joined_at < datetime.timedelta(days=7) or 'Grupo de Estudos' not in str(author.roles): 
        await ctx.channel.send(f'{ctx.message.author.mention}, você não tem permissão para usar este comando!')
        return

    else:
        msg = await channelsend(f'{author.mention}, você deseja mencionar o grupo de estudos?', delete_after=10)
        await msg.add_reaction('\U0001F44D')
        await msg.add_reaction('\U0001F44E')
        
        def check(reaction, user):
            if str(reaction.emoji) != '👍':
                return
            return user == author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('Você demorou muito para responder, operação cancelada!', delete_after=3)
        else:
            await ctx.message.channel.send(f'{discordget(ctx.message.guild.roles, name="Grupo de Estudos").mention}, {author.mention} mencionou vocês para estudar!'); 


@client.command()
async def dice(ctx):                                                    #comando pra jogar dados no rpg
    
    message = ctx.message
    channelsend = message.channel.send
    author = message.author

    if message.channel.name not in ['bots', 'rpg-chat']: await channelsend(f'{author.mention}, utilize o comando no bots ou rpg!', delete_after=10)

    #RPG stuff
    if True:

        global lasttimedonecommand

        with message.channel.typing():
            if not 'd' in message.content[6:]: await channelsend(f'{author.mention}, por favor use no formato **X**d**Y**, onde X é o número de dados, e Y é o número de lados de cada dado.'); return
            if message.content[6:].count('d') > 1: await channelsend(f'{author.mention}, por favor use meu comando corretamente.'); return
            numeroDeDados, lados = message.content[6:].split('d')
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
async def uptime(ctx):                                                  #saber quanto tempo o bot tá rodando
    #if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    await ctx.message.channel.send(f'`Bot uptime is {datetime.datetime.now() - started}`')


@client.command()
async def ping(ctx):                                                    #ping simples
    #if ctx.message.channel.name !='bots': await ctx.message.channel.send(f'{ctx.message.author.mention}, utilize o canal de bots por favor!', delete_after=10); return
    await ctx.message.channel.send(f'Ping: {round(client.latency*1000)}ms')


@client.command(aliases=['ajuda'])
async def help(ctx):                                                    #comando help
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
async def mostrarboasvindas(ctx):                                       #comando pra exibir boas vindas. somente para demonstração
    await ctx.message.channel.send(embed=getboasvindasembed(ctx.message.author))
    

@client.command()
async def mensagemDM(ctx):                                              #administradores podem usar o bot para enviar mensagens privadas para usuários
    if 'Administrador' not in str(ctx.message.author.roles) and ctx.author.id != natasid: await ctx.message.channel.send(f'{ctx.message.author.mention}, este comando só pode ser usado por administradores!'); return
    if not ctx.message.mentions: await ctx.message.channel.send(f'{ctx.message.author.mention}, você precisa mencionar alguém para enviar a mensagem!'); return
    await ctx.message.mentions[0].send(ctx.message.content[34:])
    await ctx.channel.send(f"{ctx.author.mention}, mensagem `{ctx.message.content[34:]}` enviada!", delete_after=15)
    await ctx.message.delete()


@client.command()
async def github(ctx):                                                  #comando pra mandar de volta o link do github do bot
    await ctx.message.channel.send(f"{ctx.message.author.mention}, aqui está o repositório:\n <https://github.com/NatasFX/TheProjectBot>")


@client.command()
async def sugerirfilme(ctx):                                            #comandos de filme

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
                    savelista(listasugestãofilme, 'listasugestãofilme')     #salva a lista no txt
                    await channelsend(f'{author.mention}, sua sugestão foi enviada, muito obrigado! {str(gettplove(message))}')
                    await channelsend(f'Você tem mais {3-len(eventofilmelista[message.author.id])} sugestões de filme')
                    savelista(eventofilmelista,'eventofilmelista')          #mostra quantas sugestões de filme ainda podem ser feitas
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
async def versugestão(ctx):                                             #comandos de filme

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
        await channelsend(f'{author.mention}, use este comando no chat de bots!', delete_after=10)


@client.command(aliases=['apagarsugestões'])
async def apagarsugestão(ctx):                                          #comandos de filme

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


@client.command(aliases=['userroles'])                                  #comando desnecessário aoshdaos
async def _userroles(ctx):                                         
    if 'Administrador' not in ctx.message.author.roles and ctx.author.id != natasid: return
    
    
    message = ctx.message
    author = message.author
    channelsend = message.channel.send
    global userroles
    
    
    await channelsend(f'```\n{str([role[0] for role in userroles.values()])[:1980]}\n```')
    await channelsend(f'```\n{str([role[0] for role in userroles.values()])[1980:]}\n```')
    #print(direct_messages)


@client.command(aliases=['mutar', 'mute'])
async def tempmute(ctx, muteMember: discord.Member, tempo: str, *motivo):#muta algm temporariamente

    try:
        message = ctx.message
        author = message.author
        channelsend = message.channel.send
        #muteMember = message.mentions[0] muito bom poder setar os bgl junto do ctx.
        global mutedrole, reg_tp, mutadosMembers, ademir, moderador, supervisor
            
        if not [cargo for cargo in [ademir, moderador, supervisor] if cargo in author.roles] and not author.id == natasid:
            await channelsend(f'{author.mention}, você não tem permissão para usar este comando!'); return 

        if muteMember =='': await channelsend(f'{author.mention}, especifique um usuário!', delete_after=5); await message.delete(); return
        
        try:
            if 'd' in tempo.lower():
                tempoDeMute = datetime.timedelta(days=int(tempo.replace('d', '')))
            elif 'h' in tempo.lower():
                tempoDeMute = datetime.timedelta(hours=int(tempo.replace('h', '')))
            elif 'm' in tempo.lower():
                tempoDeMute = datetime.timedelta(minutes=int(tempo.replace('m', '')))
            else:
                await channelsend(f'{author.mention}, tempo não especificado corretamente! máximo: 99d, mínimo: 1m', delete_after=30); await message.delete(); return
        except:
            await channelsend(f'{author.mention}, tempo não especificado corretamente! máximo: 99d, mínimo: 1m', delete_after=30); await message.delete(); return
            
        if tempoDeMute < datetime.timedelta(seconds=1):
            await channelsend(f'{author.mention}, tempo não especificado corretamente! máximo: 99d, mínimo: 1m', delete_after=30); await message.delete(); return


        if mutedrole not in muteMember.roles:
            await muteMember.add_roles(mutedrole); 
            lista = []; [lista.append(role.name.replace('@everyone', f'{muteMember.name}')) for role in muteMember.roles]; userroles.update({muteMember.id: lista}); savelista(userroles, 'userroles')
            #await channelsend(f'{author.mention}, usuário {muteMember.mention} mutado até {(datetime.datetime.now()+tempoDeMute).strftime("%d/%m/%Y às %T")}.\n.')
            
            embed = discord.Embed(
                title = f'🤫 {author.name}, usuário {muteMember} mutado!',
                description = f'⠀⠀\nMotivo: \n**{" ".join(motivo)}**\n\n{author.mention} {muteMember.mention}',
                colour = discord.Color.red()
                )
            embed.set_footer(text=f'Mutado até {(datetime.datetime.now()+tempoDeMute).strftime("%d/%m/%Y às %T")}')

            await channelsend(embed = embed)
            await reg_tp.send(f"🤫\t[{currenttime()}]\t{muteMember.mention} foi mutado por \"{tempo}\". motivo: \"`{' '.join(motivo)}`\"", allowed_mentions=discord.AllowedMentions(users=False))

            mutadosMembers.update({muteMember.id:datetime.datetime.now()+tempoDeMute}); savelista(mutadosMembers, 'mutadosMembers')
            print(f'[{currenttime()}] a pedido de {author}, usuario {muteMember} mutado por {tempoDeMute}'); await message.delete()
        else:
            await channelsend(f'{author.mention}, usuário {muteMember.mention} já está mutado.', delete_after=5); await message.delete(); return

    except:
        await channelsend(f'{author.mention}, uso:\n`$tempmute @user número[h/d/m] motivo`', delete_after=15); await message.delete()
        await reg_tp.send(f'{natasmember.mention}\nExceção ocorreu no tempmute. \n{traceback.format_exc()}')


@client.command(aliases=['desmutar', 'desmute'])
async def unmute(ctx, user: discord.Member=''):                         #desmutar alguém né

    global mutedrole, reg_tp, mutadosMembers, ademir, moderador, supervisor
    channelsend = ctx.message.channel.send
    author = ctx.message.author


    if not [cargo for cargo in [ademir, moderador, supervisor] if cargo in author.roles] and not author.id == natasid:
        await channelsend(f'{author.mention}, você não tem permissão para usar este comando!'); return 


    if user == '': await channelsend(f'{author.mention}, especifique um usuário!', delete_after=5); return


    if mutedrole in user.roles:
        await user.remove_roles(mutedrole)
        await reg_tp.send(f'🤐\t[{currenttime()}]\tUsuário {user.mention} desmutado por ordem direta de {author.mention}.', allowed_mentions=discord.AllowedMentions(users=False))
        await channelsend(f'{author.mention}, usuário {user.mention} desmutado!', allowed_mentions=discord.AllowedMentions(users=False))
        del mutadosMembers[user.id]; savelista(mutadosMembers, 'mutadosMembers'); await ctx.message.delete()
    else:
        await channelsend(f'{author.mention}, usuário {user.mention} não está mutado!', delete_after=5); await ctx.message.delete()
        if user.id in mutadosMembers:
            del mutadosMembers[user.id]; savelista(mutadosMembers, 'mutadosMembers')


@client.command()
async def clubedolivro(ctx):                                            #chamar galera do grupo de estudos

    author = ctx.message.author;message=ctx.message;channel = ctx.message.channel;channelsend = message.channel.send
    

    if author.id != tomzinhoID: await channelsend(f'{author.mention}, você não pode usar este comando!', delete_after=5)


    if '..' in str(author.roles) or datetime.datetime.now() - author.joined_at < datetime.timedelta(days=7) or 'Clube do Livro' not in str(author.roles): 
        await ctx.channel.send(f'{ctx.message.author.mention}, você não tem permissão para usar este comando!')
        return

    else:
        await message.delete()
        msg = await channelsend(f'{author.mention}, você deseja mencionar o Clube do Livro?', delete_after=10)
        await msg.add_reaction('\U0001F44D')
        await msg.add_reaction('\U0001F44E')
        
        def check(reaction, user):
            if str(reaction.emoji) != '👍':
                return
            return user == author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('Você demorou muito para responder, operação cancelada!', delete_after=3)
        else:
            await ctx.message.channel.send(f'<@&643190625029586979>.', allowed_mentions=discord.AllowedMentions(roles=True)); await msg.delete()


@client.command()
async def pomodoro(ctx, comando: str, *args1):                          #comando pomodoro lindo

    message = ctx.message
    author = message.author
    channelsend = message.channel.send
    global voicechannel, reg_tp, interromperLoop, pomodoroID, canalDePomodoro, pomodoroMemberCommand
    #definido coisas padrão


    if comando.lower() in ['iniciar', 'começar']:
        if client.voice_clients != []: await channelsend("Já estou em pomodoro!", delete_after=5); return       #detectar se já está em voicechannel

        if not 'm' in str(args1):                                                                               #se o user não tiver usado o 'm'
            await channelsend(f'uso: $pomodoro (iniciar/parar) (minutosDeEstudo) (minutosDePausa)`\nEx: $pomodoro iniciar 25m 5m', delete_after=5); return

        args = ['', '']                                                                                         #criando placeholders para o args1 filrado

        args[0] = args1[0][:-1]
        args[1] = args1[1][:-1]                                                                                 #adicionado args filtrados

        msg = await channelsend(embed=discord.Embed(
            title = f'**{author.name}, deseja iniciar o pomodoro com as seguintes configurações?**',
            description = f'**Tempo de estudo**: {args[0]} minutos\n**Tempo de Descanso**: {args[1]} minutos',
            colour = discord.Color.purple()
            ),
            delete_after=10
        )                                                                                                       #envia o embed
        await msg.add_reaction('\U0001F44D')                                                                    #adiciona o polegar
        
        def check(reaction, user):                                                                              #check para verificar se os statements ali são true
            if str(reaction.emoji) != '👍':
                return
            return user == author and str(reaction.emoji) == '👍' and msg.id == reaction.message.id

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=10, check=check)                     #detecção padrão
        except asyncio.TimeoutError:
            await channelsend('Você demorou muito para responder, operação cancelada!', delete_after=2.5); return
        else:                                                                                                   #se não der erro, bora, usuário aceitou o pomodoro
            await channelsend(f'{author.mention}, iniciando em 30s sessão de pomodoro!')

        
        try:
            if author.voice == None: await channelsend(f'{author.mention}, você não está conectado em um voice chat!'); return
            channel = author.voice.channel                                                                      #pega o channel q o user está conectado
            if channel.name in ['Músicas', 'Duo', 'Bate Papo']: await channelsend(f'{author.mention}, escolha outro chat para iniciar o pomodoro!'); return
            voicechannel = await channel.connect(reconnect=True)                                                #conecta nele
        except:
            await voicechannel.disconnect()                                                                     #connect() dá erro quando o bot já está conectado.
            voicechannel = await channel.connect(reconnect=True)                                                #quando isso acontece, a gente desconecta e conecta novamente
            

        pomodoroID +=1                                                                                          #aqui atualizamos o id do pomodoro mais recente.
        currentID = pomodoroID; print(f'started new pomodoro. ID: {currentID}'); canalDePomodoro = channel      

        """ Dentro do loop a seguir existe uma variável que fica com valor fixo.
        o loop consegue interagir com outras variáveis que são globais, então o loop
        verifica se ainda é o mais recente toda vez que irá fazer algo. """

        
        if pomodoroMemberCommand == '':                                                                         #define a variável que representa o user que pode desligar o pomodoro
            pomodoroMemberCommand == author.id
  


        #LOOP DO POMODORO
        while True:
            try:                                                                                                #usei um try mas não era estritamente necessário
                voice = discordget(client.voice_clients, guild=ctx.guild)                                       
                await asyncio.sleep(1)
                if pomodoroID != currentID: print(f'pomodoroID {currentID} finalizado.'); break                             #PARA NÃO BUGAR
                
                gtts(text=f'Iniciando pomodóro em 30 segundos.', lang='pt-BR').save('iniciando1.mp3')                       #google text to speech cria o áudio para nós
                os.system('ffmpeg -i \"iniciando1.mp3\" -acodec copy \"iniciando.mp3\" -y -hide_banner -loglevel panic'); await asyncio.sleep(1)#corrigimos o bug que o ffmpeg não consegue determinar corretamente a duração do áudio aqui
                voicechannel.play(discord.FFmpegPCMAudio("iniciando.mp3"), after=None); voicechannel.source = discord.PCMVolumeTransformer(voice.source); voicechannel.source.volume = 1
                #^tocamos o audio e setamos o volume no máximo pois o gtts cria audios médios                
                
                #INICIANDO POMODORO EM 30 SEGUNDOS
                await asyncio.sleep(30)

                #teremos muitas linhas dessas duas aq repetidas. são elas que tem o poder de parar o loop quando detectar alguma das condições como true
                if client.voice_clients == [] or interromperLoop or len(channel.members) <= 1: await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=None); await voicechannel.disconnect(); await channel.edit(name=f'{channel.name[:-14]}') if channel.name.find('[') != -1 else ''; break
                if pomodoroID != currentID: print(f'pomodoroID {currentID} finalizado.'); break                           #PARA NÃO BUGAR

                #INICIANDO POMODORO
                gtts(text=f'Iniciando pomodóro de {args[0]} minutos.', lang='pt-BR').save('iniciou1.mp3')
                os.system('ffmpeg -i \"iniciou1.mp3\" -acodec copy \"iniciou.mp3\" -y -hide_banner -loglevel panic'); await asyncio.sleep(1)
                voicechannel.play(discord.FFmpegPCMAudio("iniciou.mp3"), after=None)
                
                for member in channel.members:
                    if not member.bot:
                        await member.edit(mute=True)                        #MUTANDO TODOS

                if client.voice_clients == [] or interromperLoop or len(channel.members) <= 1: await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=None); await voicechannel.disconnect(); await channel.edit(name=f'{channel.name[:-14]}') if channel.name.find('[') != -1 else ''; break
                if pomodoroID != currentID: print(f'pomodoroID {currentID} finalizado.'); break                           #PARA NÃO BUGAR

                #COLOCANDO REGRA NO EVERYONE DO CANAL PRA NGM FALAR
                await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=False, connect=False)
                await channel.edit(name=f'{channel.name} [EM POMODORO]')    #ALTERANDO NOME DO CANAL

                await asyncio.sleep(int(args[0])*30)                        #ESPERANDO METADE DO TEMPO ESPECIFICADO


                if client.voice_clients == [] or interromperLoop or len(channel.members) <= 1: await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=None); await voicechannel.disconnect(); await channel.edit(name=f'{channel.name[:-14]}') if channel.name.find('[') != -1 else ''; break
                if pomodoroID != currentID: print(f'pomodoroID {currentID} finalizado.'); break                           #PARA NÃO BUGAR

                await asyncio.sleep(int(args[0])*30-15)                     #ESPERANDO A OUTRA METADE

                if client.voice_clients == [] or interromperLoop or len(channel.members) <= 1: await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=None); await voicechannel.disconnect(); await channel.edit(name=f'{channel.name[:-14]}') if channel.name.find('[') != -1 else ''; break
                if pomodoroID != currentID: print(f'pomodoroID {currentID} finalizado.'); break                           #PARA NÃO BUGAR
                
                gtts(text=f'Ei, terminando pomodóro em 15 segundos.', lang='pt-BR').save('terminando1.mp3')
                os.system('ffmpeg -i \"terminando1.mp3\" -acodec copy \"terminando.mp3\" -y -hide_banner -loglevel panic'); await asyncio.sleep(1)
                voicechannel.play(discord.FFmpegPCMAudio("terminando.mp3"), after=None)
                #TERMINANDO EM 30SG

                await asyncio.sleep(30)
                if client.voice_clients == [] or interromperLoop or len(channel.members) <= 1: await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=None); await voicechannel.disconnect(); await channel.edit(name=f'{channel.name[:-14]}') if channel.name.find('[') != -1 else ''; break
                if pomodoroID != currentID: print(f'pomodoroID {currentID} finalizado.'); break                           #PARA NÃO BUGAR

                gtts(text=f'Fim do pomodóro. Descanso de {args[1]} minutos.', lang='pt-BR').save('descanso1.mp3')
                os.system('ffmpeg -i \"descanso1.mp3\" -acodec copy \"descanso.mp3\" -y -hide_banner -loglevel panic'); await asyncio.sleep(1)
                voicechannel.play(discord.FFmpegPCMAudio("descanso.mp3"), after=None)

                if client.voice_clients == [] or interromperLoop or len(channel.members) <= 1: await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=None); await voicechannel.disconnect(); await channel.edit(name=f'{channel.name[:-14]}') if channel.name.find('[') != -1 else ''; break
                if pomodoroID != currentID: print(f'pomodoroID {currentID} finalizado.'); break                           #PARA NÃO BUGAR

                #DESCANSO
                await channel.edit(name=f'{channel.name[:-14]}')            #RETIRANDO NOME 

                for member in channel.members:
                    if not member.bot:
                        await member.edit(mute=False)                       #COLOCANDO PERMISSÕES PARA FALAR
                await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=None, connect=None)

                await channelsend(f'{author.mention} fim do pomodoro! descansando por {args[1]} minuto(s)!')
                await asyncio.sleep(int(args[1])*60)                        #ESPERANDO TEMPO ESPECIFICADO DE DESCANSO
                
                if client.voice_clients == [] or interromperLoop or len(channel.members) <= 1: await voicechannel.disconnect(); return
                if pomodoroID != currentID: print(f'pomodoroID {currentID} finalizado.'); break                           #PARA NÃO BUGAR
            except:
                print(f'erro no pomodoro: \n{traceback.format_exc()}')
                break
    elif comando.lower() == "parar":                                            #comando pra parar um pomodoro em execução


        if client.voice_clients == []: await channelsend('Não estou em pomodoro!', delete_after=10); return #se não estiver em pomodoro, n fazer nada
        if pomodoroMemberCommand != author.id and author.id != natasid: pomodoroMemberCommand = ''; await channelsend(f'Somente quem iniciou o pomodoro pode pará-lo!'); return
        interromperLoop = True
        channel = author.voice.channel
        await discord.VoiceChannel.set_permissions(channel, discordget(message.guild.roles, name="@everyone"), speak=None)

        for mutado in channel.members:
            try:
                if mutado.bot: return
                await mutado.edit(mute=False)
                print(f'encerrado {mutado} desmutado')
            except:
                print(f'não foi possível desmutar {mutado} pois não está conectado em voicechannel.')
        
        await channel.edit(name=f'{channel.name[:-14]}') if channel.name.find('[') != -1 else ''
        
        try:
            await voicechannel.disconnect()
        except:
            pass

        await channelsend(f'{author.mention}, encerrou o pomodoro!')
    else:
        await channelsend(f'{author.mention}, uso:\n`$pomodoro (iniciar/parar) (minutosDeEstudo) (minutosDePausa)`\nEx: $pomodoro iniciar 25m 5m')


@client.command(aliases=['warn'])
async def tempwarn(ctx, warnMember: discord.Member, tempo: str, *motivo):#muta algm temporariamente

    try:
        message = ctx.message
        author = message.author
        channelsend = message.channel.send

        global warnRole, reg_tp, warnedMembers, ademir, moderador, supervisor, natasid
            
        if not [cargo for cargo in [ademir, moderador, supervisor] if cargo in author.roles] and not author.id == natasid:
            await channelsend(f'{author.mention}, você não tem permissão para usar este comando!'); return 

        if warnMember =='': await channelsend(f'{author.mention}, especifique um usuário!', delete_after=5); await message.delete(); return
        
        try:
            if 'd' in tempo.lower():
                tempoDeMute = datetime.timedelta(days=int(tempo.replace('d', '')))
            elif 'h' in tempo.lower():
                tempoDeMute = datetime.timedelta(hours=int(tempo.replace('h', '')))
            elif 'm' in tempo.lower():
                tempoDeMute = datetime.timedelta(minutes=int(tempo.replace('m', '')))
            else:
                await channelsend(f'{author.mention}, tempo não especificado corretamente! máximo: 99d, mínimo: 1m', delete_after=30); await message.delete(); return
        except:
            await channelsend(f'{author.mention}, tempo não especificado corretamente! máximo: 99d, mínimo: 1m', delete_after=30); await message.delete(); return
            
        if tempoDeMute < datetime.timedelta(seconds=1):
            await channelsend(f'{author.mention}, tempo não especificado corretamente! máximo: 99d, mínimo: 1m', delete_after=30); await message.delete(); return


        if warnRole not in warnMember.roles:
            await warnMember.add_roles(warnRole)
            lista = []; [lista.append(role.name.replace('@everyone', f'{warnMember.name}')) for role in warnMember.roles]; userroles.update({warnMember.id: lista}); savelista(userroles, 'userroles')
            #await channelsend(f'{author.mention}, usuário {warnMember.mention} mutado até {(datetime.datetime.now()+tempoDeMute).strftime("%d/%m/%Y às %T")}.\n.')
            
            embed = discord.Embed(
                title = f'🤫 {author.name}, usuário {warnMember} foi avisado!',
                description = f'⠀⠀\nMotivo: \n**{" ".join(motivo)}**\n\n{author.mention} {warnMember.mention}',
                colour = discord.Color.red()
                )
            embed.set_footer(text=f'Usuário restrito até {(datetime.datetime.now()+tempoDeMute).strftime("%d/%m/%Y às %T")}')

            await channelsend(embed = embed)
            await reg_tp.send(f"🤫\t[{currenttime()}]\t{warnMember.mention} foi avisado por \"{tempo}\". motivo: \"`{' '.join(motivo)}`\"", allowed_mentions=discord.AllowedMentions(users=False))

            warnedMembers.update({warnMember.id:datetime.datetime.now()+tempoDeMute}); savelista(warnedMembers, 'warnedMembers')
            print(f'[{currenttime()}] a pedido de {author}, usuario {warnMember} avisado por {tempoDeMute}'); await message.delete()
        else:
            await channelsend(f'{author.mention}, usuário {warnMember.mention} já está avisado.', delete_after=5); await message.delete(); return

    except:
        await channelsend(f'{author.mention}, uso:\n`$tempwarn @user número[h/d/m] motivo`', delete_after=15); await message.delete()
        await reg_tp.send(f'{natasmember.mention}\nExceção ocorreu no tempwarn. \n{traceback.format_exc()}')


@client.command(aliases=['unclown'])
async def unwarn(ctx, user: discord.Member=''):                         #desmutar alguém né

    global warnRole, reg_tp, warnedMembers, ademir, moderador, supervisor
    channelsend = ctx.message.channel.send
    author = ctx.message.author


    if not [cargo for cargo in [ademir, moderador, supervisor] if cargo in author.roles] and not author.id == natasid:
        await channelsend(f'{author.mention}, você não tem permissão para usar este comando!'); return 


    if user == '': await channelsend(f'{author.mention}, especifique um usuário!', delete_after=5); return


    if warnRole in user.roles:
        await user.remove_roles(warnRole)
        await reg_tp.send(f'🤐\t[{currenttime()}]\tUsuário {user.mention} removido do aviso por ordem direta de {author.mention}.', allowed_mentions=discord.AllowedMentions(users=False))
        await channelsend(f'{author.mention}, usuário {user.mention} removido do aviso!', allowed_mentions=discord.AllowedMentions(users=False))
        del warnedMembers[user.id]; savelista(warnedMembers, 'warnedMembers'); await ctx.message.delete()
    else:
        await channelsend(f'{author.mention}, usuário {user.mention} não está avisado!', delete_after=5); await ctx.message.delete()
        if user.id in mutadosMembers:
            del warnedMembers[user.id]; savelista(warnedMembers, 'warnedMembers')





client.run(secret.key)
