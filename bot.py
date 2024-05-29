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
from admin_panel import Admin_Commands

class BOT():
    def __init__(self):
        self.dp = Dispatcher()
        self.bot = instance.bot
        self.keyboards = Keyboard_Manager()
        self.db = Database()
        self.admin_id = config.admin_id
        self.admin_command = Admin_Commands()
        
        #command
        self.dp.message(CommandStart())(self.command_start_handler)   
        self.dp.callback_query(F.data == "users")(self.admin_command.process_callback_view_users) 
        self.dp.callback_query(F.data == "clean")(self.admin_command.clean_inactive_users) 

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
