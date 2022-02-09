import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pandas.api.types import CategoricalDtype

df = pd.DataFrame
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.0F}'.format

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
    return arg.strftime('%Y-%m-%d')
    # return arg.strftime('%Y-%m')


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

## установить порядок в списке ФО
cat_type = CategoricalDtype(categories=['ЦФО', 'СЗФО', 'ПФО', 'ЮФО', 'УФО', 'СФО', 'ДВФО'], ordered=True)
df['ФО'] = df['ФО'].astype(cat_type)

df['Группа вес'] = pd.cut(df['Расчетный вес'], bins=[0, 1, 5, 30, 100, 1000000],
                          labels=['0-1', '1-5', '5-30', '30-100', '100+'], right=False)

df['Группа вес'] = df['Группа вес'].astype('category')

## установить порядок в по весам
cat_type = CategoricalDtype(categories=['0-1', '1-5', '5-30', '30-100', '100+'], ordered=True)
df['Группа вес'] = df['Группа вес'].astype(cat_type)

df.rename(columns={'Дата Cоздания': 'дата',
                   'Номер отправления': 'шт', 'Общая стоимость со скидкой': 'деньги', 'Расчетный вес': 'вес'},
          inplace=True)

# отбрасываем все нулевки, консолидированные сборы, дешевые доборы
df = df[df['деньги'] > 10]
## преобразуем  дата фрейм под Москву

mask1 = df['Отправитель.Адрес.Город'] == 'Москва'
print(df[mask1].shape[0])

mask2 = df['Получатель.Адрес.Город'] == 'Москва'
print(df[mask2].shape[0])

print((df[(mask1 | mask2)].shape[0])  + (df[(mask1 & mask2)].shape[0]))
# надо обрезать все дифис

def ch(row):
    return str(row[0:12])

df['шт']= df['шт'].apply(ch)

df1 = df.groupby('шт')['дата'].count().sort_values(ascending=False)

# print(df1.nlargest(10))



########  по дате по округам, весовой брейк вес штуки

# df_pivot = df.pivot_table(index=['дата', 'ФО'], columns=['Группа вес'],
#                           values=['шт', 'вес', 'деньги'],
#                           aggfunc={'шт': len, 'вес': sum, 'деньги': sum})
#
# # margins=True,
# ########, средний чек, вес, кг по весовым грейдам
#
# df_pivot = df_pivot.reset_index()
# # df_pivot = df_pivot.merge(df_m, left_on='дата', right_on='Дата', how='left')        ## количество рд
# # df_pivot.drop(columns=['Дата'], axis=1, inplace=True)
#
# df1 = df[(df['Группа вес'] == '100+') & (df['деньги'] > 0)][
#     ['дата', 'шт', 'Отправитель.Адрес.Город', 'Получатель.Адрес.Город', 'ФО',
#      'деньги', 'Клиент']].reset_index()
#
# df1.drop(columns=['index'], axis=1, inplace=True)
#
# for i in df['Группа вес'].values:
#     df_pivot[('Средний КГ ', i)] = df_pivot[('деньги', i)] / df_pivot[('вес', i)]
# for i in df['Группа вес'].values:
#     df_pivot[('Средний ЧЕК ', i)] = df_pivot[('деньги', i)] / df_pivot[('шт', i)]
#
# dic = {}
# for i in df_pivot.columns.values:
#     c = str(i[0] + ' ' + i[1]).strip()
#     dic[i] = c
#
# df_pivot.rename(columns=dic, inplace=True)
# df_pivot.rename(columns={'р .': 'р.д.'}, inplace=True)

########### фильтр на округ

# df_pivot = df_pivot.query('ФО == ["СФО"]')  ## фильтр по сводному

####################### сохраняем в файл

# writer = pd.ExcelWriter('consolid.xlsx', engine='xlsxwriter')
# df_pivot.to_excel(writer, sheet_name='итоги', startrow=2, index=False, header=False)  # index=False header=False
# workbook = writer.book
# worksheet = writer.sheets['итоги']
# writer.save()
