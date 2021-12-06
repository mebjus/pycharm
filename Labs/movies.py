import pandas as pd

movie = pd.read_csv('C:\\temp\SkillFactory\Labs\data\movies.csv', sep=',')
rating = pd.read_csv('C:\\temp\SkillFactory\Labs\data\\ratings1.csv', sep=',')
rating2 = pd.read_csv('C:\\temp\SkillFactory\Labs\data\\ratings2.csv', sep=',')
dates = pd.read_csv('C:\\temp\SkillFactory\Labs\data\dates.csv', sep=',')

# print(movie.nunique())
# print(rating.nunique())
# print(pd.to_datetime(dates1['date']).dt.year.mode())

ratings = pd.concat([rating, rating2], ignore_index=True)
ratings = ratings.drop_duplicates(ignore_index=True)
# print(ratings)

ratings_dates = pd.concat([ratings, dates], axis = 1)
print(ratings_dates)
