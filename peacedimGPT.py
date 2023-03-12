import asyncio
from aiogram import Bot, Dispatcher, types
import logging
import openai

logging.basicConfig(level=logging.INFO)

chat_api = "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"
bot = Bot(token="5845173175:AAEhRCADaOj2SMaaWnnHSJcvyJHUCrLfcjo")
dp = Dispatcher(bot)

async def on_startup(dp):
    logging.info("Starting the bot")

async def on_shutdown(dp):
    logging.info("Stopping the bot")
    await bot.close()

async def chat(message: types.Message):
    arg = message.get_args()
    openai.api_key = chat_api
    model_engine = "text-davinci-003"
    prompt = f"{arg}"
    completation = openai.Completion.create(
        engine = model_engine,
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.5
    )
    response = completation.choices[0].text
    await message.reply(f"{response}")

@dp.message_handler(commands=['chat'])
async def handle_chat(message: types.Message):
    asyncio.create_task(chat(message))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        logging.info("Starting the loop")
        loop.create_task(on_startup(dp))
        loop.create_task(dp.start_polling())
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Stopping the loop")
    finally:
        loop.run_until_complete(on_shutdown(dp))
        loop.close()
