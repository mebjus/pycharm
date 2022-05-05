import pandas as pd
import os
import datetime

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

df['Дата Cоздания'] = df['Дата Cоздания'].dt.strftime('%Y-%m-%d')

start = '2022-03-01'
finish = '2022-03-31'
rd = 22  # март 2022

df['Прием курьером.Пакеты доставки.Курьер.Номер курьера'] = df[
    'Прием курьером.Пакеты доставки.Курьер.Номер курьера'].astype(str)
df['Доставка курьером.Пакеты доставки.Курьер.Номер курьера'] = df[
    'Доставка курьером.Пакеты доставки.Курьер.Номер курьера'].astype(str)


def chek_ufa(row):
    if row[2:3] == '.':
        return '0' + row
    else:
        return row


df['Прием курьером.Пакеты доставки.Курьер.Номер курьера'] = df[
    'Прием курьером.Пакеты доставки.Курьер.Номер курьера'].apply(chek_ufa)
df['Доставка курьером.Пакеты доставки.Курьер.Номер курьера'] = df[
    'Доставка курьером.Пакеты доставки.Курьер.Номер курьера'].apply(chek_ufa)

df.rename(columns={'Дата Cоздания': 'дата', 'Номер отправления': 'шт', 'Общая стоимость со скидкой': 'деньги',
                   'Расчетный вес': 'вес', 'Отправитель.Адрес.Город': 'город откуда',
                   'Получатель.Адрес.Город': 'город куда',
                   'Получатель.Дата получения отправления получателем': 'дата получения',
                   'Прием курьером.Пакеты доставки.Курьер.Номер курьера': 'прием',
                   'Доставка курьером.Пакеты доставки.Курьер.Номер курьера': 'доставка'}, inplace=True)


#### уберу нулевки

# df.loc[:, 'ost'] = df.loc[:, 'шт'].apply(lambda x: x[12:])
# df = df.loc[df['ost'] != '-0']

## процедура проверки курьера из этого ли города отправление
# def chek_city(row):
#     if row['шт'][0:2] == row['прием'][0:2]:
#         return 1
#     else:
#         return 0

# df['flag'] = df.loc[:, ['шт', 'прием']].apply(chek_city, axis=1)
# df = df.loc[df['flag'] != 0]

### сборы, консолидация
df_pick = df[df['дата'] >= start]


df_pick.loc[:, 'tmp'] = df_pick.loc[:, 'Отправитель.Дата приема у отправителя'].dt.strftime('%Y-%m-%d')
df_pick = df_pick.sort_values(['tmp', 'Отправитель.Адрес', 'Отправитель.Дата приема у отправителя'])
df_pick = df_pick[df_pick['tmp'] >= start]

df_pick['diff'] = df_pick['Отправитель.Дата приема у отправителя'].diff()
df_pick = df_pick.loc[:,
         ['tmp', 'шт', 'Клиент', 'город откуда', 'Отправитель.Адрес', 'Отправитель.Дата приема у отправителя', 'diff', 'прием']]
t = datetime.datetime.strptime('00:15:00', "%H:%M:%S")
td2 = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

df_pick['консолид'] = 0 # по умолчанию все сконсолидировано

for i in range(df_pick.shape[0]):
    if df_pick.iloc[i, 6] > td2 or df_pick.iloc[i, 6] < datetime.timedelta():
        df_pick.iloc[i, 8] = 1
    if df_pick.iloc[i - 1, 4] != df_pick.iloc[i, 4]:
        df_pick.iloc[i, 6] = datetime.timedelta()
        df_pick.iloc[i, 8] = 1

df_pick.dropna(subset=['tmp'], axis=0, how='any', inplace=True)
df_pick_group = df_pick.groupby(['tmp', 'город откуда'])['консолид'].sum().reset_index()
df_pick_group = df_pick_group.reindex(df_pick_group.sort_values(by=['tmp', 'консолид'], ascending=[True, False]).index)

### доставка, консолидация
df_deliv = df[df['дата получения'] >= start]
df_deliv = df_deliv[df_deliv['дата получения'] <= finish]

df_deliv.loc[:, 'tmp'] = df_deliv.loc[:, 'дата получения'].dt.strftime('%Y-%m-%d')
df_deliv = df_deliv.sort_values(['tmp', 'Получатель.Адрес', 'дата получения'])

df_deliv['diff'] = df_deliv['дата получения'].diff()
df_deliv = df_deliv.loc[:,
         ['tmp', 'шт', 'Клиент', 'город куда', 'Получатель.Адрес', 'дата получения', 'diff', 'доставка']]

df_deliv['консолид'] = 0 # по умолчанию все сконсолидировано

for i in range(df_deliv.shape[0]):
    if df_deliv.iloc[i, 6] > td2 or df_deliv.iloc[i, 6] < datetime.timedelta():
        df_deliv.iloc[i, 8] = 1
    if df_deliv.iloc[i - 1, 4] != df_deliv.iloc[i, 4]:
        df_deliv.iloc[i, 6] = datetime.timedelta()
        df_deliv.iloc[i, 8] = 1

print(df_deliv.info())
df_deliv_group = df_deliv.groupby(['tmp', 'город куда'])['консолид'].sum().reset_index()
df_deliv_group = df_deliv_group.reindex(df_deliv_group.sort_values(by=['tmp', 'консолид'], ascending=[True, False]).index)

###############3

# ###  кол-во курьеров на сборе
# df_curr = df_dep.pivot_table(index=['дата', 'город откуда'], values=['прием'], aggfunc={'прием': set}).reset_index()
# df_curr.loc[:, 'count'] = df_curr.loc[:, 'прием'].apply(lambda x: len(x))
# df_curr = df_curr.reindex(df_curr.sort_values(by=['дата', 'count'], ascending=[True, False]).index)
#
# ###  кол-во курьеров на доставке
# df_curr2 = df_arr.pivot_table(index=['дата получения', 'город куда'], values=['доставка'],aggfunc={'доставка': set}).reset_index()
# df_curr2.loc[:, 'count'] = df_curr2.loc[:, 'доставка'].apply(lambda x: len(x))
# df_curr2 = df_curr2.reindex(df_curr2.sort_values(by=['дата получения', 'count'], ascending=[True, False]).index)
#
# ####
# # set1 = df['шт'].count()
# df_dep.loc[:, 'шт'] = df_dep.loc[:, 'шт'].apply(lambda x: x[0:12])
#
# # set2 = df.groupby(['город откуда', 'шт'])['Клиент'].count().sort_values(ascending=False).reset_index()
# # # print(round((set1 - set2['Клиент'].count()) / set1 * 100, 2), '% конс сборов')
# # set2 = set2[set2['Клиент'] > 1]  # была консолидация и поэтому > 1
# # set2 = set2.groupby(['город откуда'])['Клиент'].sum().sort_values(ascending=False).reset_index()
#
# set2 = df_dep.groupby(['дата', 'город откуда', 'шт'])['Клиент'].count().sort_values(ascending=False).reset_index()
# # set2 = set2.groupby(['дата', 'город откуда'])['Клиент'].sum().sort_values(ascending=False).reset_index()
# set2 = set2.reindex(set2.sort_values(by=['дата', 'Клиент'], ascending=[True, False]).index)
# print(set2)
#
# ##### переделать на адрес сверку, а не клиента
# # set3 = df.groupby(['дата получения', 'город куда', 'шт'])['Клиент'].count().sort_values(
# #     ascending=False).reset_index()
# # set3 = set3[set3['Клиент'] > 1]  # была консолидация и поэтому > 1
# # # print(set3)
# # set3 = set3.groupby(['город куда'])['Клиент'].sum().sort_values(ascending=False).reset_index()
#
# ####
#
# df_dep = df_dep.groupby(by='город откуда')['шт'].count().sort_values(ascending=False).reset_index()
# df_arr = df_arr.groupby(by='город куда')['шт'].count().sort_values(ascending=False).reset_index()
# df_dep.rename(columns={'город откуда': 'город'}, inplace=True)
# df_arr.rename(columns={'город куда': 'город'}, inplace=True)
#
# df_pivot = pd.concat([df_dep, df_arr], axis=0)
# df_pivot = df_pivot.groupby('город')['шт'].sum().sort_values(ascending=False).reset_index()
#
# # df_pivot = df_pivot.merge(set2, how='left', left_on='город', right_on='город откуда')
# # df_pivot.drop('город откуда', axis=1, inplace=True)
# # df_pivot.rename(columns={'Клиент': 'консолидация сбора'}, inplace=True)
# #
# # df_pivot = df_pivot.merge(set3, how='left', left_on='город', right_on='город куда')
# # df_pivot.drop('город куда', axis=1, inplace=True)
# # df_pivot.rename(columns={'Клиент': 'консолидация доставки'}, inplace=True)
#
#
# # df = df.loc[:, ['дата', 'шт', 'Клиент', 'город откуда', 'город куда',
# #                 'дата получения', 'прием', 'доставка']]
#
# #######
#
# writer = pd.ExcelWriter('calc.xlsx', engine='xlsxwriter')
# df_pivot.to_excel(writer, sheet_name='итоги', startrow=1, index=False, header=False) ## общие данные
# set2.to_excel(writer, sheet_name='итоги2', startrow=0, index=False, header=True) ## консолидация сбора
# # set3.to_excel(writer, sheet_name='итоги3', startrow=0, index=False, header=True)  ## консолидация доставки
# # df.to_excel(writer, sheet_name='df', startrow=0, index=False, header=True) ## общий датафрейм
# # df_curr.to_excel(writer, sheet_name='1', startrow=0, index=False, header=True)  ## сбор по городу
# # df_curr2.to_excel(writer, sheet_name='2', startrow=0, index=False, header=True) ## доставка по городу
#
# workbook = writer.book
# worksheet = writer.sheets['итоги']
#
# format = workbook.add_format({'border': 1, 'bg_color': '#E8FBE1', 'num_format': '#,##0'})
# worksheet.set_column('A:K', 10, format)
#
# header_format = workbook.add_format(
#     {'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'fg_color': '#D7E4BC',
#      'align': 'center_across', 'num_format': '#,##0', 'border': 1})
#
# for col_num, value in enumerate(df_pivot.columns.values):
#     worksheet.write(0, col_num, value, header_format)
#
# writer.save()


writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df_pick.to_excel(writer, sheet_name='сбор', startrow=1, index=False, header=False)  ## общие данные
df_pick_group.to_excel(writer, sheet_name='сбор_с консолид', startrow=0, index=False, header=True)
df_deliv.to_excel(writer, sheet_name='доставка', startrow=0, index=False, header=True)
df_deliv_group.to_excel(writer, sheet_name='доставка_с консолид', startrow=0, index=False, header=True)
workbook = writer.book
worksheet = writer.sheets['сбор']

format = workbook.add_format({'border': 1, 'bg_color': '#E8FBE1', 'num_format': '#,##0'})
worksheet.set_column('A:K', 10, format)

header_format = workbook.add_format(
    {'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'fg_color': '#D7E4BC',
     'align': 'center_across', 'num_format': '#,##0', 'border': 1})

for col_num, value in enumerate(df_pick.columns.values):
    worksheet.write(0, col_num, value, header_format)

writer.save()
