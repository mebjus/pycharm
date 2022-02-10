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
# print(page.title)  # Получаем тег title, отображающийся на вкладке браузера
# print(page.title.text)  # Выводим текст из полученного тега, который содержится в атрибуте text




def wiki_header(url):
    page = BeautifulSoup(requests.get(url).text, 'html.parser')
    header = page.find('h1').text
    return print(header)


# wiki_header('https://en.wikipedia.org/wiki/Operating_system')

print(page.find('div', class_='body').text)

token = ' ... '  # Указываем свой сервисный токен
url = 'https://api.vk.com/method/groups.getMembers'  # Указываем адрес обращения
params = {'group_id': 'vk', 'v': 5.95, 'access_token': token}  # Формируем строку параметров
response = requests.get(url, params=params)  # Посылаем запрос
data = response.json()  # Ответ сохраняем в переменной data в формате словаря
print(data)  # Выводим содержимое переменной data на экран (отображён фрагмент)

print(len(data['response']['items']))

import requests  # Импортируем модуль requests

token = ' ... '  # Указываем свой сервисный токен
url = 'https://api.vk.com/method/groups.getMembers'  # Указываем адрес обращения
count = 5
offset = 0
user_ids = []
max_count = 20
while offset < max_count:
    # Будем выгружать по count=5 пользователей,
    # начиная с того места, где закончили на предыдущей итерации (offset)
    print('Выгружаю {} пользователей с offset = {}'.format(count, offset))
    params = {'group_id': 'vk', 'v': 5.95, 'count': count, 'offset': offset, 'access_token': token}
    response = requests.get(url, params=params)
    data = response.json()
    user_ids += data['response']['items']
    # Увеличиваем смещение на количество строк, которое мы уже выгрузили
    offset += count
print(user_ids)

import requests  # Импортируем модуль requests
import time  # Импортируем модуль time

token = ' ... '  # Указываем свой сервисный токен
url = 'https://api.vk.com/method/groups.getMembers'  # Указываем адрес страницы, к которой делаем запрос
count = 1000
offset = 0
user_ids = []
while offset < 5000:
    params = {'group_id': 'vk', 'v': 5.95, 'count': count, 'offset': offset, 'access_token': token}
    response = requests.get(url, params=params)
    data = response.json()
    user_ids += data['response']['items']
    offset += count
    print('Ожидаю 0.5 секунды...')
    time.sleep(0.5)
print('Цикл завершен, offset =', offset)

import schedule


def task():
    print('Hello! I am a task!')
    return


schedule.every(15).minutes.do(task)

import time

while True:
    schedule.run_pending()
    time.sleep(1)