import pandas as pd
import numpy as np


# def create_companyDF(income, expenses, years):
#     """
#     Создайте функцию create_companyDF(income, expenses, years), которая  возвращает DataFrame, 
#     составленный из входных данных со столбцами “Income” и “Expenses” и индексами, соответствующим годам рассматриваемого периода.
#     """
#     df = pd.DataFrame({'Income': income, 'Expenses': expenses}, index = years)
#     return df

# def get_profit(df, year):
    
#     """
#     А также напишите функцию get_profit(df, year), которая возвращает разницу между доходом и расходом, записанных в таблице df, за год year.
#     Учтите, что если информация за запрашиваемый год не указана в вашей таблице вам необходимо вернуть None. 
#     """
#     profit = df[year]
#     return profit

# expenses = [156, 130, 270]
# income = [478, 512, 196]
# years = [2018, 2019, 2020]
    
# scienceyou = create_companyDF(income, expenses, years)
# print(scienceyou)
# print(scienceyou.loc[2019]['Income'])
# # print(get_profit(scienceyou, 2019))

melb_data = pd.read_csv('C:\\temp\SkillFactory\Labs\data\melb_data.csv', sep=',')
# print(melb_data.iloc[3521]['Landsize']/melb_data.iloc[1690]['Landsize'])
print(melb_data['Type'].value_counts(normalize=True))