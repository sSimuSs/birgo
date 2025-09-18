# pylint: skip-file
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
bot.set_my_description(
"""
Monifi - mualliflarga obunalar, donatlar va raqamli mahsulotlarni sotish orqali o‘z kontentidan daromad topishga yordam beradi.

Obuna yarating, noyob raqamli mahsulotlar ishlab chiqaring, xayriya to‘lovlarini (donat) ulang. Uzcard, Humo, Visa va Mastercard orqali to‘lovlarni qabul qiling va barqaror daromadga ega bo‘ling.

Monifi’ga qo‘shiling va o‘z ijodingizdan pul ishlashni boshlang!
""",
    "uz"
)

bot.set_my_description(
"""
Monifi - помогает авторам зарабатывать на своём контенте через подписки, донаты и продажу цифровых продуктов.

Создавайте подписку, уникальные цифровые продукты, подключайте донаты, принимайте платежи через Uzcard, Humo, Visa и Mastercard и получайте стабильный доход.

Присоединяйтесь к Monifi и начните зарабатывать на своем креативе!
""",
    "ru"
)

bot.set_my_description(
"""
Monifi helps creators earn from their content through subscriptions, donations, and digital product sales.

Create subscriptions, offer unique digital products, enable donations, accept payments via Uzcard, Humo, Visa, and Mastercard, and generate a steady income.

Join Monifi and start monetizing your creativity!
"""
)

bot.set_my_short_description(
    "Obuna va raqamli mahsulotlar savdosi orqali kontentdan ko’proq daromad qiling!\n\nAloqa uchun: @monifi_support",
    "uz"
)

bot.set_my_short_description(
    "Зарабатывайте больше на контенте через продажи подписки и цифровых продукции!\n\nДля связи: @monifi_support",
    "ru"
)

bot.set_my_short_description(
    "Earn more from your content through subscription and digital sales!\n\nFor contact: @monifi_support"
)
