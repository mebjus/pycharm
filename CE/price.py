import numpy as np
import pandas as pd
import os
import requests
from pprint import pprint
import pickle
import math
from pandas.api.types import CategoricalDtype

token = '25945DB021CBCB00A59775B430B5B8BC'

url = 'https://apitest.cityexpress.ru/v1/25945DB021CBCB00A59775B430B5B8BC/Calculate'
# url = 'https://api.cityexpress.ru/v1/25945DB021CBCB00A59775B430B5B8BC/Calculate'


df = pd.DataFrame()
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.0F}'.format

for file in fullpaths:
    df1 = pd.read_excel(file, header=2, sheet_name=None)
    df1 = pd.concat(df1, axis=0).reset_index(drop=True)
    df = pd.concat([df, df1], axis=0)

price_dict = {}
price_freq = {}

filename = 'price.bin'
with open(filename, 'rb') as f:
    price_dict = pickle.load(open(filename, 'rb'))
###########
print(len(price_dict))
tn = 1.22
counter = 0

dict_fo = {'СЗФО': ['ВЕЛИКИЙ НОВГОРОД', 'МУРМАНСК', 'ПЕТРОЗАВОДСК', 'СЫКТЫВКАР', 'САНКТ-ПЕТЕРБУРГ', 'АРХАНГЕЛЬСК',
                    'КАЛИНИНГРАД'],
           'УФО': ['КУРГАН', 'НИЖНЕВАРТОВСК', 'НОВЫЙ УРЕНГОЙ', 'СТЕРЛИТАМАК', 'МАГНИТОГОРСК', 'ОРЕНБУРГ', 'СУРГУТ',
                   'ЕКАТЕРИНБУРГ', 'ПЕРМЬ', 'ТЮМЕНЬ', 'УФА', 'ЧЕЛЯБИНСК'],
           'ПФО': ['ИЖЕВСК', 'ПЕНЗА', 'УЛЬЯНОВСК', 'ЧЕБОКСАРЫ', 'КИРОВ', 'НИЖНИЙ НОВГОРОД', 'КАЗАНЬ', 'САМАРА',
                   'САРАТОВ', 'ТОЛЬЯТТИ'],
           'ЮФО': ['НОВОРОССИЙСК', 'СИМФЕРОПОЛЬ', 'ПЯТИГОРСК', 'РОСТОВ-НА-ДОНУ', 'ВОЛГОГРАД', 'ВОРОНЕЖ', 'КРАСНОДАР',
                   'СТАВРОПОЛЬ', 'АСТРАХАНЬ', 'СОЧИ'],
           'СФО': ['БАРНАУЛ', 'НОВОКУЗНЕЦК', 'ТОМСК', 'УЛАН-УДЭ', 'НОВОСИБИРСК', 'КРАСНОЯРСК', 'ОМСК', 'ИРКУТСК',
                   'КЕМЕРОВО'],
           'ДВФО': ['ВЛАДИВОСТОК', 'ХАБАРОВСК']}

df['Заказ.Клиент.Не применять топливную надбавку'] = df['Заказ.Клиент.Не применять топливную надбавку'].fillna(0)

df['tn'] = df['Заказ.Клиент.Не применять топливную надбавку'].apply(lambda x: 1 if x == 1 else tn)

df = df[~df['Режим доставки'].isin(
    ['ЭКСПРЕСС возврат документов', 'ЛОЖНЫЙ ВЫЗОВ', 'СКЛАД', 'ЭКСПРЕСС Груз', 'ВТОРИЧНАЯ ДОСТАВКА',
     'СИБИРСКИЙ ЭКСПРЕСС  Для физ.лиц', 'ВОЛЖСКИЙ ЭКСПРЕСС  склад-дверь до 0,5 кг', 'ЭКСПРЕСС B', 'ПРАЙМ А',
     'ЭКСПРЕСС А', 'ПРАЙМ B', 'ЭКОНОМ  склад-склад', 'ЮЖНЫЙ ЭКСПРЕСС  дверь-дверь',
     'ЭКСПРЕСС ДАЛЬНИЙ ВОСТОК  Для физ.лиц'])]


def ret(cell):  # столбец и ячейку передаю, возрат - округ
    for i in dict_fo.keys():
        if str(cell).upper() in dict_fo[i]:
            return i
    else:
        return 'ЦФО'


df['ФО'] = df['Заказ.Клиент.Подразделение.Адрес.Город'].apply(ret)
df['ФО'] = df['ФО'].astype('category')

cat_type = CategoricalDtype(categories=['ЦФО', 'СЗФО', 'ПФО', 'ЮФО', 'УФО', 'СФО', 'ДВФО'], ordered=True)
df['ФО'] = df['ФО'].astype(cat_type)


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
    row['Режим доставки'] = row['Режим доставки'].upper()
    lst = (row['Отправитель.Адрес.Город'], row['Получатель.Адрес.Город'], row['вес'], row['Режим доставки'])
    if price_freq.get(lst) == None: price_freq[lst] = 0
    if lst in price_dict.keys():
        price_freq[lst] += 1
        return price_dict[lst]
    else:
        return -1


def tarif(row):
    global counter
    lst = (row['Отправитель.Адрес.Город'], row['Получатель.Адрес.Город'], row['вес'], row['Режим доставки'])
    row['Режим доставки'] = row['Режим доставки'].upper().strip()
    if lst in price_dict.keys(): return price_dict[lst]
    if row['price'] == -1:
        params = {'cityFrom': row['Отправитель.Адрес.Город'], 'cityTo': row['Получатель.Адрес.Город'],
                  'physicalWeight': row['вес'], 'name': row['Режим доставки'], 'quantity': '1', 'width': '5',
                  'height': '5',
                  'length': '5'}
        response = requests.get(url, params=params)
        for i in response.json()['Result']:
            if i['Name'].upper() == row['Режим доставки']:
                counter += 1
                print(counter, ':', row['Режим доставки'].capitalize(), ':', round(i['TotalPrice'], 0))
                price_dict[lst] = i['TotalPrice']
                return i['TotalPrice']
    price_dict[lst] = 'нет тарифа'
    return 'нет тарифа'


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


df['вес'] = df.loc[:, ['Вид доставки', 'Расчетный вес', 'Режим доставки', 'Режим', 'Отправитель.Адрес.Город',
                       'Получатель.Адрес.Город']].apply(weight, axis=1)
df['price'] = df.loc[:, ['Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'вес', 'Режим доставки']].apply(
    old, axis=1)

df['price'] = df.loc[:, ['Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'вес', 'Режим доставки', 'price']].apply(tarif, axis=1)

print(len(price_dict))

######### частота направлений
sorted_dict = {}
sorted_keys = sorted(price_freq, key=price_freq.get)
for w in sorted_keys:
    sorted_dict[w] = price_freq[w]

for i,j in sorted_dict.items():
    if j > 10:
        print(i, j)

###### очистить "нет тарифа"

# dict_new = {}
# for i, j in price_dict.items():
# 	if j != 'нет тарифа':
# 		# print(i, j)
# 		dict_new[i] = j
# price_dict = dict_new.copy()
# print(len(price_dict))
# #######

f = open('price.bin', 'wb')
pickle.dump(price_dict, f)
f.close()

df1 = df[df['price'] == -1]
df2 = df[df['price'] == 'нет тарифа']

df = df[df['price'] != -1]
df = df[df['price'] != 'нет тарифа']

df['price'] = df['price'] * df['tn']

df = df[df['Общая стоимость со скидкой'] > 0]
df = df[df['price'] > 0]

df['discount'] = ((df['Общая стоимость со скидкой'] / df['price'])) - 1

df_group = df.groupby('Клиент')[['price', 'Общая стоимость со скидкой']].agg({'price': 'sum', 'Общая стоимость со скидкой': 'sum'})
df_group = df_group.reset_index()


df = df.loc[:,
     ['ФО', 'Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес',
      'вес', 'Режим доставки', 'Вид доставки',
      'Общая стоимость со скидкой', 'price', 'tn', 'discount']]
df1 = df1.loc[:,
      ['ФО', 'Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес',
       'вес', 'Режим доставки', 'Вид доставки',
       'Общая стоимость со скидкой', 'price', 'tn']]
df2 = df2.loc[:,
      ['ФО', 'Клиент', 'Номер отправления', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'Расчетный вес',
       'вес', 'Режим доставки', 'Вид доставки',
       'Общая стоимость со скидкой', 'price', 'tn']]



writer = pd.ExcelWriter('цены.xlsx', engine='xlsxwriter')

df.to_excel(writer, sheet_name='итоги', startrow=1, index=False, header=False)
# df1.to_excel(writer, sheet_name='нет тарифа', startrow=1, index=False, header=False)
df2.to_excel(writer, sheet_name='не определен', startrow=1, index=False, header=False)
df_group.to_excel(writer, sheet_name='группировка', startrow=1, index=False, header=False)

workbook = writer.book

worksheet = writer.sheets['итоги']
# worksheet2 = writer.sheets['нет тарифа']
worksheet3 = writer.sheets['не определен']
worksheet4 = writer.sheets['группировка']

header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'vcenter',
    'fg_color': '#D7E4BC',
    'align': 'center_across',
    'num_format': '#,##0',
    'border': 1})

for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num, value, header_format)
for col_num, value in enumerate(df_group.columns.values):
    worksheet4.write(0, col_num, value, header_format)
writer.save()
