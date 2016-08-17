# -*- coding: utf-8 -*-
"""
Created on Tue May 24 16:14:19 2016

@author: Raunak Mundada
"""
from __future__ import print_function

import pandas as pd
import sqlSetup

if __name__ == '__main__':
	'''
	sql = """SELECT * FROM 
			(SELECT id,year, count(Name) as athletes,avg(age) as avg_age,sport,sum(Gold_Medals) as Total_Gold, sum(Silver_Medals) as Total_Silver, 
				sum(Bronze_Medals) as Total_Bronze, sum(total) as Grand_Total FROM athlete group by Id, sport) 
		as AGG_MEDALTALLY LEFT JOIN economic_indicators on AGG_MEDALTALLY.id = economic_indicators.id;"""
	'''
	sql = """	select * from 
			country_medals_2016 as cm left join (select Country, Country_Code from country_medals group by Country) 
			as names on cm.Country_Code=names.Country_Code;"""
	query_list,field_names = sqlSetup.query_with_fetchmany(sql)
	df_2016 = sqlSetup.make_frame(query_list,field_names)
	print (df_2016)

