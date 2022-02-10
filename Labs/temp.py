#### api ####

import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup


# url = 'https://www.cbr-xml-daily.ru/daily_json.js'  # Определяем значение URL страницы для запроса
# response = requests.get(url)
#
# currencies = response.json()  # Применяем метод json()
# # pprint(currencies['Valute']['AMD']['Value'])
# print(currencies['Valute']['CZK']['Name'])


url = 'https://nplus1.ru/news/2021/10/11/econobel2021'  # Определяем адрес страницы
response = requests.get(url)  # Выполняем GET-запрос, содержимое ответа присваивается переменной response
page = BeautifulSoup(response.text, 'html.parser')  # Создаём объект BeautifulSoup, указывая html-парсер
print(page.title)  # Получаем тег title, отображающийся на вкладке браузера
print(page.title.text)  # Выводим текст из полученного тега, который содержится в атрибуте text