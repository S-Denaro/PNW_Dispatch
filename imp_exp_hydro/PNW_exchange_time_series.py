# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:29:16 2018
@author: jdkern
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_data = pd.read_excel('Synthetic_Path_data.xlsx',sheetname='2010',header=0)

# select dispatchable imports 
imports = df_data
paths = ['Path3','Path8','Path14','Path65','Path66']

for p in paths:
    for i in range(0,len(imports)):     
        
        if p=='Path3' or p=='Path65' or p=='Path66':   #SCRIPT ASSUMPTION: NEGATIVE = EXPORT. revert sign when needed
            if imports.loc[i,p] >= 0:
                imports.loc[i,p] = 0
            else:
                imports.loc[i,p] = -imports.loc[i,p]
        
        else:
            if imports.loc[i,p] < 0:
                imports.loc[i,p] = 0

imports.columns = ['Path3','Path8','Path14','Path65','Path66']
imports.to_csv('imports.csv')


# convert to minimum flow time series and dispatchable (daily)
df_mins = pd.read_excel('PNW_imports_minflow_profiles.xlsx',header=0)
lines = ['Path3','Path8','Path14','Path65','Path66']

for i in range(0,len(df_data)):
    for L in lines:
        
        if df_mins.loc[i,L]*24 >= imports.loc[i,L]:
            df_mins.loc[i,L] = imports.loc[i,L]/24
            imports.loc[i,L] = 0
        
        else:
            imports.loc[i,L] = np.max((0,imports.loc[i,L]-df_mins.loc[i,L]*24))

dispatchable_imports = imports
dispatchable_imports.to_csv('dispatchable_imports.csv')


df_data = pd.read_csv('imports.csv',header=0)

# hourly minimum flow for paths
hourly = np.zeros((8760,len(lines)))

for i in range(0,365):
    for L in lines:
        index = lines.index(L)
        
        hourly[i*24:i*24+24,index] = np.min((df_mins.loc[i,L], df_data.loc[i,L]))
        
H = pd.DataFrame(hourly)
H.columns = ['Path3','Path8','Path14','Path65','Path66']
H.to_csv('PNW_path_mins.csv')

# hourly exports
df_data = pd.read_excel('Synthetic_Path_data.xlsx',header=0)
e = np.zeros((8760,5))

for p in paths:
    
    path_profiles = pd.read_excel('PNW_Path_export_profiles.xlsx',sheetname=p,header=None)
    
    p_index = paths.index(p)
    pp = path_profiles.values
    
    if p=='Path3' or p=='Path65' or p=='Path66':   #SCRIPT ASSUMPTION: NEGATIVE = EXPORT. revert sign when needed
            df_data.loc[:,p]=-df_data.loc[:,p]

    for i in range(0,len(df_data)):
        if df_data.loc[i,p] < 0:
            e[i*24:i*24+24,p_index] = pp[i,:]*-df_data.loc[i,p]

exports = pd.DataFrame(e) 
exports.columns = ['Path3','Path8','Path14','Path65','Path66']
exports.to_csv('exports.csv')



##########################3
##########################

# HYDRO

# convert to minimum flow time series and dispatchable (daily)

df_data = pd.read_excel('Synthetic_hydro_data.xlsx',header=0)
hydro = df_data
df_mins = pd.read_excel('PNW_hydro_minflow_profile.xlsx',header=0)

for i in range(0,len(hydro)):
        if df_mins.loc[i]*24 >= hydro.loc[i]:
            df_mins.loc[i] = hydro.loc[i]/24
            hydro.loc[i] = 0       
        else:
            hydro.loc[i] = np.max((0,hydro.loc[i]-df_mins.loc[i]*24))

dispatchable_hydro = hydro
dispatchable_hydro.to_csv('dispatchable_hydro.csv')

# hourly minimum flow for hydro
hourly = np.zeros(8760,1)

df_data = pd.read_excel('Synthetic_hydro_data.xlsx',header=0)

for i in range(0,365):
        hourly[i*24:i*24+24] = np.min((df_mins.loc[i],df_data.loc[i]))
        
H = pd.DataFrame(hourly)
H.to_csv('PNW_hydro_mins.csv')