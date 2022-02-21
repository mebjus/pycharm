import numpy as np
import pandas as pd
import os
import requests
from pprint import pprint

token = ' 25945DB021CBCB00A59775B430B5B8BC'

url = 'https://apitest.cityexpress.ru/v1/25945DB021CBCB00A59775B430B5B8BC/Calculate'

df = pd.DataFrame()
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.0F}'.format

for file in fullpaths:
	df1 = pd.read_excel(file, header=2, sheet_name=None)
	df1 = pd.concat(df1, axis=0).reset_index(drop=True)
	df = pd.concat([df, df1], axis=0)

# print(df.info())
# print(df)


def tarif(row):
	row['Режим доставки'] = row['Режим доставки'].upper().strip()
	params = {'cityFrom':row['Отправитель.Адрес.Город'], 'cityTo':row['Получатель.Адрес.Город'],
	          'physicalWeight':row['Расчетный вес'], 'name': row['Режим доставки'], 'quantity': '1', 'width': '5',
	          'height':         '5',
	          'length':         '5'}
	response = requests.get(url, params=params)
	for i in response.json()['Result']:
		if i['Name'].upper() == row['Режим доставки']:
			return i['TotalPrice']


df['price'] = df.loc[:,['Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес', 'Режим доставки']].apply(tarif, axis=1)

print(df['price'])


