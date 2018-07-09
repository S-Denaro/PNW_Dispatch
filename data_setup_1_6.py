# -*- coding: utf-8 -*-
"""
Created on Wed May 03 15:01:31 2017

@author: jdkern
"""

import pandas as pd
import numpy as np

v_year = 2011

#read generator parameters into DataFrame
df_gen = pd.read_csv('generators.csv',header=0)
  
##time series of load for each zone
df_load = pd.read_csv('load_%d.csv'% v_year,header=0)   

##time series of operational reserves for each zone
df_reserves = pd.read_csv('reserves_%d.csv' % v_year,header=0)

##time series of hydropower for each zone
df_hydro = pd.read_csv('hydro_%d.csv' % v_year,header=0)
   
##time series of wind generation for each zone
df_wind = pd.read_csv('wind_%d.csv' % v_year,header=0)
   
##time series solar for each TAC
df_solar = pd.read_csv('solar_%d.csv' % v_year,header=0)   
   
##time series external exchange for each zone
df_imports = pd.read_csv('imports_%d.csv' % v_year,header=0)
df_exports = pd.read_csv('exports_%d.csv' % v_year,header=0)
     
#must run resources (LFG,ag_waste,nuclear)
df_must = pd.read_csv('must_run.csv',header=0)

#natural gas prices
df_ng = pd.read_csv('NG_%d.csv' % v_year, header=0)

#list zones
zones = ['PGE_valley', 'PGE_bay', 'SCE', 'SDGE']

#list plant types
types = ['ngct', 'ngcc', 'ngst', 'coal','oil', 'psh', 'slack']

# must run generation (including san onofre (SCE/SDGE) and diablo canyon (PGE))      
must_run_PGE_valley = []
must_run_PGE_bay = []
must_run_SCE = []
must_run_SDGE = []
if v_year == 2010:  
    for i in range(0,len(df_load)):
        month = df_load.loc[i,'Month']
        if month == 1:
            must_run_SCE = np.append(must_run_SCE,1107.97*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1107.97*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2096+df_must.loc[0,'PGE_valley'])
        elif month == 2:
            must_run_SCE = np.append(must_run_SCE,1116.60*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1116.60*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2183+df_must.loc[0,'PGE_valley'])
        elif month == 3:
           must_run_SCE = np.append(must_run_SCE,593.55*.78+df_must.loc[0,'SCE'])
           must_run_SDGE = np.append(must_run_SDGE,593.55*.2+df_must.loc[0,'SDGE'])
           must_run_PGE_valley = np.append(must_run_PGE_valley,2280+df_must.loc[0,'PGE_valley'])
        elif month == 4:
            must_run_SCE = np.append(must_run_SCE,1190.08*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1190.08*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2282+df_must.loc[0,'PGE_valley'])
        elif month == 5:
           must_run_SCE = np.append(must_run_SCE,2224.73*.78+df_must.loc[0,'SCE'])
           must_run_SDGE = np.append(must_run_SDGE,2224.73*.2+df_must.loc[0,'SDGE'])
           must_run_PGE_valley = np.append(must_run_PGE_valley,2285+df_must.loc[0,'PGE_valley'])
        elif month == 6:
           must_run_SCE = np.append(must_run_SCE,2254.71*.78+df_must.loc[0,'SCE'])
           must_run_SDGE = np.append(must_run_SDGE,2254.71*.2+df_must.loc[0,'SDGE'])
           must_run_PGE_valley = np.append(must_run_PGE_valley,2286+df_must.loc[0,'PGE_valley'])
        elif month == 7:
           must_run_SCE = np.append(must_run_SCE,2261.17*.78+df_must.loc[0,'SCE'])
           must_run_SDGE = np.append(must_run_SDGE,2261.17*.2+df_must.loc[0,'SDGE'])
           must_run_PGE_valley = np.append(must_run_PGE_valley,2280+df_must.loc[0,'PGE_valley'])
        elif month == 8:
            must_run_SCE = np.append(must_run_SCE,2266.17*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,2266.17*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2280+df_must.loc[0,'PGE_valley'])
        elif month == 9:
            must_run_SCE = np.append(must_run_SCE,2222.91*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,2222.91*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2272+df_must.loc[0,'PGE_valley'])
        elif month == 10:
            must_run_SCE = np.append(must_run_SCE,1345.48*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1345.48*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,1139+df_must.loc[0,'PGE_valley'])
        elif month == 11:
            must_run_SCE = np.append(must_run_SCE,1132.9*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1132.9*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,1640+df_must.loc[0,'PGE_valley'])
        else:
            must_run_SCE = np.append(must_run_SCE,1120.36*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1120.36*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2233+df_must.loc[0,'PGE_valley'])
             
        must_run_PGE_bay = np.ones((len(df_load),1))*df_must.loc[0,'PGE_bay'] 
        
elif v_year == 2011:  
    for i in range(0,len(df_load)):
        month = df_load.loc[i,'Month']
        if month == 1:
            must_run_SCE = np.append(must_run_SCE,1123.16*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1123.16*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2275+df_must.loc[0,'PGE_valley'])
        elif month == 2:
            must_run_SCE = np.append(must_run_SCE,1440.71*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1440.71*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2275+df_must.loc[0,'PGE_valley'])
        elif month == 3:
           must_run_SCE = np.append(must_run_SCE,2259.29*.78+df_must.loc[0,'SCE'])
           must_run_SDGE = np.append(must_run_SDGE,2259.29*.2+df_must.loc[0,'SDGE'])
           must_run_PGE_valley = np.append(must_run_PGE_valley,2073+df_must.loc[0,'PGE_valley'])
        elif month == 4:
            must_run_SCE = np.append(must_run_SCE,2262.15*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,2262.15*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2236+df_must.loc[0,'PGE_valley'])
        elif month == 5:
           must_run_SCE = np.append(must_run_SCE,2250.22*.78+df_must.loc[0,'SCE'])
           must_run_SDGE = np.append(must_run_SDGE,2250.22*.2+df_must.loc[0,'SDGE'])
           must_run_PGE_valley = np.append(must_run_PGE_valley,1135+df_must.loc[0,'PGE_valley'])
        elif month == 6:
           must_run_SCE = np.append(must_run_SCE,2266.68*.78+df_must.loc[0,'SCE'])
           must_run_SDGE = np.append(must_run_SDGE,2266.68*.2+df_must.loc[0,'SDGE'])
           must_run_PGE_valley = np.append(must_run_PGE_valley,2023+df_must.loc[0,'PGE_valley'])
        elif month == 7:
           must_run_SCE = np.append(must_run_SCE,2259.42*.78+df_must.loc[0,'SCE'])
           must_run_SDGE = np.append(must_run_SDGE,2259.42*.2+df_must.loc[0,'SDGE'])
           must_run_PGE_valley = np.append(must_run_PGE_valley,2272+df_must.loc[0,'PGE_valley'])
        elif month == 8:
            must_run_SCE = np.append(must_run_SCE,2154.43*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,2154.43*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2262+df_must.loc[0,'PGE_valley'])
        elif month == 9:
            must_run_SCE = np.append(must_run_SCE,1993.13*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,1993.13*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2118+df_must.loc[0,'PGE_valley'])
        elif month == 10:
            must_run_SCE = np.append(must_run_SCE,2267.03*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,2267.03*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2247+df_must.loc[0,'PGE_valley'])
        elif month == 11:
            must_run_SCE = np.append(must_run_SCE,2268.99*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,2268.99*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2270+df_must.loc[0,'PGE_valley'])
        else:
            must_run_SCE = np.append(must_run_SCE,2201.95*.78+df_must.loc[0,'SCE'])
            must_run_SDGE = np.append(must_run_SDGE,2201.95*.2+df_must.loc[0,'SDGE'])
            must_run_PGE_valley = np.append(must_run_PGE_valley,2267+df_must.loc[0,'PGE_valley'])
               
        must_run_PGE_bay = np.ones((len(df_load),1))*df_must.loc[0,'PGE_bay'] 

else:
        must_run_PGE_valley = np.ones((len(df_load),1))*(df_must.loc[0,'PGE_valley'] + 1920.5)  
        must_run_PGE_bay = np.ones((len(df_load),1))*df_must.loc[0,'PGE_bay']
        must_run_SCE = np.ones((len(df_load),1))*df_must.loc[0,'SCE']    
        must_run_SDGE = np.ones((len(df_load),1))*df_must.loc[0,'SDGE']     
        
must_run = np.column_stack((must_run_PGE_valley,must_run_PGE_bay,must_run_SCE,must_run_SDGE))
df_total_must_run =pd.DataFrame(must_run,columns=('PGE_valley','PGE_bay','SCE','SDGE'))

        
############
#  sets    #
############

#write data.dat file
with open('data.dat', 'w') as f:
    
    # generator sets by zone
    for z in zones:
        # zone string
        z_int = zones.index(z)
        f.write('set Zone%dGenerators :=\n' % (z_int+1))
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'zone'] == z:
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')    
        
    # generator sets by type
    # coal
    f.write('set Coal :=\n')
    # pull relevant generators
    for gen in range(0,len(df_gen)):
        if df_gen.loc[gen,'typ'] == 'coal':
            unit_name = df_gen.loc[gen,'name']
            unit_name = unit_name.replace(' ','_')
            f.write(unit_name + ' ')
    f.write(';\n\n')    
   
    # oil
    f.write('set Oil :=\n')
    # pull relevant generators
    for gen in range(0,len(df_gen)):
        if df_gen.loc[gen,'typ'] == 'oil':
            unit_name = df_gen.loc[gen,'name']
            unit_name = unit_name.replace(' ','_')
            f.write(unit_name + ' ')
    f.write(';\n\n')        

    # Pumped Storage
    f.write('set PSH :=\n')
    # pull relevant generators
    for gen in range(0,len(df_gen)):
        if df_gen.loc[gen,'typ'] == 'psh':
            unit_name = df_gen.loc[gen,'name']
            unit_name = unit_name.replace(' ','_')
            f.write(unit_name + ' ')
    f.write(';\n\n')      
    
    # Slack
    f.write('set Slack :=\n')
    # pull relevant generators
    for gen in range(0,len(df_gen)):
        if df_gen.loc[gen,'typ'] == 'slack':
            unit_name = df_gen.loc[gen,'name']
            unit_name = unit_name.replace(' ','_')
            f.write(unit_name + ' ')
    f.write(';\n\n')  
      
    # gas generator sets by zone and type
    for z in zones:
        # zone string
        z_int = zones.index(z)
        
        # Natural Gas
        # find relevant generators
        trigger = 0
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'zone'] == z and (df_gen.loc[gen,'typ'] == 'ngcc' or df_gen.loc[gen,'typ'] == 'ngct' or df_gen.loc[gen,'typ'] == 'ngst'):
                trigger = 1
        if trigger > 0:
            # pull relevant generators
            f.write('set Gas :=\n' % (z_int+1))      
            for gen in range(0,len(df_gen)):
                if df_gen.loc[gen,'zone'] == z and (df_gen.loc[gen,'typ'] == 'ngcc' or df_gen.loc[gen,'typ'] == 'ngct' or df_gen.loc[gen,'typ'] == 'ngst'):
                    unit_name = df_gen.loc[gen,'name']
                    unit_name = unit_name.replace(' ','_')
                    f.write(unit_name + ' ')
            f.write(';\n\n')
   
            
    # zones
    f.write('set zones :=\n')
    for z in zones:
        f.write(z + ' ')
    f.write(';\n\n')
        
################
#  parameters  #
################
    
    # simulation details
    SimHours = 8760
    f.write('param SimHours := %d;' % SimHours)
    f.write('\n')
    f.write('param SimDays:= %d;' % int(SimHours/24))
    f.write('\n\n')
    HorizonHours = 48
    f.write('param HorizonHours := %d;' % HorizonHours)
    f.write('\n\n')


    # create parameter matrix for transmission paths (source and sink connections)
    f.write('param:' + '\t' + 'limit' + '\t' +'hurdle :=' + '\n')
    for z in zones:
        for x in zones:           
            f.write(z + '\t' + x + '\t')
            match = 0
            for p in range(0,len(df_paths)):
                source = df_paths.loc[p,'start_zone']
                sink = df_paths.loc[p,'end_zone']
                if source == z and sink == x:
                    match = 1
                    p_match = p
            if match > 0:
                f.write(str(df_paths.loc[p_match,'limit']) + '\t' + str(df_paths.loc[p_match,'hurdle']) + '\n')
            else:
                f.write('0' + '\t' + '0' + '\n')
    f.write(';\n\n')
    
# create parameter matrix for generators
    f.write('param:' + '\t')
    for c in df_gen.columns:
        if c != 'name':
            f.write(c + '\t')
    f.write(':=\n\n')
    for i in range(0,len(df_gen)):    
        for c in df_gen.columns:
            if c == 'name':
                unit_name = df_gen.loc[i,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + '\t')  
            else:
                f.write(str((df_gen.loc[i,c])) + '\t')               
        f.write('\n')
    f.write(';\n\n')     
    
    # times series data
    # zonal (hourly)
    f.write('param:' + '\t' + 'SimDemand' + '\t' + 'SimWind' \
    + '\t' + 'SimSolar' + '\t' + 'SimHydro' + '\t' + 'SimCAISOImports'  + '\t' + 'SimCAISOExports'  + '\t' + 'SimMustRun:=' + '\n')      
    for z in zones:
        for h in range(0,len(df_load)): 
            f.write(z + '\t' + str(h+1) + '\t' + str(df_load.loc[h,z])\
            + '\t' + str(df_wind.loc[h,z]) + '\t' + str(df_solar.loc[h,z]) + '\t' + str(df_hydro.loc[h,z])\
            + '\t' + str(df_imports.loc[h,z]) + '\t' + str(df_exports.loc[h,z]) + '\t' + str(df_total_must_run.loc[h,z]) + '\n')
    f.write(';\n\n')
    
    # zonal (daily)
    f.write('param:' + '\t' + 'SimGasPrice:=' + '\n')      
    for z in zones:
        for d in range(0,int(SimHours/24)): 
            f.write(z + '\t' + str(d+1) + '\t' + str(df_ng.loc[d,z]) + '\n')
    f.write(';\n\n')
    
    
    #system wide (hourly)
    f.write('param' + '\t' + 'SimReserves:=' + '\n')
    for h in range(0,len(df_load)):
            f.write(str(h+1) + '\t' + str(df_reserves.loc[h,'reserves']) + '\n')
    f.write(';\n\n')
        

    
    