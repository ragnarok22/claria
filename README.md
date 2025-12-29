<div align="center">
  <img src="claria-logo.png" alt="Clar IA Logo">

  # Clar IA - Bot de Telegram

  Bot de Telegram que responde en español como un apasionado defensor del régimen cubano, impulsado por OpenAI.
</div>

## Características

- **Solo grupos**: El bot únicamente responde en grupos y supergrupos de Telegram
- **Detección de menciones**: Responde cuando es mencionado por su nombre de usuario (@bot_username) o nombre
- **Personalidad cubana**: Responde en español con expresiones cubanas y apoyando la revolución
- **Impulsado por IA**: Usa OpenAI GPT-4o-mini para generar respuestas contextuales

## Requisitos

- Python 3.14+
- Token de bot de Telegram (obtener de [@BotFather](https://t.me/botfather))
- API Key de OpenAI

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con:

```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
OPENAI_API_KEY=tu_api_key_aqui
```

## Uso

### Desarrollo Local

1. Instalar dependencias:
```bash
make install
```

2. Ejecutar el bot:
```bash
make run
```

### Producción con Docker

#### Opción 1: Docker directo

1. Construir la imagen:
```bash
make docker-build
```

2. Ejecutar el contenedor:
```bash
make docker-run
```

3. Ver logs:
```bash
make docker-logs
```

4. Detener el bot:
```bash
make docker-stop
```

#### Opción 2: Docker Compose (Recomendado)

1. Iniciar el bot:
```bash
make compose-up
```

2. Ver logs:
```bash
make compose-logs
```

3. Detener el bot:
```bash
make compose-down
```

## Comandos Disponibles

```bash
make help          # Muestra todos los comandos disponibles
make install       # Instala dependencias
make run           # Ejecuta el bot localmente
make lint          # Ejecuta linter (ruff)
make format        # Formatea el código
make clean         # Limpia archivos de cache
make docker-build  # Construye imagen Docker
make docker-run    # Ejecuta bot en Docker
make docker-stop   # Detiene contenedor Docker
make docker-logs   # Muestra logs del contenedor
make compose-up    # Inicia con docker-compose
make compose-down  # Detiene con docker-compose
make compose-logs  # Muestra logs de docker-compose
```

## Estructura del Proyecto

```
clar-ia/
├── config.py           # Configuración y variables de entorno
├── ai.py              # Integración con OpenAI
├── bot.py             # Lógica del bot de Telegram
├── main.py            # Punto de entrada
├── Dockerfile         # Imagen Docker
├── docker-compose.yml # Configuración Docker Compose
├── Makefile           # Comandos útiles
├── pyproject.toml     # Dependencias del proyecto
└── .env               # Variables de entorno (no incluido en git)
```

## Comportamiento del Bot

El bot:
- Solo responde en grupos/supergrupos (ignora mensajes privados)
- Solo responde cuando es mencionado por su username o nombre
- Responde en español cubano con expresiones típicas
- Defiende la revolución cubana y sus logros
- Critica el embargo estadounidense
- Menciona figuras históricas como Fidel Castro y el Che Guevara

## Desarrollo

### Formatear código:
```bash
make format
```

### Verificar código:
```bash
make lint
```

## Licencia

MIT
