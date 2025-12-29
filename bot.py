import logging
from telegram import Update
from telegram.ext import (
    Application,
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
            return False

        text_lower = text.lower()
        return self.bot_username.lower() in text_lower or self.bot_name in text_lower

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handle incoming messages.

        Args:
            update (Update): Telegram update.
            context (ContextTypes.DEFAULT_TYPE): Callback context.
        """
        if not update.message or not update.message.text:
            return

        chat_type = update.effective_chat.type
        if chat_type not in ["group", "supergroup"]:
            logger.info(f"Received message from {chat_type} chat")
            await update.message.reply_text(
                "¡Oye compañero! Este bot solo funciona en grupos. "
                "Agrégame a un grupo y mencióneme para que podamos hablar."
            )
            return

        message_text = update.message.text
        if not self.is_mentioned(message_text):
            logger.info("Bot not mentioned, ignoring message")
            return

        logger.info(f"Processing message: {message_text}")

        try:
            await update.message.chat.send_action(action="typing")
            response = await self.ai.get_response(message_text)
            await update.message.reply_text(response)
            logger.info(f"Sent response: {response}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text(
                "Disculpa compañero, tuve un problema técnico. ¡Intenta de nuevo!"
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
        logger.error(f"Update {update} caused error {context.error}")

    async def post_init(self, application: Application) -> None:
        """
        Post initialization callback.

        Args:
            application (Application): Telegram application.
        """
        await self.initialize_bot_info(application)

    def run(self) -> None:
        """Run the bot."""
        logger.info("Starting Clar IA bot...")

        application = (
            Application.builder()
            .token(self.config.telegram_bot_token)
            .post_init(self.post_init)
            .build()
        )

        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        application.add_error_handler(self.error_handler)

        logger.info("Bot is running. Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
