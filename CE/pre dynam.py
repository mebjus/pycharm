import pandas as pd
import os
from pandas.api.types import CategoricalDtype
import datetime
from time import gmtime, strftime

df = pd.DataFrame()
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.0F}'.format

for file in fullpaths:
    if file == 'data/kis/.DS_Store': os.remove('data/kis/.DS_Store')
    df1 = pd.read_excel(file, header=3, sheet_name=None)
    df1 = pd.concat(df1, axis=0).reset_index(drop=True)
    df = pd.concat([df, df1], axis=0)

df_zakrep = pd.read_excel('data/закрепление.xlsx', header=2)
df_zakrep['Бренд'].fillna(0)

df = df.drop(df.tail(1).index)  # удалить итоги строку

dict_fo = {'СЗФО': ['ВЕЛИКИЙ НОВГОРОД', 'МУРМАНСК', 'ПЕТРОЗАВОДСК', 'СЫКТЫВКАР', 'САНКТ-ПЕТЕРБУРГ', 'АРХАНГЕЛЬСК',
                    'КАЛИНИНГРАД'],
           'УФО':  ['КУРГАН', 'НИЖНЕВАРТОВСК', 'НОВЫЙ УРЕНГОЙ', 'СТЕРЛИТАМАК', 'МАГНИТОГОРСК', 'ОРЕНБУРГ', 'СУРГУТ',
                    'ЕКАТЕРИНБУРГ', 'ПЕРМЬ', 'ТЮМЕНЬ', 'УФА', 'ЧЕЛЯБИНСК'],
           'ПФО':  ['ИЖЕВСК', 'ПЕНЗА', 'УЛЬЯНОВСК', 'ЧЕБОКСАРЫ', 'КИРОВ', 'НИЖНИЙ НОВГОРОД', 'КАЗАНЬ', 'САМАРА',
                    'САРАТОВ', 'ТОЛЬЯТТИ'],
           'ЮФО':  ['НОВОРОССИЙСК', 'СИМФЕРОПОЛЬ', 'ПЯТИГОРСК', 'РОСТОВ-НА-ДОНУ', 'ВОЛГОГРАД', 'ВОРОНЕЖ', 'КРАСНОДАР',
                    'СТАВРОПОЛЬ', 'АСТРАХАНЬ', 'СОЧИ'],
           'СФО':  ['БАРНАУЛ', 'НОВОКУЗНЕЦК', 'ТОМСК', 'УЛАН-УДЭ', 'НОВОСИБИРСК', 'КРАСНОЯРСК', 'ОМСК', 'ИРКУТСК',
                    'КЕМЕРОВО'],
           'ДВФО': ['ВЛАДИВОСТОК', 'ХАБАРОВСК']}

def ret(cell):
    for i in dict_fo.keys():
        if str(cell).upper() in dict_fo[i]:
            return i
    else:
        return 'ЦФО'

df1 = df.iloc[:, 3:-1]
header = []
col = df1.columns.values
for item in col:
    header.append(item)

ls = header[2::3]
df = df.iloc[:, 0:3]

df1 = df1.loc[:, ls]
df1 = df1.fillna(0)
df = df.join(df1)

df['ФО'] = df['Подразделение клиента'].apply(ret)
df['ФО'] = df['ФО'].astype('category')

df = df.merge(df_zakrep, on='Клиентский номер', how='left')

df = df[['ФО','Подразделение клиента','Бренд','Клиентский номер','Наименование клиента',
 'Зона ответственности менеджера по продажам',
 'Зона ответственности менеджеров по сопровождению','Статусы НБ',
 'Стоимость','Стоимость.1','Стоимость.2','Стоимость.3','Стоимость.4',
 'Стоимость.5','Стоимость.6','Стоимость.7','Стоимость.8','Стоимость.9',
 'Стоимость.10', 'Стоимость.11', 'Стоимость.12', 'Стоимость.13',
 'Стоимость.14', 'Стоимость.15', 'Стоимость.16', 'Стоимость.17',
 'Стоимость.18', 'Стоимость.19', 'Стоимость.20', 'Стоимость.21',
 'Стоимость.22', 'Стоимость.23', 'Стоимость.24']]

with pd.ExcelWriter('data/dynam.xlsx') as writer:
    df.to_excel(writer, index=False)
