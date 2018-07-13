# -*- coding: utf-8 -*-
"""
Created on Mon Jul 09 15:49:33 2018

@author: sdenaro
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 07 12:23:45 2017

@author: jdkern
"""

#######################################################################################################
# a basic unit commitment model for CAISO system                                                       #
# This is the trial version of the electricity market model                                            #
# 4 Zone system                                                                                        #                                                                                #
#######################################################################################################


from __future__ import division # This line is used to ensure that int or long division arguments are converted to floating point values before division is performed 
from pyomo.environ import * # This command makes the symbols used by Pyomo known to Python
from pyomo.opt import SolverFactory
import itertools

##Create a solver
opt = SolverFactory('cplex')

model = AbstractModel()
#
######################################################################
## string indentifiers for the set of generators in different zones. #
######################################################################
#

model.Zone1Gas = Set()
model.Zone1Generators =  Set()
#PGE_valley

model.Zone2Gas = Set()
model.Zone2Generators = Set()
#PGE_bay

model.Zone3Gas = Set()
model.Zone3Generators = Set()
#SCE

model.Zone4Gas = Set()
model.Zone4Generators = Set()
#PGE_bay

model.Coal = Set()
model.Gas = model.Zone1Gas | model.Zone2Gas | model.Zone3Gas | model.Zone4Gas 
model.Oil = Set()
model.PSH = Set()
model.Slack = Set()


#for i in range(1,5):
# eval('model.Zone%dGenerators.construct()' %i)
   
model.Generators = model.Zone1Generators | model.Zone2Generators | model.Zone3Generators | model.Zone4Generators

#
model.zones =Set()
model.sources = Set(within=model.zones)
model.sinks = Set(within=model.zones)

#########################################################
# These are the generators parameters from model input  #
#########################################################


#Generator Type
model.typ = Param(model.Generators)

#Zone parameters
model.zone = Param(model.Generators)

#Max Generating Capacity
model.netcap = Param(model.Generators)

#Min Generating Capacity
model.mincap = Param(model.Generators)

#Minimun up time
model.minu = Param(model.Generators)

#Minmun down time
model.mind = Param(model.Generators)

#Ramp rate
model.ramp  = Param(model.Generators)

#Start cost
model.st_cost = Param(model.Generators)

#Piecewice varible cost segments
model.seg1= Param(model.Generators)
model.seg2= Param(model.Generators)
model.seg3= Param(model.Generators)

#Variable O&M
model.var_om = Param(model.Generators)

#No load cost
model.no_load  = Param(model.Generators)

#Transmission Path parameters
model.hurdle = Param(model.sources, model.sinks)
model.limit = Param(model.sources, model.sinks)
#
###########################################################
### These are the detailed parameters for model runs      #
###########################################################
##
## Full range of time series information provided in .dat file (1 year)
model.SimHours = Param(within=PositiveIntegers)
model.SH_periods = RangeSet(1,model.SimHours+1)
model.SimDays = Param(within=PositiveIntegers)
model.SD_periods = RangeSet(1,model.SimDays+1)

# Operating horizon information 
model.HorizonHours = Param(within=PositiveIntegers)
model.HH_periods = RangeSet(0,model.HorizonHours)
model.hh_periods = RangeSet(1,model.HorizonHours)

#Demand over simulation period
model.SimDemand = Param(model.zones*model.SH_periods, within=NonNegativeReals)

#Must run generation over simulation period
model.SimMustRun = Param(model.zones*model.SH_periods, within=NonNegativeReals)

#Horizon demand
model.HorizonDemand = Param(model.zones*model.hh_periods,within=NonNegativeReals,mutable=True)

#Horizon must run generation
model.HorizonMustRun = Param(model.zones*model.hh_periods,within=NonNegativeReals,mutable=True)

#Reserve for the entire system
model.SimReserves = Param(model.SH_periods, within=NonNegativeReals)
model.HorizonReserves = Param(model.hh_periods, within=NonNegativeReals,mutable=True)
##
##Variable resources over simulation period
model.SimWind = Param(model.zones, model.SH_periods, within=NonNegativeReals)
model.SimSolar = Param(model.zones, model.SH_periods, within=NonNegativeReals)
model.SimHydro = Param(model.zones, model.SH_periods, within=NonNegativeReals)
model.SimCAISOImports = Param(model.zones, model.SH_periods, within=NonNegativeReals)
model.SimCAISOExports = Param(model.zones, model.SH_periods, within=NonNegativeReals)

#Natural gas prices over simulation period
model.SimGasPrice = Param(model.zones,model.SD_periods, within=NonNegativeReals)
model.GasPrice = Param(model.zones,within = NonNegativeReals, mutable=True,initialize=0)

#Variable resources over horizon
model.HorizonWind = Param(model.zones,model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonSolar = Param(model.zones,model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonHydro = Param(model.zones,model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonCAISOImports = Param(model.zones,model.hh_periods,within=NonNegativeReals,mutable=True)
model.HorizonCAISOExports = Param(model.zones,model.hh_periods,within=NonNegativeReals,mutable=True)

##Initial conditions
model.ini_on = Param(model.Generators, within=Binary, initialize=0,mutable=True) 
model.ini_mwh_1 = Param(model.Generators,initialize=0,mutable=True) #seg1
model.ini_mwh_2 = Param(model.Generators,initialize=0,mutable=True) #seg2
model.ini_mwh_3 = Param(model.Generators,initialize=0,mutable=True) #seg3

###########################################################
### Decision variables                                    #
###########################################################

##Amount of day-ahead energy generated by each thermal unit's 3 segments at each hour
model.mwh_1 = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)
model.mwh_2 = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)
model.mwh_3 = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)

#1 if unit is on in hour i
model.on = Var(model.Generators,model.HH_periods, within=Binary, initialize=0)

#1 if unit is switching on in hour i
model.switch = Var(model.Generators,model.HH_periods, within=Binary,initialize=0)

#Amount of spining reserce offered by each unit in each hour
model.srsv = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)

#Amount of non-sping reserve ovvered by each unit in each hour
model.nrsv = Var(model.Generators,model.HH_periods, within=NonNegativeReals,initialize=0)

#Renewable energy production
model.hydro = Var(model.zones,model.HH_periods,within=NonNegativeReals)
model.solar = Var(model.zones,model.HH_periods,within=NonNegativeReals)
model.wind = Var(model.zones,model.HH_periods,within=NonNegativeReals)
model.CAISOImports = Var(model.zones,model.HH_periods,within=NonNegativeReals)
#
#
#Power flows on each path
model.flow = Var(model.sources*model.sinks*model.HH_periods, within=NonNegativeReals)
#
#
####################################################################
##Objective function                                               #
##To minimize overall system cost while satistfy system constraints#
####################################################################
#
##
def SysCost(model):
    fixed = sum(model.no_load[j]*model.on[j,i] for i in model.hh_periods for j in model.Generators)
    coal1 = sum(model.mwh_1[j,i]*(model.seg1[j]*2 + model.var_om[j]) for i in model.hh_periods for j in model.Coal) 
    coal2 = sum(model.mwh_2[j,i]*(model.seg2[j]*2 + model.var_om[j]) for i in model.hh_periods for j in model.Coal) 
    coal3 = sum(model.mwh_3[j,i]*(model.seg3[j]*2 + model.var_om[j]) for i in model.hh_periods for j in model.Coal) 
    gas1_1 = sum(model.mwh_1[j,i]*(model.seg1[j]*model.GasPrice['PGE_valley'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone1Gas) 
    gas2_1 = sum(model.mwh_2[j,i]*(model.seg2[j]*model.GasPrice['PGE_valley'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone1Gas)  
    gas3_1 = sum(model.mwh_3[j,i]*(model.seg3[j]*model.GasPrice['PGE_valley'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone1Gas)  
    gas1_2 = sum(model.mwh_1[j,i]*(model.seg1[j]*model.GasPrice['PGE_bay'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone2Gas) 
    gas2_2 = sum(model.mwh_2[j,i]*(model.seg2[j]*model.GasPrice['PGE_bay'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone2Gas)  
    gas3_2 = sum(model.mwh_3[j,i]*(model.seg3[j]*model.GasPrice['PGE_bay'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone2Gas)  
    gas1_3 = sum(model.mwh_1[j,i]*(model.seg1[j]*model.GasPrice['SCE'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone3Gas) 
    gas2_3 = sum(model.mwh_2[j,i]*(model.seg2[j]*model.GasPrice['SCE'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone3Gas)  
    gas3_3 = sum(model.mwh_3[j,i]*(model.seg3[j]*model.GasPrice['SCE'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone3Gas)  
    gas1_4 = sum(model.mwh_1[j,i]*(model.seg1[j]*model.GasPrice['SDGE'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone4Gas) 
    gas2_4 = sum(model.mwh_2[j,i]*(model.seg2[j]*model.GasPrice['SDGE'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone4Gas)  
    gas3_4 = sum(model.mwh_3[j,i]*(model.seg3[j]*model.GasPrice['SDGE'] + model.var_om[j]) for i in model.hh_periods for j in model.Zone4Gas)    
    oil1 = sum(model.mwh_1[j,i]*(model.seg1[j]*20 + model.var_om[j]) for i in model.hh_periods for j in model.Oil) 
    oil2 = sum(model.mwh_2[j,i]*(model.seg2[j]*20 + model.var_om[j]) for i in model.hh_periods for j in model.Oil)  
    oil3 = sum(model.mwh_3[j,i]*(model.seg3[j]*20 + model.var_om[j]) for i in model.hh_periods for j in model.Oil)  
    psh1 = sum(model.mwh_1[j,i]*10 for i in model.hh_periods for j in model.PSH)
    psh2 = sum(model.mwh_2[j,i]*10 for i in model.hh_periods for j in model.PSH)
    psh3 = sum(model.mwh_3[j,i]*10 for i in model.hh_periods for j in model.PSH)
    slack1 = sum(model.mwh_1[j,i]*model.seg1[j]*10000 for i in model.hh_periods for j in model.Slack)
    slack2 = sum(model.mwh_2[j,i]*model.seg2[j]*10000 for i in model.hh_periods for j in model.Slack)
    slack3 = sum(model.mwh_3[j,i]*model.seg3[j]*10000 for i in model.hh_periods for j in model.Slack)
    starts = sum(model.st_cost[j]*model.switch[j,i] for i in model.hh_periods for j in model.Generators) 
    exchange = sum(model.flow[s,k,i]*model.hurdle[s,k] for s in model.sources for k in model.sinks for i in model.hh_periods)
    return fixed + coal1 + coal2 + coal3 + gas1_1 + gas1_2 + gas1_3 + gas1_4 + gas2_1 + gas2_2 + gas2_3 + gas2_4 + gas3_1 + gas3_2 + gas3_3 + gas3_4 + oil1 + oil2 + oil3 + psh1 + psh2 + psh3 + slack1 + slack2 + slack3 + starts + exchange
model.SystemCost = Objective(rule=SysCost, sense=minimize)
    
   
####################################################################
#   Constraints                                                    #
####################################################################
   
#WECC Constraint 25% of internal demand must be generated locally
def WECC1(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone1Generators) 
    s2 = sum(model.mwh_2[j,i] for j in model.Zone1Generators) 
    s3 = sum(model.mwh_3[j,i] for j in model.Zone1Generators) 
    renew = model.hydro['PGE_valley',i] + model.solar['PGE_valley',i]\
    + model.wind['PGE_valley',i] 
    must_run = model.HorizonMustRun['PGE_valley',i]
    return s1 + s2 + s3 + renew + must_run >=  0.25*model.HorizonDemand['PGE_valley',i]
model.Local1= Constraint(model.hh_periods,rule=WECC1)
##
def WECC2(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone2Generators) 
    s2 = sum(model.mwh_2[j,i] for j in model.Zone2Generators) 
    s3 = sum(model.mwh_3[j,i] for j in model.Zone2Generators) 
    renew = model.hydro['PGE_bay',i] + model.solar['PGE_bay',i]\
    + model.wind['PGE_bay',i] 
    must_run = model.HorizonMustRun['PGE_bay',i]
    return s1 + s2 + s3 + renew + must_run >=  0.25*model.HorizonDemand['PGE_bay',i]
model.Local2= Constraint(model.hh_periods,rule=WECC2)
###
def WECC3(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone3Generators) 
    s2 = sum(model.mwh_2[j,i] for j in model.Zone3Generators) 
    s3 = sum(model.mwh_3[j,i] for j in model.Zone3Generators) 
    renew = model.hydro['SCE',i] + model.solar['SCE',i]\
    + model.wind['SCE',i] 
    must_run = model.HorizonMustRun['SCE',i]
    return s1 + s2 + s3 + renew + must_run >=  0.25*model.HorizonDemand['SCE',i]
model.Local3= Constraint(model.hh_periods,rule=WECC3)
#
def WECC4(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone4Generators) 
    s2 = sum(model.mwh_2[j,i] for j in model.Zone4Generators) 
    s3 = sum(model.mwh_3[j,i] for j in model.Zone4Generators) 
    renew = model.hydro['SDGE',i] + model.solar['SDGE',i]\
    + model.wind['SDGE',i] 
    must_run = model.HorizonMustRun['SDGE',i]
    return s1 + s2 + s3 + renew + must_run >=  0.25*model.HorizonDemand['SDGE',i]
model.Local4= Constraint(model.hh_periods,rule=WECC4)

#
###Power Balance 
def Zone1_Balance(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone1Generators)
    s2 = sum(model.mwh_2[j,i] for j in model.Zone1Generators)  
    s3 = sum(model.mwh_3[j,i] for j in model.Zone1Generators)  
    other = model.hydro['PGE_valley',i] + model.solar['PGE_valley',i]\
    + model.wind['PGE_valley',i] + model.HorizonMustRun['PGE_valley',i]
    imports = sum(model.flow[s,'PGE_valley',i] for s in model.sources) + model.CAISOImports['PGE_valley',i]
    exports = sum(model.flow['PGE_valley',k,i] for k in model.sinks) + model.HorizonCAISOExports['PGE_valley',i]         
    return s1 + s2 + s3 + other + imports - exports >= model.HorizonDemand['PGE_valley',i]
model.Bal1Constraint= Constraint(model.hh_periods,rule=Zone1_Balance)
#
def Zone2_Balance(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone2Generators)
    s2 = sum(model.mwh_2[j,i] for j in model.Zone2Generators)  
    s3 = sum(model.mwh_3[j,i] for j in model.Zone2Generators)  
    other = model.hydro['PGE_bay',i] + model.solar['PGE_bay',i]\
    + model.wind['PGE_bay',i] + model.HorizonMustRun['PGE_bay',i]   
    imports = sum(model.flow[s,'PGE_bay',i] for s in model.sources) + model.CAISOImports['PGE_bay',i]
    exports = sum(model.flow['PGE_bay',k,i] for k in model.sinks) + model.HorizonCAISOExports['PGE_bay',i]         
    return s1 + s2 + s3 + other + imports - exports >= model.HorizonDemand['PGE_bay',i]
model.Bal2Constraint= Constraint(model.hh_periods,rule=Zone2_Balance)
#
def Zone3_Balance(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone3Generators)
    s2 = sum(model.mwh_2[j,i] for j in model.Zone3Generators)  
    s3 = sum(model.mwh_3[j,i] for j in model.Zone3Generators)  
    other = model.hydro['SCE',i] + model.solar['SCE',i]\
    + model.wind['SCE',i] + model.HorizonMustRun['SCE',i]   
    imports = sum(model.flow[s,'SCE',i] for s in model.sources) + model.CAISOImports['SCE',i]
    exports = sum(model.flow['SCE',k,i] for k in model.sinks) + model.HorizonCAISOExports['SCE',i]         
    return s1 + s2 + s3 + other + imports - exports >= model.HorizonDemand['SCE',i]
model.Bal3Constraint= Constraint(model.hh_periods,rule=Zone3_Balance)

def Zone4_Balance(model,i):
    s1 = sum(model.mwh_1[j,i] for j in model.Zone4Generators)
    s2 = sum(model.mwh_2[j,i] for j in model.Zone4Generators)  
    s3 = sum(model.mwh_3[j,i] for j in model.Zone4Generators)  
    other = model.hydro['SDGE',i] + model.solar['SDGE',i]\
    + model.wind['SDGE',i] + model.HorizonMustRun['SDGE',i]   
    imports = sum(model.flow[s,'SDGE',i] for s in model.sources) + model.CAISOImports['SDGE',i]
    exports = sum(model.flow['SDGE',k,i] for k in model.sinks) + model.HorizonCAISOExports['SDGE',i]         
    return s1 + s2 + s3 + other + imports - exports >= model.HorizonDemand['SDGE',i]
model.Bal4Constraint= Constraint(model.hh_periods,rule=Zone4_Balance)

#
#Max capacity constraints on variable resources 
def HydroC(model,z,i):
    return model.hydro[z,i] <= model.HorizonHydro[z,i]  
model.HydroConstraint= Constraint(model.zones,model.hh_periods,rule=HydroC)

def SolarC(model,z,i):
    return model.solar[z,i] <= model.HorizonSolar[z,i]
model.SolarConstraint= Constraint(model.zones,model.hh_periods,rule=SolarC)

def WindC(model,z,i):
    return model.wind[z,i] <= model.HorizonWind[z,i]
model.WindConstraint= Constraint(model.zones,model.hh_periods,rule=WindC)

def ImportsC(model,z,i):
    return model.CAISOImports[z,i] <= model.HorizonCAISOImports[z,i]
model.ImportsConstraint= Constraint(model.zones,model.hh_periods,rule=ImportsC)


##max capacity constraints on flows, etc. 
def FlowC(model,s,k,i):
    return model.flow[s,k,i] <= model.limit[s,k]        
model.FlowConstraint= Constraint(model.sources,model.sinks,model.hh_periods,rule=FlowC)


#Max Capacity Constraint
def MaxC(model,j,i):
    return model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i] <= model.on[j,i] * model.netcap[j]
model.MaxCap= Constraint(model.Generators,model.hh_periods,rule=MaxC)

#
##Min Capacity Constraint
def MinC(model,j,i):
    return model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i] >= model.on[j,i] * model.mincap[j]
model.MinCap= Constraint(model.Generators,model.hh_periods,rule=MinC)

#
##System Reserve Requirement (excludes pumped storage)
def SysReserve(model,i):
    return sum(model.srsv[j,i] for j in model.Coal) + sum(model.srsv[j,i] for j in model.Gas) + sum(model.srsv[j,i] for j in model.Oil) + sum(model.nrsv[j,i] for j in model.Coal) + sum(model.nrsv[j,i] for j in model.Gas) + sum(model.nrsv[j,i] for j in model.Oil) >= model.HorizonReserves[i]
model.SystemReserve = Constraint(model.hh_periods,rule=SysReserve)
##
def SpinningReq(model,i):
    return sum(model.srsv[j,i] for j in model.Generators ) >= 0.5 * model.HorizonReserves[i]
model.SpinReq = Constraint(model.hh_periods,rule=SpinningReq)           
#
#
##Spinning reserve can only be offered by units that are online
def SpinningReq2(model,j,i):
    return model.srsv[j,i] <= model.on[j,i]*model.netcap[j]
model.SpinReq2= Constraint(model.Generators,model.hh_periods,rule=SpinningReq2)
#
##
###Segment capacity requirements
def Seg1(model,j,i):
    return model.mwh_1[j,i] <= .6*model.netcap[j]
model.Segment1 = Constraint(model.Generators,model.hh_periods,rule=Seg1)
#
def Seg2(model,j,i):
    return model.mwh_2[j,i] <= .2*model.netcap[j]
model.Segment2 = Constraint(model.Generators,model.hh_periods,rule=Seg2)

def Seg3(model,j,i):
    return model.mwh_3[j,i] <= .2*model.netcap[j]
model.Segment3 = Constraint(model.Generators,model.hh_periods,rule=Seg3)
##
#
##Zero Sum Constraint
def ZeroSum(model,j,i):
    return model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i] + model.srsv[j,i] + model.nrsv[j,i] <= model.netcap[j]
model.ZeroSumConstraint=Constraint(model.Generators,model.hh_periods,rule=ZeroSum)
#
#
##Switch is 1 if unit is turned on in current period
def SwitchCon(model,j,i):
    return model.switch[j,i] >= 1 - model.on[j,i-1] - (1 - model.on[j,i])
model.SwitchConstraint = Constraint(model.Generators,model.hh_periods,rule = SwitchCon)
#
#
##Min Up time
def MinUp(model,j,i,k):
    if i > 0 and k > i and k < min(i+model.minu[j]-1,model.HorizonHours):
        return model.on[j,i] - model.on[j,i-1] <= model.on[j,k]
    else: 
        return Constraint.Skip
model.MinimumUp = Constraint(model.Generators,model.HH_periods,model.HH_periods,rule=MinUp)
#
##Min Down time
def MinDown(model,j,i,k):
   if i > 0 and k > i and k < min(i+model.mind[j]-1,model.HorizonHours):
       return model.on[j,i-1] - model.on[j,i] <= 1 - model.on[j,k]
   else:
       return Constraint.Skip
model.MinimumDown = Constraint(model.Generators,model.HH_periods,model.HH_periods,rule=MinDown)

#Pumped Storage constraints
def PSHC(model,j,i):
    days  = int(model.HorizonHours/24)
    for d in range(0,days):
        return sum(model.mwh_1[j,i] + model.mwh_2[j,i] + model.mwh_3[j,i] for i in range(d*24+1,d*24+25)) <= 10*model.netcap[j]
model.PumpTime = Constraint(model.PSH,model.hh_periods,rule=PSHC)