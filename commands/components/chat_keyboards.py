from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import os
from .user import UserInfo

class Keyboard_Manager:
    def __init__(self):
        self.example_url = 'https://github.com/tasuboyz/aiogram-bot-example'

    def create_start_inline_keyboard(self, message=None):
        keyboard = []
        text = "Open Link"
        keyboard.append([InlineKeyboardButton(text=text, web_app=WebAppInfo(url=self.example_url))])
        keyboard.append([InlineKeyboardButton(text=text, url=self.example_url)])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def admin_keyboards(self, message=None):
        keyboard = []
        text = "Open Link"
        keyboard.append([InlineKeyboardButton(text="View Users", callback_data="users")])
        keyboard.append([InlineKeyboardButton(text="Send Ads", callback_data="ads")])
        keyboard.append([InlineKeyboardButton(text="Clean Users", callback_data="clean")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def create_start_reply_keyboard(self, message=None):
        keyboard = []
        text = "Open Link"
        keyboard.append([KeyboardButton(text=text, web_app=WebAppInfo(url=self.example_url))])

        keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
        return keyboard
