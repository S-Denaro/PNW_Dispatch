# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:29:16 2018

@author: jdkern
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


years = ['2001','2005','2010','2011']
num_years = int(len(years))
days = 365
hours = 8760
#regions = ['PNW']
#num_regions = int(len(regions))
upramps = np.zeros((days,num_years))
downramps = np.zeros((days,num_years))
min_flow = np.zeros((days,num_years))
max_flow = np.zeros((days,num_years))

for y in (0,3):
    
    y_index = y
    
#    for r in regions:
#        r_index = regions.index(r)
        
    #load data - should include 2006 and 2001 data to include hydrologic conditions
    filename = years[y] + ' hydro gen' + '.xlsx'
    M = pd.read_excel(filename,header=None)
    m = M.as_matrix()
            
    v = np.sum(m,axis=1)
            
    for d in range(0,days):
            
                        
        sample = v[d*24:d*24+24]
        min_flow[d,y_index] = np.min(sample)
        max_flow[d,y_index] = np.max(sample)
            
        ramp = 0
            
        for h in range(0,22):
            if ramp < sample[h+1] - sample[h]:
                ramp = sample[h+1] - sample[h]
            
        upramps[d,y_index] = ramp
                
        ramp = 0
            
        for h in range(0,22):
            if ramp < sample[h] - sample[h+1]:
                ramp = sample[h] - sample[h+1]
            
        downramps[d,y_index] = ramp
                

# select ramping rates across years
#for r in regions:
    
#    r_index = regions.index(r)
    
    plt.figure()
    
    for y in years:
            
        y_index = years.index(y)
            
        plt.plot(upramps[:,y_index])
        plt.title('Upramps')
 
    plt.figure()
    
    for y in years:
            
        y_index = years.index(y)
        plt.plot(downramps[:,y_index])
        plt.title('Downramps')           

    plt.figure()
    
    for y in years:
            
        y_index = years.index(y)
        plt.plot(min_flow[:,y_index])
        plt.title('Minflow')      
    
    plt.figure()
    
    for y in years:
            
        y_index = years.index(y)
        plt.plot(max_flow[:,y_index])
        plt.title('Maxflow')  
        
#min flows for each zone       
f = min_flow[:,:]
PNW_min = np.min(f,axis=1)

#f = min_flow[:,0,:]
#PGE_V_min = np.min(f,axis=1)
#
##max flows for each zone       
f = max_flow[:,:]
PNW_max = np.max(f,axis=1)
#
#f = max_flow[:,0,:]
#PGE_V_max = np.max(f,axis=1)



#add low pass filter
PNW_min_filtered = np.zeros((365,1))
#PGE_V_min_filtered = np.zeros((365,1))

for i in range(15,350):
    PNW_min_filtered[i] = np.mean(PNW_min[i-15:i+15])
   

PNW_min_filtered[0:15] = PNW_min_filtered[15]
PNW_min_filtered[350:] = PNW_min_filtered[349]


np.savetxt('PNW_hydro_minflow.txt',PNW_min_filtered)
np.savetxt('PNW_hydro_upramps.txt',upramps)
np.savetxt('PNW_hydro_downramps.txt',downramps)

    


#ramp rates
PNW_down = np.percentile(downramps[:,2:],90)
PNW_up = np.percentile(upramps[:,2:],90)

    
#max capacity
PNW_cap = np.max(PNW_max)

