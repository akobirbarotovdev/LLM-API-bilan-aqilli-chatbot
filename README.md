# 🤖 Teligram Bot - LLM API bilan aqilli chatbot

Telegram orqali OpenAI GPT-4o modelini foydalanib, foydalanuvchilar bilan o'zbek tilida real vaqtda suhbatlashning imkoniyati beradigan aqilli chatbot.

## 📋 Loyihaning asosiy xususiyatlari

- **🌐 Telegram integratsiyasi**: `python-telegram-bot` kutubxonasi yordamida
- **🧠 Sun'iy intellekt**: OpenAI GPT-4o modelini ishlatish
- **💬 O'zbek tili**: Foydalanuvchilarga o'zbek tilida javoblar beradigan bot
- **📝 Chat tarixi**: Har bir foydalanuvchi uchun o'ziga xos chat tarixi saqlanadi
- **📊 Statistika**: So'rovlar va xatolarni kuzatish
- **⏰ Avtomatik hisobotlar**: Har kuni belgilangan vaqtlarda admin ga status yuboradi
- **🛠️ Log fayl boshqaruvi**: 10 MB dan oshgan log fayllarni avtomatik tozalash

## 🛠️ Texnologiyalar

```
- Python 3.8+
- python-telegram-bot (version 20.7) - Telegram API
- openai (version 1.10.0) - OpenAI API
- python-dotenv (version 1.0.0) - .env fayllarni o'qish
- pytz (version 2023.3) - Vaqt mintaqalarini boshqarish
```

## 📁 Fayl tuzilishi

```
teligram-bot/
├── bot.py              # Botning asosiy kodi
├── requirements.txt    # Python bog'liqliklarining ro'yxati
├── Procfile           # Heroku deployment uchun konfiguratsiya
├── .gitignore         # Git uchun e'tibor berilmaydigan fayllar
└── README.md          # Bu fayl
```

## ⚙️ O'rnatish va konfiguratsiya

### 1️⃣ Loyihani klon qilish

```bash
git clone https://github.com/akobirbarotovdev/teligram-bot.git
cd teligram-bot
```

### 2️⃣ Bog'liqliklarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3️⃣ .env faylini yaratish

Loyiha ildizida `.env` faylini yarating va quyidagi o'zgaruvchilarni qo'shing:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
TELEGRAM_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
ADMIN_CHAT_ID=1234567890
```

**Zarur o'zgaruvchilar:**
- `OPENAI_API_KEY`: [platform.openai.com](https://platform.openai.com) da API kaliti
- `TELEGRAM_TOKEN`: [@BotFather](https://t.me/BotFather) dan olingan bot tokeni
- `ADMIN_CHAT_ID`: Admin foydalanuvchining chat ID si

## 🚀 Ishga tushirish

### Lokal test uchun:

```bash
python bot.py
```

### Heroku da deploy qilish:

```bash
heroku login
heroku create your-bot-name
heroku config:set OPENAI_API_KEY=sk-xxxx
heroku config:set TELEGRAM_TOKEN=123456:ABC
heroku config:set ADMIN_CHAT_ID=1234567890
git push heroku main
```

## 💡 Asosiy funksiyalar

### 1. `/start` - Bot boshlash
- Foydalanuvchi botga birinchi marta ulanganida chat tarixi yaratiladi
- System xabari foydalanuvchining ismi bilan personalizatsiya qilinadi

### 2. Matnli xabarlar - AI javoblar
- Foydalanuvchi har qanday xabar yuborganda, bot OpenAI dan javob oladi
- Oxirgi 10 ta xabar saqlanadi (MAX_HISTORY_LENGTH = 10)
- Javob tayyorlanayotgani aytiladi ("⏳" emoji)

### 3. "Yangi chat boshlash" tugmasi
- Oldingi suhbatning tarixi o'chiriladi
- Yangi sessiya boshlash imkoniyati beriladi

### 4. `/stats` - Statistika ko'rish
- Umumiy so'rovlar soni
- Xatolar soni

## 📊 Bot asosiy xususiyatlari

| Xususiyat | Tafsifi |
|-----------|---------|
| **Model** | GPT-4o |
| **Max tokens** | 700 (javob uzunligi) |
| **Temperature** | 0.7 (kreativlik darajasi) |
| **Chat tarixi** | Oxirgi 10 ta xabar |
| **Til** | O'zbek (Uzbek) |
| **Kutubxona** | python-telegram-bot |

## 📅 Avtomatik vazifalar

Bot quyidagi vazifalarni avtomatik bajaradi:

1. **Har kuni 09:00 (Tashkent vaqti)** - Admin ga status hisoboti yuboriladi
2. **Har kuni 21:00 (Tashkent vaqti)** - Admin ga status hisoboti yuboriladi
3. **Har kuni 00:00 (Tashkent vaqti)** - Log fayl hajmi tekshiriladi va tozalanadi

## 🔍 Loglar va monitoring

Bot barcha jarayonlarni `bot.log` fayliga qayd etadi:

```bash
# Log faylni kuzatish (real vaqtda)
tail -f bot.log

# Log faylni ko'rish
cat bot.log
```

**Log qoliplar:**
- Bot ishga tushishi
- Yangi sessiyalarning ochilishi
- OpenAI API so'rovlari
- Xatoliklar va istisno hollar
- Foydalanuvchi statistikasi

## ⚠️ Xatolarni hal qilish

### OpenAI API kaliti topilmadi
```
OPENAI_API_KEY .env faylida topilmadi!
```
**Yechim**: `.env` faylida `OPENAI_API_KEY` ni qo'shing

### Telegram token topilmadi
```
TELEGRAM_TOKEN .env faylida topilmadi!
```
**Yechim**: `.env` faylida `TELEGRAM_TOKEN` ni qo'shing

### Rate limit xatosi
```
Hozir so'rovlar chegarasi oshdi, biroz kuting va qayta urinib ko'ring!
```
**Yechim**: OpenAI rate limit i oshdi. Biroz kutib qayta urinib ko'ring

## 📝 Kod tuzilishi

### Asosiy funksiyalar:

- **`start()`** - Bot sessiyasini boshlash
- **`handle_message()`** - Foydalanuvchi xabarlarini qayta ishlash
- **`get_openai_response()`** - OpenAI dan AI javoblarini olish
- **`new_chat()`** - Yangi chat boshlash
- **`get_stats()`** - Statistikani ko'rsatish
- **`send_status_report()`** - Admin ga status hisoboti yuborish
- **`check_log_size()`** - Log fayl hajmini tekshirish
- **`clean_log_file()`** - Log faylni tozalash

## 🔒 Xavfsizlik tavsiyalari

1. `.env` faylini `git` ga qo'shmang (`.gitignore` da mavjud)
2. API kalitlarini GitHub ga jonatmang
3. Admin chat ID ni yashirin qo'ling
4. Production da environment variables ishlatish tavsiya etiladi

## 📞 Aloqa

- **GitHub**: [@akobirbarotovdev](https://github.com/akobirbarotovdev)
- **Telegram Bot**: [@teligram_bot](https://t.me/)

## 📄 Litsenziya

Ushbu loyiha ochiq kodli va foydalanish uchun bepul.

---

**Yaratilgan sana**: 28 March 2025  
**Oxirgi yangilanish**: 2 June 2026  
**Tillar**: Python (99.8%)
