
# coding: utf-8

# In[3]:

import pandas as pd


# In[7]:

import os
import sys


# In[54]:

df = pd.read_csv("C:/Users/pwendel3/Desktop/OlympicData/gdp.csv")
df2 = pd.DataFrame(columns = ("Id","Country_Name","Year","GDP_Current"))


# In[59]:

for country in range(1,len(df)):
    for i in range(0,10):
        yearin=1980+4*i
        yeareval=yearin
        if yearin==2016:
            yeareval=2015
        column=str(yeareval)
        id=df.ix[country,'Country Code']+"_"+str(yearin)
        if df.ix[country,column] is not 'NaN':
            id = id
            gdp_val = df.ix[country,column]
            data = pd.DataFrame([[id,df.ix[country,'Country Name'],yearin,gdp_val]],columns = df2.columns)
            #print (data)
            df2 = df2.append(data,ignore_index=True)
df2.head()


# In[47]:

df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
df.append(df2)
df.head()


# In[58]:

df = pd.read_csv("C:\Users\pwendel3\Downloads\API_SP.POP.TOTL_DS2_en_csv_v2\pop.csv")
df2 = pd.DataFrame(columns = ("Id","Country_Name","Year","Population"))
for country in range(1,len(df)):
    for i in range(0,10):
        yearin=1980+4*i
        yeareval=yearin
        if yearin==2016:
            yeareval=2015
        column=str(yeareval)
        id=df.ix[country,'Country Code']+"_"+str(yearin)
        if df.ix[country,column] is not 'NaN':
            id = id
            pop = df.ix[country,column]
            data = pd.DataFrame([[id,df.ix[country,'Country Name'],yearin,pop]],columns = df2.columns)
            #print (data)
            df2 = df2.append(data,ignore_index=True)
df2.head()


# In[ ]:



