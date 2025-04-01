import pandas as pd

df = pd.read_excel('path/to/file.xlsx', sheet_name='Sheet1', header=0)
df. to_csv('path/to/file.csv', index=False)