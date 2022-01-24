import pandas as pd

covid_data = pd.read_csv('data/covid/covid_19_data.csv', index_col='SNo')
vaccinations_data = pd.read_csv('data/covid/country_vaccinations.csv')
vaccinations_data = vaccinations_data[
    ['country', 'date', 'total_vaccinations',
     'people_vaccinated', 'people_vaccinated_per_hundred',
     'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred',
     'daily_vaccinations', 'vaccines']
]

print(covid_data)
print(vaccinations_data)