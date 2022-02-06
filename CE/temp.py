import pandas as pd
import os

df = pd.DataFrame
dirname = 'data/kis/'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)
pd.options.display.float_format = '{:,.0F}'.format

n = 500  ## количество строк из каждого месяца

for file in fullpaths:
    if df.empty:
        df = pd.read_excel(file, header=2, sheet_name=None)
    else:
        df1 = pd.read_excel(file, sheet_name=None)
        df = pd.concat([df, df1], axis=0)


# print(df['Sheet1'].index)
#
# df.drop(df[[df['Sheet1'].index][1,2]], axis=0)
df_pivot = pd.concat(df, axis=0).reset_index(drop=True)




writer = pd.ExcelWriter('summary.xlsx', engine='xlsxwriter')
df_pivot.to_excel(writer, sheet_name='итоги')

workbook = writer.book
worksheet = writer.sheets['итоги']


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
