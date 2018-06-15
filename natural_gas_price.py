# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:45:25 2018

@author: Joy Hill
"""

import pandas as pd
import numpy as np

#monthly prices
Henry_2010 = pd.read_excel('fuel_prices/Henry Hub prices.xls',sheetname='2010')
Henry_2011 = pd.read_excel('fuel_prices/Henry Hub prices.xls',sheetname='2011')

#trade prices (every few days)
Henry_2015 = pd.read_excel('fuel_prices/ice_natgas-2015final.xls',sheetname='Henry')
Malin_2015 = pd.read_excel('fuel_prices/ice_natgas-2015final.xls',sheetname='Malin')


