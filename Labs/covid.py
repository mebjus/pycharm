import pandas as pd

covid_data = pd.read_csv('data/covid/covid_data.csv')
vaccinations_data = pd.read_csv('data/covid/country_vaccinations.csv')
vaccinations_data = vaccinations_data[
    ['country', 'date', 'total_vaccinations',
     'people_vaccinated', 'people_vaccinated_per_hundred',
     'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred',
     'daily_vaccinations', 'vaccines']
]


print(covid_data['date'])
covid_data['date'] = pd.to_datetime(covid_data['date'])
covid_data = covid_data.groupby(['date', 'country'], as_index=False)[['confirmed', 'deaths', 'recovered']].sum()

print(vaccinations_data)
