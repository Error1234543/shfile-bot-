import telebot
import re
import os
from flask import Flask

# Flask app (Koyeb expects web service)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# BotFather token (Koyeb env variable se)
TOKEN = os.getenv("8033969537:AAF_TeB3pFGNjc7zTYolaNq-eZSQP0jF6T4")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        text = downloaded_file.decode("utf-8", errors="ignore")

        output_lines = []

        # 🎥 Video extractor (mp4 + m3u8)
        video_pattern = r'"(.+?\.mp4)"\s+"(https?://[^\s"]+)"'
        video_matches = re.findall(video_pattern, text)
        for name, url in video_matches:
            clean_name = name.replace(".mp4", "")
            output_lines.append(f"📹 {clean_name} : {url}")

        # 📄 PDF extractor
        pdf_pattern = r'"(.+?\.pdf)"\s+"(https?://[^\s"]+)"'
        pdf_matches = re.findall(pdf_pattern, text)
        for name, url in pdf_matches:
            clean_name = name.replace(".pdf", "")
            output_lines.append(f"📄 {clean_name} : {url}")

        if output_lines:
            output_text = "\n".join(output_lines)
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(output_text)
            with open("output.txt", "rb") as f:
                bot.send_document(message.chat.id, f)
        else:
            bot.reply_to(message, "⚠️ File me koi video/pdf link nahi mila.")

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# Start bot polling in background
import threading
def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))