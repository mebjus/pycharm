import numpy as np
import pandas as pd
import os
import requests
from pprint import pprint
import pickle

token = '25945DB021CBCB00A59775B430B5B8BC'

url = 'https://apitest.cityexpress.ru/v1/25945DB021CBCB00A59775B430B5B8BC/Calculate'

df = pd.DataFrame()
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
# pd.options.display.float_format = '{:,.0F}'.format

for file in fullpaths:
	df1 = pd.read_excel(file, header=2, sheet_name=None)
	df1 = pd.concat(df1, axis=0).reset_index(drop=True)
	df = pd.concat([df, df1], axis=0)

price_dict = {}

###### если новый размер тн - закомментировать на первый запуск
filename = 'price.bin'
with open(filename, 'rb') as f:
	price_dict = pickle.load(open(filename, 'rb'))
###########
tn = 1.22
counter = 0

df['Заказ.Клиент.Не применять топливную надбавку'] = df['Заказ.Клиент.Не применять топливную надбавку'].fillna(0)

df['tn'] = df['Заказ.Клиент.Не применять топливную надбавку'].apply(lambda x: 1 if x == 1 else tn)

df = df[~df['Режим доставки'].isin(
	['ЭКСПРЕСС возврат документов', 'ЛОЖНЫЙ ВЫЗОВ', 'СКЛАД', 'ЭКСПРЕСС Груз', 'ВТОРИЧНАЯ ДОСТАВКА',
	 'СИБИРСКИЙ ЭКСПРЕСС  Для физ.лиц', 'ВОЛЖСКИЙ ЭКСПРЕСС  склад-дверь до 0,5 кг', 'ЭКСПРЕСС B', 'ПРАЙМ А',
	 'ЭКСПРЕСС А', 'ПРАЙМ B', 'ЭКОНОМ  склад-склад', 'ЮЖНЫЙ ЭКСПРЕСС  дверь-дверь', 'ЭКСПРЕСС ДАЛЬНИЙ ВОСТОК  Для физ.лиц'])]

def old(row):
	row['Режим доставки'] = row['Режим доставки'].upper()
	lst = (row['Отправитель.Адрес.Город'], row['Получатель.Адрес.Город'], row['Расчетный вес'], row['Режим доставки'])
	if lst in price_dict.keys():
		print(price_dict[lst], '*')
		return price_dict[lst]
	else:
		return -1



def tarif(row):
	global counter
	if row['price'] == -1:
		row['Режим доставки'] = row['Режим доставки'].upper().strip()
		lst = (
			row['Отправитель.Адрес.Город'], row['Получатель.Адрес.Город'], row['Расчетный вес'], row['Режим доставки'])
		params = {'cityFrom':       row['Отправитель.Адрес.Город'], 'cityTo': row['Получатель.Адрес.Город'],
		          'physicalWeight': row['Расчетный вес'], 'name': row['Режим доставки'], 'quantity': '1', 'width': '5',
		          'height':         '5',
		          'length':         '5'}
		response = requests.get(url, params=params)
		# print(row['Режим доставки'])
		for i in response.json()['Result']:
			if i['Name'].upper() == row['Режим доставки']:
				counter += 1
				print(counter, '-')
				print(round(i['TotalPrice'], 2))
				price_dict[lst] = i['TotalPrice']
				return price_dict[lst]
			else:
				price_dict[lst] = 'нет тарифа'
				return price_dict[lst]
	else:
		return row['price']


df['price'] = df.loc[:, ['Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес', 'Режим доставки']].apply(
	old, axis=1)

df['price'] = df.loc[:,
              ['Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес', 'Режим доставки', 'price']].apply(
	tarif, axis=1)

print(len(price_dict))

df1=df[df['price'] == 'нет тарифа']
df = df[df['price'] != 'нет тарифа']
df['price'] = df['price'] * df['tn']
df2 = df[df['price'] == '']


df = df[df['Общая стоимость со скидкой'] > 0]
df = df[df['price'] > 0]

df['discount'] = ((df['Общая стоимость со скидкой'] / df['price'])*100)-100


df = df.loc[:, ['Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес',
                'Режим доставки',
                'Общая стоимость со скидкой', 'price', 'tn', 'discount']]
df1 = df1.loc[:, ['Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес',
                'Режим доставки',
                'Общая стоимость со скидкой', 'price', 'tn']]
df2 = df2.loc[:, ['Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес',
                'Режим доставки',
                'Общая стоимость со скидкой', 'price', 'tn']]

f = open('price.bin', 'wb')
pickle.dump(price_dict, f)
f.close()

writer = pd.ExcelWriter('цены.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='итоги', startrow=1, index=False, header=False)
df1.to_excel(writer, sheet_name='нет тарифа', startrow=1, index=False, header=False)
df2.to_excel(writer, sheet_name='не определен', startrow=1, index=False, header=False)
workbook = writer.book
worksheet = writer.sheets['итоги']
worksheet2 = writer.sheets['нет тарифа']
worksheet3 = writer.sheets['не определен']

header_format = workbook.add_format({
	'bold':       True,
	'text_wrap':  True,
	'valign':     'vcenter',
	'fg_color':   '#D7E4BC',
	'align':      'center_across',
	'num_format': '#,##0',
	'border':     1})

for col_num, value in enumerate(df.columns.values):
	worksheet.write(0, col_num, value, header_format)


writer.save()
