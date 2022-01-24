import pandas as pd
import matplotlib.pyplot as plt

covid_data = pd.read_csv('data/covid/covid_data.csv')
vaccinations_data = pd.read_csv('data/covid/country_vaccinations.csv')
vaccinations_data = vaccinations_data[
    ['country', 'date', 'total_vaccinations',
     'people_vaccinated', 'people_vaccinated_per_hundred',
     'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred',
     'daily_vaccinations', 'vaccines']
]


covid_data = covid_data.groupby(['date', 'country'], as_index=False)[['confirmed', 'deaths', 'recovered']].sum()

covid_data['date'] = pd.to_datetime(covid_data['date'])
covid_data['active'] = covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']
covid_data = covid_data.sort_values(by=['country', 'date'])

covid_data['daily_confirmed'] = covid_data.groupby('country')['confirmed'].diff()
covid_data['daily_deaths'] = covid_data.groupby('country')['deaths'].diff()
covid_data['daily_recovered'] = covid_data.groupby('country')['recovered'].diff()

vaccinations_data['date'] = pd.to_datetime(vaccinations_data['date'])

# print(covid_data['date'].min(), covid_data['date'].max())

covid_df = covid_data.merge(vaccinations_data, on=['date', 'country'], how='left')
# print(covid_df.shape)

covid_df['death_rate'] = (covid_df['deaths'] / covid_df['confirmed']) * 100
covid_df['recover_rate'] = (covid_df['recovered'] / covid_df['confirmed']) * 100

c = covid_df[covid_df['country'] == 'United States'].groupby('country')['death_rate'].max()
# print(round(c, 2))
russia = covid_df[covid_df['country'] == 'Russia'].groupby('country')['recover_rate'].mean()
print(round(russia, 2))
grouped_cases = covid_df.groupby('date')['daily_confirmed'].sum()
grouped_cases.plot(kind='line', figsize=(12, 4), title='Ежедневная заболеваемость по всем странам', grid=True, lw=3)
plt.show()