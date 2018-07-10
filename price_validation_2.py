# -*- coding: utf-8 -*-
"""
Created on Wed May 03 15:01:31 2017

@author: jdkern
"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#==============================================================================
 
df_mwh1 = pd.read_csv('mwh_1.csv',header=0)
df_mwh2 = pd.read_csv('mwh_2.csv',header=0)
df_mwh3 = pd.read_csv('mwh_3.csv',header=0)
df_gen = pd.read_csv('generators.csv',header=0)
oil_price = 20
coal_price = 2
#df_histprice = pd.read_excel('2011_historical_prices.xlsx',header=0)
df_load = pd.read_csv('load.csv',header=0)
df_gasprice = pd.read_csv('NG.csv',header=0)
 
mwh_1 = df_mwh1.values
mwh_2 = df_mwh2.values
mwh_3 = df_mwh3.values

zone5 = [] # PG&E bay

 #
sorted_mwh1 = sorted(mwh_1,key=lambda x: x[3],reverse=True)
sorted_mwh2 = sorted(mwh_2,key=lambda x: x[3],reverse=True)
sorted_mwh3 = sorted(mwh_3,key=lambda x: x[3],reverse=True)
mwh1count = 0
mwh2count = 0
mwh3count = 0
zone51count = 0
zone52count = 0
zone53count = 0

for i in range(0,len(sorted_mwh1)):
    
    a = sorted_mwh1[i]
    b = sorted_mwh2[i]
    c = sorted_mwh3[i]
 # 
    if a[3] > 0:
        mwh1count = mwh1count+1
     
    if b[3] > 0:
        mwh2count = mwh2count+1
         
    if c[3] > 0:
         mwh3count = mwh3count+1
 
sorted_mwh1 = sorted_mwh1[0:mwh1count]
sorted_mwh2 = sorted_mwh2[0:mwh2count]
sorted_mwh3 = sorted_mwh3[0:mwh3count]
 
for i in range(0,mwh1count):
    a = sorted_mwh1[i]
    if a[4] == 'PNW':
        zone51count = zone51count + 1
 
for i in range(0,mwh2count):
    b = sorted_mwh2[i]
    if b[4] == 'PNW':
        zone52count = zone52count + 1
            
for i in range(0,mwh3count):
    c = sorted_mwh3[i]
    if c[4] == 'PNW':
        zone53count = zone53count + 1

sorted_mwh1 = sorted(sorted_mwh1,key=lambda x: x[4])
sorted_mwh2 = sorted(sorted_mwh2,key=lambda x: x[4])
sorted_mwh3 = sorted(sorted_mwh3,key=lambda x: x[4])
 
costs_mwh1 = np.zeros((mwh1count,1))
costs_mwh2 = np.zeros((mwh2count,1))
costs_mwh3 = np.zeros((mwh3count,1))
 
#assign $/MWh costs
for i in range(0,mwh1count):
     
     a = sorted_mwh1[i]
     
     name = a[1]   
     hour = a[2]     
     day = hour/24
    
     names = df_gen['name']
     for j in range(0,len(names)):
         if names[j] == name:
             idx = j
             
     type = df_gen.loc[idx,'typ']  
     zone = a[4]
    
     if type == 'ngcc' or type == 'ngct' or type == 'ngst':
         costs_mwh1[i,0] = df_gen.loc[idx,'seg1']*df_gasprice.loc[day,zone]
     elif type == 'coal':
         costs_mwh1[i,0] = df_gen.loc[idx,'seg1']*2
     elif type == 'oil':
         costs_mwh1[i,0] = df_gen.loc[idx,'seg1']*20
     elif type == 'psh' or type =='hydro' or type=='imports':
         costs_mwh1[i,0] = 0
     else:
         costs_mwh1[i,0] = 700
     
     if i%100000<1:
         print i
 
for i in range(0,mwh2count):
     
     a = sorted_mwh2[i]
     
     name = a[1]   
     hour = a[2]     
     day = hour/24
    
     names = df_gen['name']
     for j in range(0,len(names)):
         if names[j] == name:
             idx = j
             
     type = df_gen.loc[idx,'typ']  
     zone = a[4]
    
     if type == 'ngcc' or type == 'ngct' or type == 'ngst':
         costs_mwh2[i,0] = df_gen.loc[idx,'seg1']*df_gasprice.loc[day,zone]
     elif type == 'coal':
         costs_mwh2[i,0] = df_gen.loc[idx,'seg1']*2
     elif type == 'oil':
         costs_mwh2[i,0] = df_gen.loc[idx,'seg1']*20
     elif type == 'psh' or type =='hydro' or type=='imports':
         costs_mwh2[i,0] = 0
     else:
         costs_mwh2[i,0] = 700   

     if i%100000<1:
        print i
         
for i in range(0,mwh3count):
     
     a = sorted_mwh3[i]
     
     name = a[1]   
     hour = a[2]     
     day = hour/24
    
     names = df_gen['name']
     for j in range(0,len(names)):
         if names[j] == name:
             idx = j
             
     type = df_gen.loc[idx,'typ']  
     zone = a[4]
        
     if type == 'ngcc' or type == 'ngct' or type == 'ngst':
         costs_mwh3[i,0] = df_gen.loc[idx,'seg1']*df_gasprice.loc[day,zone]
     elif type == 'coal':
         costs_mwh3[i,0] = df_gen.loc[idx,'seg1']*2
     elif type == 'oil':
         costs_mwh3[i,0] = df_gen.loc[idx,'seg1']*20
     elif type == 'psh'or type =='hydro' or type=='imports':
         costs_mwh3[i,0] = 0
     else:
         costs_mwh3[i,0] = 700        
         
     if i%100000<1:
        print i
 
sorted_mwh1 = np.concatenate((np.array(sorted_mwh1).reshape(len(sorted_mwh1),6), costs_mwh1[:]), axis = 1)
sorted_mwh2 = np.concatenate((np.array(sorted_mwh2).reshape(len(sorted_mwh2),6), costs_mwh2[:]), axis = 1)
sorted_mwh3 = np.concatenate((np.array(sorted_mwh3).reshape(len(sorted_mwh3),6), costs_mwh3[:]), axis = 1)
        
zone51 = sorted_mwh1[0:zone51count-1]
zone52 = sorted_mwh2[0:zone52count-1]
zone53 = sorted_mwh3[0:zone53count-1]
 
zone51 = sorted(zone51,key=lambda x: x[2])
zone52 = sorted(zone52,key=lambda x: x[2])
zone53 = sorted(zone53,key=lambda x: x[2])

#==============================================================================

#make sure price can be zero
#look at mwh1, then mwh2, then mwh3
        
zone5_price = np.zeros((8712,1))

for i in range(0,8712):
    
    #zone5
    
    #mwh1
    prices = []
    count = 0
    switch = 0
    a = zone51[count]
    if a[2] > i+1:
        zone5_price[i] = 0
    else:
        while switch < 1:
            prices = np.append(prices,a[6])
            count = count + 1
            if count == len(zone51):
                switch = 1
                zone5_price[i] = max(prices)
            else:
                a = zone51[count]
                if a[2] > i+1:
                    switch = 1
                    zone5_price[i] = max(prices)
    zone51 = zone51[count:len(zone51)]
            
    #mwh2
    prices = []
    count = 0
    switch = 0
    a = zone52[count]
    if a[2] == i+1:
        while switch < 1:
            prices = np.append(prices,a[6])
            count = count + 1
            if count == len(zone52):
                switch = 1
                zone5_price[i] = max(max(prices),zone5_price[i])
            else: 
                a = zone52[count]
                if a[2] > i+1:
                    switch = 1
                    zone5_price[i] = max(max(prices),zone5_price[i])      
    zone52 = zone52[count:len(zone52)]
    
    #mwh3
    prices = []
    count = 0
    switch = 0
    a = zone53[count]
    if a[2] == i+1:
        while switch < 1:
            prices = np.append(prices,a[6])
            count = count + 1
            if count == len(zone53):
                switch = 1
                zone5_price[i] = max(max(prices),zone5_price[i])
            else: 
                a = zone53[count]
                if a[2] > i+1:
                    switch = 1
                    zone5_price[i] = max(max(prices),zone5_price[i])      
    zone53 = zone53[count:len(zone53)]

    if i%100<1:
        print i
        
   

zonal_prices = zone5_price

np.savetxt('zonal_prices2_min.csv',zonal_prices,delimiter = ',')



