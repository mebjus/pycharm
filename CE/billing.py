import numpy as np
import pandas as pd
import os
from pandas.api.types import CategoricalDtype

df = pd.DataFrame()
file = 'data/pay.xls'
df1 = pd.read_excel(file, header=2, sheet_name=None)
df1 = pd.concat(df1, axis=0).reset_index(drop=True)
df = pd.concat([df, df1], axis=0)
df.reset_index()
pd.options.display.float_format = '{:,.2F}'.format

df = df[df['Статус оплаты счета'] == 'Оплачен']
start = df.shape[0]

# df = df[df['Клиент'] == 'ООО «Здоровит»']

def dw(row):
	if row == 0: d = 'понедельник'
	elif row == 1: d = 'вторник'
	elif row == 2: d = 'среда'
	elif row == 3: d = 'четверг'
	elif row == 4: d = 'пятница'
	elif row == 5: d = 'суббота'
	elif row == 6: d = 'воскресенье'
	else: d = np.NAN
	return d
	

dict_fo = {'СЗФО': ['ВЕЛИКИЙ НОВГОРОД', 'МУРМАНСК', 'ПЕТРОЗАВОДСК', 'СЫКТЫВКАР', 'САНКТ-ПЕТЕРБУРГ', 'АРХАНГЕЛЬСК',
                    'КАЛИНИНГРАД'],
           'УФО':  ['КУРГАН', 'НИЖНЕВАРТОВСК', 'НОВЫЙ УРЕНГОЙ', 'СТЕРЛИТАМАК', 'МАГНИТОГОРСК', 'ОРЕНБУРГ', 'СУРГУТ',
                    'ЕКАТЕРИНБУРГ', 'ПЕРМЬ', 'ТЮМЕНЬ', 'УФА', 'ЧЕЛЯБИНСК'],
           'ПФО':  ['ИЖЕВСК', 'ПЕНЗА', 'УЛЬЯНОВСК', 'ЧЕБОКСАРЫ', 'КИРОВ', 'НИЖНИЙ НОВГОРОД', 'КАЗАНЬ', 'САМАРА',
                    'САРАТОВ', 'ТОЛЬЯТТИ'],
           'ЮФО':  ['НОВОРОССИЙСК', 'СИМФЕРОПОЛЬ', 'ПЯТИГОРСК', 'РОСТОВ-НА-ДОНУ', 'ВОЛГОГРАД', 'ВОРОНЕЖ', 'КРАСНОДАР',
                    'СТАВРОПОЛЬ', 'АСТРАХАНЬ', 'СОЧИ'],
           'СФО':  ['БАРНАУЛ', 'НОВОКУЗНЕЦК', 'ТОМСК', 'УЛАН-УДЭ', 'НОВОСИБИРСК', 'КРАСНОЯРСК', 'ОМСК', 'ИРКУТСК',
                    'КЕМЕРОВО'],
           'ДВФО': ['ВЛАДИВОСТОК', 'ХАБАРОВСК']
           }

def ret(cell):  # столбец и ячейку передаю, возрат - округ
	for i in dict_fo.keys():
		if str(cell).upper() in dict_fo[i]:
			return i
	else:
		return 'ЦФО'


df['ФО'] = df['Клиент.Подразделение.Адрес.Город'].apply(ret)
df['ФО'] = df['ФО'].astype('category')

cat_type = CategoricalDtype(categories=['ЦФО', 'СЗФО', 'ПФО', 'ЮФО', 'УФО', 'СФО', 'ДВФО'], ordered=True)
df['ФО'] = df['ФО'].astype(cat_type)

print(df.info())

df['week'] = df['Оплатить до'].dt.dayofweek
df['week'] = df['week'].apply(dw)

print(df['week'].value_counts(normalize=True)*100)

df['delay'] = df['Фактическая дата оплаты'] - df['Оплатить до']
df = df[df['delay'].dt.components.days > 1]
finish = df.shape[0]/start
print('просроченных=', round(finish*100, 2), '%')

lst = ['Статус счета','Статус оплаты счета','week','Сумма с учетом НДС', 'Клиент.Подразделение.Адрес.Город', 'Дата счета']
df.drop(columns=lst, axis=1, inplace=True)

df = df.sort_values(by=['Клиент', 'Оплатить до'], ascending=[True, True])


# def ower_city(row):
# 	if str(row).upper() not in city_dict:
# 		return np.NAN
# 	else:
# 		return row
#
# #### фильтр на свою географю
#
# # df['Отправитель.Адрес.Город'] = df['Отправитель.Адрес.Город'].apply(ower_city)
# # df['Получатель.Адрес.Город'] = df['Получатель.Адрес.Город'].apply(ower_city)
# # df = df.dropna(how='any', axis=0)
#######

writer = pd.ExcelWriter('billing.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='оплаты', startrow=1, index=False, header=False)

workbook = writer.book
worksheet = writer.sheets['оплаты']

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
