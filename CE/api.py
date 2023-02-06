import requests
import json
import pprint

url = 'https://apitest.cityexpress.ru/v1/B6943005F57A8F24962C9DCC6537FC7F/Calculate'

params = {'cityFrom': 'Москва', 'cityTo': 'Красноярск', 'physicalWeight': '3.5', 'quantity': '1', 'width': '5', 'height': '5',
          'length': '5'}
response = requests.get(url, params=params)


for i in response.json()['Result']:
    if i['Name'].upper() == 'ОПТИМА':
        print(i['TotalPrice'])


# for i in response.json()['Result']:
#     print(i)
