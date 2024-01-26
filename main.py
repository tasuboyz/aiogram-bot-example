from bot import BOT

import asyncio
from logger_config import logger

async def on_start():
    print("Bot avviato")

async def on_stop():
    print("Bot fermato")

async def main():
    try:       
        my_bot = BOT()
        await on_start()
        await my_bot.dp.start_polling(my_bot.bot)
    except Exception as ex:
        logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
    except KeyboardInterrupt:
        print("Interrotto dall'utente")
    finally:
        await on_stop()
        
if __name__ == '__main__':   
    asyncio.run(main())
