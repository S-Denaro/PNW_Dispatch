# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 10:20:22 2018

@author: Joy Hill
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


##time series of load for each zone
df_load = pd.read_csv('load.csv',header=0)
load = np.array(df_load['PNW'])



##daily hydropower availability 
df_hydro = pd.read_excel('imp_exp_hydro/2010 hydro gen.xlsx',header=None)
hydro = np.array(df_hydro)
hydro = np.reshape(hydro,8760)
   
##time series of wind generation for each zone
df_wind = pd.read_csv('wind.csv',header=0)
wind = np.array(df_wind['PNW'])     
   
##daily time series of dispatchable imports by path
df_imports = pd.read_excel('imp_exp_hydro/Imports and Exports 2010.xlsx',sheetname='imports',header=0)
imports = np.array(df_imports)
imports = np.reshape(imports,8760)

##hourly time series of exports by zone
df_exports = pd.read_excel('imp_exp_hydro/Imports and Exports 2010.xlsx',sheetname='exports',header=0)
exports = np.array(df_exports)
exports = np.reshape(exports,8760)
     

demandandexp = exports + load

reduction = hydro + wind + imports

net_demand = demandandexp - reduction

plt.figure()
plt.plot(demandandexp)
plt.plot(reduction)
plt.plot(net_demand)
plt.legend(['Demand and Exports','Imports, Hydro, and Wind','Net Demand'])
plt.xlabel('day')
plt.ylabel('MW')


