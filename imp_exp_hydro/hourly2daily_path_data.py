# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 16:44:12 2018

@author: sdenaro
"""

from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import load_workbook


years = [2011]
num_years = int(len(years))
days = 365
paths = ['Path3','Path8','Path14','Path65','Path66']
num_paths = int(len(paths))

daily = np.zeros((days,num_paths))
count=0   

for p in paths:
    sheetname = p
    df_data = pd.read_excel('PNW_Path_data.xlsx',sheetname=p,header=0)
   
    for y in years:         
        v = df_data.loc[:,y].values
        for d in range(0,days):   #for each day    
            daily[d,count] = np.sum(v[d*24:d*24+24])    #sum the hourly value of the 24 hours
    count+=1
    
paths_daily = pd.DataFrame(daily) 
paths_daily.columns = paths

book = load_workbook('Synthetic_Path_data.xlsx')
writer = pd.ExcelWriter('Synthetic_Path_data.xlsx', engine = 'openpyxl')
writer.book = book
paths_daily.to_excel(writer,sheet_name='2011')
writer.save()
writer.close()