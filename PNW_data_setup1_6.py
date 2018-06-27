# -*- coding: utf-8 -*-
"""
Created on Wed May 03 15:01:31 2017

@author: jdkern
"""

import pandas as pd
import numpy as np

#read generator parameters into DataFrame
df_gen = pd.read_csv('generators.csv',header=0)

#read transmission path parameters into DataFrame
#df_paths = pd.read_csv('paths.csv',header=0)
   
##time series of load for each zone
df_load = pd.read_csv('load.csv',header=0)   

##time series of operational reserves for each zone
df_reserves = pd.read_csv('reserves.csv',header=0)

##daily hydropower availability 
df_hydro = pd.read_csv('dispatchable_hydro.csv',header=0)
   
##time series of wind generation for each zone
df_wind = pd.read_csv('wind.csv',header=0)
   
##time series solar for each TAC
df_solar = pd.read_csv('solar.csv',header=0)   
   
##daily time series of dispatchable imports by path
df_imports = pd.read_csv('dispatchable_imports.csv',header=0)

##hourly time series of exports by zone
df_exports = pd.read_csv('exports.csv',header=0)
     
#must run resources (LFG,ag_waste,nuclear)
df_must = pd.read_csv('must_run.csv',header=0)

#natural gas prices
df_ng = pd.read_csv('NG.csv', header=0)

#california imports hourly minimum flows
df_PNW_import_mins = pd.read_csv('PNW_path_mins.csv', header=0)

#california hydro hourly minimum flows
df_PNW_hydro_mins = pd.read_csv('PNW_hydro_mins.csv', header=0)

#list zones
zones = ['PNW']

#list plant types
types = ['ngct', 'ngcc', 'ngst', 'coal','oil', 'nuc','psh', 'slack', 'imports','hydro'] 

# must run generation   
must_run_PNW = np.ones((len(df_load),1))*(df_must.loc[0,'PNW'])  
        
must_run = np.column_stack((must_run_PNW))
df_total_must_run =pd.DataFrame(must_run,columns=('PNW'))

        
############
#  sets    #
############

#write data.dat file  ##need to add a NUCLEAR set??###
filename = 'data.dat'
with open(filename, 'w') as f:
    
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
        
    # WECC imports
    f.write('set WECCImports :=\n')
    # pull relevant generators
    for gen in range(0,len(df_gen)):
        if df_gen.loc[gen,'typ'] == 'imports':
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
    
    #nuc
    f.write('set Nuclear :=\n')
    # pull relevant generators
    for gen in range(0,len(df_gen)):
        if df_gen.loc[gen,'typ'] == 'nuc':
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

    # Hydro
    f.write('set Hydro :=\n')
    # pull relevant generators
    for gen in range(0,len(df_gen)):
        if df_gen.loc[gen,'typ'] == 'hydro':
            unit_name = df_gen.loc[gen,'name']
            unit_name = unit_name.replace(' ','_')
            f.write(unit_name + ' ')
    f.write(';\n\n')   
    
    # Ramping
    f.write('set Ramping :=\n')
    # pull relevant generators
    for gen in range(0,len(df_gen)):
        if df_gen.loc[gen,'typ'] == 'hydro' or df_gen.loc[gen,'typ'] == 'imports':
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
            f.write('set Zone%dGas :=\n' % (z_int+1))      
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
    HorizonDays = int(HorizonHours/24)
    f.write('param HorizonDays := %d;' % HorizonDays)
    f.write('\n\n')
    

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
    + '\t' + 'SimSolar' + '\t' + 'SimMustRun:=' + '\n')      
    for z in zones:
        for h in range(0,len(df_load)): 
            f.write(z + '\t' + str(h+1) + '\t' + str(df_load.loc[h,z])\
            + '\t' + str(df_wind.loc[h,z]) + '\t' + str(df_solar.loc[h,z])\
            + '\t' + str(df_total_must_run.loc[h,z]) + '\n')
    f.write(';\n\n')
    
    # zonal (daily)
    f.write('param:' + '\t' + 'SimGasPrice:=' + '\n')      
    for z in zones:
        for d in range(0,int(SimHours/24)): 
            f.write(z + '\t' + str(d+1) + '\t' + str(df_ng.loc[d,z]) + '\n')
    f.write(';\n\n')

    #system wide (daily)
    f.write('param:' + '\t' + 'SimPath66_imports' + '\t' + 'SimPath65_imports' + '\t' + 'SimPath3_imports' + '\t' + 'SimPath8_imports' + '\t' + 'SimPath14_imports' + '\t' + 'SimPNW_hydro:=' + '\n')
    for d in range(0,len(df_imports)):
            f.write(str(d+1) + '\t' + str(df_imports.loc[d,'Path66']) + '\t' + str(df_imports.loc[d,'Path65']) + '\t' + str(df_imports.loc[d,'Path3']) + '\t' + str(df_imports.loc[d,'Path8']) + '\t' + str(df_imports.loc[d,'Path14']) + '\t' + str(df_hydro.loc[d,'PNW']) + '\n')
    f.write(';\n\n')
    
    
    #system wide (hourly)
    f.write('param:' + '\t' + 'SimPath66_exports' + '\t' + 'SimPath65_exports' + '\t' + 'SimPath3_exports' + '\t' + 'SimPath8_exports' + '\t' + 'SimPath14_exports' + '\t' + 'SimReserves' + '\t' + 'SimPNW_hydro_minflow' + '\t' + 'SimPath3_imports_minflow' + '\t' + 'SimPath8_imports_minflow' + '\t' + 'SimPath14_imports_minflow:=' + '\n')
    for h in range(0,len(df_load)):
            f.write(str(h+1) + '\t' + str(df_exports.loc[h,'Path66']) + '\t' + str(df_exports.loc[h,'Path65']) + '\t' + str(df_exports.loc[h,'Path3']) + '\t' + str(df_exports.loc[h,'Path8']) + '\t' + str(df_exports.loc[h,'Path14']) + '\t' + str(df_reserves.loc[h,'reserves'])  + '\t' + str(df_PNW_hydro_mins.loc[h,'PNW']) + '\t' + str(df_PNW_import_mins.loc[h,'Path3']) + '\t' + str(df_PNW_import_mins.loc[h,'Path8']) + '\t' + str(df_PNW_import_mins.loc[h,'Path14']) + '\n')
    f.write(';\n\n')
    
    