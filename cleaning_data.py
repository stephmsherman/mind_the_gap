#!/usr/bin/env python
# -*- coding: utf-8 -*-
###insert path so I can reference functions that live in folder
#%%
import sys
sys.path.insert(0,"/Users/stephaniesherman/Dropbox/insight_data_science_program/opm_federal_employment_data/create_db_fed_employment")
from models import dbsession, EmployeeInfo
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import re
#%%
#using pandas with a column specification   
col_specification =[(0, 9),(9, 32), (32, 36), (36, 38),(38, 40),(40, 42),(42, 44),(44, 46),(46, 50),(50, 53), (53, 58),(59,61),(61,63),(63,65),(65,70), (70,75),(75,76) ,(76,82),(82,83),(83,85),(85,86),(86,87)]
files =glob.glob('/Users/stephaniesherman/Dropbox/insight_data_science_program/opm_federal_employment_data/fedscope_buzzfeed/1973-09-to-2014-06/non-dod/status/Status_Non_DoD_????_12.txt')

#%%
appended_data = []
for f in files:
    e = pd.read_fwf(f,header = None,converters={0:str,3:str,4:str,5:str,6:str,8:str, 9:str,10:str,11:str,16:str},colspecs=col_specification)
    e = e.rename(columns={0: 'employee_id',1: 'employee_name',2:'year',3: 'month',4:'day',
                     5: 'agency',6:'sub_agency',7:'state', 8: 'city',9: 'country',10:'age',11:'education_level', 
                      12: 'pay_plan', 13: 'pay_grade',14: 'length_of_service', 15: 'occupation',16: 'occupational_cat',17:'adjusted_basic_pay',18: 'supervisory_status',
                      19:'type_of_appointment',20:'work_schedule', 21: 'nsftp'})

    e = e.replace('*','')
    e = e.replace('**','')
    e = e.replace('***','')
    e = e.replace('****','')
    e = e.replace('******','')
    e['date1'] =pd.to_datetime(e[['year', 'month', 'day']])
    e.insert(5, 'date', e['date1'])
    del e['date1']
    appended_data.append(e)
appended_data = pd.concat(appended_data, axis = 1)
appended_data.to_csv('/Users/stephaniesherman/Dropbox/insight_data_science_program/opm_federal_employment_data/fedscope_buzzfeed/1973-09-to-2014-06/non-dod/status/all_data.csv')
#%%
