import numpy as np
import pandas as pd
import os
import requests
from pprint import pprint
import pickle
import math
from pandas.api.types import CategoricalDtype


df = pd.DataFrame()
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.2F}'.format

for file in fullpaths:
	df1 = pd.read_excel(file, header=2, sheet_name=None)
	df1 = pd.concat(df1, axis=0).reset_index(drop=True)
	df = pd.concat([df, df1], axis=0)

price_dict = {}
price_freq = {}
price_freq_money = {}
price_freq_public = {}

filename = 'price.bin'
with open(filename, 'rb') as f:
	price_dict = pickle.load(open(filename, 'rb'))

###########

dirname = 'data/размер тн.xlsx'
df_tn = pd.read_excel(dirname)

df_tn['Дата'] = df_tn['Дата'].dt.to_period('D')
df['Дата Cоздания'] = df['Дата Cоздания'].dt.to_period('D')

df = df.merge(df_tn, left_on='Дата Cоздания', right_on='Дата', how='left')
df['Размер'] = df['Размер'] + 1

counter = 0


#
# ##########   ограничения на веса и стоимость
# df = df[df['Расчетный вес'] <= 0.25]
# df = df[df['Общая стоимость со скидкой'] > 220]

df = df[df['Общая стоимость со скидкой'] > 0]



df['Заказ.Клиент.Не применять топливную надбавку'] = df['Заказ.Клиент.Не применять топливную надбавку'].fillna(0)


def fuel(row):
	if row['Заказ.Клиент.Не применять топливную надбавку'] == 1:
		return 1
	else:
		return row['Размер']


df['tn'] = df.loc[:, ['Заказ.Клиент.Не применять топливную надбавку', 'Размер']].apply(fuel, axis=1)

df = df[~df['Режим доставки'].isin(
	['ЭКСПРЕСС возврат документов', 'ЛОЖНЫЙ ВЫЗОВ', 'СКЛАД', 'ЭКСПРЕСС Груз', 'ВТОРИЧНАЯ ДОСТАВКА',
	 'СИБИРСКИЙ ЭКСПРЕСС  Для физ.лиц', 'ВОЛЖСКИЙ ЭКСПРЕСС  склад-дверь до 0,5 кг', 'ЭКСПРЕСС B', 'ПРАЙМ А',
	 'ЭКСПРЕСС А', 'ПРАЙМ B', 'ЭКОНОМ  склад-склад', 'ЮЖНЫЙ ЭКСПРЕСС  дверь-дверь', 'ЮЖНЫЙ ЭКСПРЕСС  дверь-склад',
	 'ЭКСПРЕСС ДАЛЬНИЙ ВОСТОК  Для физ.лиц'])]


def mod(arg):
	if arg.find('ЭКСПРЕСС') != -1:
		return 'ЭКСПРЕСС'
	elif arg.find('ПРАЙМ') != -1:
		return 'ПРАЙМ'
	elif arg.find('ОПТИМА') != -1:
		return 'ОПТИМА'
	else:
		return 'ПРОЧИЕ'


df['Режим'] = df['Режим доставки'].apply(mod)
df['Режим'] = df['Режим'].astype('category')


def old(row):
	global counter
	counter += 1
	row['Режим доставки'] = row['Режим доставки'].upper()
	lst = (row['Отправитель.Адрес.Город'], row['Получатель.Адрес.Город'], row['вес'], row['Режим доставки'])
	if lst in price_dict.keys():
        print(counter)
		if price_freq.get(lst) == None: price_freq[lst] = 0
		if price_freq_money.get(lst) == None: price_freq_money[lst] = 0
		price_freq[lst] += 1
		if price_dict[lst] != 'нет тарифа': price_freq_money[lst] += row['Общая стоимость со скидкой']
		return price_dict[lst]
	else:
		return -1


def round_custom(num, step):
	return math.ceil(num / step) * step


def weight(row):
	if row['Вид доставки'] == 'Междугородная':
		if row['Режим доставки'] == 'ЭКОНОМ  склад-склад': return round_custom(row['Расчетный вес'], 1)
		if row['Расчетный вес'] <= 0.5:
			return 0.5
		elif (row['Расчетный вес'] > 0.5) and (row['Расчетный вес'] <= 20):
			return round_custom(row['Расчетный вес'], 0.5)
		elif (row['Расчетный вес'] > 20):
			return round_custom(row['Расчетный вес'], 1)

	if row['Вид доставки'] == 'Международная': return round_custom(row['Расчетный вес'], 0.5)

	if row['Вид доставки'] == 'Местная' and row['Отправитель.Адрес.Город'] == 'Москва':
		if row['Режим'] == 'ПРАЙМ' or row['Режим'] == 'ЭКСПРЕСС':
			if row['Расчетный вес'] <= 1:
				return round_custom(row['Расчетный вес'], 0.25)
			elif row['Расчетный вес'] > 1:
				return round_custom(row['Расчетный вес'], 1)

	if row['Вид доставки'] == 'Областная' and row['Отправитель.Адрес.Город'] == 'Москва':
		if row['Расчетный вес'] <= 1:
			return round_custom(row['Расчетный вес'], 0.5)
		elif row['Расчетный вес'] > 1:
			return round_custom(row['Расчетный вес'], 1)

	if row['Вид доставки'] == 'Местная' and row['Отправитель.Адрес.Город'] == 'Санкт-Петербург':
		if row['Режим'] == 'ПРАЙМ' or row['Режим'] == 'ЭКСПРЕСС':
			if row['Расчетный вес'] <= 1:
				return round_custom(row['Расчетный вес'], 0.25)
			elif row['Расчетный вес'] > 1:
				return round_custom(row['Расчетный вес'], 1)

	if row['Вид доставки'] == 'Областная' and row['Отправитель.Адрес.Город'] == 'Санкт-Петербург':
		if row['Расчетный вес'] <= 1: return round_custom(row['Расчетный вес'], 1)

	if row['Вид доставки'] == 'Местная' and row['Отправитель.Адрес.Город'] != 'Москва' and row[
		'Отправитель.Адрес.Город'] != 'Санкт-Петербург':
		if row['Режим'] == 'ПРАЙМ' or row['Режим'] == 'ЭКСПРЕСС' or row['Режим'] == 'ОПТИМА':
			if row['Расчетный вес'] <= 1:
				return round_custom(row['Расчетный вес'], 1)
			elif row['Расчетный вес'] > 1:
				return round_custom(row['Расчетный вес'], 1)

	if row['Вид доставки'] == 'Областная' and row['Отправитель.Адрес.Город'] != 'Москва' and row[
		'Отправитель.Адрес.Город'] != 'Санкт-Петербург':
		if row['Расчетный вес'] <= 1:
			return round_custom(row['Расчетный вес'], 1)
		elif row['Расчетный вес'] > 1:
			return round_custom(row['Расчетный вес'], 1)
	return row['Расчетный вес']


df['Общая стоимость со скидкой'] = df['Общая стоимость со скидкой'].fillna(0)

df['вес'] = df.loc[:, ['Вид доставки', 'Расчетный вес', 'Режим доставки', 'Режим', 'Отправитель.Адрес.Город',
                       'Получатель.Адрес.Город']].apply(weight, axis=1)

df['price'] = df.loc[:, ['Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'вес', 'Режим доставки',
                         'Общая стоимость со скидкой']].apply(
	old, axis=1)

df['price'] = df['price'].fillna(0)

# df['price'] = df.loc[:, ['Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'вес', 'Режим доставки',
#                          'Общая стоимость со скидкой', 'price']].apply(
# 	old_2, axis=1)


# print(len(price_dict))


######### частота направлений
sorted_dict = {}
sorted_dict_money = {}
sorted_dict_money_public = {}

sorted_keys = sorted(price_freq, key=price_freq.get, reverse=True)
sorted_keys_money = sorted(price_freq_money, key=price_freq_money.get, reverse=True)
sorted_keys_money_public = sorted(price_freq_public, key=price_freq_public.get, reverse=True)

for w in sorted_keys:
	sorted_dict[w] = price_freq[w]
for w in sorted_keys_money:
	sorted_dict_money[w] = price_freq_money[w]
for w in sorted_keys_money_public:
	sorted_dict_money_public[w] = price_freq_public[w]

df_dict = pd.DataFrame(sorted_dict.items(), columns=['Кортеж', 'Кол отправлений'])
df_dict_money = pd.DataFrame(sorted_dict_money.items(), columns=['Кортеж', 'Продали'])

print('размер df=', df.shape[0])

# print(df[df['Режим']=='ПРОЧИЕ']['Общая стоимость со скидкой'].sum())

# print(df_dict_money['Продали'].sum())

# s=0
# for w in price_freq.values():
# 	s += w
# print(s)

df_dict_money_public = pd.DataFrame(sorted_dict_money_public.items(), columns=['Кортеж', 'Паблик'])

df_dict['Кол отправлений'].dropna(inplace=True)
df_dict_money['Продали'].dropna(inplace=True)
df_dict_money_public['Паблик'].dropna(inplace=True)

df_dict = df_dict.merge(df_dict_money, how='left')
df_dict = df_dict.merge(df_dict_money_public, how='left')

# df_dict = df_dict[df_dict['Кол отправлений'] > 0]

# print(df_dict)




df1 = df[df['price'] == -1]
df2 = df[df['price'] == 'нет тарифа']

df = df[df['price'] != -1]
df = df[df['price'] != 'нет тарифа']

df['price'] = df['price'] * df['tn']

df = df[df['price'] > 0]

df['discount'] = (df['Общая стоимость со скидкой'] / df['price']) - 1

df_group = df.groupby('Клиент')[['price', 'Общая стоимость со скидкой']].agg(
	{'price': 'sum', 'Общая стоимость со скидкой': 'sum'})
df_group = df_group.reset_index()
df_group['discount'] = (df_group['Общая стоимость со скидкой'] / df_group['price']) - 1

df = df.loc[:,
     ['Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес',
      'вес', 'Режим доставки', 'Вид доставки',
      'Общая стоимость со скидкой', 'price', 'tn', 'discount']]

df2 = df2.loc[:,
      ['Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес',
       'вес', 'Режим доставки', 'Вид доставки',
       'Общая стоимость со скидкой', 'price', 'tn']]

writer = pd.ExcelWriter('цены.xlsx', engine='xlsxwriter')


df_dict.to_excel(writer, sheet_name='популярность', startrow=1, index=False)

# df_dict
workbook = writer.book

worksheet4 = writer.sheets['популярность']

format = workbook.add_format({'border': 1, 'bg_color': '#E8FBE1', 'num_format': '#,##0'})
worksheet4.set_column('A:B', 50, format)
worksheet4.set_column('B:D', 15, format)



writer.save()
