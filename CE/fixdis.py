import numpy as np
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

df.rename(columns={'Заказ.Клиент.Клиентский номер':'кн',
					'Дата Cоздания':'дата',
					'Номер отправления':'шт',
					'Общая стоимость со скидкой':'деньги',
					'Расчетный вес':'вес',
					'Заказ.Клиент.Подразделение.Адрес.Город':'город'}, inplace=True)

# отбрасываем все нулевки, консолидированные сборы, дешевые доборы

# df = df[df['деньги'] > 50]
# df = df[df['вес'] <= 0.5]
# df = df[df['ФО'] == 'ЦФО']
# df = df[df['Вид доставки'] == 'Местная']

df_pivot = df.pivot_table(index=['ФО', 'дата', 'город', 'Клиент'], values=['деньги'], aggfunc={'деньги':sum})
df_pivot = df_pivot[df_pivot['деньги'] > 0]
df_pivot = df_pivot.reindex(df_pivot.sort_values(by=['ФО', 'дата', 'деньги'], ascending=[True, True, False]).index).reset_index()

####
dirname = 'data/totaldis.xlsx'
df_tmp = pd.read_excel(dirname)
df_tmp.reset_index()
df_pivot = df_pivot.merge(df_tmp, how='left', on='Клиент')
df_pivot = df_pivot.loc[:, ['ФО','дата', 'город', 'Клиент', 'деньги', 'dis']]

#
# dirname = 'data/скидка.xlsx'
# df_total = pd.read_excel(dirname)
# df_total.reset_index()
# df_pivot = df_pivot.merge(df_total, how='left', on='Клиент')
# df_pivot.drop(['паблик', 'цена', 'ФО_y'], axis=1, inplace=True)

# ### закрепленный прайс лист
# dirname = 'data/hold_price.xls'
# df_total = pd.read_excel(dirname)
# df_total.reset_index()
# df_pivot = df_pivot.merge(df_total, how='left', on='Клиент')
# df_pivot['Не применять топливную надбавку'] = df_pivot['Не применять топливную надбавку'].fillna(0)
# df_pivot.drop(['Дата создания', 'Подразделение.Адрес.Город', 'Тип клиента', '№ договора', 'Дата окончания договора'],
# 	axis=1, inplace=True)
# df_pivot.rename(columns={'Не применять топливную надбавку' : 'тн', 'Заказ.Клиент.Подразделение.Адрес.Город' : 'город',
# 	'Клиентский номер' : 'кн', '(Юридическое лицо).Период формирования счетов': 'период'}, inplace=True)


#######

writer = pd.ExcelWriter('clients.xlsx', engine='xlsxwriter')
df_pivot.to_excel(writer, sheet_name='итоги', startrow=1, index=False, header=False)

workbook = writer.book
worksheet = writer.sheets['итоги']

format = workbook.add_format({'border' : 1, 'bg_color' : '#E8FBE1', 'num_format' : '#,##0'})
worksheet.set_column('A:B', 10, format)
worksheet.set_column('B:C', 15, format)
worksheet.set_column('C:D', 10, format)
worksheet.set_column('D:E', 65, format)
worksheet.set_column('E:K', 15, format)

header_format = workbook.add_format(
	{'bold' :          True, 'text_wrap' : True, 'valign' : 'vcenter', 'fg_color' : '#D7E4BC',
		'align' :      'center_across', 'num_format' : '#,##0', 'border' : 1})

for col_num, value in enumerate(df_pivot.columns.values) :
	worksheet.write(0, col_num, value, header_format)

writer.save()
