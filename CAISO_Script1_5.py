# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 15:24:59 2018

@author: Joy Hill
"""


# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:14:07 2017

@author: YSu
"""

from pyomo.opt import SolverFactory
from CAISO1_8 import model
from pyomo.core import Var
from pyomo.core import Param
from operator import itemgetter
import pandas as pd

instance = model.create('CAISO_data.dat')

opt = SolverFactory("cplex")
H = instance.HorizonHours
K=range(1,H+1)


#Space to store results
mwh_1=[]
mwh_2=[]
mwh_3=[]
on=[]
switch=[]
srsv=[]
nrsv=[]
hydro=[]
solar=[]
wind=[]
CAISOImports=[]
flow=[]
Generator=[]

#max here can be (1,365)
for day in range(1,5):
     #load time series data
 for z in instance.zones:
        instance.GasPrice[z] = instance.SimGasPrice[z,day]
        for i in K:
            instance.HorizonDemand[z,i] = instance.SimDemand[z,(day-1)*24+i]
            instance.HorizonWind[z,i] = instance.SimWind[z,(day-1)*24+i]
            instance.HorizonSolar[z,i] = instance.SimSolar[z,(day-1)*24+i]
            instance.HorizonHydro[z,i] = instance.SimHydro[z,(day-1)*24+i]
            instance.HorizonCAISOImports[z,i] = instance.SimCAISOImports[z,(day-1)*24+i]
            instance.HorizonCAISOExports[z,i] = instance.SimCAISOExports[z,(day-1)*24+i]
            instance.HorizonReserves[i] = instance.SimReserves[(day-1)*24+i] 
            instance.HorizonMustRun[z,i] = instance.SimMustRun[z,(day-1)*24+i]
 CAISO_result = opt.solve(instance)
 instance.solutions.load_from(CAISO_result)   
 
 #The following section is for storing and sorting results
 for v in instance.component_objects(Var, active=True):
    varobject = getattr(instance, str(v))
    a=str(v)
    if a=='mwh_1':
     
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        if index[0] in instance.Zone1Generators:
            if index[0] in instance.Gas:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Gas'))
            elif index[0] in instance.Coal:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Coal'))
            elif index[0] in instance.Oil:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Oil'))
            elif index[0] in instance.PSH:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','PSH'))
            elif index[0] in instance.Slack:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Slack'))               
                
        elif index[0] in instance.Zone2Generators:
            if index[0] in instance.Gas:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Gas'))
            elif index[0] in instance.Coal:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Coal'))
            elif index[0] in instance.Oil:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Oil'))
            elif index[0] in instance.PSH:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','PSH'))
            elif index[0] in instance.Slack:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Slack'))  

        elif index[0] in instance.Zone3Generators:
            if index[0] in instance.Gas:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Gas'))
            elif index[0] in instance.Coal:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Coal'))
            elif index[0] in instance.Oil:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Oil'))
            elif index[0] in instance.PSH:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','PSH'))
            elif index[0] in instance.Slack:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Slack'))  

        elif index[0] in instance.Zone4Generators:
            if index[0] in instance.Gas:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Gas'))
            elif index[0] in instance.Coal:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Coal'))
            elif index[0] in instance.Oil:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Oil'))
            elif index[0] in instance.PSH:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','PSH'))
            elif index[0] in instance.Slack:
                mwh_1.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Slack'))  

        
     
     
    if a=='mwh_2':
   
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        if index[0] in instance.Zone1Generators:
            if index[0] in instance.Gas:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Gas'))
            elif index[0] in instance.Coal:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Coal'))
            elif index[0] in instance.Oil:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Oil'))
            elif index[0] in instance.PSH:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','PSH'))
            elif index[0] in instance.Slack:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Slack')) 
                
        elif index[0] in instance.Zone2Generators:
            if index[0] in instance.Gas:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Gas'))
            elif index[0] in instance.Coal:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Coal'))
            elif index[0] in instance.Oil:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Oil'))
            elif index[0] in instance.PSH:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','PSH'))
            elif index[0] in instance.Slack:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Slack'))  

        elif index[0] in instance.Zone3Generators:
            if index[0] in instance.Gas:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Gas'))
            elif index[0] in instance.Coal:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Coal'))
            elif index[0] in instance.Oil:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Oil'))
            elif index[0] in instance.PSH:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','PSH'))
            elif index[0] in instance.Slack:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Slack'))  
                
        elif index[0] in instance.Zone4Generators:
            if index[0] in instance.Gas:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Gas'))
            elif index[0] in instance.Coal:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Coal'))
            elif index[0] in instance.Oil:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Oil'))
            elif index[0] in instance.PSH:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','PSH'))
            elif index[0] in instance.Slack:
                mwh_2.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Slack'))  
     
    if a=='mwh_3':
       
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        if index[0] in instance.Zone1Generators:
            if index[0] in instance.Gas:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Gas'))
            elif index[0] in instance.Coal:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Coal'))
            elif index[0] in instance.Oil:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Oil'))
            elif index[0] in instance.PSH:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','PSH'))
            elif index[0] in instance.Slack:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley','Slack')) 
                
        elif index[0] in instance.Zone2Generators:
            if index[0] in instance.Gas:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Gas'))
            elif index[0] in instance.Coal:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Coal'))
            elif index[0] in instance.Oil:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Oil'))
            elif index[0] in instance.PSH:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','PSH'))
            elif index[0] in instance.Slack:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay','Slack'))  
                
        elif index[0] in instance.Zone3Generators:
            if index[0] in instance.Gas:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Gas'))
            elif index[0] in instance.Coal:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Coal'))
            elif index[0] in instance.Oil:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Oil'))
            elif index[0] in instance.PSH:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','PSH'))
            elif index[0] in instance.Slack:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE','Slack')) 
        elif index[0] in instance.Zone4Generators:
            if index[0] in instance.Gas:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Gas'))
            elif index[0] in instance.Coal:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Coal'))
            elif index[0] in instance.Oil:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Oil'))
            elif index[0] in instance.PSH:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','PSH'))
            elif index[0] in instance.Slack:
                mwh_3.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE','Slack'))  

     
    if a=='on':
        
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        if index[0] in instance.Zone1Generators:
         on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley'))
        elif index[0] in instance.Zone2Generators:
         on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay'))
        elif index[0] in instance.Zone3Generators:
         on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE'))
        elif index[0] in instance.Zone4Generators:
         on.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE'))     
     #on=pd.DataFrame(on,columns=('Time','Value'))
     
    if a=='switch':
    
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        if index[0] in instance.Zone1Generators:
         switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley'))
        elif index[0] in instance.Zone2Generators:
         switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay'))
        elif index[0] in instance.Zone3Generators:
         switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE'))
        elif index[0] in instance.Zone4Generators:
         switch.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE'))    

     
    if a=='srsv':
    
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        if index[0] in instance.Zone1Generators:
         srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley'))
        elif index[0] in instance.Zone2Generators:
         srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay'))
        elif index[0] in instance.Zone3Generators:
         srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE'))
        elif index[0] in instance.Zone4Generators:
         srsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE'))  

     
    if a=='nrsv':
   
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        if index[0] in instance.Zone1Generators:
         nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_valley'))
        elif index[0] in instance.Zone2Generators:
         nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'PGE_bay'))
        elif index[0] in instance.Zone3Generators:
         nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SCE'))
        elif index[0] in instance.Zone4Generators:
         nrsv.append((index[0],index[1]+((day-1)*24),varobject[index].value,'SDGE'))
     
    if a=='hydro':
      
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        hydro.append((index[0],index[1]+((day-1)*24),varobject[index].value))   
     
     
    if a=='solar':
       
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        solar.append((index[0],index[1]+((day-1)*24),varobject[index].value))   
     
      
    if a=='wind':
       
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        wind.append((index[0],index[1]+((day-1)*24),varobject[index].value))  
     
      
    if a=='CAISOImports':
       
     for index in varobject:
       if int(index[1]>0 and index[1]<25):
        CAISOImports.append((index[0],index[1]+((day-1)*24),varobject[index].value))   
     
      
    if a=='flow':
       
     for index in varobject:
       if int(index[2]>0 and index[2]<25):
        flow.append((index[0],index[1],index[2]+((day-1)*24),varobject[index].value))   
     

    for j in instance.Generators:
        if instance.on[j,H] == 1:
            instance.on[j,0] = 1
        else: 
            instance.on[j,0] = 0
        instance.on[j,0].fixed = True
                   
        if instance.mwh_1[j,H].value <=0 and instance.mwh_1[j,H].value>= -0.0001:
            newval_1=0
        else:
            newval_1=instance.mwh_1[j,H].value
        instance.mwh_1[j,0] = newval_1
        instance.mwh_1[j,0].fixed = True
                      
        if instance.mwh_2[j,H].value <=0 and instance.mwh_2[j,H].value>= -0.0001:
            newval=0
        else:
            newval=instance.mwh_2[j,H].value
                                 
        if instance.mwh_3[j,H].value <=0 and instance.mwh_3[j,H].value>= -0.0001:
            newval2=0
        else:
            newval2=instance.mwh_3[j,H].value
                                  
                                  
        instance.mwh_2[j,0] = newval
        instance.mwh_2[j,0].fixed = True
        instance.mwh_3[j,0] = newval2
        instance.mwh_3[j,0].fixed = True 
        if instance.switch[j,H] == 1:
            instance.switch[j,0] = 1
        else:
            instance.switch[j,0] = 0
        instance.switch[j,0].fixed = True
      
        if instance.srsv[j,H].value <=0 and instance.srsv[j,H].value>= -0.0001:
            newval_srsv=0
        else:
            newval_srsv=instance.srsv[j,H].value
        instance.srsv[j,0] = newval_srsv 
        instance.srsv[j,0].fixed = True        

        if instance.nrsv[j,H].value <=0 and instance.nrsv[j,H].value>= -0.0001:
            newval_nrsv=0
        else:
            newval_nrsv=instance.nrsv[j,H].value
        instance.nrsv[j,0] = newval_nrsv 
        instance.nrsv[j,0].fixed = True        
       
   
   
 mwh_1_pd=pd.DataFrame(mwh_1,columns=('Generator','Time','Value','Zones','Type'))
 mwh_2_pd=pd.DataFrame(mwh_2,columns=('Generator','Time','Value','Zones','Type'))
 mwh_3_pd=pd.DataFrame(mwh_3,columns=('Generator','Time','Value','Zones','Type'))
 on_pd=pd.DataFrame(on,columns=('Generator','Time','Value','Zones'))
 switch_pd=pd.DataFrame(switch,columns=('Generator','Time','Value','Zones'))
 srsv_pd=pd.DataFrame(srsv,columns=('Generator','Time','Value','Zones'))
 nrsv_pd=pd.DataFrame(nrsv,columns=('Generator','Time','Value','Zones'))
 hydro_pd=pd.DataFrame(hydro,columns=('Zone','Time','Value'))
 solar_pd=pd.DataFrame(solar,columns=('Zone','Time','Value'))
 wind_pd=pd.DataFrame(wind,columns=('Zone','Time','Value'))
 flow_pd=pd.DataFrame(flow,columns=('Source','Sink','Time','Value'))
 CAISOImports_pd=pd.DataFrame(CAISOImports,columns=('Zone','Time','Value'))


#This looks at zone 3 problem
#talist=[]
#slack3list=[]
#mwh_1_Zone3=pd.DataFrame(mwh_1_Zone3,columns=('Generator','Time','Value'))
#for i in range(0,len(mwh_1)):
#    if mwh_1.loc[i][0] =='SLACK3' and mwh_1.loc[i][2] >0:
#        slack3=[mwh_1.loc[i][0],mwh_1.loc[i][1],mwh_1.loc[i][2]]
#        slack3list.append(slack3)
#        time1=mwh_1.loc[i][1]
#        timelist.append(time1)
#
#for i in range(0,len(mwh_1_Zone3)):
#    if mwh_1_Zone3.loc[i][1] in timelist and mwh_1_Zone3.loc[i][2]==0:
#        ta=[mwh_1_Zone3.loc[i][0],mwh_1_Zone3.loc[i][1],mwh_1_Zone3.loc[i][2]]
#        talist.append(ta)
#        
#talistdf=pd.DataFrame(talist,columns=('Generator','Time','Value'))
#slack3df=pd.DataFrame(slack3list,columns=('Generator','Time','Value'))
        
#flow=pd.DataFrame(flow,columns=('Source','Sink','Time','Value'))
#for i in range(1,Model_days):
#    instance.solutions.load_from(results)
#    instance.HorizonHours=(i*24)+24;
#    instance.HH_periods= RangeSet(((i-1)*24)-1,instance.HorizonHours+1);                      
#    
# CAISO_result = opt.solve(instance)
# CAISO_result.write()
 mwh_1_pd.to_csv('mwh_1.csv')
 mwh_2_pd.to_csv('mwh_2.csv')
 mwh_3_pd.to_csv('mwh_3.csv')
 on_pd.to_csv('on.csv')
 switch_pd.to_csv('switch.csv')
 srsv_pd.to_csv('srsv.csv')
 nrsv_pd.to_csv('nrsv.csv')
 hydro_pd.to_csv('hydro.csv')
 solar_pd.to_csv('solar.csv')
 wind_pd.to_csv('wind.csv')
 flow_pd.to_csv('flow.csv')
 CAISOImports_pd.to_csv('CAISOImports.csv')
 
 print(day)
#talistdf.to_csv('non-zone3generators.csv')
#slack3df.to_csv('slack3value_greater_than_0.csv')