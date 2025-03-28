import logging
import os
import sys
from typing import Dict, List
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv
from functools import lru_cache
import pytz
from datetime import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY .env faylida topilmadi!")
    raise ValueError("OPENAI_API_KEY .env faylida topilmadi!")
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN .env faylida topilmadi!")
    raise ValueError("TELEGRAM_TOKEN .env faylida topilmadi!")
if not ADMIN_CHAT_ID:
    logger.error("ADMIN_CHAT_ID .env faylida topilmadi!")
    raise ValueError("ADMIN_CHAT_ID .env faylida topilmadi!")

masked_token = TELEGRAM_TOKEN[:8] + "..." + TELEGRAM_TOKEN[-4:] if TELEGRAM_TOKEN else "yo‘q"
logger.info(f"TELEGRAM_TOKEN o‘qildi: {masked_token}")

try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logger.error(f"OpenAI mijozini sozlashda xatolik: {str(e)}")
    raise

chat_histories: Dict[int, List[Dict[str, str]]] = {}
user_profiles: Dict[int, Dict[str, str]] = {}
stats = {"requests": 0, "errors": 0}
MAX_HISTORY_LENGTH = 10  

reply_keyboard = [[KeyboardButton("Yangi chat boshlash")]]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Botni boshlash funksiyasi."""
    try:
        chat_id = update.effective_chat.id
        user_name = update.effective_user.first_name or "Foydalanuvchi"
        chat_histories[chat_id] = [{"role": "system", "content": f"Siz do‘stona AI yordamchisiz. Foydalanuvchi {user_name} ga o‘zbek tilida javob bering."}]
        user_profiles[chat_id] = {"name": user_name, "requests": 0}
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Salom, {user_name}! Men sizga yordam berishga tayyorman. Nima haqida gaplashamiz? 😊",
            parse_mode='Markdown',
            reply_markup=markup
        )
        logger.info(f"Chat {chat_id} uchun yangi sessiya boshlandi. Foydalanuvchi: {user_name}")
    except Exception as e:
        stats["errors"] += 1
        logger.error(f"Start funksiyasida xatolik: {str(e)}")
        await context.bot.send_message(chat_id=chat_id, text="Kechirasiz, xatolik yuz berdi. Iltimos, qayta urinib ko‘ring! 😔", parse_mode='Markdown')

@lru_cache(maxsize=200)
def get_openai_response(chat_id: int, message: str) -> str:
    """OpenAI dan javob olish funksiyasi."""
    try:
        chat_histories[chat_id].append({"role": "user", "content": message})
        if len(chat_histories[chat_id]) > MAX_HISTORY_LENGTH:
            system_message = chat_histories[chat_id][0]
            chat_histories[chat_id] = [system_message] + chat_histories[chat_id][-MAX_HISTORY_LENGTH+1:]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_histories[chat_id],
            max_tokens=700,
            temperature=0.7
        )
        ai_response = response.choices[0].message.content
        chat_histories[chat_id].append({"role": "assistant", "content": ai_response})
        return ai_response
    except Exception as e:
        stats["errors"] += 1
        logger.error(f"OpenAI javob olishda xatolik: {str(e)}")
        if "rate limit" in str(e).lower():
            return "Hozir so‘rovlar chegarasi oshdi, biroz kuting va qayta urinib ko‘ring! 😅"
        return f"Kechirasiz, xatolik yuz berdi: {str(e)}. Iltimos, qayta urinib ko‘ring!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Matnli xabarlarni qayta ishlash funksiyasi."""
    try:
        chat_id = update.effective_chat.id
        user_message = update.message.text
        stats["requests"] += 1

        if user_message == "Yangi chat boshlash":
            await new_chat(update, context)
            return

        if chat_id not in chat_histories:
            user_name = update.effective_user.first_name or "Foydalanuvchi"
            chat_histories[chat_id] = [{"role": "system", "content": f"Siz do‘stona AI yordamchisiz. Foydalanuvchi {user_name} ga o‘zbek tilida javob bering."}]
            user_profiles[chat_id] = {"name": user_name, "requests": 0}

        user_profiles[chat_id]["requests"] += 1

        loading_message = await context.bot.send_message(
            chat_id=chat_id,
            text="Javob tayyorlanmoqda... ⏳",
            parse_mode='Markdown'
        )

        ai_response = get_openai_response(chat_id, user_message)

        await context.bot.delete_message(chat_id=chat_id, message_id=loading_message.message_id)

        await context.bot.send_message(
            chat_id=chat_id,
            text=ai_response,
            parse_mode='Markdown',
            reply_markup=markup
        )
        logger.info(f"Chat {chat_id} uchun matnli so‘rov: {user_message}")
    except Exception as e:
        stats["errors"] += 1
        logger.error(f"Matnli xabarni qayta ishlashda xatolik: {str(e)}")
        await context.bot.send_message(chat_id=chat_id, text="Xabarni qayta ishlashda xatolik yuz berdi. Iltimos, qayta urinib ko‘ring! 😔", parse_mode='Markdown')

async def new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yangi chat boshlash funksiyasi."""
    try:
        chat_id = update.effective_chat.id
        user_name = user_profiles.get(chat_id, {}).get("name", "Foydalanuvchi")
        chat_histories[chat_id] = [{"role": "system", "content": f"Siz do‘stona AI yordamchisiz. Foydalanuvchi {user_name} ga o‘zbek tilida javob bering."}]
        await context.bot.send_message(
            chat_id=chat_id,
            text="Yangi chat boshlandi! Endi yangi savollaringizni kutaman. 😊",
            parse_mode='Markdown',
            reply_markup=markup
        )
        logger.info(f"Chat {chat_id} uchun yangi chat boshlandi.")
    except Exception as e:
        stats["errors"] += 1
        logger.error(f"Yangi chat boshlashda xatolik: {str(e)}")
        await context.bot.send_message(chat_id=chat_id, text="Yangi chat boshlashda xatolik yuz berdi. Iltimos, qayta urinib ko‘ring! 😔", parse_mode='Markdown')

async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Statistikani ko‘rsatish funksiyasi."""
    try:
        chat_id = update.effective_chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Statistika:\n- So‘rovlar: {stats['requests']}\n- Xatolar: {stats['errors']}",
            parse_mode='Markdown',
            reply_markup=markup
        )
        logger.info(f"Chat {chat_id} uchun statistika so‘raldi.")
    except Exception as e:
        stats["errors"] += 1
        logger.error(f"Statistikani ko‘rsatishda xatolik: {str(e)}")
        await context.bot.send_message(chat_id=chat_id, text="Statistikani ko‘rsatishda xatolik yuz berdi. Iltimos, qayta urinib ko‘ring! 😔", parse_mode='Markdown')

async def send_status_report(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Botning holati haqida admin ga xabar yuborish."""
    admin_chat_id = ADMIN_CHAT_ID
    status_message = (
        f"Bot holati:\n"
        f"- Ishlayapti: {app.running}\n"
        f"- So‘rovlar: {stats['requests']}\n"
        f"- Xatolar: {stats['errors']}\n"
        f"- Log fayl hajmi: {os.path.getsize('bot.log') / (1024 * 1024):.2f} MB"
    )
    try:
        await context.bot.send_message(chat_id=admin_chat_id, text=status_message, parse_mode='Markdown')
        logger.info("Admin ga holat xabari yuborildi.")
    except Exception as e:
        logger.error(f"Admin ga xabar yuborishda xatolik: {str(e)}")

def clean_log_file():
    """Log fayl hajmi 10 MB dan oshsa, eski qismlarni tozalash."""
    log_file = "bot.log"
    max_size_mb = 10
    try:
        if os.path.exists(log_file):
            size_mb = os.path.getsize(log_file) / (1024 * 1024) 
            if size_mb > max_size_mb:
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                new_lines = lines[len(lines) // 2:]
                with open(log_file, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                logger.info(f"Log fayl tozalandi. Yangi hajm: {os.path.getsize(log_file) / (1024 * 1024):.2f} MB")
    except Exception as e:
        logger.error(f"Log faylni tozalashda xatolik: {str(e)}")

async def check_log_size(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Har kuni log fayl hajmini tekshirish."""
    clean_log_file()

if __name__ == "__main__":
    try:
        app = Application.builder().token(TELEGRAM_TOKEN).build()

        app.job_queue.scheduler.timezone = pytz.timezone("Asia/Tashkent")

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_handler(CommandHandler("stats", get_stats))

        app.job_queue.run_daily(send_status_report, time(hour=9, minute=0, tzinfo=pytz.timezone("Asia/Tashkent")))
        app.job_queue.run_daily(send_status_report, time(hour=21, minute=0, tzinfo=pytz.timezone("Asia/Tashkent")))
        app.job_queue.run_daily(check_log_size, time(hour=0, minute=0, tzinfo=pytz.timezone("Asia/Tashkent")))

        logger.info("Bot ishga tushdi...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Botni ishga tushirishda xatolik: {str(e)}")
        sys.exit(1)