# Nossa História 💛 — Thiago & Mel (Django)

## Instalação

```bash
pip install django
```

## Configurar a chave da API Anthropic

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Rodar o servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## Adicionar fotos/vídeos

Crie pastas dentro de `media/galeria/` com o padrão `AAAA-MM-nome/`:

```
media/
  galeria/
    2024-11-inicio/
      foto1.jpg
      foto2.jpg
    2024-12-natal/
      natal.jpg
    2025-02-namorados/
      restaurante.jpg
      video.mp4
```

As mídias aparecem automaticamente na seção "Fotos", organizadas por mês.

## Estrutura do projeto

```
nossa_historia/
├── nossa_historia/      # Configurações Django
│   ├── settings.py
│   └── urls.py
├── historia/            # App principal
│   ├── views.py         # Dados + views + proxy da API
│   ├── urls.py
│   └── templates/
│       └── historia/
│           └── index.html
├── media/
│   └── galeria/         # Suas fotos aqui!
├── manage.py
└── README.md
```

## Personalizar os dados

Edite `historia/views.py` — todos os dados do casal estão nos dicionários no topo do arquivo:
- `STATS` — estatísticas
- `PALAVRAS` — apelidos e palavras frequentes
- `FRASES` — frases marcantes
- `TIMELINE` — linha do tempo
- `MUSICAS` — playlist
- `CHART_DATA` — gráfico de intensidade por mês
- `CHAT_CONTEXT` — contexto para a IA do chat
