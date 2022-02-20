import numpy as np
import pandas as pd
import os
from pandas.api.types import CategoricalDtype


dirname = 'data/2021-pay.xls'
df = pd.read_excel(dirname)
df.reset_index()

print(df.info())

# for i in df_m.index:
# 	mounth[df_m.iloc[i]['Дата']] = df_m.iloc[i]['р.д.']
#
# df['Дата Cоздания'] = df['Дата Cоздания'].dt.to_period('M')
#
# ##### фильтр на дату
#
# df = df[df['Дата Cоздания'] == '2021-11']
#
# ######
#
#
# def ret(cell):  # столбец и ячейку передаю, возрат - округ
# 	for i in dict_fo.keys():
# 		if str(cell).upper() in dict_fo[i]:
# 			return i
# 	else:
# 		return 'ЦФО'
#
#
# df['ФО'] = df['Заказ.Клиент.Подразделение.Адрес.Город'].apply(ret)
# df['ФО'] = df['ФО'].astype('category')
#
#
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
#
#
# # установить порядок в списке ФО
# cat_type = CategoricalDtype(categories=['ЦФО', 'СЗФО', 'ПФО', 'ЮФО', 'УФО', 'СФО', 'ДВФО'], ordered=True)
# df['ФО'] = df['ФО'].astype(cat_type)
#
# df['Группа вес'] = pd.cut(df['Расчетный вес'], bins=[0, 1, 5, 30, 100, 1000000],
#                           labels=['0-1', '1-5', '5-30', '30-100', '100+'], right=False)
#
# df['Группа вес'] = df['Группа вес'].astype('category')
#
# ## установить порядок по весам
# cat_type = CategoricalDtype(categories=['0-1', '1-5', '5-30', '30-100', '100+'], ordered=True)
# df['Группа вес'] = df['Группа вес'].astype(cat_type)
#
# df.rename(columns={'Дата Cоздания':     'дата',
#                    'Номер отправления': 'шт', 'Общая стоимость со скидкой': 'деньги', 'Расчетный вес': 'вес'},
#           inplace=True)
#
# def mod(arg):
# 	if arg.find('ЭКСПРЕСС') != -1:
# 		return 'ЭКСПРЕСС'
# 	elif arg.find('ПРАЙМ') != -1:
# 		return 'ПРАЙМ'
# 	elif arg.find('ОПТИМА') != -1:
# 		return 'ОПТИМА'
# 	else:
# 		return 'ПРОЧИЕ'
#
#
# df['Режим доставки'] = df['Режим доставки'].apply(mod)
# df['Режим доставки'] = df['Режим доставки'].astype('category')
#
# # отбрасываем все условия:
#
# df = df[df['деньги'] > 50]
# # df = df[df['вес'] <= 0.250]
# # df = df[df['ФО'] == 'СЗФО']
# # df = df[df['Режим доставки'] == 'ЭКСПРЕСС']
# # df = df[df['Вид доставки'] == 'Местная']
# df = df[df['Клиент'] == 'ООО "ЭЙ энд ДИ РУС"']
#
# num_start = df.shape[0]
#
# #### если положительное значение - просрочка
#
# df['delta_delivery'] = df['Получатель.Дата получения отправления получателем'] - df['Заказ.Дата и время доставки']
# df['delta_get'] = df['Отправитель.Дата приема у отправителя'] - df['Дата dead-line приема отправления']
#
# df1 = df[df['delta_delivery'].dt.components.days > 0]
# df1 = df1.reset_index()
# df1.drop(columns=['Отправитель.Дата приема у отправителя', 'Дата dead-line приема отправления'], axis=1, inplace=True)
# print(round((df1['delta_delivery'].shape[0] / num_start) * 100, 2), '%', 'нарушены сроки доставки')
#
# df2 = df[df['delta_get'].dt.components.days > 0]
# df2 = df2.reset_index()
# df2.drop(columns=['Заказ.Дата и время доставки', 'Получатель.Дата получения отправления получателем'], axis=1,
#          inplace=True)
# print(round((df2['delta_get'].shape[0] / num_start) * 100, 2), '%', 'нарушены сроки сбора')
#
# #######
#
# writer = pd.ExcelWriter('billing.xlsx', engine='xlsxwriter')
# df1.to_excel(writer, sheet_name='не доставки', startrow=1, index=False, header=False)
# df2.to_excel(writer, sheet_name='не сборы', startrow=1, index=False, header=False)
#
# workbook = writer.book
# worksheet = writer.sheets['не доставки']
# worksheet2 = writer.sheets['не сборы']
#
# header_format = workbook.add_format({
# 	'bold':       True,
# 	'text_wrap':  True,
# 	'valign':     'vcenter',
# 	'fg_color':   '#D7E4BC',
# 	'align':      'center_across',
# 	'num_format': '#,##0',
# 	'border':     1})
#
# for col_num, value in enumerate(df1.columns.values):
# 	worksheet.write(0, col_num, value, header_format)
# for col_num, value in enumerate(df2.columns.values):
# 	worksheet2.write(0, col_num, value, header_format)
#
# writer.save()
