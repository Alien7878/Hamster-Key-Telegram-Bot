import subprocess
import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import server

# Paste Token Here if you don't want to put it in an env. variable
TOKEN_INSECURE = "7234061545:AAH-R0O6QjfIo0R78sIIp1ifIyABKhqx608"

if os.name == 'posix':
    TOKEN = subprocess.run(["printenv", "HAMSTER_BOT_TOKEN"],
                           text=True,
                           capture_output=True).stdout.strip()
elif os.name == 'nt':
    TOKEN = subprocess.run(["echo", "%HAMSTER_BOT_TOKEN%"],
                           text=True,
                           capture_output=True,
                           shell=True).stdout.strip()
    TOKEN = "" if TOKEN == "%HAMSTER_BOT_TOKEN%" else TOKEN

AUTHORIZED_USERS = []
EXCLUSIVE = False

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🐹")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "The Commands are:\n*/bike*\n*/clone*\n*/cube*\n*/train*\n*/merge*\n*/twerk*\n*/poly*\n*/mud*\n*/trim*\n*/all*\nThese will generate 4 keys for their respective games\\.",
        parse_mode='MARKDOWNV2')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "You can also set how many keys are generated\\. For example, */cube 8* will generate *EIGHT* keys for the cube game\\.",
        parse_mode='MARKDOWNV2')


async def game_handler(update: Update,
                       context: ContextTypes.DEFAULT_TYPE,
                       chosen_game: int,
                       all: bool,
                       delay=0):
    await asyncio.sleep(delay)
    server.logger.info(f"Delay for {delay} seconds")

    if EXCLUSIVE and update.effective_chat.id not in AUTHORIZED_USERS:
        return

    server.logger.info(
        f"Generating for client: {update.effective_chat.first_name} : {update.effective_chat.id}"
    )

    if not all:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="🐹")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Generating\\.\\.\\.",
                                       parse_mode='MARKDOWNV2')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="This will only take a moment\\.\\.\\.",
            parse_mode='MARKDOWNV2')

    no_of_keys = int(context.args[0]) if context.args else 4
    keys = await server.run(chosen_game=chosen_game, no_of_keys=no_of_keys)
    generated_keys = [f"`{key}`" for key in keys]
    formatted_keys = '\n'.join(generated_keys)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"{formatted_keys}",
                                   parse_mode='MARKDOWNV2')
    server.logger.info("Message sent to the client.")


# Define individual game handlers
async def bike(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=1, all=all)


async def clone(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=2, all=all)


async def cube(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=3, all=all)


async def train(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=4, all=all)


async def merge(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=5, all=all)


async def twerk(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=6, all=all)


async def poly(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=7, all=all)


async def mud(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=8, all=all)


async def trim(update: Update, context: ContextTypes.DEFAULT_TYPE, all=False):
    await game_handler(update, context, chosen_game=9, all=all)


# Handle the /all command
async def all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if EXCLUSIVE and update.effective_chat.id not in AUTHORIZED_USERS:
        return

    server.logger.info(
        f"Generating for client: {update.effective_chat.first_name} : {update.effective_chat.id}"
    )
    server.logger.info("Generating keys for All Games.")

    await context.bot.send_message(chat_id=update.effective_chat.id, text="🐹")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Currently generating for all games\\.\\.\\.",
        parse_mode='MARKDOWNV2')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Come Back in about 5\\-10 minutes\\.",
                                   parse_mode='MARKDOWNV2')

    tasks = [
        game_handler(update, context, i + 1, True, i * 30) for i in range(6)
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN or TOKEN_INSECURE).build()
    server.logger.info("Server is running. Awaiting users...")

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('bike', bike))
    application.add_handler(CommandHandler('clone', clone))
    application.add_handler(CommandHandler('cube', cube))
    application.add_handler(CommandHandler('train', train))
    application.add_handler(CommandHandler('merge', merge))
    application.add_handler(CommandHandler('twerk', twerk))
    application.add_handler(CommandHandler('poly', poly))
    application.add_handler(CommandHandler('mud', mud))
    application.add_handler(CommandHandler('trim', trim))
    application.add_handler(CommandHandler('all', all))

    application.run_polling()
