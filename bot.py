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
        self.bot_username = f"@{config.bot_username}"
        self.bot_name = config.bot_name.lower()

    def is_mentioned(self, text: str) -> bool:
        """
        Check if bot is mentioned in the message.

        Args:
            text (str): Message text.

        Returns:
            bool: True if bot is mentioned.
        """
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
            logger.info(f"Ignoring message from {chat_type} chat")
            return

        message_text = update.message.text
        if not self.is_mentioned(message_text):
            logger.info("Bot not mentioned, ignoring message")
            return

        logger.info(f"Processing message: {message_text}")

        try:
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

    def run(self) -> None:
        """Run the bot."""
        logger.info("Starting Clar IA bot...")

        application = (
            Application.builder().token(self.config.telegram_bot_token).build()
        )

        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        application.add_error_handler(self.error_handler)

        logger.info("Bot is running. Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
