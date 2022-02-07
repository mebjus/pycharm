import pandas as pd
import os

dirname = 'data/kis'
dirfiles = os.listdir(dirname)
fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)

for i in fullpaths:
    if i.find('.xls') != -1:
        df = pd.read_excel(i, header=2, sheet_name=None)
        print(i)

print(df)