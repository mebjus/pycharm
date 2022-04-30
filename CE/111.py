import pandas as pd
import os
from pandas.api.types import CategoricalDtype


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

df['Дата Cоздания'] = df['Дата Cоздания'].dt.strftime('%Y-%m-%d')
df['Заказ.Дата и время доставки'] = df['Заказ.Дата и время доставки'].dt.strftime('%Y-%m-%d')

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


df.rename(columns={'Дата Cоздания':'дата', 'Номер отправления':'шт', 'Общая стоимость со скидкой':'деньги',
	'Расчетный вес':'вес', 'Отправитель.Адрес.Город':'город откуда', 'Получатель.Адрес.Город':'город куда'}, inplace=True)


set1 = df['шт'].count()
df.loc[:,'шт'] = df.loc[:, 'шт'].apply(lambda x: x[0:12])
set2 = df.groupby(['город откуда', 'шт'])['Клиент'].count().sort_values(ascending=False).reset_index()
print(round((set1-set2['Клиент'].count())/set1*100, 2), '% конс сборов')
set2 = set2[set2['Клиент'] > 1] # была консолидация и поэтому > 1
set2 = set2.groupby(['город откуда'])['Клиент'].sum().sort_values(ascending=False).reset_index()

set3 = df.groupby(['Заказ.Дата и время доставки', 'город куда', 'шт'])['Клиент'].count().sort_values(ascending=False).reset_index()
set3 = set3[set3['Клиент'] > 1] # была консолидация и поэтому > 1
print(set3)
set3 = set3.groupby(['город куда'])['Клиент'].sum().sort_values(ascending=False).reset_index()


df_dep = df.groupby(by='город откуда')['шт'].count().sort_values(ascending=False).reset_index()
df_arr = df.groupby(by='город куда')['шт'].count().sort_values(ascending=False).reset_index()
df_dep.rename(columns={'город откуда': 'город'}, inplace=True)
df_arr.rename(columns={'город куда': 'город'}, inplace=True)

df_pivot = pd.concat([df_dep, df_arr], axis=0)
df_pivot = df_pivot.groupby('город')['шт'].sum().sort_values(ascending=False).reset_index()

df_pivot = df_pivot.merge(set2, how='left', left_on='город', right_on='город откуда')
df_pivot.drop('город откуда', axis=1, inplace=True)
df_pivot.rename(columns={'Клиент':'консолидация сбора'}, inplace=True)

df_pivot = df_pivot.merge(set3, how='left', left_on='город', right_on='город куда')
df_pivot.drop('город куда', axis=1, inplace=True)
df_pivot.rename(columns={'Клиент':'консолидация доставки'}, inplace=True)


# # df_pivot['р.д.'] = df_pivot['дата'].apply(lambda x : mounth[str(x)])
#
# #### средний чек, средний рд
# # df_pivot['деньги р.д.'] = df_pivot['деньги'] / df_pivot['р.д.']
# # df_pivot['ср чек'] = df_pivot['деньги'] / df_pivot['шт']
#
# # если нужно проверить у кого скидка заканчивается
#
# ####
# # dirname = 'data/скидка.xls'
# # df_dis = pd.read_excel(dirname)
# # df_dis = df_dis.rename(columns={'Наименование': 'Клиент'}).reset_index()
# # df_pivot['Не применять топливную надбавку'] = df_pivot['Не применять топливную надбавку'].fillna(0)
# # # df_pivot = df_pivot.merge(df_dis, how='inner', on='Клиент')
# #
#
#
#######

writer = pd.ExcelWriter('calc.xlsx', engine='xlsxwriter')
df_pivot.to_excel(writer, sheet_name='итоги', startrow=1, index=False, header=False)
set2.to_excel(writer, sheet_name='итоги2', startrow=1, index=False, header=False)
set3.to_excel(writer, sheet_name='итоги3', startrow=1, index=False, header=False)

workbook = writer.book
worksheet = writer.sheets['итоги']

format = workbook.add_format({'border' : 1, 'bg_color' : '#E8FBE1', 'num_format' : '#,##0'})
worksheet.set_column('A:K', 10, format)


header_format = workbook.add_format(
	{'bold' :          True, 'text_wrap' : True, 'valign' : 'vcenter', 'fg_color' : '#D7E4BC',
		'align' :      'center_across', 'num_format' : '#,##0', 'border' : 1})

for col_num, value in enumerate(df_pivot.columns.values) :
	worksheet.write(0, col_num, value, header_format)

writer.save()
