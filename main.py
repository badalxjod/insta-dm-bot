import time
from instagrapi import Client
from telegram import Bot
from telegram.error import TelegramError

# --- CONFIGURATION (Hardcoded) ---
INSTA_USERNAME = "INSTA_USERNAME"
INSTA_PASSWORD = "INSTA_PASSWORD"
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"
PROXY = "PROXY"

# --- Initialize Clients ---
cl = Client()
cl.set_proxy(PROXY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# --- Login to Instagram ---
try:
    cl.login(INSTA_USERNAME, INSTA_PASSWORD)
    print("✅ Instagram Login Success!")
except Exception as e:
    print(f"❌ Instagram Login Failed: {e}")
    exit()

# --- Store Already Seen Message IDs ---
seen_messages = set()

# --- Main Function to Forward New DMs ---
def forward_messages():
    while True:
        try:
            threads = cl.direct_threads()
            for thread in threads:
                messages = cl.direct_messages(thread.id, amount=20)
                for msg in reversed(messages):
                    if msg.id not in seen_messages:
                        try:
                            sender_username = cl.user_info(msg.user_id).username
                            text = f"📩 From: @{sender_username}\n🕒 {msg.timestamp}\n\n{msg.text}"
                            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
                            seen_messages.add(msg.id)
                            print(f"✅ Sent: {text[:40]}...")
                        except TelegramError as te:
                            print(f"⚠️ Telegram Error: {te}")
                        time.sleep(2)  # Avoid Telegram flood
            time.sleep(30)
        except Exception as e:
            print(f"⚠️ Error: {e} | Retrying in 15s")
            time.sleep(15)

# --- Start the Bot ---
if __name__ == "__main__":
    forward_messages()
