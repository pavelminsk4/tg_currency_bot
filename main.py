import requests
import logging
import os
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
url = os.getenv('CURRENCY_API_URL')

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Функция для получения курса доллара
def get_exchange_rate():
    try:
        response = requests.get(url)
        data = response.json()
        return data['rates']['RUB']  # Возвращаем курс доллара к рублю
    except Exception as e:
        logger.error(f"Ошибка получения курса: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rate = get_exchange_rate()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"I'm a bot, please talk to me!{rate}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()
