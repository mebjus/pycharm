dict_fo = {'СЗФО': ['ВЕЛИКИЙ НОВГОРОД', 'МУРМАНСК', 'ПЕТРОЗАВОДСК', 'СЫКТЫВКАР', 'САНКТ-ПЕТЕРБУРГ', 'АРХАНГЕЛЬСК', 'КАЛИНИНГРАД'],
           'УФО': ['КУРГАН', 'НИЖНЕВАРТОВСК', 'НОВЫЙ УРЕНГОЙ', 'СТЕРЛИТАМАК', 'МАГНИТОГОРСК', 'ОРЕНБУРГ', 'СУРГУТ', 'ЕКАТЕРИНБУРГ', 'ПЕРМЬ', 'ТЮМЕНЬ', 'УФА', 'ЧЕЛЯБИНСК'],
           'ПФО': ['ИЖЕВСК', 'ПЕНЗА', 'УЛЬЯНОВСК', 'ЧЕБОКСАРЫ', 'КИРОВ', 'НИЖНИЙ НОВГОРОД', 'КАЗАНЬ', 'САМАРА', 'САРАТОВ', 'ТОЛЬЯТТИ'],
           'ЮФО': ['НОВОРОССИЙСК', 'СИМФЕРОПОЛЬ', 'ПЯТИГОРСК', 'РОСТОВ-НА-ДОНУ', 'ВОЛГОГРАД', 'ВОРОНЕЖ', 'КРАСНОДАР', 'СТАВРОПОЛЬ', 'АСТРАХАНЬ', 'СОЧИ'],
           'СФО': ['БАРНАУЛ', 'НОВОКУЗНЕЦК', 'ТОМСК', 'УЛАН-УДЭ', 'НОВОСИБИРСК', 'КРАСНОЯРСК', 'ОМСК', 'ИРКУТСК', 'КЕМЕРОВО'],
           'ДВФО': ['ВЛАДИВОСТОК', 'ХАБАРОВСК']
           }

for i in dict_fo.keys():  # преобразование словаря верхний регистр
    d = []
    for j in dict_fo[i]:
        c = j.upper()
        d.append(c)
    dict_fo[i] = d
    print(d)


# df1 = pd.read_excel('data/2021_07_2.xls', header=2)
# df2 = pd.read_excel('data/2021_08_1.xls', header=2)
# df3 = pd.read_excel('data/2021_08_2.xls', header=2)
# df4 = pd.read_excel('data/2021_09_1.xls', header=2)
# df5 = pd.read_excel('data/2021_09_2.xls', header=2)
# df6 = pd.read_excel('data/2021_10_1.xls', header=2)
# df7 = pd.read_excel('data/2021_10_2.xls', header=2)
# df8 = pd.read_excel('data/2021_11_1.xls', header=2)
# df9 = pd.read_excel('data/2021_11_2.xls', header=2)
# df10 = pd.read_excel('data/2021_12_1.xlsx', header=2)
# df11 = pd.read_excel('data/2021_12_2.xlsx', header=2)

# df = df.merge(df1, how='outer')
# df = df.merge(df2, how='outer')
# df = df.merge(df3, how='outer')
# df = df.merge(df4, how='outer')
# df = df.merge(df5, how='outer')
# df = df.merge(df6, how='outer')
# df = df.merge(df7, how='outer')
# df = df.merge(df8, how='outer')
# df = df.merge(df9, how='outer')
# df = df.merge(df10, how='outer')
# df = df.merge(df11, how='outer')
