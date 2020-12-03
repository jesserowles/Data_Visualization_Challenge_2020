import pandas as pd
import os
import numpy as np
import datetime as dt


def read_data():
    os.chdir('C:/Users/jesse/Documents/Grad_School/Other/Data Visualization Challenge')
    mf = 0.041619
    raw = pd.read_csv('raw_data.csv',header=3)
    raw.columns = ['time','rec','pulses']
    raw.index = pd.to_datetime(raw['time'])
    raw = raw.drop('time',axis=1)
    raw['vol'] = mf*raw['pulses']
    raw['gpm'] = raw['vol']/(4/60) #convert gallons per 4 seconds to gallons per minute
    evn = pd.read_csv('classified_events.csv')
    evn.columns = ['start','end','dur','vol','flow_gpm','peak','mode','label']
    evn['start'] = pd.to_datetime(evn['start'])
    evn['end'] = pd.to_datetime(evn['end'])

    evn['col'] = 'grey'
    typs = np.unique(evn['label'])
    cols = ['red','blue','green','magenta','goldenrod','purple','teal']
    nums = np.arange(0,len(typs))
    for i in range(len(typs)):
        evn.loc[evn['label']==typs[i],'col'] = cols[i]
        evn.loc[evn['label']==typs[i],'cnum'] = nums[i]
    tdc = [typs,nums,cols[0:len(typs)]]
    return raw, evn, mf, tdc
