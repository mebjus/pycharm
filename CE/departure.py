import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.DataFrame
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.0F}'.format

for file in fullpaths:
    if df.empty:
        df = pd.read_excel(file, header=2)
    else:
        df1 = pd.read_excel(file, header=2)
        df = pd.concat([df, df1], axis=0)


def todate(arg):
    arg = pd.to_datetime(arg)
    return arg.strftime('%Y-%m')


df['Дата Cоздания'] = df['Дата Cоздания'].apply(todate)

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

df['Группа вес'] = pd.cut(df['Расчетный вес'], bins=[0, 1, 5, 30, 100, 1000000],
                          labels=['0-1', '1-5', '5-30', '30-100', '100+'], right=False)

df['Группа вес'] = df['Группа вес'].astype('category')


def mod(arg):
    if arg.find('ЭКСПРЕСС') != -1:
        return 'ЭКСПРЕСС'
    elif arg.find('ПРАЙМ') != -1:
        return 'ПРАЙМ'
    elif arg.find('ОПТИМА') != -1:
        return 'ОПТИМА'
    else:
        return 'ПРОЧИЕ'


df['Режим доставки'] = df['Режим доставки'].apply(mod)
df['Режим доставки'] = df['Режим доставки'].astype('category')

######################  рисование  ##############

# money = df.groupby(['ФО'])['Общая стоимость со скидкой'].sum().round()
# dep = df.groupby(['ФО'])['Расчетный вес'].sum().round()
# kg = df.groupby(['ФО'])['Номер отправления'].count().round()
#
#
# fig = plt.figure(figsize=(15, 5))
# colors = sns.color_palette('pastel')[0:7]
#
# plt.subplot(131)
# plt.title('Распределение ФО, деньги')
# plt.pie(money, labels=money.index, colors=colors, autopct='%.1f%%')
#
# plt.subplot(132)
# plt.title('Распределение количество')
# plt.pie(dep, labels=dep.index, colors=colors, autopct='%.1f%%')
#
# plt.subplot(133)
# plt.title('Распределение ФО, вес')
# plt.pie(kg, labels=kg.index, colors=colors, autopct='%.1f%%')
#
# plt.show()


### ФО по режиму колво
# df_pivot = df.pivot_table(index='ФО', columns='Режим доставки', values='Номер отправления', aggfunc='count')

## ФО деньги по сумме
# df_pivot = df.pivot_table(index='ФО', columns='Дата Cоздания', values='Общая стоимость со скидкой',
#                           aggfunc='sum').round(0)


########### по дате по округам, деньги вес штуки
# df_pivot = df.pivot_table(index=['Дата Cоздания', 'ФО'],
#                           values=['Общая стоимость со скидкой', 'Расчетный вес', 'Номер отправления'],
#                           aggfunc={'Общая стоимость со скидкой': sum, 'Расчетный вес': sum,
#                                    'Номер отправления': len})
## , margins=True
#
# df_pivot.rename(columns={'Номер отправления': 'Количество отправлений'}, inplace=True)
#
# # df_pivot.query('ФО == ["СФО"]')  ## фильтр по сводному


######################  по дате по округам, весовой брейк вес штуки

df_pivot = df.pivot_table(index=['Дата Cоздания', 'ФО'], columns=['Группа вес'],
                          values=['Номер отправления', 'Общая стоимость со скидкой', 'Расчетный вес'],
                          aggfunc={'Номер отправления': len, 'Общая стоимость со скидкой': sum, 'Расчетный вес': sum})
## margins=True
df_pivot = df_pivot.fillna(1)
# df_pivot.query('ФО == ["ЮФО"]', inplace=True)  ## фильтр по сводному

# print(df_pivot)
# ll = list(df_pivot.columns)

########, средний чек, вес, кг по весовым грейдам

set_weihht = ['100+', '30-100', '5-30', '1-5', '0-1']

for i in set_weihht:
    ll = []
    for j in range(0, df_pivot.shape[0]):
        ll.append((df_pivot.iloc[j]['Общая стоимость со скидкой'][i]) / (df_pivot.iloc[j]['Расчетный вес'][i]))
    df_pivot.insert(loc=int(0), column=str('Средний КГ ' + i), value=ll, allow_duplicates=False)

for i in set_weihht:
    ll = []
    for j in range(0, df_pivot.shape[0]):
        ll.append((df_pivot.iloc[j]['Общая стоимость со скидкой'][i]) / (df_pivot.iloc[j]['Номер отправления'][i]))
    df_pivot.insert(loc=int(0), column=str('Средний ЧЕК ' + i), value=ll, allow_duplicates=False)


####################### сохраняем в файл +++

writer = pd.ExcelWriter('summary.xlsx', engine='xlsxwriter')
df_pivot.to_excel(writer, sheet_name='итоги')

workbook = writer.book
worksheet = writer.sheets['итоги']
worksheet.add_table(1, 1, df_pivot.shape[0] + 2, 1, {'first_column': True, 'style': None, 'columns':
    [{'header': 'ФО'}]})

format1 = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#E8FBE1', 'num_format': '#,##0'})
format2 = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#FAF8DF', 'num_format': '#,##0'})
format3 = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#E0F2F1', 'num_format': '#,##0'})

worksheet.set_column('C:H', 10, format1)
worksheet.set_column('H:M', 10, format2)
worksheet.set_column('M:AH', 10, format3)

# workbook  = writer.book
# worksheet = writer.sheets['итоги']
#
# header_format = workbook.add_format({
#     'bold': True,
#     'text_wrap': True,
#     'valign': 'top',
#     'fg_color': '#D7E4BC',
#     'border': 1})
#
# # Write the column headers with the defined format.
# for col_num, value in enumerate(df_pivot.columns.values):
#     worksheet.write(0, col_num + 1, value, header_format)

writer.save()
