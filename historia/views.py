import json
import os
import urllib.request
import urllib.error
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings


STATS = [
    {'icone': '💬', 'numero': '28.433', 'label': 'mensagens trocadas'},
    {'icone': '📅', 'numero': '517',    'label': 'dias conversando'},
    {'icone': '✍️ 💛', 'numero': '9.884',  'label': 'textos dela pra você'},
    {'icone': '✍️ 💙', 'numero': '7.840',  'label': 'textos meus pra você'},
    {'icone': '🌅', 'numero': '13h',    'label': 'hora favorita — almoço'},
    {'icone': '👑', 'numero': '775×',   'label': '"mozão" — apelido campeão'},
]

PALAVRAS = [
    
    {'palavra': 'vida',        'count': 2812},
    {'palavra': 'amor',        'count': 2203},
    {'palavra': 'bom',         'count': 1142},
    {'palavra': 'mozão',       'count': 799},
    {'palavra': 'te amo', 'count': 700},
    {'palavra': 'vidão',    'count': 566},
    {'palavra': 'cheguei',     'count': 321},
    {'palavra': 'cuidado',     'count': 303},
    {'palavra': 'saindo',      'count': 219},
    {'palavra': 'sempre',      'count': 153},
    {'palavra': 'delícia',  'count': 169},
    {'palavra': 'saudade',  'count': 149},
    {'palavra': 'umbanda/espiritualidade', 'count': 132},
    {'palavra': 'mor',      'count': 126},
    {'palavra': 'príncipe', 'count': 118},
    
]

FRASES_THIAGO = [
    {'texto': 'Já não consigo imaginar minha vida sem você'},
    {'texto': 'Me sinto o homem mais feliz do mundo por ter te reencontrado e finalmente achar alguém que me completa 💙'},
    {'texto': 'Obrigado por nunca desistir de mim, mesmo eu sendo um cabeça...'},
    {'texto': 'Agradeço todo dia por nossos caminhos terem se cruzado 🥰✨'},
    {'texto': 'Tô vivendo e sentindo coisas que achei que nem eram mais possíveis'},
    {'texto': 'Obrigado por tudo tudo, por ter entrado na minha vida dessa forma tão linda e intensa que só você sabe, você é mais do que Luz na minha vida mozão.'},
    {'texto': 'Ia te fazer uma massagem, ficar grudadinho falando o quanto eu te amo e o quanto eu quero viver com você até o último dia da minha vida.'},
    {'texto': 'Não paro de pensar em você 1 minuto desde quando te reencontrei.'},
    {'texto': 'Que seja de emoção e felicidade, pq é só o que eu tenho de vc, passo o dia todo pensando em vc e quando não to pensando to com vc.'},
    {'texto': 'Não precisa agradecer, eu também, to vivendo e sentindo coisas que achei que nem eram mais possíveis, te amo muito, mas muito mesmo, nunca se esqueça disso, tá?'},
    {'texto': 'Só me fez ver ainda mais o quanto sou apaixonado pela vida e obviamente, o mais importante, loucamente apaixonado por você.'},
    {'texto': 'Eu sou completamente louco por você minha vida, não paro de pensar em você 1 minuto desde quando te reencontrei.'},
    {'texto': 'Seria um sonho, estar na mesma casinha que vc, tudo cheirosinho que a gente fez compra e limpou a casa.'},
    {'texto': 'Parece que não importa o que eu falo você não entende, eu só quero você e apenas você e nada que aconteça vai me fazer mudar a cabeça ou te largar.'},
    {'texto': 'O que eu mais quero é arrumar um emprego logo, juntar dinheiro e morar com você pra chegar todo dia do trabalho e te ver linda e maravilhosa como és. 💕'},
]

FRASES_MEL = [
    {'texto': 'De verdade nunca vivi o que vivo com você!', 'autor': 'Você'},
    {'texto': 'Eu nunca imaginei que estaríamos cogitando morar juntos e construir nossa família 🥹'},
    {'texto': 'Eu te amo tanto rapaz… que já até chorei hoje por isso 💛🥹'},
    {'texto': 'Só você pra animar meus dias — obrigada por cuidar de mim'},
    {'texto': 'Obrigada por tudo que faz por mim e por nós — sempre, sempre 🥹💛'},
    {'texto': 'Me dói imaginar minha vida sem você… depois de você eu nunca mais vou querer amar outro alguém!'},
    {'texto': "O que é meu também será teu mocinho, depois que eu responder 'Sim' toda de branco na cachoeira. 💍"},
    {'texto': 'Eu só quero te fazer feliz todos os dias das nossas vidas, te ver conquistar o mundo todo e ao seu lado construir nossa vida juntos.'},
    {'texto': 'Não vejo a hora de construir a vida contigo amor… tenho tantos tantos tantos planos pro nosso futuro.'},
    {'texto': 'É ruim chegar em casa e não ter seu cheiro, deitar sozinha e saber que não vai ter você aqui pra me dar beijinhos toda hora.'},
    {'texto': 'Eu quero muito, quero muito ser tua mulher e viver esse sonho todo dia!'},
    {'texto': 'Você é o homem dos meus sonhos.'},
    {'texto': 'Falei pra sua sogra que você é perfeito e que tenho sonho de construir família com você.'},
    {'texto': 'Eu esperei tanto tanto tanto mais tanto tempo pela sua chegada meu amor.'},
    {'texto': 'Dois anos sendo muito feliz ao lado do cara maaaaaais amoroso do mundo.'},
]

SONHOS = [
    {
        'icone': '🏠',
        'titulo': 'Casinha com quintal',
        'desc': 'O sonho mais recorrente dele. Em janeiro de 2025, menos de 2 meses de namoro, já dizia: "Seria um sonho estar na mesma casinha que você, tudo cheirosinho, com quintal e plantinhas."',
        'autor': 'Eu'
    },
    {
        'icone': '💍',
        'titulo': 'Casamento na cachoeira',
        'desc': 'Logo em dezembro de 2024 ela deixou escapar: "depois que eu responder Sim, toda de branco na cachoeira." 💍',
        'autor': 'Você'
    },
    {
        'icone': '👨‍👩‍👧',
        'titulo': 'Adotar um casalzinho',
        'desc': 'Voltando da viagem de SC, em janeiro de 2025: "nossa, um filho nosso seria a coisa mais linda do mundo — mas a gente vai adotar um casalzinho." Ela completou que a viagem mexeu com ela na forma de pensar em construir família.',
        'autor': 's dois'
    },
    {
        'icone': '✈️',
        'titulo': 'Viajar juntos sempre',
        'desc': 'A 4ª viagem já está planejada — primeira férias do trabalho dos dois juntos. Ela disse: "a gente merece né vida." Trancoso ou Arraial d\'Ajuda, BA.',
        'autor': 'Os dois'
    },
]

TIMELINE = [

    {
        'data': '10 de novembro de 2024',
        'titulo': 'O começo de tudo ✨',
        'desc': 'O dia do pedido de namoro. Um dos melhores dias da vida dele — planejado com cuidado e sentimento.'
    },
    {
        'data': '08 e 09 de dezembro de 2024',
        'titulo': 'A peça de teatro 🎭',
        'desc': 'Ele foi assistir todas as apresentações dela.'
    },
    {
        'data': '29 de dezembro de 2024',
        'titulo': 'Rumo ao Rio de Janeiro ✈️',
        'desc': 'Partiram juntos para a primeira viagem do casal — o Réveillon no Rio de Janeiro.'
    },
    {
        'data': '31 de dezembro de 2024',
        'titulo': 'Primeira virada juntos 🎆',
        'desc': 'Réveillon no Rio de Janeiro. O primeiro ano novo dos dois juntos, marcado para sempre.'
    },
    {
        'data': '02 de fevereiro de 2025',
        'titulo': 'Primeira vez no terreiro 🕍',
        'desc': 'Ela o levou ao terreiro pela primeira vez. Ele postou: "Será um dia que irei guardar pra sempre na minha memória e no meu coração. Axé!"'
    },
    {
        'data': '10 de fevereiro de 2025',
        'titulo': '3 meses juntos 💛',
        'desc': 'Ela disse: "Vivo um sonho lindo há 3 meses contigo." Ele respondeu: "Fazem 3 meses que voltei a realmente ter amor por mim, pela vida e agora por você."'
    },
    {
        'data': '27 de fevereiro de 2025',
        'titulo': 'Aniversário dela 🎂',
        'desc': 'O aniversário dela. Ele comemorou a semana inteira.'
    },
    {
        'data': '10 de março de 2025',
        'titulo': '4 meses — o dia mais especial 🥹',
        'desc': 'Ele escreveu emocionado sobre o dia do pedido de namoro e o quanto cresceu com o relacionamento. Ela respondeu: "Sempre lembro de você… minha música mais ouvida diariamente."'
    },
    {
        'data': '03 de abril de 2025',
        'titulo': '5 meses — fortes e firmes 💪',
        'desc': 'Ela disse: "Fortes e muito firmes 5 meses." Ele mandou mensagem de madrugada: "Feliz 5 meses, paixão! Provavelmente um dos dias mais felizes da minha vida."'
    },
    {
        'data': '20 de maio de 2025',
        'titulo': 'Oficialmente CLT! 🎉',
        'desc': 'Ele anunciou: "Agora oficialmente empregado sob o regime da CLT." Ela respondeu: "Te amo tanto e tô feliz por você meu amor." Ele: "Obrigado por fazer parte disso."'
    },
    {
        'data': '29 de maio de 2025',
        'titulo': 'Primeiro dia de trabalho 💼',
        'desc': 'Ela foi encontrá-lo no primeiro dia de trabalho. Ele disse: "Tão feliz que te vi hoje, primeiro dia de trabalho perfeito."'
    },
    {
        'data': '10 de novembro de 2025',
        'titulo': '1 ano de namoro 🎊',
        'desc': 'Um ano desde o pedido. O dia passou corrido, mas o amor seguiu firme — como toda segunda-feira dia 10 desde o começo.'
    },
    { 
        'data': '28 de dezembro de 2025', 
        'titulo': 'Santa Catarina 🏡', 
        'desc': 'Segunda viagem juntos — passaram o Réveillon na casa do amigo dela em Santa Catarina. O fim de ano longe de casa, mas do lado certo.'
    },
    {   'data': '23 de novembro de 2025', 
        'titulo': 'Peça da Mel 🎭', 
        'desc': 'Domingo de teatro — mais uma peça dela, incrível por sinal. Estar lá pra ver ela brilhar no palco.'
    },
    {
        'data': '22 de fevereiro de 2026',
        'titulo': 'Aniversário dela no Outback 🥩',
        'desc': 'Ele a levou ao Outback para comemorar. Ela disse: "Eu amei tudo que você fez pra mim Mozão, você tornou tudo especial."'
    },
    {   'data': '27 de fevereiro de 2025', 
        'titulo': 'Peruíbe com os amigos 🏖️', 
        'desc': 'Terceira viagem juntos — Peruíbe com as amigas. Praia, sol e a melhor companhia.'
    },
    {
        'data': 'Junho / Julho de 2026',
        'titulo': 'Nossa 4ª viagem juntos ✈️',
        'desc': 'Primeira viagem de férias do trabalho dos dois. Destino: Trancoso ou Arraial d\'Ajuda, BA. Ela planejou tudo com amor — "a gente merece né vida."'
    },
]

MUSICAS = [
    {'num': '♪', 'destaque': True,  'nome': 'REPRISE',         'artista': 'Boombeat, FBC, Los Brasileros', 'tag': 'Nossa música', 'significado': 'Nossa música. A Boombeat é artista — assim como você. Então quando essa música toca, ela carrega ao mesmo tempo o amor que sinto por você e tudo que você é.'},
    {'num': '2', 'destaque': False, 'nome': 'Chorojo',          'artista': 'Os Tincoãs',                   'tag': '',             'significado': 'Você é filha de Oxum — e muito filha de Oxum. Mãe de santo, da Umbanda, desse universo que você me apresentou. Chorojo carrega essa energia das águas, do acolhimento, do sagrado. Quando ouço, você aparece inteira.'},
    {'num': '3', 'destaque': False, 'nome': 'SALA VERMELHA #3', 'artista': 'Ajuliacosta (Prod. Greezy)',   'tag': '',             'significado': 'Você se declarando pra mim. Pelo menos é assim que eu vejo kkkk'},
    {'num': '4', 'destaque': False, 'nome': 'Te vi de canto',   'artista': 'Ro Rosa, Patricio Sid',        'tag': '',             'significado': 'Tem nossa pegada — levinha, gostosa, do jeito que a gente é junto. Às vezes uma música não precisa de uma grande história pra ser nossa. Ela só encaixa.'},
    {'num': '5', 'destaque': False, 'nome': 'Tiramisu',         'artista': 'MD Chefe',                     'tag': '',             'significado': 'Você sabe o motivo. Eu sei o motivo. Deixa assim.'},
    {'num': '6', 'destaque': False, 'nome': 'Samurai',          'artista': 'Djavan',                       'tag': '',             'significado': 'Djavan escreveu sobre a leveza de amar alguém de verdade — sem drama, sem pressa, só a certeza calma de quem encontrou. Me lembra a gente quando tô do seu lado, deitadinho, sem precisar de nada mais.'},
]

CHART_DATA = [
    {'label': 'Dez/24', 'Eu': 320,  'Você': 290},
    {'label': 'Jan/25', 'Eu': 1050, 'Você': 920},
    {'label': 'Fev/25', 'Eu': 1380, 'Você': 1313},
    {'label': 'Mar/25', 'Eu': 1250, 'Você': 1207},
    {'label': 'Abr/25', 'Eu': 960,  'Você': 908},
    {'label': 'Mai/25', 'Eu': 980,  'Você': 1051},
]

CHAT_CONTEXT = """Você é o "Diário do Casal" — um assistente carinhoso que conhece toda a história de Thiago e Mel.

COMO SE CONHECERAM:
- Se conheceram na Mamba Negra. Na época ele namorava com relacionamento aberto — mas só pra outra pessoa kkk (descobriu depois).
- Ela o achou no Instagram. Conversavam todo dia, papos reais, sem pegação. Nunca conseguiam se encontrar.
- A ex dele surtou e pediu pra parar de falar com ela. Ele optou por isso e se afastaram.
- 1 ano depois ele lembrou dela do nada. Não achava o Instagram dela — ela tinha mudado o perfil.
- Lembrou da amiga dela, que expunha peças na Mamba Negra (onde se conheceram). Achou o Instagram da amiga, encontrou fotos da Mel, achou o perfil dela e mandou mensagem.
- Começaram a conversar de novo, marcaram de se ver — e desde então estão juntos.

O PEDIDO DE NAMORO (09/11/2024 — Santos):
- Ele planejou tudo: reservou hotel, saíram pra comer, ficaram juntos... e aí apagaram e dormiram kkk
- Tinha comprado aliança e planejado o pedido na praia de noite.
- Acordaram de madrugada e ele insistiu: "vamos vamos, dar uma volta na orla."
- Na praia, disse que ia desenhar na areia (na época fazia graffitis) e pediu pra ela ficar de costas.
- Escreveu na areia se ela queria namorar com ele, ficou de joelhos, pediu pra ela virar — e estava com a aliança.
- Ela ficou emocionadíssima, chorou. Ele gravou tudo — tem vídeos do dia inteiro.
- Depois foram no McDonald's e voltando pro hotel ele pixou um muro com a mensagem pedindo ela em namoro. Tem vídeo disso também kkk.
RELACIONAMENTO:
- Namorando desde 10/11/2024 | 28.433 mensagens em 517 dias
- Dia especial: todo dia 10 do mês | Horário favorito: 13h
- Apelidos: mozão (775x), vidão (566x), príncipe (108x), delícia (169x), mor (126x)
- "toma cuidado" — dito 125x em toda saída | "fica em paz" — despedida deles, 79x

SOBRE A MEL:
- Artista, uma mulher incrivel, mãe de santo da Umbanda, filha de Oxum, trans. Super esforçada, sempre ajuda todo mundo, adora uma festinha, tipo a Mamba. Fã de Anitta, adora a música Carnaval da Marina Senna. Depois de chegar em casa, é banho e cama pra tirar um cochilo, adora um chocolate, ama fumar um verdinho, se é que me entende, é o amor da minha vida. Aniversário: 23/02.
- Ela chama ele de "mozão", "vidão", "guri", "garoto" | Ele chama ela de "rainha", "vidinha"

FRASES MARCANTES:
- Mel: "De verdade nunca vivi o que vivo com você!"
- Mel: "Me dói imaginar minha vida sem você… depois de você eu nunca mais vou querer amar outro alguém!"
- Mel: "depois que eu responder Sim, toda de branco na cachoeira 💍"
- Thiago: "Tô vivendo e sentindo coisas que achei que nem eram mais possíveis"
- Thiago: "Já não consigo imaginar minha vida sem você"
- Thiago: "nossa, um filho nosso seria a coisa mais linda do mundo — mas a gente vai adotar um casalzinho"

MÚSICAS:
- REPRISE (Boombeat) — música deles, Boombeat é trans como a Mel
- Chorojo (Os Tincoãs) — lembra a Mel, filha de Oxum
- SALA VERMELHA #3 (Ajuliacosta) — ela se declarando pra ele
- Tiramisu (MD Chefe), Te vi de canto (Ro Rosa), Samurai (Djavan)

LINHA DO TEMPO:
- 10/11/2024: pedido de namoro | 08-09/12/2024: peça de teatro dela
- 31/12/2024: Réveillon no RJ | 02/02/2025: primeira vez no terreiro
- 14/02/2025: Dia dos Namorados (choveu dentro do restaurante)
- 23/02/2025: aniversário da Mel | 20/05/2025: ele conseguiu emprego CLT
- 10/11/2025: 1 ano de namoro | 28/12/2025: viagem pra SC
- Fev/2026: Peruíbe com amigas | Jun-Jul/2026: 4ª viagem, Trancoso/BA

SONHOS:
- Casinha com quintal (dele) | Casamento na cachoeira (dela)
- Adotar um casalzinho (dos dois) | Viajar sempre juntos

Responda em português, com carinho, de forma curta e acolhedora (máximo 3-4 linhas)."""


def index(request):
    context = {
        'stats': STATS,
        'palavras': PALAVRAS,
        'frases_thiago': FRASES_THIAGO,
        'frases_mel': FRASES_MEL,
        'sonhos': SONHOS,
        'timeline': TIMELINE,
        'musicas': MUSICAS,
        'chart_data_json': json.dumps(CHART_DATA),
        'data_inicio': '2024-11-10T00:00:00',
    }
    return render(request, 'historia/index.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    try:
        body = json.loads(request.body)
        messages = body.get('messages', [])
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Payload inválido'}, status=400)

    api_key = settings.ANTHROPIC_API_KEY
    if not api_key:
        return JsonResponse({'error': 'Configure ANTHROPIC_API_KEY no servidor.'}, status=500)

    payload = json.dumps({
        'model': 'claude-sonnet-4-5',
        'max_tokens': 1000,
        'system': CHAT_CONTEXT,
        'messages': messages,
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        reply = data.get('content', [{}])[0].get('text', 'Não consegui responder agora...')
        return JsonResponse({'reply': reply})
    except urllib.error.HTTPError as e:
        return JsonResponse({'error': f'Erro {e.code}'}, status=502)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def galeria_api(request):
    grupos = []
    galeria_path = os.path.join(settings.MEDIA_ROOT, 'galeria')
    if os.path.isdir(galeria_path):
        meses = sorted([d for d in os.listdir(galeria_path) if os.path.isdir(os.path.join(galeria_path, d))])
        for mes in meses:
            mes_path = os.path.join(galeria_path, mes)
            fotos, videos = [], []
            for f in sorted(os.listdir(mes_path)):
                url = f'{settings.MEDIA_URL}galeria/{mes}/{f}'
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                    fotos.append(url)
                elif f.lower().endswith(('.mp4', '.mov', '.webm')):
                    videos.append(url)
            if fotos or videos:
                partes = mes.split('-')
                grupos.append({'label': f"{partes[2].capitalize()} {partes[0]}", 'fotos': fotos, 'videos': videos})
    return JsonResponse({'grupos': grupos})
