import config

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from user import UserInfo
import instance
import uuid
import shutil
import os
import re
import time
from logger_config import logger
from chat_keyboards import Keyboard_Manager
from db import Database

class BOT():
    def __init__(self):
        self.dp = Dispatcher()
        self.bot = instance.bot
        self.keyboards = Keyboard_Manager()
        self.db = Database()
        self.admin_id = config.admin_id
        
        #command
        self.dp.message(CommandStart())(self.command_start_handler)   
        self.dp.callback_query(F.data == "users")(self.process_callback_view_users) 
        self.dp.callback_query(F.data == "clean")(self.clean_inactive_users) 

    async def command_start_handler(self, message: Message):
        info = UserInfo(message)
        chat_id = info.chat_id
        user_id = info.user_id
        username = info.username
        try:
            self.db.insert_user_data(user_id=user_id, username=username)
            keyboard = self.keyboards.create_start_inline_keyboard()
            await message.answer("bot started", reply_markup=keyboard)
        except Exception as ex:
            logger.error(ex)
            
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
