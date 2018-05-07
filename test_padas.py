import numpy as np
import pandas as pd
import os

#load .csv
df=pd.read_txt("")
df=pd.read_csv("200W.csv",nrows=400,usecols=(0,1,2,5,6))
print("type of df",type(df))
value=df.values
print("type of value:",type(value))
print("shape of value:",value.shape)