import pandas as pd
import os

df = pd.DataFrame
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.2F}'.format

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


def todate(arg):
    arg = pd.to_datetime(arg)
    return arg.strftime('%Y-%m-%d')


def todate1(arg):
    arg = pd.to_datetime(arg)
    return arg.strftime('%Y-%m')


df['Дата Cоздания'] = df['Дата Cоздания'].apply(todate)

df.rename(columns={'Дата Cоздания': 'дата',
                   'Номер отправления': 'шт', 'Общая стоимость со скидкой': 'деньги'},
          inplace=True)

# отбрасываем все нулевки, консолидированные сборы, дешевые доборы
# df = df[df['деньги'] > 10]

## преобразуем  дата фрейм под Москву

df.loc[:,'шт'] = df.loc[:, 'шт'].apply(lambda x: x[0:12])   # отрезаем отправления -

mask1 = df['Отправитель.Адрес.Город'] == 'Москва'
mask2 = df['Получатель.Адрес.Город'] == 'Москва'
df_dep = df[mask1]
df_arr = df[mask2]

df_inner = df[(mask1 & mask2)]
df_or = df[(mask1 | mask2)]


df_cons_dep = df_dep.groupby(['шт', 'дата'])['Клиент'].count().reset_index()
df_cons_arr = df_arr.groupby(['шт', 'дата'])['Клиент'].count().reset_index()


df_cons_dep.rename(columns={'шт': 'номер', 'Клиент': 'количество'}, inplace=True)
df_cons_arr.rename(columns={'шт': 'номер', 'Клиент': 'количество'}, inplace=True)

df_cons_dep = df_cons_dep[df_cons_dep['количество'] > 1]
df_cons_arr = df_cons_arr[df_cons_arr['количество'] > 1]  # >1

a1 = df_dep.shape[0] + df_arr.shape[0]
a2 = a1 - df_cons_dep['количество'].sum() + df_cons_dep['номер'].count()

# print('Кол отправлений из Москвы или в Москву: {:,.0F}'.format(a1))
# print('Кол отправлений в Москву из Москвы (вкл в общ): ', df[(mask1 & mask2)].shape[0])
print('Кол стопов: {:,.0F}'.format(a2))

a3 = df_or['дата'].apply(todate1).reset_index()
a3 = a3.groupby('дата').sum()
a3 = a3.merge(df_m, left_on='дата', right_on='Дата', how='left')

print('Сумма деньги: {:,.0F}'.format((df_inner['деньги'].sum() + df_or['деньги'].sum())/2))
print('Расчетный вес: {:,.0F}'.format((df_inner['Расчетный вес'].sum() + df_or['Расчетный вес'].sum())/2))


df = pd.Series({'Количество отправлений': a1, 'Количество стопов': a2, 'Количество рд': a3['р.д.'][0]})

print('Количество рд', a3['р.д.'][0])


###################### сохраняем в файл

# writer = pd.ExcelWriter('consolid.xlsx', engine='xlsxwriter')
#
# df.to_excel(writer, sheet_name='итоги', header=False, index=True)
# df_cons_dep.to_excel(writer, sheet_name='отправлено из Мск', index=False)  # index=False header=False
# df_cons_arr.to_excel(writer, sheet_name='доставлено в Мск', index=False)
#
# df_or.to_excel(writer, sheet_name='отправитель_получатель', index=False)  # index=False header=False
# df_inner.to_excel(writer, sheet_name='из Мск в Мск', index=False)
#
# workbook = writer.book
# writer.save()
