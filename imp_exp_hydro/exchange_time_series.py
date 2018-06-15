# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:29:16 2018

@author: jdkern
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_data = pd.read_excel('Synthetic_Path_data.xlsx',header=0)

# select dispatchable imports (positve flow days)
imports = df_data
paths = ['Path66','Path46','Path61','Path42','Path24','Path45']

for p in paths:
    for i in range(0,len(imports)):     
        
        if p == 'Path42':
            if imports.loc[i,p] > 0:
                imports.loc[i,p] = 0
            else:
                imports.loc[i,p] = -imports.loc[i,p]
        
        elif p == 'Path46':
            if imports.loc[i,p] < 0:
                imports.loc[i,p] = 0
            else:
                imports.loc[i,p] = imports.loc[i,p]*.404 + 24*424
        
        else:
            if imports.loc[i,p] < 0:
                imports.loc[i,p] = 0

imports.columns = ['Path66','Path46_SCE','Path61','Path42','Path24','Path45']
imports.to_csv('imports.csv')


# convert to minimum flow time series and dispatchable (daily)
df_mins = pd.read_excel('CA_imports_minflow_profile.xlsx',header=0)
lines = ['Path66','Path46_SCE','Path61']

for i in range(0,len(df_data)):
    for L in lines:
        
        if df_mins.loc[i,L]*24 >= imports.loc[i,L]:
            df_mins.loc[i,L] = imports.loc[i,L]/24
            imports.loc[i,L] = 0
        
        else:
            imports.loc[i,L] = imports.loc[i,L]-df_mins.loc[i,L]*24

dispatchable_imports = imports
dispatchable_imports.to_csv('dispatchable_imports.csv')

# hourly minimum flow for paths
hourly = np.zeros((8760,len(lines)))

for i in range(0,365):
    for L in lines:
        index = lines.index(L)
        
        hourly[i*24:i*24+24,index] = df_mins.loc[i,L]
        
H = pd.DataFrame(hourly)
H.columns = ['Path66','Path46_SCE','Path61']
H.to_csv('CA_path_mins.csv')

# hourly exports
df_data = pd.read_excel('Synthetic_Path_data.xlsx',header=0)
e = np.zeros((8760,4))

#Path 42
path_profiles = pd.read_excel('path_export_profiles.xlsx',sheetname='Path42',header=None)
pp = path_profiles.values

for i in range(0,len(df_data)):
    if df_data.loc[i,'Path42'] > 0:
        e[i*24:i*24+24,0] = pp[i,:]*df_data.loc[i,'Path42']

#Path 24
path_profiles = pd.read_excel('path_export_profiles.xlsx',sheetname='Path24',header=None)
pp = path_profiles.values

for i in range(0,len(df_data)):
    if df_data.loc[i,'Path24'] < 0:
        e[i*24:i*24+24,1] = pp[i,:]*df_data.loc[i,'Path24']*-1

#Path 45
path_profiles = pd.read_excel('path_export_profiles.xlsx',sheetname='Path45',header=None)
pp = path_profiles.values

for i in range(0,len(df_data)):
    if df_data.loc[i,'Path45'] < 0:
        e[i*24:i*24+24,2] = pp[i,:]*df_data.loc[i,'Path45']*-1  
        
#Path 66
path_profiles = pd.read_excel('path_export_profiles.xlsx',sheetname='Path66',header=None)
pp = path_profiles.values

for i in range(0,len(df_data)):
    if df_data.loc[i,'Path66'] < 0:
        e[i*24:i*24+24,2] = pp[i,:]*df_data.loc[i,'Path66']*-1  

exports = pd.DataFrame(e) 
exports.columns = ['Path42','Path24','Path45','Path66']
exports.to_csv('exports.csv')



##########################3
##########################

# HYDRO

# convert to minimum flow time series and dispatchable (daily)

hydro = pd.read_excel('Synthetic_hydro_data.xlsx',header=0)
zones = ['PGE_valley','SCE']
df_mins = pd.read_excel('CA_hydro_minflow_profile.xlsx',header=0)

for i in range(0,len(hydro)):
    for z in zones:
        
        if df_mins.loc[i,z]*24 >= hydro.loc[i,z]:
            df_mins.loc[i,z] = hydro.loc[i,z]/24
            hydro.loc[i,z] = 0
        
        else:
            hydro.loc[i,z] = hydro.loc[i,z]-df_mins.loc[i,z]*24

dispatchable_hydro = hydro
dispatchable_hydro.to_csv('dispatchable_hydro.csv')

# hourly minimum flow for hydro
hourly = np.zeros((8760,len(zones)))

for i in range(0,365):
    for z in zones:
        index = zones.index(z)
        
        hourly[i*24:i*24+24,index] = df_mins.loc[i,z]
        
H = pd.DataFrame(hourly)
H.columns = zones
H.to_csv('CA_hydro_mins.csv')