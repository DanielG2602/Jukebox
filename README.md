🎶 Jukebox Discord Bot (Dockerizado)

Um bot de música para Discord construído em Python com discord.py e yt-dlp. O projeto é empacotado com Docker e Docker Compose, garantindo que o FFmpeg (necessário para o áudio) esteja sempre instalado e configurado corretamente.

🚀 Como Executar o Projeto

Siga estes passos para configurar e iniciar o bot usando o Docker Compose.

Pré-requisitos

Você precisa ter o Docker e o Docker Compose instalados na sua máquina.

1. Obtenha o Token do Discord

Crie um novo aplicativo de bot no Portal do Desenvolvedor do Discord.

Copie o TOKEN do bot.

Convide o bot para o seu servidor, garantindo que ele tenha as permissões de Connect (Conectar), Speak (Falar) e Use Voice Activity (Usar Atividade de Voz).

2. Configure as Variáveis de Ambiente

Crie um arquivo chamado .env na raiz do projeto (na mesma pasta onde estão o docker-compose.yaml e o dockerfile) e adicione seu token:

DISCORD_TOKEN=SEU_TOKEN_AQUI_DEVE_SER_MUITO_LONGO


3. Build e Execução

Com os arquivos dockerfile, docker-compose.yaml e .env configurados, execute o seguinte comando no terminal na raiz do projeto:

# 1. Constrói a imagem (instalando Python, dependências e FFmpeg)
# 2. Inicia o contêiner em segundo plano (-d)

```bash
docker-compose up --build -d
```

4. Verifique o Status

Para confirmar que o bot se conectou ao Discord com sucesso, visualize os logs:

```bash
docker logs music_bot -f
```

Você deve ver uma mensagem como: ✅ Login efetuado como: SEU_BOT

🎧 Comandos do Bot

O prefixo de comando é !.

Comando

Aliases

Descrição

```bash
!entrar
```


Faz o bot entrar no seu canal de voz atual.

```bash
!play <busca ou URL>
```


Toca a música ou a adiciona à fila de reprodução.

```bash
!skip
```


Pula a música que está tocando atualmente.

```bash
!pause
```


Pausa a música em reprodução.

```bash
!resume
```


Retoma a música que estava pausada.

```bash
!queue
||
!fila
```

Mostra a lista de músicas que estão na fila.
```bash
!stop
```


Interrompe a reprodução imediatamente e limpa toda a fila.

```bash
!sair
||
!dc
```

Desconecta o bot do canal de voz e limpa a fila do servidor.

🛠️ Estrutura do Projeto

dockerfile: Define a imagem Docker, baseada em python:3.11-slim, e instala o FFmpeg e as dependências Python.

docker-compose.yaml: Orquestra o serviço bot, injetando o token do .env e iniciando o main.py.

main.py: Ponto de entrada que inicializa o bot e carrega o MusicCog.

cogs/music_cog.py: Contém toda a lógica de voz, fila de reprodução e comandos de controle.

.env: Arquivo para armazenar variáveis de ambiente sensíveis (como o DISCORD_TOKEN).
