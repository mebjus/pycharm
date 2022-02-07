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

n = 500  ## количество строк из каждого месяца  nrows: Any = None,

for file in fullpaths:
    if df.empty:
        if file.find('.xls') != -1:
            df = pd.read_excel(file, header=2, sheet_name=None)
            df = pd.concat(df, axis=0).reset_index(drop=True)
    else:
        if file.find('.xls') != -1:
            df1 = pd.read_excel(file, header=2, sheet_name=None)
            df1 = pd.concat(df1, axis=0).reset_index(drop=True)
            df = pd.concat([df, df1], axis=0)

dirname = 'data/day_of_month.xlsx'
df_m = pd.read_excel(dirname)

dupl = list(df.columns)
df_dupl = df[df.duplicated(subset=dupl)]
df_dupl.index.nunique()
df = df.drop_duplicates(subset=dupl)


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

df.rename(columns={"Номер отправления": "шт", "Общая стоимость со скидкой": "деньги", "Расчетный вес": "вес"},
          inplace=True)

######################  рисование  ##############

# money = df.groupby(['ФО'])['деньги'].sum().round()
# dep = df.groupby(['ФО'])['вес'].sum().round()
# kg = df.groupby(['ФО'])['шт'].count().round()
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
# df_pivot = df.pivot_table(index='ФО', columns='Режим доставки', values='шт', aggfunc='count')

## ФО деньги по сумме
# df_pivot = df.pivot_table(index='ФО', columns='Дата Cоздания', values='деньги',
#                           aggfunc='sum').round(0)


########### по дате по округам, деньги вес штуки
# df_pivot = df.pivot_table(index=['Дата Cоздания', 'ФО'],
#                           values=['деньги', 'вес', 'шт'],
#                           aggfunc={'деньги': sum, 'вес': sum,
#                                    'шт': len})
## , margins=True
#
# df_pivot.rename(columns={'шт': 'Количество отправлений'}, inplace=True)
#
# # df_pivot.query('ФО == ["СФО"]')  ## фильтр по сводному


######################  по дате по округам, весовой брейк вес штуки

df_pivot = df.pivot_table(index=['Дата Cоздания', 'ФО'], columns=['Группа вес'],
                          values=['шт', 'вес', 'деньги'],
                          aggfunc={'шт': len, 'вес': sum, 'деньги': sum})
# margins=True,
########, средний чек, вес, кг по весовым грейдам

df_pivot = df_pivot.reset_index()
df_pivot = df_pivot.merge(df_m, left_on='Дата Cоздания', right_on='Дата', how='left')
df_pivot.drop(columns=['Дата'], axis=1, inplace=True)

df1 = df[df['Группа вес'] == '100+'][
    ['Дата Cоздания', 'шт', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'ФО',
     'Клиент']].reset_index()
df1.drop(columns=['index'], axis=1, inplace=True)

set_weight = ['0-1', '1-5', '5-30', '30-100', '100+']

for i in set_weight:
    df_pivot[('Средний КГ ', i)] = df_pivot[('деньги', i)] / df_pivot[('вес', i)]
for i in set_weight:
    df_pivot[('Средний ЧЕК ', i)] = df_pivot[('деньги', i)] / df_pivot[('шт', i)]

dic = {}
for i in df_pivot.columns.values:
    c = str(i[0] + ' ' + i[1]).strip()
    dic[i] = c

df_pivot.rename(columns=dic, inplace=True)

df_pivot.rename(columns={'р .': 'р.д.'}, inplace=True)

####################### сохраняем в файл

writer = pd.ExcelWriter('summary.xlsx', engine='xlsxwriter')
df_pivot.to_excel(writer, sheet_name='итоги', startrow=2, index=False, header=False)  # index=False header=False
df1.to_excel(writer, sheet_name='>100кг', index=False)

workbook = writer.book
worksheet = writer.sheets['итоги']
worksheet2 = writer.sheets['>100кг']
worksheet.add_table(1, 0, df_pivot.shape[0] + 1, 1, {'first_column': False, 'style': None, 'columns':
    [{'header': 'Дата'},
     {'header': 'ФО'}]})
worksheet2.add_table(0, 0, df1.shape[0], 5, {'first_column': False, 'style': None, 'columns':
    [{'header': 'Дата'},
     {'header': 'шт'},
     {'header': 'Город отправки'},
     {'header': 'Город доставки'},
     {'header': 'ФО'},
     {'header': 'Клиент'}]})

format1 = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#E8FBE1', 'num_format': '#,##0'})
format2 = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#FAF8DF', 'num_format': '#,##0'})
format3 = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#E0F2F1', 'num_format': '#,##0'})
format4 = workbook.add_format({'border': 1, 'bg_color': '#E8FBE1'})

worksheet.set_column('A:H', 14, format1)
worksheet.set_column('H:M', 14, format2)
worksheet.set_column('M:AH', 14, format3)
worksheet2.set_column('A:E', 25, format4)
worksheet2.set_column('F:F', 60, format4)

workbook = writer.book
worksheet = writer.sheets['итоги']
#
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'vcenter',
    'fg_color': '#D7E4BC',
    'align': 'center_across',
    'num_format': '#,##0',
    'border': 1})

for col_num, value in enumerate(df_pivot.columns.values):
    worksheet.write(0, col_num, value, header_format)

writer.save()