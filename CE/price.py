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


tn = 1.22
price_dict = {}

#### сделать буфер
# список из кортеж ключ - значение цена


def tarif(row):
	row['Режим доставки'] = row['Режим доставки'].upper().strip()

	lst = (row['Отправитель.Адрес.Город'], row['Получатель.Адрес.Город'], row['Расчетный вес'], row['Режим доставки'])

	if lst in price_dict.keys():
		print(price_dict[lst], '*')
		return price_dict[lst]

	params = {'cityFrom':       row['Отправитель.Адрес.Город'], 'cityTo': row['Получатель.Адрес.Город'],
	          'physicalWeight': row['Расчетный вес'], 'name': row['Режим доставки'], 'quantity': '1', 'width': '5',
	          'height':         '5',
	          'length':         '5'}
	response = requests.get(url, params=params)

	for i in response.json()['Result']:
		if i['Name'].upper() == row['Режим доставки']:
			print(round(i['TotalPrice'] * tn, 2))
			price_dict[lst] = i['TotalPrice'] * tn
			return price_dict[lst]


df['price'] = df.loc[:, ['Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес', 'Режим доставки']].apply(
	tarif, axis=1)

print(price_dict)
print(len(price_dict))


df = df.loc[:, ['Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес', 'Режим доставки',
                'Общая стоимость со скидкой', 'price']]

writer = pd.ExcelWriter('цены.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='итоги', startrow=1, index=False, header=False)

workbook = writer.book
worksheet = writer.sheets['итоги']

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
