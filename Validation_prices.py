# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:56:56 2018

@author: sdenaro
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
from scipy import stats
import datetime as dt

#%%==============================================================================
# load simulated zonal prices
v_year = 2011

df_sim = pd.read_csv('%d_simulation/zonal_prices%d_min.csv'% (v_year,v_year),header=0)
sim_prices=np.zeros((365,1))
for i in range(0,365):
   sim_prices[i]=np.mean(df_sim[i*24:(i+1)*24])

df_prices_hist = pd.read_excel('fuel_prices/MID-C Hub_hist.xls',header=0)

start=dt.datetime(v_year,01,01).strftime("%Y-%m-%d %H:%M:%S") 
dates=[dt.datetime.strptime(start,"%Y-%m-%d %H:%M:%S") + dt.timedelta(days=d) for d in range(0,365)]
hist_prices=pd.DataFrame(data=dates,columns=['Trade Date'])

hist_prices=hist_prices.merge(df_prices_hist[['Trade Date','Wtd Avg Price $/MWh']],how='left')

# Plot Valid
t=range(1,len(sim_prices)+1)
plt.figure()
plt.plot(t,sim_prices, 'r', lw=.8)
plt.plot(t,hist_prices['Wtd Avg Price $/MWh'], '.b')
plt.legend(['simulated','historical'])
plt.title('MID-C avg daily Price $/MWh %d'% v_year)
plt.show
py.savefig('%d_simulation/Prices_valid%d.png'% (v_year,v_year), bbox_inches='tight')
