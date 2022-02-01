import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('/Users/mebjus/SynologyDrive/temp/DispatchesCount_online.xlsx', header=1)
df_m = pd.read_excel('/Users/mebjus/SynologyDrive/temp/day_of_month.xlsx')
df = df.drop('Unnamed: 7', axis=1)
df = df.drop('Unnamed: 0', axis=1)


for i,j in enumerate(df.iloc[0]): #делаем названия столбцов год-месяц-день
    y = pd.to_datetime(j)
    y = y.strftime('%Y-%m')
    df.iloc[0][i] = y

df = df.T

df.rename(columns = {0 : 'месяц',
                      53 : 'Владивосток, шт',
                      55 : 'Владивосток, деньги',
                      56 : 'Владивосток, кг',

                      65 : 'Волгоград, шт',
                      67 : 'Волгоград, деньги',
                      68 : 'Волгоград, кг',

                      73 : 'Воронеж, шт',
                      75 : 'Воронеж, деньги',
                      76 : 'Воронеж, кг',

                      189 : 'Москва',
                      481 : 'РФ, шт',
                      483 : 'РФ, деньги',
                      484 : 'РФ, кг',
                      }, inplace = True)

df = df.groupby(['месяц'], as_index=False).sum().round(0)
df = df.merge(df_m, how='left')
df['РФ, деньги на рд'] = (df['РФ, деньги'] / df['count']).round()
df['РФ, кг на рд'] = (df['РФ, кг'] / df['count']).round()

df.drop(482,axis=1,inplace = True)


df.to_excel('./summary.xlsx', sheet_name='итоги', index=False)

fig = plt.figure(figsize=(15, 5))

plt.subplot(121)
sns.lineplot(x = 'месяц', y='РФ, кг на рд', data=df, lw=5)
plt.xticks(rotation=45)

plt.subplot(122)
sns.lineplot(x = 'месяц', y='РФ, деньги на рд', data=df, lw=5)
plt.xticks(rotation=45)
plt.show()

# print(df)