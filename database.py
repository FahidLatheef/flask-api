import pandas as pd
import datetime


# df1 is table1 and df2 is table2
df1 = pd.read_csv("data/table1.csv")
df2 = pd.read_csv("data/table2.csv")

# Function to convert time string to datetime format
def date_convert(date_to_convert):
    try:
        return datetime.datetime.strptime(str(date_to_convert), f'%Y-%m-%d %X.%f')
    except:
        return float('nan')

# Converting time string to datetime format for table1
df1['created_at'] = df1['created_at'].apply(date_convert)
df1['updated_at'] = df1['updated_at'].apply(date_convert)

# Converting time string to datetime format for table2
df2['created_at'] = df2['created_at'].apply(date_convert)
df2['updated_at'] = df2['updated_at'].apply(date_convert)

