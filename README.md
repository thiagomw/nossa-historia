# Nossa História  — Full Stack + DevOps

> Projeto pessoal construído do zero com **Django**, integrado à **API da Anthropic (Claude AI)**, com deploy completo em **VPS Oracle Cloud** usando Nginx, Gunicorn e systemd.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=gunicorn&logoColor=white)
![Oracle Cloud](https://img.shields.io/badge/Oracle_Cloud-C74634?style=flat&logo=oracle&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu_22.04-E95420?style=flat&logo=ubuntu&logoColor=white)
![Claude AI](https://img.shields.io/badge/Claude_AI-412991?style=flat&logo=anthropic&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20produção-brightgreen)

---

## Sobre o projeto

Site interativo que conta a história de um relacionamento — desenvolvido como presente pessoal, mas com foco em boas práticas de desenvolvimento e infraestrutura.

**O que foi implementado:**

- **Backend Django** com views, templates e API proxy para a Anthropic
- **Chatbot com IA** contextualizado via Claude API — responde perguntas sobre a história do casal com base em dados reais extraídos do WhatsApp
- **Galeria dinâmica** organizada por mês, servida via Nginx com suporte a fotos e vídeos
- **Análise de dados** do histórico do WhatsApp com Python (pandas, wordcloud) — estatísticas, palavras mais usadas, gráficos de intensidade por mês
- **Linha do tempo** e seção de músicas com significados personalizados
- **Contador em tempo real** calculando anos, meses, dias, horas, minutos e segundos desde o início do relacionamento
- **Tela de entrada** com senha personalizada
- **Player de música** flutuante com playlist completa
- **100% responsivo** — mobile first, com menu hambúrguer e layout adaptado

---

## Infraestrutura e Deploy

Deploy em produção em **VPS Oracle Cloud Free Tier** (Ubuntu 22.04, São Paulo):

- **Gunicorn** como servidor WSGI com 2 workers
- **Nginx** como reverse proxy e para servir arquivos estáticos e de mídia
- **systemd** para gerenciamento do processo Gunicorn (restart automático)
- **Swap de 1GB** configurado para otimizar o uso de RAM (1GB disponível)
- Variáveis de ambiente via `.env` com `python-dotenv` — sem secrets no código
- Deploy via `git pull` + `systemctl restart gunicorn`
- Transferência de mídia para o servidor via `scp`

---

## Instalação local

**1. Clone o repositório e crie o ambiente virtual:**
```bash
git clone https://github.com/thiagomw/nossa-historia.git
cd nossa-historia
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

```env
SECRET_KEY=sua-secret-key-aqui
DEBUG=True
ANTHROPIC_API_KEY=sk-ant-...
ALLOWED_HOSTS=localhost,127.0.0.1
```

**3. Rode o servidor:**
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000`

---

## Adicionando fotos e vídeos

Crie pastas dentro de `media/galeria/` com o padrão `AAAA-MM-nome/`:

```
media/
└── galeria/
    ├── 2024-11-novembro/
    │   ├── foto1.jpg
    │   └── foto2.jpg
    ├── 2024-12-dezembro/
    │   └── natal.jpg
    └── 2025-02-fevereiro/
        ├── restaurante.jpg
        └── video.mp4
```

As mídias aparecem automaticamente na seção **Fotos**, organizadas por mês e ano.

Para enviar mídias para o servidor em produção:
```bash
scp -i sua-chave.pem -r media/ ubuntu@seu-ip:/home/ubuntu/nossa-historia/
```

---

## Estrutura do projeto

```
nossa_historia/
├── nossa_historia/          # Configurações Django
│   ├── settings.py
│   └── urls.py
├── historia/                # App principal
│   ├── views.py             # Dados + views + proxy da Claude API
│   ├── urls.py
│   └── templates/
│       └── historia/
│           └── index.html   # Frontend completo (CSS + JS)
├── media/
│   ├── galeria/             # Fotos e vídeos organizados por mês
│   └── audio/               # Músicas da playlist
├── manage.py
├── requirements.txt
└── README.md
```

---

## Personalizando os dados

Edite `historia/views.py` — todos os dados estão nos dicionários no topo do arquivo:

| Variável | O que controla |
|---|---|
| `STATS` | Estatísticas do relacionamento |
| `PALAVRAS` | Apelidos e palavras frequentes |
| `FRASES_THIAGO` / `FRASES_MEL` | Frases marcantes separadas por pessoa |
| `TIMELINE` | Linha do tempo com datas especiais |
| `MUSICAS` | Playlist com significados |
| `SONHOS` | Sonhos compartilhados do casal |
| `CHART_DATA` | Gráfico de intensidade por mês |
| `CHAT_CONTEXT` | Contexto completo para o chatbot de IA |

---

## Tecnologias

| Categoria | Tecnologia |
|---|---|
| Backend | Python 3.13, Django 5 |
| Frontend | HTML5, CSS3, JavaScript (vanilla) |
| IA | Anthropic Claude API (claude-sonnet-4-5) |
| Servidor web | Nginx |
| WSGI | Gunicorn |
| Processo | systemd |
| Cloud | Oracle Cloud Free Tier (Ubuntu 22.04) |
| Análise de dados | Python, pandas, wordcloud, re |
| Controle de versão | Git, GitHub |

---

## Aprendizados aplicados

- Deploy completo em VPS Linux do zero, sem PaaS
- Configuração de Nginx como reverse proxy com socket Unix
- Gerenciamento de processos com systemd
- Boas práticas de segurança: secrets via variáveis de ambiente, `.gitignore` para arquivos sensíveis
- Integração com API externa (Anthropic) via backend Django — sem expor credenciais no frontend
- Análise e tratamento de dados reais com Python
- Responsividade mobile com CSS puro

---

*Projeto pessoal — desenvolvido com Python, Django e muito amor. 💛*
