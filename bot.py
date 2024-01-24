import config

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message
from user import UserInfo
import instance
import uuid
import shutil
import os
import re
import time

class BOT():
    def __init__(self):
        self.dp = Dispatcher()
        self.bot = instance.bot
        
        self.url = "https://www.survio.com/survey/d/F4K4J8C8D2F9D7L8O"
        
        #command
        self.dp.message(CommandStart())(self.command_start_handler)    

    async def command_start_handler(self, message: Message):
        info = UserInfo(message)
        chat_id = info.chat_id
        await message.answer("bot started")




