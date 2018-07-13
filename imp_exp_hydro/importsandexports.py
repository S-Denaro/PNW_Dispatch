# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 15:45:47 2018

@author: Joy Hill
"""

#converting path data to exports or imports

import matplotlib.pyplot as plt
import pandas as pd 
from pandas.plotting import autocorrelation_plot
from pandas import ExcelWriter
import numpy as np
import scipy.stats as stats
from sklearn import linear_model
from sklearn.metrics import r2_score

Path_2010 = pd.read_excel('Path data.xlsx',sheetname='2010 Path')
Path_2011 = pd.read_excel('Path data.xlsx',sheetname='2011 Path')

#3 -- negative is import, pos is export
path3_2010 = Path_2010['Path3']
path3_2011 = Path_2011['Path3']

path3_2010_im = np.zeros(len(path3_2010))
path3_2010_exp = np.zeros(len(path3_2010))

for i in range(0,len(path3_2010)):
    if path3_2010[i] < 0:
        path3_2010_im[i] = -1*path3_2010[i]
    elif path3_2010[i] > 0:
        path3_2010_exp[i] = path3_2010[i]
        
path3_2011_im = np.zeros(len(path3_2011))
path3_2011_exp = np.zeros(len(path3_2011))

for i in range(0,len(path3_2011)):
    if path3_2011[i] < 0:
        path3_2011_im[i] = -1*path3_2011[i]
    elif path3_2011[i] > 0:
        path3_2011_exp[i] = path3_2011[i]        
        

#8 -- positive is import, neg is export
path8_2010 = Path_2010['Path8']
path8_2011 = Path_2011['Path8']

path8_2010_im = np.zeros(len(path8_2010))
path8_2010_exp = np.zeros(len(path8_2010))

for i in range(0,len(path8_2010)):
    if path8_2010[i] > 0:
        path8_2010_im[i] = path8_2010[i]
    elif path8_2010[i] < 0:
        path8_2010_exp[i] = -1*path8_2010[i]
        
path8_2011_im = np.zeros(len(path8_2011))
path8_2011_exp = np.zeros(len(path8_2011))

for i in range(0,len(path8_2011)):
    if path8_2011[i] > 0:
        path8_2011_im[i] = path8_2011[i]
    elif path8_2011[i] < 0:
        path8_2011_exp[i] = -1*path8_2011[i] 


#14 -- positive is import, neg is export
path14_2010 = Path_2010['Path14']
path14_2011 = Path_2011['Path14']

path14_2010_im = np.zeros(len(path14_2010))
path14_2010_exp = np.zeros(len(path14_2010))

for i in range(0,len(path14_2010)):
    if path14_2010[i] > 0:
        path14_2010_im[i] = path14_2010[i]
    elif path14_2010[i] < 0:
        path14_2010_exp[i] = -1*path14_2010[i]
        
path14_2011_im = np.zeros(len(path14_2011))
path14_2011_exp = np.zeros(len(path14_2011))

for i in range(0,len(path14_2011)):
    if path14_2011[i] > 0:
        path14_2011_im[i] = path14_2011[i]
    elif path14_2011[i] < 0:
        path14_2011_exp[i] = -1*path14_2011[i] 



#65 -- negative is import, pos is export
path65_2010 = Path_2010['Path65']
path65_2011 = Path_2011['Path65']

path65_2010_im = np.zeros(len(path65_2010))
path65_2010_exp = np.zeros(len(path65_2010))

for i in range(0,len(path65_2010)):
    if path65_2010[i] < 0:
        path65_2010_im[i] = -1*path65_2010[i]
    elif path65_2010[i] > 0:
        path65_2010_exp[i] = path65_2010[i]
        
path65_2011_im = np.zeros(len(path65_2011))
path65_2011_exp = np.zeros(len(path65_2011))

for i in range(0,len(path65_2011)):
    if path65_2011[i] < 0:
        path65_2011_im[i] = -1*path65_2011[i]
    elif path65_2011[i] > 0:
        path65_2011_exp[i] = path65_2011[i]    


#66 -- negative is import, pos is export
path66_2010 = Path_2010['Path66']
path66_2011 = Path_2011['Path66']

path66_2010_im = np.zeros(len(path66_2010))
path66_2010_exp = np.zeros(len(path66_2010))

for i in range(0,len(path66_2010)):
    if path66_2010[i] < 0:
        path66_2010_im[i] = -1*path66_2010[i]
    elif path66_2010[i] > 0:
        path66_2010_exp[i] = path66_2010[i]
        
path66_2011_im = np.zeros(len(path66_2011))
path66_2011_exp = np.zeros(len(path66_2011))

for i in range(0,len(path66_2011)):
    if path66_2011[i] < 0:
        path66_2011_im[i] = -1*path66_2011[i]
    elif path66_2011[i] > 0:
        path66_2011_exp[i] = path66_2011[i]  

#imports for each path stacked together, do we need to sum?
imports_2010 = np.stack((path3_2010_im,path8_2010_im,path14_2010_im,path65_2010_im,path66_2010_im),axis=1)
imports_2011 = np.stack((path3_2011_im,path8_2011_im,path14_2011_im,path65_2011_im,path66_2011_im),axis=1)

imports_2010_total = np.sum(imports_2010,axis=1)
imports_2011_total = np.sum(imports_2011,axis=1)

#exports for each path stacked together, do we need to sum?
exports_2010 = np.stack((path3_2010_exp,path8_2010_exp,path14_2010_exp,path65_2010_exp,path66_2010_exp),axis=1)
exports_2011 = np.stack((path3_2011_exp,path8_2011_exp,path14_2011_exp,path65_2011_exp,path66_2011_exp),axis=1)


exports_2010_total = np.sum(exports_2010,axis=1)
exports_2011_total = np.sum(exports_2011,axis=1)

imports10 = pd.DataFrame(imports_2010_total)
exports10 = pd.DataFrame(exports_2010_total)
writer = pd.ExcelWriter('Imports and Exports 2010.xlsx')
imports10.to_excel(writer,'imports')
exports10.to_excel(writer,'exports')

imports11 = pd.DataFrame(imports_2011_total)
exports11 = pd.DataFrame(exports_2011_total)
writer = pd.ExcelWriter('Imports and Exports 2011.xlsx')
imports11.to_excel(writer,'imports')
exports11.to_excel(writer,'exports')