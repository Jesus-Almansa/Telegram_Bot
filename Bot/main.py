from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes 

import os
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env.
TOKEN = os.getenv("API_KEY")
BOT_USERNAME = os.getenv("BOT_USERNAME")


# Commands
async def start_command(update: Update, context: ContextTypes):
    await update.message.reply_text("Bienvenido a tu bot de Telegram!")
    
async def help_command(update: Update, context: ContextTypes):
    await update.message.reply_text("Si necesitas ayuda, puedes preguntarme lo que quieras!")
    
async def custom_command(update: Update, context: ContextTypes):
    await update.message.reply_text("Este es un comando personalizado!")
    
# Responses

import random

def handle_response(text: str):
    processed: str = text.lower()

    greetings = ["hello", "hi", "hey", "hola"]
    farewells = ["bye", "goodbye", "see you", "adios"]
    well_being = ["how are you", "how are you doing", "what's up", "how's it going"]
    morning_greetings = ["good morning", "buenos días"]
    night_greetings = ["good night", "buenas noches"]
    thanks = ["thank you", "thanks", "gracias"]
    bot_identity = ["who are you", "what is your name"]

    if any(greet in processed for greet in greetings):
        return random.choice([
            "¡Hola! ¿Cómo estás?",
            "¡Hey! Encantado de verte.",
            "¡Hola, bienvenido!",
            "¡Hola! ¿En qué puedo ayudarte?"
        ])

    if any(farewell in processed for farewell in farewells):
        return random.choice([
            "¡Adiós! Nos vemos pronto.",
            "Hasta luego, cuídate.",
            "¡Chao! Que tengas un buen día.",
            "Espero verte pronto, ¡cuídate!"
        ])

    if any(wb in processed for wb in well_being):
        return random.choice([
            "Estoy bien, gracias por preguntar 😊",
            "¡Genial! ¿Y tú?",
            "Me siento excelente, ¿cómo estás tú?",
            "No me puedo quejar, ¿qué hay de ti?"
        ])

    if any(morning in processed for morning in morning_greetings):
        return random.choice([
            "¡Buenos días! Espero que tengas un día increíble.",
            "¡Hola! Que tengas un gran día ☀️",
            "¡Buenos días! ¿Cómo amaneciste?",
            "¡Buenos días! ¿Cómo va todo?"
        ])

    if any(night in processed for night in night_greetings):
        return random.choice([
            "¡Buenas noches! Que descanses.",
            "Dulces sueños 🌙",
            "Espero que tengas una noche tranquila.",
            "¡Nos vemos mañana!"
        ])

    if any(thank in processed for thank in thanks):
        return random.choice([
            "¡De nada! 😊",
            "No hay de qué.",
            "Siempre feliz de ayudar.",
            "¡Con gusto!"
        ])

    if any(bot in processed for bot in bot_identity):
        return random.choice([
            "Soy un bot, aquí para ayudarte. 😊",
            "Me puedes llamar tu asistente virtual.",
            "Soy un programa de IA, ¿en qué puedo ayudarte?",
            "¡Soy un bot, pero con mucha personalidad!"
        ])

    return random.choice([
        "No entiendo lo que quieres decir. 🤔",
        "¿Podrías reformular tu pregunta?",
        "Lo siento, no te entendí bien.",
        "No estoy seguro de cómo responder a eso."
    ])


# Message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}" ')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
        
    print('Bot:', response)
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    
if __name__ == "__main__":
    print("Bot is running!")
    app = Application.builder().token(TOKEN).build()
    
    # Commnads
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("anonymous", anonymous_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polls the bot
    print("Bot is polling!")
    app.run_polling(poll_interval=1)