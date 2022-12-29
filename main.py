from requests import get
from datetime import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='5960666175:AAE-Syn5EWu_GYd9gJckR1QT-PZJrwEIVds')
db = Dispatcher(bot)

@db.message_handler(commands=["go"])
async def start_command(message: types.Message):
    await message.reply('Привет!\nНапиши мне название города и я пришлю сводку погоды!')


@db.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {"Clear": "Ясно \U00002600", "Clouds": "Облачно \U00002601", "Rain": "Дождь \U00002614",
        "Show": "Снег \U0001F328"}
    try:
        r = get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={'c71e63fa8ac486fa77c2e6c20cc82798'}&units=metric")
        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        wheather_description = data["weather"][0]["main"]
        if wheather_description in code_to_smile:
            wd = code_to_smile[wheather_description]
        else:
            wd = 'Посмотри в окно, не пойму что там за погода!'

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.now().strftime('%d-%m-%Y %H:%M')}***\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp.strftime('%d-%m-%Y %H:%M')}\nЗакат солнца: {sunset_timestamp.strftime('%d-%m-%Y %H:%M')}\nПродолжительность дня: {length_of_the_day}\n"
                            f"Хорошего дня")
    except:
        await message.reply('проверьте название города')


if __name__ == '__main__':

    executor.start_polling(db)