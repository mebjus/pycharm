import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.DataFrame
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
# os.remove('data/kis/.DS_Store')


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

df['Группа вес'] = pd.cut(df['Расчетный вес'], bins=[0, 1, 5, 30, 100, 1000000],
                          labels=['0-1', '1-5', '5-30', '30-100', '100+'], right=False)

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

############## запись в файл ##############

# df_pivot.to_excel('data/summary.xlsx', sheet_name='итоги', index=False)


# написать группировку -  собрать по дате, шт, деньги и кг по сумме группа, а категорию веса в количестве значений
#
# df_pivot = df.pivot_table(index='ФО', columns='Группа вес', values='Расчетный вес',
#                    aggfunc='sum')
#
# df_pivot = df_pivot.append(df_pivot.sum(axis=0), ignore_index=True)
# #
# df1 = c.groupby(by='ФО')['Группа вес'].sum()
#
# print(df_pivot)

df_pivot = df.pivot_table(index='ФО', columns='Режим доставки', values='Номер отправления',
                          aggfunc='count')


# for i in df_pivot.columns:
#     if i not in ['ОПТИМА', 'ПРАЙМ', 'ПРАЙМ 1 до 13:00', 'ПРАЙМ 18:00', 'ПРАЙМ 2 дня до 13:00',
#                            'ПРАЙМ 2 дня до 15:00', 'ПРАЙМ 2 дня до 18:00', 'ПРАЙМ до 10:00', 'ПРАЙМ до 13:00',
#                            'ПРАЙМ до 15:00',
#                            'ПРАЙМ до 18:00', 'ЭКСПРЕСС', 'ЭКСПРЕСС Лайт']:
#         df_pivot.drop(i, axis=1, inplace=True)

# for i in df['Режим доставки']:
#     if i.find('ЭКСПРЕСС') != -1:
#         print(i)


# df_pivot.to_excel('data/summary.xlsx', sheet_name='итоги')

print(df_pivot)