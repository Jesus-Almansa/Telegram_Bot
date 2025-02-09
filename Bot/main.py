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
    
async def anonymous_command(update: Update, context: ContextTypes):
    await update.message.reply_text("Este es un comando anónimo!")
    
# Responses

def handle_response(text: str):
    processed: str = text.lower()
    if 'hello' in processed:
        return "Hola! ¿En qué puedo ayudarte?"
    
    if 'bye' in processed:
        return "Adiós! Espero verte pronto."
    
    if 'how are you' in processed:
        return "Estoy bien, gracias por preguntar."
    
    if 'good morning' in processed:
        return "¡Buenos días! ¿Cómo estás?"
    
    return "No entiendo lo que quieres decir."

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