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

dirname = 'data/day_of_month.xlsx'
df_m = pd.read_excel(dirname)
df_m.reset_index()
mounth = {}

df_m['Дата'] = df_m['Дата'].dt.strftime('%Y-%m')
for i in df_m.index :
	mounth[df_m.iloc[i]['Дата']] = df_m.iloc[i]['р.д.']


df['Дата Cоздания'] = df['Дата Cоздания'].dt.strftime('%Y-%m')

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



df.rename(columns={'Дата Cоздания':'дата', 'Номер отправления':'шт', 'Общая стоимость со скидкой':'деньги',
	'Расчетный вес':'вес', 'Отправитель.Адрес.Город':'город откуда', 'Получатель.Адрес.Город':'город куда'}, inplace=True)

# отбрасываем все нулевки, консолидированные сборы, дешевые доборы

# df = df[df['деньги'] > 50]
# df = df[df['вес'] <= 0.5]
# df = df[df['ФО'] == 'ЦФО']
# df = df[df['Вид доставки'] == 'Местная']


df_dep = df.pivot_table(index=['ФО','дата','город откуда'], values=['шт'], aggfunc={'шт':len})
df_arr = df.pivot_table(index=['ФО','дата','город куда'], values=['шт'], aggfunc={'шт':len})
# df_pivot = df_pivot[df_pivot['шт'] > 0]

# df_pivot = df_pivot.reindex(
# 	df_pivot.sort_values(by=['ФО', 'дата', 'деньги'], ascending=[True, True, False]).index).reset_index()
#
# df_pivot['р.д.'] = df_pivot['дата'].apply(lambda x : mounth[str(x)])

#### средний чек, средний рд
# df_pivot['деньги р.д.'] = df_pivot['деньги'] / df_pivot['р.д.']
# df_pivot['ср чек'] = df_pivot['деньги'] / df_pivot['шт']

# если нужно проверить у кого скидка заканчивается

####
# dirname = 'data/скидка.xls'
# df_dis = pd.read_excel(dirname)
# df_dis = df_dis.rename(columns={'Наименование': 'Клиент'}).reset_index()
# df_pivot['Не применять топливную надбавку'] = df_pivot['Не применять топливную надбавку'].fillna(0)
# # df_pivot = df_pivot.merge(df_dis, how='inner', on='Клиент')
#


#######

writer = pd.ExcelWriter('calc.xlsx', engine='xlsxwriter')
df_dep.to_excel(writer, sheet_name='итоги', startrow=1, index=False, header=False)

workbook = writer.book
worksheet = writer.sheets['итоги']

format = workbook.add_format({'border' : 1, 'bg_color' : '#E8FBE1', 'num_format' : '#,##0'})
worksheet.set_column('A:K', 10, format)


header_format = workbook.add_format(
	{'bold' :          True, 'text_wrap' : True, 'valign' : 'vcenter', 'fg_color' : '#D7E4BC',
		'align' :      'center_across', 'num_format' : '#,##0', 'border' : 1})

for col_num, value in enumerate(df_dep.columns.values) :
	worksheet.write(0, col_num, value, header_format)

writer.save()
