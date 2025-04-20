from telethon import TelegramClient, events, Button
import random
import asyncio
import os
from telethon.sessions import StringSession
from keep_alive import keep_alive
import time
from flask import Flask

# بيانات البوت
API_ID = 22696039
API_HASH = "00f9cc1d3419e879013f7a9d2d9432e2"
BOT_TOKEN = "7732686950:AAEJ8M2DrM6wUS1sIwDrUd47y0n9R8fsiRo"

# أيدي الجروبات المستهدفة
CHAT_IDS = [-1002457023914, -1002414213451]

# تأكيد بداية التشغيل
print("✅ البوت بدأ التشغيل...")

# تشغيل البوت باستخدام StringSession
bot = TelegramClient(StringSession(), API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# تحميل الأذكار من ملف التكست
def load_azkar(file_path):
    if not os.path.exists(file_path):
        print("⚠ ملف الأذكار مش موجود! اتأكد إنه معمول باسم 'azkar.txt'.")
        return []
    
    with open(file_path, "r", encoding="utf-8") as file:
        azkar = file.read().splitlines()
    
    if not azkar:
        print("⚠ ملف الأذكار موجود لكنه **فارغ**، لازم تضيف الأذكار علشان يشتغل البوت.")
    
    return azkar

azkar_list = load_azkar("azkar.txt")

# تأكيد تعريف البوت قبل الحدث
print("🔹 البوت متصل بالتليجرام بنجاح!")

# كود فحص استقبال الرسائل
@bot.on(events.NewMessage)
async def check_messages(event):
    print(f"📌 استلم البوت رسالة من: {event.chat_id} - محتوى الرسالة: {event.text}")

@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    print(f"🚀 استقبل البوت أمر /start من: {event.chat_id}")

    message = """✨ **ذكِّر قلبك بالله، وارتقِ بروحك 📿**  
    في زحمة الحياة، البوت ده هيكون **رفيقك للذكر والدعاء والتسبيح** 🌙  
    خلّي لسانك رطب بذكر الله، وابدأ كل يوم بنور جديد 💛  
    ﴿ **فَاذْكُرُونِي أَذْكُرْكُمْ** ﴾ – وعد ربّاني لا يُخلف!  
    💻 **مبرمج البوت:** @Mavdiii"""

    keyboard = [[Button.url("📖 تلاوات قرآنية", "https://t.me/Telawat_Quran_0")]]
    await event.respond(message, buttons=keyboard)

# إرسال ذكر عشوائي لكل الجروبات
async def send_zekr():
    while True:
        if azkar_list:
            zekr = random.choice(azkar_list)
            keyboard = [[Button.url("📖 تلاوات قرآنية", "https://t.me/Telawat_Quran_0")]]
            
            for chat_id in CHAT_IDS:
                await bot.send_message(chat_id, zekr, buttons=keyboard)
                print(f"✅ تم إرسال الذكر إلى الجروب {chat_id}")
        else:
            print("⚠ مفيش أذكار! تأكد إنك ضفتها في 'azkar.txt'.")

        await asyncio.sleep(300)  # كل 5 دقائق

# إعداد Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت يعمل بنجاح!"

@app.route('/status')
def status():
    return "البوت متصل بالتليجرام بنجاح!"

# تشغيل البوت والاستجابة للأحداث
keep_alive()  # تشغيل السيرفر علشان يفضل البوت شغال

# استخدم ensure_future لتشغيل send_zekr في الخلفية
asyncio.ensure_future(send_zekr())

with bot:
    bot.loop.run_forever()

# تأكيد أن البوت يعمل مع Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
