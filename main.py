import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# ቁልፎችህን እዚህ ጋር ተካ
TELEGRAM_TOKEN = "እዚህ_ጋር_የቴሌግራም_ቶከንህን_ለጥፍ"
GEMINI_KEY = "እዚህ_ጋር_የጂሚኒ_ኤፒአይ_ኪይህን_ለጥፍ"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="ሰላም! እኔ የ AI ረዳት ነኝ። የምትፈልገውን ጥያቄ መጠየቅ ትችላለህ!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ይቅርታ፣ ስህተት አጋጥሟል።")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    app.add_handler(start_handler)
    app.add_handler(message_handler)
    
    print("ቦቱ ስራ ጀምሯል...")
    app.run_polling()
