from datetime import datetime
import pandas as pd


filename = "last_update2.csv"

df = pd.read_csv(filename)

print(df)

print(type(df.last_update))

datetime_column = []
for last_update in df.last_update:
    print(type(last_update), last_update)
    new_last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
    datetime_column.append(new_last_update)
    df.apply(lambda x: x.replace(last_update, new_last_update))


# new_column = pd.Series(datetime_column, name='last_update')
# df.update(new_column)
print(df)
print(type(df.last_update[0]))


# df.last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
