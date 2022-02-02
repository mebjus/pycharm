# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# df = pd.read_excel('/Users/mebjus/SynologyDrive/temp/DispatchesCount_online.xlsx', header=1)
# # df_m = pd.read_excel('/Users/mebjus/SynologyDrive/temp/day_of_month.xlsx')
# df = df.drop('Unnamed: 7', axis=1)
# # df = df.drop('Unnamed: 0', axis=1)
#
#
# for i in range(1, df.shape[0], 4):
#     # print(df.iloc[i][0])
#     # for j in range(1)
#     df.rename(index={i: df.iloc[i][0] + ' шт.',
#                      i+1: df.iloc[i][0] + ' без скидки',
#                      i+2: df.iloc[i][0] + ' деньги',
#                      i+3: df.iloc[i][0] + ' кг.',
#               }, inplace = True)
#
# # l1 = list(df.columns)
# # print(l1)
# df = df.drop(['Unnamed: 0'], axis=1)
#
# # for i,j in enumerate(df.iloc[0]): #делаем названия столбцов год-месяц-день
# #     y = pd.to_datetime(j)
# #     y = y.strftime('%Y-%m')
# #     df.iloc[0][i] = y
# #
# # df = df.T
#
# # df.rename(columns = {0 : 'месяц',
# #                       }, inplace = True)
# #
# # df = df.groupby(['месяц'], as_index=False).sum().round(0)
# # df = df.merge(df_m, how='left')
# # df['РФ, деньги на рд'] = (df['РФ, деньги'] / df['count']).round()
# # df['РФ, кг на рд'] = (df['РФ, кг'] / df['count']).round()
# #
# # df.drop(482,axis=1,inplace = True)
# #
# #
# df.to_excel('./summary.xlsx', sheet_name='итоги', index=False)
#
#
# print(df)
#
#
#

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('/Users/mebjus/SynologyDrive/temp/DispatchesCount_online.xlsx', header=1)
df_m = pd.read_excel('/Users/mebjus/SynologyDrive/temp/day_of_month.xlsx')
df = df.drop('Unnamed: 7', axis=1)
# df = df.drop([0], axis=0)
# for i in range(1, df.shape[0], 4):
#     df.rename(index={i: df.iloc[i][0] + ' шт',
#                      i+1: df.iloc[i][0] + ' без скидки',
#                      i+2: df.iloc[i][0] + ' деньги',
#                      i+3: df.iloc[i][0] + ' кг',
#               }, inplace = True)



# for i, j in enumerate(df.iloc[0]): #делаем названия столбцов год-месяц-день
#     if i == 0:
#         i = 1
#     y = pd.to_datetime(j)
#     y = y.strftime('%Y-%m')
#     df.iloc[i] = y
print(df)
df.to_excel('./summary.xlsx', sheet_name='итоги', index=False)

# df = df.T

# # df = df.drop([0], axis=1)
# print((df.columns[0]))
# df.rename(columns = {0 : 'месяц'}, inplace = True)

# df = df.groupby(['месяц'], as_index=False).sum().round(0)
# df = df.merge(df_m, how='left')
# df['Итого, деньги на рд'] = (df['Итого деньги'] / df['count']).round()
# df['Итого, кг на рд'] = (df['Итого кг'] / df['count']).round()
# print((df))

#
# df.to_excel('./summary.xlsx', sheet_name='итоги', index=False)
#
# fig = plt.figure(figsize=(15, 5))
#
# plt.subplot(121)
# sns.lineplot(x = 'месяц', y='РФ, кг на рд', data=df, lw=5)
# plt.xticks(rotation=45)
#
# plt.subplot(122)
# sns.lineplot(x = 'месяц', y='РФ, деньги на рд', data=df, lw=5)
# plt.xticks(rotation=45)
# plt.show()
#
# print(df)