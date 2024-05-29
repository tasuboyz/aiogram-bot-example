from aiogram.types import Message, CallbackQuery
import asyncio
from db import Database
from chat_keyboards import Keyboard_Manager
from instance import bot
from user import UserInfo
from logger_config import logger
import instance
import config
from aiogram.fsm.context import FSMContext
from memory import Form

class Admin_Commands:
    def __init__(self):
        self.example_url = 'https://github.com/tasuboyz/aiogram-bot-example'
        self.db = Database()
        self.keyboards = Keyboard_Manager()
        self.bot = instance.bot
        self.admin_id = config.admin_id

    async def process_callback_view_users(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        user_id = info.user_id
        question = info.user_data
        message_id = info.message_id
        try:
            results = self.db.get_all_users()
            self.write_ids(results)
            count_users = Database().count_users()
            await self.bot.delete_message(chat_id, message_id)
            await self.bot.send_message(self.admin_id, f"👤 The number of users are {count_users}")  
        except Exception as ex:
            logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{user_id}:{ex}")
    
    def write_ids(self, results):
          info = UserInfo(None)
          with open('ids.txt', 'w') as file:
            for result in results:
                # status = info.get_vip_member(result[0])
                # if status != 'member':
                file.write(str(result[0]) + '\n')

    async def clean_inactive_users(self, callback_query: CallbackQuery):       
        count = 0
        id_to_delate = []
        try:
            counter = await callback_query.message.answer(f"{count}")
            async for user_id in self.db.users_ids():
                try:
                    await self.bot.send_chat_action(user_id[0], "typing")

                    #logger.error(f"{user_id[0]} Sended! {count}")
                    
                    count += 1
                    await self.bot.edit_message_text(chat_id=self.admin_id, text=f"{count}", message_id=counter.message_id)
                except Exception as e:     
                    logger.error(f"{e}")         
                    #logger.error(f"{user_id[0]}, delated \n{e}") 
                    id_to_delate.append(user_id[0])
        finally:
            for ids in id_to_delate:
                self.db.delate_ids(ids)      
                await self.bot.send_message(self.admin_id, "Completed!")
                #logger.error(f"Completed!")        

    async def wait_document(self, callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.answer("Send file txt:")
        await state.set_state(Form.set_repair)

    async def repair_user_id(self, message: Message, state: FSMContext):
        await state.clear()
        try:
            _, file_path = await self.image.recive_image(message, False)
            self.db.insert_all_users(file_path)
            await message.reply("Repair succesful!")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")
    
    async def recive_ads(self, callback_query: CallbackQuery, state: FSMContext):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        await state.set_state(Form.set_ads)  
        await self.bot.send_message(self.admin_id, "Ads:")
    
    async def send_ads(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        ads = message.text
        await state.clear()
        count = 0
        #id_da_escludere = self.estrai_id("send file.txt")
        id_to_delate = []
        try:
            counter = await message.answer(f"{count}")
            async for user_id in Database().users_ids():
                #if user_id[0] in id_da_escludere:
                #    continue
                #if count == 5111:
                #    logger.error(f"Completed!")
                #    break
                try:
                    await message.send_copy(user_id[0])
                    #logger.error(f"{user_id[0]} Sended! {count}")
                    count += 1
                    await asyncio.sleep(0.2)
                    await self.bot.edit_message_text(chat_id=self.admin_id, text=f"{count}", message_id=counter.message_id)
                except Exception as e:             
                    logger.error(f"{user_id[0]}, delated \n{e}") 
                    id_to_delate.append(user_id[0])
        finally:
            for ids in id_to_delate:
                Database().delate_ids(ids)      
                logger.error(f"Completed!")        
