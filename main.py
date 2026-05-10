import telegram
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)
from collections import Counter
import requests

TOKEN = "8698359891:AAEzbpSztC5A_2VV87zVsUhhI6gFAEct3Cw"

# Common English dictionary
url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt"

print("Downloading dictionary 😭")

words_text = requests.get(url).text

dictionary = set(
    word.strip().lower()
    for word in words_text.splitlines()
    if len(word.strip()) > 2
)

print("Dictionary loaded 😭")

# Check if word can be made
def can_make(word, letters):
    word_count = Counter(word)
    letters_count = Counter(letters)

    for letter in word_count:
        if word_count[letter] > letters_count.get(letter, 0):
            return False

    return True

# Solve words
def solve_letters(letters):
    letters = letters.lower().replace(" ", "")

    matches = []

    for word in dictionary:
        if can_make(word, letters):
            matches.append(word)

    # Filter normal words only
    filtered = []

    for word in matches:
        if 3 <= len(word) <= 9:
            filtered.append(word)

    # Best words first
    filtered.sort(key=len, reverse=True)

    return filtered[:10]

# Telegram reply
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    bot_username = context.bot.username.lower()

    # Group mode → only reply if tagged
    if update.message.chat.type in ["group", "supergroup"]:
        if f"@{bot_username}" not in text:
            return

        text = text.replace(f"@{bot_username}", "").strip()

    words = solve_letters(text)

    if words:
        best_word = words[0]

        other_words = "\n".join(words[1:])

        if other_words:
            message = (
                f"🎯 Best Word:\n{best_word}\n\n"
                f"📚 Other Words:\n{other_words}"
            )
        else:
            message = f"🎯 Best Word:\n{best_word}"

    else:
        message = "No words found 😭"

    await update.message.reply_text(message)

# Start bot
app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
)

print("Bot running 😭")

app.run_polling()
