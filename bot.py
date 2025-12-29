import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import Config
from ai import AIAssistant

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class ClarIABot:
    """Telegram bot for Clar IA."""

    def __init__(self, config: Config):
        self.config = config
        self.ai = AIAssistant(config)
        self.bot_username = None
        self.bot_name = None

    async def initialize_bot_info(self, application: Application) -> None:
        """
        Initialize bot information from Telegram.

        Args:
            application (Application): Telegram application.
        """
        bot = await application.bot.get_me()
        self.bot_username = f"@{bot.username}" if bot.username else ""
        self.bot_name = bot.first_name.lower() if bot.first_name else ""
        logger.info(f"Bot initialized: {self.bot_username} ({self.bot_name})")

    def is_mentioned(self, text: str) -> bool:
        """
        Check if bot is mentioned in the message.

        Args:
            text (str): Message text.

        Returns:
            bool: True if bot is mentioned.
        """
        if not self.bot_username or not self.bot_name:
            logger.warning("Bot username or name not initialized yet")
            return False

        text_lower = text.lower()
        username_match = self.bot_username.lower() in text_lower
        name_match = self.bot_name in text_lower

        logger.info(
            f"Mention check - Username match: {username_match}, Name match: {name_match}"
        )
        return username_match or name_match

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle incoming messages.

        Args:
            update (Update): Telegram update.
            context (ContextTypes.DEFAULT_TYPE): Callback context.
        """
        logger.info("=== New message received ===")

        if not update.message or not update.message.text:
            logger.info("Message or text is None, ignoring")
            return

        chat_type = update.effective_chat.type
        logger.info(f"Chat type: {chat_type}")

        if chat_type not in ["group", "supergroup"]:
            logger.info(
                f"Received message from {chat_type} chat, sending private chat warning"
            )
            await update.message.reply_text(
                "¡Oye compañero! Este bot solo funciona en grupos. "
                "Agrégame a un grupo y mencióneme para que podamos hablar."
            )
            return

        message_text = update.message.text
        logger.info(f"Message text: {message_text}")
        logger.info(f"Bot username: {self.bot_username}, Bot name: {self.bot_name}")

        if not self.is_mentioned(message_text):
            logger.info("Bot not mentioned, ignoring message")
            return

        logger.info(f"Bot mentioned! Processing message: {message_text}")

        try:
            logger.info("Sending typing action...")
            await update.message.chat.send_action(action="typing")
            logger.info("Typing action sent successfully")

            logger.info("Calling AI to get response...")
            response = await self.ai.get_response(message_text)
            logger.info(f"AI response received: {response[:100]}...")

            logger.info("Sending reply to user...")
            await update.message.reply_text(response)
            logger.info(f"Response sent successfully: {response}")
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            await update.message.reply_text(
                "Disculpa compañero, tuve un problema técnico. ¡Intenta de nuevo!"
            )

    async def start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle /start command.

        Args:
            update (Update): Telegram update.
            context (ContextTypes.DEFAULT_TYPE): Callback context.
        """
        logger.info("=== /start command received ===")

        if not update.message:
            return

        chat_type = update.effective_chat.type
        logger.info(f"/start command from {chat_type} chat")

        if chat_type not in ["group", "supergroup"]:
            logger.info("Sending private chat warning for /start")
            await update.message.reply_text(
                "¡Oye compañero! Este bot solo funciona en grupos. "
                "Agrégame a un grupo y mencióneme para que podamos hablar."
            )
        else:
            logger.info("Sending group welcome message for /start")
            await update.message.reply_text(
                "¡Qué bolá asere! Estoy aquí pa' defender la revolución. "
                "Mencióneme cuando necesites que hable de lo grande que es Cuba. "
                "¡Dale compay!"
            )

    async def error_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle errors.

        Args:
            update (Update): Telegram update.
            context (ContextTypes.DEFAULT_TYPE): Callback context.
        """
        logger.error(
            f"Update {update} caused error {context.error}", exc_info=context.error
        )

    async def post_init(self, application: Application) -> None:
        """
        Post initialization callback.

        Args:
            application (Application): Telegram application.
        """
        await self.initialize_bot_info(application)

    async def log_all_updates(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Log all received updates for debugging."""
        logger.info(f"RAW UPDATE RECEIVED: {update}")

    def run(self) -> None:
        """Run the bot."""
        logger.info("Starting Clar IA bot...")

        application = (
            Application.builder()
            .token(self.config.telegram_bot_token)
            .post_init(self.post_init)
            .build()
        )

        # Log all updates for debugging
        application.add_handler(
            MessageHandler(filters.ALL, self.log_all_updates), group=-1
        )

        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        application.add_error_handler(self.error_handler)

        logger.info("Bot is running. Press Ctrl+C to stop.")
        logger.info("IMPORTANT: Make sure Privacy Mode is DISABLED in @BotFather")
        logger.info(
            "Send /mybots -> Select your bot -> Bot Settings -> Group Privacy -> Turn OFF"
        )
        application.run_polling(allowed_updates=Update.ALL_TYPES)
