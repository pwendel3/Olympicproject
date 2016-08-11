
# coding: utf-8

import pandas as pd
import os
import sys
import zipfile, urllib, csv
import sqlSetup

DB_NAME = "Olympics_DB"

def get_items(url):
    filehandle, _ = urllib.urlretrieve(url)
    zip_file_object = zipfile.ZipFile(filehandle, 'r')
    first_file = zip_file_object.namelist()[1]
    file = zip_file_object.open(first_file)
    content = pd.read_csv(file,header=2)
    return content


#Arrange world bank raw data in desired format
def cleanData(df,Economic_Factor):
    df_cleaned = pd.DataFrame(columns = ("Id","Country_Name","Year",Economic_Factor))
    for country in range(1,len(df)):
        for i in range(0,10):
            year_in = 1980+4*i
            year_val = year_in
            if year_in == 2016:
                year_val = 2015
            column = str(year_val)
            id = df.ix[country,'Country Code'] + "_" + str(year_in)
            if df.ix[country,column] is not 'NaN':
                eco_fac = df.ix[country,column]
                data = pd.DataFrame([[id,df.ix[country, 'Country Name'], year_val, eco_fac]],columns = df_cleaned.columns)
                df_cleaned = df_cleaned.append(data,ignore_index = True)
    return df_cleaned


if __name__ == '__main__':
    # Get GDP (Current $) data
    gdp_url = 'http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv'
    gdp_contents = get_items(gdp_url)
    gdp = cleanData(gdp_contents,"GDP_Val")
    # Get total population
    total_pop_url = 'http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv'
    total_pop_contents = get_items(total_pop_url)
    total_pop = cleanData(total_pop_contents,"Total_Population")
    #Merge the two data frames
    Economic_indicators = gdp.merge(total_pop,on='Id',how = 'inner')
    Economic_indicators = Economic_indicators.drop(['Country_Name_x','Year_x'], axis = 1)
    Economic_indicators = Economic_indicators.rename(index = str,columns={'Country_Name_y':'Country_Name','Year_y':'Year'})

    # Add to SQL database
    print ("Update Economic Factors")
    sqlSetup.mysqlConn()
    sqlSetup.update_EconomicIndicators(Economic_indicators)

    #Write file to CSV
    Economic_indicators.to_csv(path_or_buf = "D:\Olympics_Data\Data\Economic_Indicators.csv")

