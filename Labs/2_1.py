import pandas as pd

melb_data = pd.read_csv('data/melb_data_fe.csv', sep=',')
melb_df = melb_data.copy()

print(melb_df.head(10))
