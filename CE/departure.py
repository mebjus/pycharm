import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('data/test.xlsx', header=2)
# df = pd.read_excel('data/2021_12_1.xlsx', header=2)
# df1 = pd.read_excel('data/2021_12_2.xlsx', header=2)
#
# df = df.merge(df1, how='outer')


def todate(arg):
    arg = pd.to_datetime(arg)
    return arg.strftime('%Y-%m')


df['Дата Cоздания'] = df['Дата Cоздания'].apply(todate)

dict_fo = {'СЗФО': ['Великий Новгород', 'Мурманск', 'Петрозаводск', 'Сыктывкар', 'Санкт-Петербург', 'Архангельск',
                    'Калининград'],
           'УФО': ['Курган', 'Нижневартовск', 'Новый Уренгой', 'Стерлитамак', 'Магнитогорск', 'Оренбург', 'Сургут',
                   'Екатеринбург', 'Пермь', 'Тюмень', 'Уфа', 'Челябинск'],
           'ПФО': ['Ижевск', 'Пенза', 'Ульяновск', 'Чебоксары', 'Киров', 'Нижний Новгород', 'Казань', 'Самара',
                   'Саратов', 'Тольятти'],
           'ЮФО': ['Новороссийск', 'Симферополь', 'Пятигорск', 'Ростов-на-Дону', 'Волгоград', 'Воронеж', 'Краснодар',
                   'Ставрополь',
                   'Астрахань', 'Сочи'],
           'СФО': ['Барнаул', 'Новокузнецк', 'Томск', 'Улан-Удэ', 'Новосибирск', 'Красноярск', 'Омск', 'Иркутск',
                   'Кемерово'],
           'ДВФО': ['Владивосток', 'Хабаровск']
           }

for i in dict_fo.keys():  # преобразование словаря верхний регистр
    d = []
    for j in dict_fo[i]:
        c = j.upper()
        d.append(c)
    dict_fo[i] = d


def ret(cell):  # столбец и ячейку передаю, возрат - округ
    for i in dict_fo.keys():
        if str(cell).upper() in dict_fo[i]:
            return i
    else:
        return 'ЦФО'


df['ФО'] = df['Заказ.Клиент.Подразделение.Адрес.Город'].apply(ret)
df['Группа вес'] = pd.cut(df['Расчетный вес'], bins=[0, 1, 5, 30, 100, 1000000],
                          labels=['0-1', '1-5', '5-30', '30-100', '100+'], right=False)
# df.drop('Расчетный вес', axis=1, inplace=True)


#######################  рисование  ##############

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

# df_pivot.to_excel('data/summary.xlsx', sheet_name='итоги')


# написать группировку -  собрать по дате, шт, деньги и кг по сумме группа, а категорию веса в количестве значений

df_pivot = df.pivot_table(index='ФО', columns='Группа вес', values='Расчетный вес',
                          aggfunc='sum').reset_index()

print(df_pivot)