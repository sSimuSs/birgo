# pylint: skip-file
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
bot.set_my_description(
"""
BirGo — shaharlararo sayohatlarni topishning eng oson yo‘li.
Biz yo‘lovchilar va haydovchilarni darhol bog‘laymiz, Telegram guruhlari, cheksiz xabarlar yoki qo‘ng‘iroqlarsiz. Mavjud haydovchilarni, bo‘sh o‘rinlarni, narxlarni va jo‘nash vaqtini bir joyda ko‘ring.
BirGo Angren–Toshkent yo‘nalishini hamma uchun tezroq, sodda va ishonchli qiladi.
""",
    "uz"
)

bot.set_my_description(
"""
BirGo — это самый простой способ найти поездки между городами.
Мы мгновенно соединяем пассажиров и водителей, без Telegram-групп, бесконечных сообщений или звонков. Смотрите доступных водителей, свободные места, цены и время отправления — всё в одном месте.
BirGo делает маршрут Ангрен–Ташкент быстрее, проще и надёжнее для всех.
""",
    "ru"
)

bot.set_my_description(
"""
BirGo is the easiest way to find intercity rides.
We connect passengers and drivers instantly, without Telegram groups, endless messages, or phone calls. See available drivers, free seats, prices, and departure time — all in one place.
BirGo makes the Angren–Tashkent route faster, simpler, and more reliable for everyone.
"""
)

bot.set_my_short_description(
    "BirGo yo‘lovchi va haydovchilarni bir zumda bog‘laydi — kutishsiz, tartibsizliksiz, stresssiz",
    "uz"
)

bot.set_my_short_description(
    "BirGo мгновенно соединяет пассажиров и водителей — без ожиданий, хаоса и стресса",
    "ru"
)

bot.set_my_short_description(
    "BirGo connects passengers and drivers instantly — no waiting, no chaos, no stress"
)
