# pylint: skip-file
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
bot.set_my_description(
"""
Wishr — bu e'lonlar taxtasining yangi turi. 
Bu yerda hammasi mahsulotdan emas, sizga kerakli narsalardan boshlanadi. 
O‘zingiz xohlagan narsani yozing — va sotuvchilar taklif yuborishadi.
""",
    "uz"
)

bot.set_my_description(
"""
Wishr — это доска объявлений наоборот. 
Здесь всё начинается не с товара, а с вашего желания. 
Опишите, что вам нужно — и продавцы сами предложат цену и условия.
""",
    "ru"
)

bot.set_my_description(
"""
Wishr is a reverse marketplace. 
Here, everything starts not with a product — but with your wish. 
Describe what you need, and sellers will offer their prices and terms.
"""
)

bot.set_my_short_description(
    "Istagingizni yozing. Haqiqiy takliflarni oling",
    "uz"
)

bot.set_my_short_description(
    "Разместите хотелку. Получайте реальные предложения",
    "ru"
)

bot.set_my_short_description(
    "Post your wish. Get real offers"
)
