# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 11:34:07 2018

@author: sdenaro
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
from scipy import stats

#%%==============================================================================
# load dispatch data
v_year = 2011
 
df_mwh1 = pd.read_csv('%d_simulation/mwh_1.csv'% v_year,header=0)
df_mwh2 = pd.read_csv('%d_simulation/mwh_2.csv'% v_year,header=0)
df_mwh3 = pd.read_csv('%d_simulation/mwh_3.csv'% v_year,header=0)

# select thermal
df_mwh1 = df_mwh1.drop(df_mwh1[(df_mwh1.Type == "Hydro")|(df_mwh1.Type == "Slack")|(df_mwh1.Type == "imports")|(df_mwh1.Type == "PSH")].index)
df_mwh2 = df_mwh2.drop(df_mwh2[(df_mwh2.Type == "Hydro")|(df_mwh2.Type == "Slack")|(df_mwh2.Type == "imports")|(df_mwh2.Type == "PSH")].index)
df_mwh3 = df_mwh3.drop(df_mwh3[(df_mwh3.Type == "Hydro")|(df_mwh3.Type == "Slack")|(df_mwh3.Type == "imports")|(df_mwh3.Type == "PSH")].index)

# sum hourly thermal
thermal_dispatch=np.zeros((24*364,1))
for i in range (0,len(thermal_dispatch)):
    thermal_dispatch[i] =sum(df_mwh1[df_mwh1.Time == i+1]['Value']) + sum(df_mwh2[df_mwh2.Time == i+1]['Value']) + sum(df_mwh3[df_mwh3.Time == i+1]['Value'])

# load BPA thermal data
df_BPA_thermal = pd.read_excel('BPA_thermal_07_17.xlsx',header=0, sheetname="year %d"% v_year)

# BPA thermal is about 60% of total thermal in the PNW.
PNW_thermal = df_BPA_thermal['thermal generation (MW)']*10/6

# Plot Valid
t=range(1,len(thermal_dispatch)+1)
plt.figure()
plt.plot(t,thermal_dispatch, 'r', lw=.8)
plt.plot(t,df_BPA_thermal.iloc[0:len(thermal_dispatch)], 'b', lw=.8)
plt.plot(t,PNW_thermal[0:len(thermal_dispatch)], 'g', lw=.8)
plt.legend(['simulated','BPA historical', 'BPA scaled to PNW capacity'])
plt.title('Thermal generation (MW) %d'% v_year)
plt.show
py.savefig('%d_simulation/Thermal_valid%d.png'% (v_year,v_year), bbox_inches='tight')
