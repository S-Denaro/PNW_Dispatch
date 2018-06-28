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
paths = ['Path3','Path8','Path14','Path65','Path66']
num_paths = int(len(paths))


# calculate export profiles for each path
for p in paths:
    
    profile = np.zeros((days,24,num_years))
    avg_profile = np.zeros((365,24))
    
    sheetname = p
    df_data = pd.read_excel('PNW_Path_data.xlsx',sheetname=p,header=0)

    p_index = paths.index(p)
    
    for y in years:

        y_index = years.index(y)            
    
        v = df_data.loc[:,y].values
        
        if p=='Path3' or p=='Path65' or p=='Path66':   #SCRIPT ASSUMPTION: NEGATIVE = EXPORT. revert sign when needed
            v =-v
        
        for d in range(0,days):   #for each day
            
            sample = np.abs(v[d*24:d*24+24])    #sample the abs value of the 24 hours
            
            if np.sum(v[d*24:d*24+24]) < 0:    #if the sum in the 24 hours is negative(EXPORT)
                
                profile[d,:,y_index] = sample/np.sum(sample)  #calculate hourly profile 
 
        for d in range(0,days):
            
            sample = np.abs(v[d*24:d*24+24])
            
            if np.sum(v[d*24:d*24+24]) > 0:      #if the sum in the 24 hours is positive (IMPORT)
                
                profile[d,:,y_index] = profile[d-1,:,y_index]  #the hourly profile is the same as the previous day
        
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

    filename = p + 'export_profiles.txt'
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
    df_data = pd.read_excel('PNW_Path_data.xlsx',sheetname=p,header=0)

    p_index = paths.index(p)
    
    for y in years:

        y_index = years.index(y)
    
        v = df_data.loc[:,y].values
        
        if p=='Path3' or p=='Path65' or p=='Path66':   #SCRIPT ASSUMPTION: POSITIVE = IMPORT. revert sign when needed
            v =-v
            
        for d in range(0,days):
            
            sample = v[d*24:d*24+24]
            min_flow[d,p_index,y_index] = np.max((0,np.min(sample)))
            
            if any(i>0 for i in sample):

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
                
                #min_flow[d,p_index,y_index] = min_flow[d-1,p_index,y_index]
                max_flow[d,p_index,y_index] = max_flow[d-1,p_index,y_index]
                upramps[d,p_index,y_index] = upramps[d-1,p_index,y_index]                   
                downramps[d,p_index,y_index] = downramps[d-1,p_index,y_index]
        
    #min flows for each path       
    f = min_flow[:,p_index,:]
    Path_min = np.min(f,axis=1)

    #max flows for each path       
    f = max_flow[:,p_index,:]
    Path_max = np.max(f,axis=1)
        
    #add low pass filter
    Path_min_filtered = np.zeros((365,1))

    for i in range(15,350):
        Path_min_filtered[i] = np.mean(Path_min[i-15:i+15])
        Path_min_filtered[0:15] = Path_min_filtered[15]
        Path_min_filtered[350:] = Path_min_filtered[349]
    
    filename = p + 'minflow.txt'
    np.savetxt(filename,Path_min_filtered)
    
    #ramp rates
    Path_down = np.percentile(downramps[:,p_index,:],90)
    Path_up = np.percentile(upramps[:,p_index,:],90)    
    #max capacity
    Path_cap = np.max(Path_max)
    filename = p + '_down_up_cap.txt'
    np.savetxt(filename,np.c_[Path_down, Path_up, Path_cap])
                
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
    





