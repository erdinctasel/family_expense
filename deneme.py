import pandas as pd
import numpy as np

#Read the data
df=pd.read_csv("expenses.csv")
print(df.info())
print(df)
print(df.shape)
