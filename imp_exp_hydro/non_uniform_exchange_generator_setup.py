# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:29:16 2018

@author: jdkern
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


years = [2010,2011,2012]
num_years = int(len(years))
days = 365
hours = 8760
paths = ['Path42']
num_paths = int(len(paths))

   
for p in paths:
    
    profile = np.zeros((days,24,num_years))
    avg_profile = np.zeros((365,24))
    
    sheetname = p
    df_data = pd.read_excel('OtherCA_Path_data.xlsx',sheetname=p,header=0)

    p_index = paths.index(p)
    
    for y in years:

        y_index = years.index(y)            
    
        v = df_data.loc[:,y].values
        
        if p=='Path42':
            v =-v
        
        for d in range(0,days):
            
            sample = np.abs(v[d*24:d*24+24])
            
            if np.sum(v[d*24:d*24+24]) < 0:
                
                profile[d,:,y_index] = sample/np.sum(sample)
 
        for d in range(0,days):
            
            sample = np.abs(v[d*24:d*24+24])
            
            if np.sum(v[d*24:d*24+24]) > 0:
                
                profile[d,:,y_index] = profile[d-1,:,y_index]
        
# average profile
for d in range(0,days):
    
    count = 0
    
    for y in years: 
        
        y_index = years.index(y)
        
        if profile[d,0,y_index] > 0:
           
            count = count + 1
            avg_profile[d,:] = avg_profile[d,:] + profile[d,:,y_index]

    if count > 0:
        avg_profile[d,:] = avg_profile[d,:]/count

filename = p + 'profiles.txt'
np.savetxt(filename,avg_profile)
    
plt.figure()
plt.title(p)
plt.plot(np.transpose(avg_profile))
    

# positive flow parameters
    
upramps = np.zeros((days,num_paths,num_years))
downramps = np.zeros((days,num_paths,num_years))
min_flow = np.zeros((days,num_paths,num_years))
max_flow = np.zeros((days,num_paths,num_years))

for p in paths:
    
    sheetname = p
    df_data = pd.read_excel('OtherCA_Path_data.xlsx',sheetname=p,header=0)

    p_index = paths.index(p)
    
    for y in years:

        y_index = years.index(y)
    
        v = df_data.loc[:,y].values
        
        if p=='Path42':
            v = -v
    
        for d in range(0,days):
            
            sample = v[d*24:d*24+24]
            
            if all(i>0 for i in sample):
                
                min_flow[d,p_index,y_index] = np.min(sample)
                max_flow[d,p_index,y_index] = np.max(sample)
                
                ramp = 0
                
                for h in range(0,23):
                    if ramp < sample[h+1] - sample[h]:
                        ramp = sample[h+1] - sample[h]
                
                upramps[d,p_index,y_index] = ramp
                    
                ramp = 0
                
                for h in range(0,23):
                    if ramp < sample[h] - sample[h+1]:
                        ramp = sample[h] - sample[h+1]
                
                downramps[d,p_index,y_index] = ramp
    
        for d in range(0,days):
            
            sample = v[d*24:d*24+24]
            
            if any(i<0 for i in sample):
                
                min_flow[d,p_index,y_index] = min_flow[d-1,p_index,y_index]
                max_flow[d,p_index,y_index] = max_flow[d-1,p_index,y_index]
                upramps[d,p_index,y_index] = upramps[d-1,p_index,y_index]                   
                downramps[d,p_index,y_index] = downramps[d-1,p_index,y_index]
                
# plot
for p in paths:
    
    p_index = paths.index(p)
    
    plt.figure()
    
    for y in years:
            
        y_index = years.index(y)
            
        plt.plot(upramps[:,p_index,y_index])
        plt.title(p + '_Upramps')
 
    plt.figure()
    
    for y in years:
            
        y_index = years.index(y)
        plt.plot(downramps[:,p_index,y_index])
        plt.title(p + '_Downramps')           

    plt.figure()
    
    for y in years:
            
        y_index = years.index(y)
        plt.plot(min_flow[:,p_index,y_index])
        plt.title(p + '_Minflow')      
    
    plt.figure()
    
    for y in years:
            
        y_index = years.index(y)
        plt.plot(max_flow[:,p_index,y_index])
        plt.title(p + '_Maxflow')  
    
#min flows for each path       

f = min_flow[:,0,:]
Path_min = np.min(f,axis=1)

#max flows for each path       
f = max_flow[:,0,:]
Path_max = np.max(f,axis=1)


#add low pass filter
Path_min_filtered = np.zeros((365,1))

for i in range(15,350):
    Path_min_filtered[i] = np.mean(Path_min[i-15:i+15])
    

Path_min_filtered[0:15] = Path_min_filtered[15]
Path_min_filtered[350:] = Path_min_filtered[349]


np.savetxt('Path_minflow.txt',Path_min_filtered)

#ramp rates
Path_down = np.percentile(downramps[:,0,:],90)
Path_up = np.percentile(upramps[:,0,:],90)
    
#max capacity
Path_cap = np.max(Path_max)


