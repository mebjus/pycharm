import numpy as np
import pandas as pd
import os
from pandas.api.types import CategoricalDtype

df = pd.DataFrame()
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.0F}'.format

for file in fullpaths:
	df1 = pd.read_excel(file, header=2, sheet_name=None)
	df1 = pd.concat(df1, axis=0).reset_index(drop=True)
	df = pd.concat([df, df1], axis=0)

dirname = 'data/day_of_month.xlsx'
df_m = pd.read_excel(dirname)
df_m.reset_index()
mounth = {}

for i in df_m.index:
	mounth[df_m.iloc[i]['Дата']] = df_m.iloc[i]['р.д.']

df['Дата Cоздания'] = df['Дата Cоздания'].dt.to_period('D')

######

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


df['ФО'] = df['Заказ.Клиент.Подразделение.Адрес.Город'].apply(ret)
df['ФО'] = df['ФО'].astype('category')

#### фильтр на свою географю

# df['Отправитель.Адрес.Город'] = df['Отправитель.Адрес.Город'].apply(ower_city)
# df['Получатель.Адрес.Город'] = df['Получатель.Адрес.Город'].apply(ower_city)
# df = df.dropna(how='any', axis=0)


# установить порядок в списке ФО
cat_type = CategoricalDtype(categories=['ЦФО', 'СЗФО', 'ПФО', 'ЮФО', 'УФО', 'СФО', 'ДВФО'], ordered=True)
df['ФО'] = df['ФО'].astype(cat_type)

# отбрасываем все условия:

df = df[df['Общая стоимость со скидкой'] > 50]
df = df[df['ФО'] == 'ЦФО']
# df = df[df['Клиент'] == 'ООО "СИНТЕГА"']

def moscow(row):
	if row != 'nan' and str(row)[:3] == '770': return row
	else: return np.NAN

df['Прием курьером.Пакеты доставки.Курьер.Номер курьера'] = df['Прием курьером.Пакеты доставки.Курьер.Номер курьера'].apply(moscow)
df['Доставка курьером.Пакеты доставки.Курьер.Номер курьера'] = df['Доставка курьером.Пакеты доставки.Курьер.Номер курьера'].apply(moscow)

df1 = df.copy()
df2 = df.copy()
df1['Прием курьером.Пакеты доставки.Курьер.Номер курьера'] = df1['Прием курьером.Пакеты доставки.Курьер.Номер курьера'].astype(str)
df2['Доставка курьером.Пакеты доставки.Курьер.Номер курьера'] = df2['Доставка курьером.Пакеты доставки.Курьер.Номер курьера'].astype(str)

df1 = df1.groupby('Дата Cоздания')['Прием курьером.Пакеты доставки.Курьер.Номер курьера'].agg(size= len, set= lambda x: set(x))
df2 = df2.groupby('Дата Cоздания')['Доставка курьером.Пакеты доставки.Курьер.Номер курьера'].agg(size= len, set= lambda x: set(x))

df1['set2'] = df2['set']


def discarded(row):
	return row.discard('nan')

df1['set_all'] = df1.apply(lambda x: x.set.union(x.set2), axis=1)
df1['количество'] = df1['set_all'].apply(discarded)
df1['количество'] = df1['set_all'].apply(lambda x: len(x))
df1 = df1.drop(columns=['set', 'set2', 'size'])
df1 = df1.reset_index()
print(df1.info())
######

writer = pd.ExcelWriter('курьеры.xlsx', engine='xlsxwriter')
df1.to_excel(writer, sheet_name='итоги', startrow=1, index=False, header=False)

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

for col_num, value in enumerate(df1.columns.values):
	worksheet.write(0, col_num, value, header_format)

writer.save()
