import logging
import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIG ---
TOKEN = "8403520800:AAGwQoHL92EEwPn85AAHy_y6m385peFTSIo"
ADMIN_ID = 8251224100  # your Telegram ID

# Approved users
approved_users = set()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# --- FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greeting message with Start & Register options"""
    keyboard = [
        [InlineKeyboardButton("▶️ Start Mining", callback_data="start_mining")],
        [InlineKeyboardButton("📝 Register", callback_data="register")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "🦁Welcome onboard lucky user to TEAMLION888\n\n"
        "NEW???🥂\n"
        "🦁Register first with promocode LION888 to connect your session to your personalised bot for accurate mine signals\n"
        "🦁Our powerful tool uses OpenAI technology to detect the signals straight from your game server💎‼️\n\n"
        "🦁When you are done with registration text @Lionteamadmin for verification and linkage to our bot💎💙⚙️🤖\n\n"
        "🦁Start getting your personalised signals with the \"Start Mining\" button. "
        "To reset a session just press it again or use /start to reboot the bot.\n\n"
        "🦁NOTE⚠️\n"
        "YOU MUST CREATE NEW ACCOUNT WITH PROMOCODE LION888 OR BOT CANT WORK FOR YOUR SESSION‼️‼️⚠️\n"
        "Text @Teamlionadmin for help on creating a new account when you have an account already ☄️"
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()

    if query.data == "start_mining":
        if query.from_user.id not in approved_users:
            await query.edit_message_text(
                "❌ You are not approved yet. Text @Teamlionadmin to verify."
            )
            return

        await query.edit_message_text("loading⏳️")

        # Generate session details
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        session_number = random.randint(100, 999)
        probability = round(random.uniform(85.00, 99.00), 2)
        traps = random.choices([3, 5, 7], weights=[70, 20, 10])[0]  # mostly 3

        caption = (
            f"🦁 {today}\n"
            f"Session {session_number} 💎\n"
            f"Probability {probability}% 🦁💎\n"
            f"💣Traps: {traps}\n"
        )

        keyboard = [
            [InlineKeyboardButton("Get another signal 🦁", callback_data="start_mining")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(caption, reply_markup=reply_markup)

    elif query.data == "register":
        keyboard = [
            [InlineKeyboardButton("1️⃣ Use link to register here", url="https://1wcreg.life/casino/list?open=register&p=672y")],
            [InlineKeyboardButton("2️⃣ Check Registration", url="https://t.me/Teamlionadmin")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "📲 Follow the steps below to register:", reply_markup=reply_markup
        )


async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to approve a user"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "⛔ You are not authorized to use this command. "
            "If you have created new account with code LION888 already, text @Teamlionadmin for access💙"
        )
        return

    try:
        user_id = int(context.args[0])
        approved_users.add(user_id)
        await update.message.reply_text(f"✅ User {user_id} has been approved.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /approve <user_id>")


# --- MAIN ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("approve", approve))

    app.run_polling()


if __name__ == "__main__":
    main()
