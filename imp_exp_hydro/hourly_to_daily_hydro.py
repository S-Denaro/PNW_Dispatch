# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:05:35 2018

@author: Joy Hill
"""

from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


year = '2010'
#num_years = int(len(years))
days = 365


daily = np.zeros(days)
   

filename = year + ' hydro gen' + '.xlsx'
df_data = pd.read_excel(filename,header=0)
   
v = df_data.loc[:].values
for d in range(0,days):   #for each day    
    daily[d] = np.sum(v[d*24:d*24+24])    #sum the hourly value of the 24 hours
  
    
paths_daily = pd.DataFrame(daily) 
paths_daily.columns = [year + ' hydro']
paths_daily.to_excel('Synthetic_hydro_data.xlsx')