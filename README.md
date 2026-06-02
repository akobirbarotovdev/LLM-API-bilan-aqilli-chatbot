# 🤖 Teligram Bot - LLM API bilan aqilli chatbot

Telegram orqali **OpenAI GPT-4o** modelini foydalanib, foydalanuvchilar bilan **o'zbek tilida** real vaqtda suhbatlashning imkoniyati beradigan kuchli aqilli chatbot.

## ✨ Asosiy xususiyatlari

- 🌐 **Telegram integratsiyasi** - `python-telegram-bot` kutubxonasi yordamida
- 🧠 **Sun'iy intellekt** - OpenAI GPT-4o modelini ishlatish
- 💬 **O'zbek tilida javoblar** - Foydalanuvchilarga ayni mamlakat tilida yechimlar
- 📝 **Chat tarixi** - Har bir foydalanuvchi uchun o'ziga xos suhbat tarixi
- 📊 **Real-time statistika** - So'rovlar, xatolar va foydalanish ma'lumotlari
- ⏰ **Avtomatik hisobotlar** - Har kuni belgilangan vaqtlarda admin ga status
- 🛠️ **Smart Log boshqaruvi** - 10 MB dan oshgan log fayllarni avtomatik tozalash
- 🔄 **Yangi chat sessiyasi** - Tugma orqali suhbat tarixini qayta boshlash

## 🛠️ Texnologiya stacki

```
✓ Python 3.8+
✓ python-telegram-bot (20.7) - Telegram API
✓ openai (1.10.0) - OpenAI API (GPT-4o)
✓ python-dotenv (1.0.0) - Environment variables
✓ pytz (2023.3) - Timezone management
```

## 📁 Loyiha tuzilishi

```
teligram-bot/
├── bot.py                 # 🎯 Botning asosiy kodi
├── requirements.txt       # 📦 Python bog'liqliklarni
├── Procfile              # 🚀 Heroku deployment
├── .gitignore            # 🔒 Himoyalangan fayllar
├── .env.example          # 📋 Environment template
└── README.md             # 📖 Bu fayl
```

## ⚙️ Tezkor o'rnatish

### 1️⃣ Repositoriyani klon qilish

```bash
git clone https://github.com/akobirbarotovdev/teligram-bot.git
cd teligram-bot
```

### 2️⃣ Virtual environment yaratish (tavsiya etiladi)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Bog'liqliklarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4️⃣ .env faylini sozlash

Loyiha ildizida `.env` faylini yarating:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
TELEGRAM_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
ADMIN_CHAT_ID=1234567890
```

**O'zgaruvchilari:**
- `OPENAI_API_KEY` - [OpenAI Platform](https://platform.openai.com/api-keys) dan API ključ
- `TELEGRAM_TOKEN` - [@BotFather](https://t.me/BotFather) dan bot token
- `ADMIN_CHAT_ID` - Admin uchun Chat ID (raqamli)

## 🚀 Boshlash

### Lokal test qilish:

```bash
python bot.py
```

### Heroku da deploy qilish (cloud hosting):

```bash
heroku login
heroku create your-bot-name
heroku config:set OPENAI_API_KEY=sk-xxxx
heroku config:set TELEGRAM_TOKEN=123456:ABC
heroku config:set ADMIN_CHAT_ID=1234567890
git push heroku main
```

## 💡 Bot funksiyalari

| Komanda | Tafsifi |
|---------|---------|
| `/start` | Bot bilan suhbat boshlash, chat tarixi yaratish |
| `/stats` | Statistika ko'rish (umumiy so'rovlar, xatolar) |
| Matnli xabar | AI javoblarini olish |
| "Yangi chat boshlash" | Suhbat tarixini tozalash, yangi sessiya |

### 🔄 Avtomatik vazifalar

Bot quyidagi jarayonlarni avtomatik bajaradi:

1. **09:00 (Tashkent vaqti)** - Admin ga kunlik hisobot
2. **21:00 (Tashkent vaqti)** - Kechki status xabari
3. **00:00 (Tashkent vaqti)** - Log fayl hajmini tekshirish va tozalash

## ⚙️ Bot konfiguratsiyasi

```python
Model: GPT-4o
Max Tokens: 700 (javob uzunligi)
Temperature: 0.7 (kreativlik)
Chat Tarixi: Oxirgi 10 ta xabar
Til: O'zbek (Uzbek)
```

## 🔍 Debugging va Log fayllari

Bot barcha harakatlarni `bot.log` fayliga yozadi:

```bash
# Real-time log kuzatish
tail -f bot.log

# Butun log ko'rish
cat bot.log
```

**Log ma'lumotlari:**
- Bot ishga tushishi
- Yangi chat sessiyalari
- API so'rovlari va javoblar
- Xatolar va muammolar
- Foydalanuvchi statistikasi

## ❌ Muammolarni hal qilish

### OpenAI API kaliti topilmadi
```
Error: OPENAI_API_KEY .env faylida topilmadi!
```
✅ **Yechim**: `.env` faylga `OPENAI_API_KEY=sk-...` qo'shing

### Telegram token noto'g'ri
```
Error: TELEGRAM_TOKEN .env faylida topilmadi!
```
✅ **Yechim**: `.env` faylga to'g'ri token qo'shing

### Rate limit xatosi
```
⚠️ Hozir so'rovlar chegarasi oshdi, biroz kuting!
```
✅ **Yechim**: OpenAI qat'i chiqlandi. Birkaç daqiqadan sonra urinib ko'ring

### Connection xatosi
```
Error: Telegram bilan ulanib bo'lmadi
```
✅ **Yechim**: Internet ulanishini tekshiring va token to'g'riligini qayta ko'ring

## 📊 Kod tuzilishi

### Asosiy funksiyalar:

```python
start()                   # Bot sessiyasini boshlash
handle_message()         # Xabarlarni qayta ishlash
get_openai_response()    # AI javoblarini olish
new_chat()              # Yangi chat sessiyasi
get_stats()             # Statistikani ko'rsatish
send_status_report()    # Admin ga xabar yuborish
check_log_size()        # Log fayl tekshirish
clean_log_file()        # Log tozalash
```

## 🔒 Xavfsizlik

✅ `.env` faylini `.gitignore` ga qo'shing (repository-ga qo'shmang)  
✅ API kalitlarini GitHub-ga jonatmang  
✅ Admin Chat ID ni sirli saqlang  
✅ Production-da environment variables ishlatish majburi  

## 📈 Kelajaki rejalar

- [ ] Fayl qabul qilish va qayta ishlash
- [ ] Voice message qo'llab-quvvatlash
- [ ] Foydalanuvchi profilini saqlash
- [ ] Rate limiting va user quotas
- [ ] Database integratsiyasi (SQLite/PostgreSQL)
- [ ] Web dashboard tayyorlash

## 📞 Aloqa va yordam

- **GitHub**: [@akobirbarotovdev](https://github.com/akobirbarotovdev)
- **Email**: Contact repository owner
- **Issues**: Muammolar uchun [Issues](https://github.com/akobirbarotovdev/teligram-bot/issues) bo'limini ishlating

## 📄 Litsenziya

MIT Litsenziyasi ostida. Batafsil: [LICENSE](LICENSE)

---

**📅 Created**: 28 March 2025  
**🔄 Last Update**: 2 June 2026  
**💻 Language**: Python (99.8%)  
**⭐ Star**: Agar yoqsa, yulduz qo'ying!
