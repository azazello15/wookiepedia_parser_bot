from aiogram import types, executor, Dispatcher, Bot
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

bot = Bot(token='Ваш телеграм-токен')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, 'Привет фанат Звездных войн')


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    url = 'https://starwars.fandom.com/ru/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA?query=' + message.text
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    links = soup.find_all('li', class_='unified-search__result')
    if len(links) > 0:
        url = links[0].find("a").get("href")

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 200)")
    driver.save_screenshot("img.png")
    driver.close()

    photo = open("img.png", "rb")
    await bot.send_photo(message.chat.id, photo=photo, caption=f'Ссылка на статью : <a href="{url}">тык</a>', parse_mode="HTML")



executor.start_polling(dp)
