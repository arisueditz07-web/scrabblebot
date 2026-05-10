from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)
from collections import Counter
import requests

TOKEN = "8698359891:AAHDZVLlgQWoxpoteUCkbRaTY1YSMY2cvDQ"

# Download full dictionary
url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

print("Downloading dictionary 😭")

words_text = requests.get(url).text

dictionary = set(
    word.strip().lower()
    for word in words_text.splitlines()
    if len(word.strip()) > 1
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

    matches.sort(key=len, reverse=True)

    return matches[:25]

# Telegram reply
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    words = solve_letters(text)

    if words:
        message = "🎯 Found Words:\n\n" + "\n".join(words)
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
