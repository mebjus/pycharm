import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.DataFrame
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name : os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.0F}'.format

for file in fullpaths :
	if df.empty :
		if file.find('.xls') != -1 :
			df = pd.read_excel(file, header=2, sheet_name=None)
			df = pd.concat(df, axis=0).reset_index(drop=True)
	else :
		if file.find('.xls') != -1 :
			df1 = pd.read_excel(file, header=2, sheet_name=None)
			df1 = pd.concat(df1, axis=0).reset_index(drop=True)
			df = pd.concat([df, df1], axis=0)

dirname = 'data/day_of_month.xlsx'
df_m = pd.read_excel(dirname)
df_m.reset_index()
mounth = {}

df_m['Дата'] = df_m['Дата'].dt.strftime('%Y-%m')
for i in df_m.index :
	mounth[df_m.iloc[i]['Дата']] = df_m.iloc[i]['р.д.']

dupl = list(df.columns)
df_dupl = df[df.duplicated(subset=dupl)]
df_dupl.index.nunique()
df = df.drop_duplicates(subset=dupl)

df['Дата Cоздания'] = pd.to_datetime(df['Дата Cоздания']).dt.strftime('%Y-%m')
df['р.д.'] = df['Дата Cоздания'].apply(lambda x: mounth[str(x)])

dict_fo = {'СЗФО' : ['ВЕЛИКИЙ НОВГОРОД', 'МУРМАНСК', 'ПЕТРОЗАВОДСК', 'СЫКТЫВКАР', 'САНКТ-ПЕТЕРБУРГ', 'АРХАНГЕЛЬСК',
	'КАЛИНИНГРАД'],
	'УФО' : ['КУРГАН', 'НИЖНЕВАРТОВСК', 'НОВЫЙ УРЕНГОЙ', 'СТЕРЛИТАМАК', 'МАГНИТОГОРСК', 'ОРЕНБУРГ', 'СУРГУТ',
		'ЕКАТЕРИНБУРГ', 'ПЕРМЬ', 'ТЮМЕНЬ', 'УФА', 'ЧЕЛЯБИНСК'],
	'ПФО' : ['ИЖЕВСК', 'ПЕНЗА', 'УЛЬЯНОВСК', 'ЧЕБОКСАРЫ', 'КИРОВ', 'НИЖНИЙ НОВГОРОД', 'КАЗАНЬ', 'САМАРА', 'САРАТОВ',
		'ТОЛЬЯТТИ'],
	'ЮФО' : ['НОВОРОССИЙСК', 'СИМФЕРОПОЛЬ', 'ПЯТИГОРСК', 'РОСТОВ-НА-ДОНУ', 'ВОЛГОГРАД', 'ВОРОНЕЖ', 'КРАСНОДАР',
		'СТАВРОПОЛЬ', 'АСТРАХАНЬ', 'СОЧИ'],
	'СФО' : ['БАРНАУЛ', 'НОВОКУЗНЕЦК', 'ТОМСК', 'УЛАН-УДЭ', 'НОВОСИБИРСК', 'КРАСНОЯРСК', 'ОМСК', 'ИРКУТСК', 'КЕМЕРОВО'],
	'ДВФО' : ['ВЛАДИВОСТОК', 'ХАБАРОВСК']}


def ret(cell) :  # столбец и ячейку передаю, возрат - округ
	for i in dict_fo.keys() :
		if str(cell).upper() in dict_fo[i] :
			return i
	else :
		return 'ЦФО'

df['ФО'] = df['Заказ.Клиент.Подразделение.Адрес.Город'].apply(ret)
df['ФО'] = df['ФО'].astype('category')

## установить порядок в списке ФО
cat_type = CategoricalDtype(categories=['ЦФО', 'СЗФО', 'ПФО', 'ЮФО', 'УФО', 'СФО', 'ДВФО'], ordered=True)
df['ФО'] = df['ФО'].astype(cat_type)

df['Группа вес'] = pd.cut(df['Расчетный вес'], bins=[0, 0.5, 1, 5, 30, 100, 1000000],
	labels=['0-0.5', '0.5-1', '1-5', '5-30', '30-100', '100+'], right=False)
df['Группа вес'] = df['Группа вес'].astype('category')

## установить порядок в по весам
cat_type = CategoricalDtype(categories=['0-0.5', '0.5-1', '1-5', '5-30', '30-100', '100+'], ordered=True)
df['Группа вес'] = df['Группа вес'].astype(cat_type)
df.rename(columns={'Дата Cоздания' : 'дата', 'Номер отправления' : 'шт', 'Общая стоимость со скидкой' : 'деньги',
	'Расчетный вес':'вес'}, inplace=True)
# print(df.info())
df = df.pivot_table(values=['деньги'], index=['ФО','Группа вес'], aggfunc=[np.sum, len], margins=True)
df.reset_index()
df['средний чек'] = df[('sum', 'деньги')]/df[('len', 'деньги')]
print(df)
####################
writer = pd.ExcelWriter('data/23.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='итоги', index=True, header=True)
workbook = writer.book
worksheet = writer.sheets['итоги']

writer.save()
