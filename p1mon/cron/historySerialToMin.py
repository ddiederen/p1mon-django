#%% clear
for name in dir():
    if not name.startswith('_'):
        if name not in ["In","Out","exit","get_ipython","quit",]:
            print('deleting: '+name)
            del globals()[name]
del globals()['name']

#%% libraries
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','p1mon.settings')
django.setup()

import pandas as pd
from django_pandas.io import read_frame
from datetime import timedelta
from django.utils import timezone

from serialdata.models import SerialLive
from history.models import HistoryMin

import gc
gc.collect()

#%% data query
# length of record
deltaT = timedelta(days=0.1)
datetime_query = timezone.now().date() - deltaT

# query set
qs1 = SerialLive.objects.filter(timestamp__gte=datetime_query)

# to data frame
df1 = read_frame(qs1)

#%% maxima per interval
df1Hist = df1.copy(deep=True)

df1Hist['minute'] = df1Hist['timestamp'].dt.minute
df1Hist['hour'] = df1Hist['timestamp'].dt.hour
df1Hist['day'] = df1Hist['timestamp'].dt.day
df1Hist['month'] = df1Hist['timestamp'].dt.month
df1Hist['year'] = df1Hist['timestamp'].dt.year

# variables
varMax = ['timestamp','verbr_kwh_181', 'verbr_kwh_182','gelvr_kwh_281','gelvr_kwh_282','verbr_gas_2421',]

# by groups
byMin = ['year','month','day','hour','minute',]
#byHour = ['year','month','day','hour',]
#byDay = ['year','month','day',]
#byMonth = ['year','month',]
#byYear = ['year',]

# get max by groups
df1HistMin1 = df1Hist[byMin+varMax].groupby(by=byMin).max()
#df1HistHour1 = df1Hist[byHour+varMax].groupby(by=byHour).max()
#df1HistDay1 = df1Hist[byDay+varMax].groupby(by=byDay).max()
#df1HistMonth1 = df1Hist[byMonth+varMax].groupby(by=byMonth).max()
#df1HistYear1 = df1Hist[byYear+varMax].groupby(by=byYear).max()

# merge in tariefcode
df1HistMin1 =    pd.merge(left=df1HistMin1,right=df1[['timestamp','tariefcode']],how='left',on='timestamp') 
#df1HistHour1 =   pd.merge(left=df1HistHour1,right=df1[['timestamp','tariefcode']],how='left',on='timestamp') 
#df1HistDay1 =    pd.merge(left=df1HistDay1,right=df1[['timestamp','tariefcode']],how='left',on='timestamp') 
#df1HistMonth1 =  pd.merge(left=df1HistMonth1,right=df1[['timestamp','tariefcode']],how='left',on='timestamp') 
#df1HistYear1 =   pd.merge(left=df1HistYear1,right=df1[['timestamp','tariefcode']],how='left',on='timestamp') 

#%% Calculate usage
# function to calculate usage
def funCalcUsage(dfIn,deltaT):
    # shift one time step
    tabVerbr1 = dfIn[['verbr_kwh_181','verbr_kwh_182','gelvr_kwh_281','gelvr_kwh_282','verbr_gas_2421',]]
    tabVerbr1.columns
    tabVerbr2 = tabVerbr1[0:-1]            # second row to last
    tabVerbr2 = tabVerbr2.rename(columns={'verbr_kwh_181':'verbr_kwh_181x','verbr_kwh_182':'verbr_kwh_182x'})
    tabVerbr2 = tabVerbr2.rename(columns={'gelvr_kwh_281':'gelvr_kwh_281x','gelvr_kwh_282':'gelvr_kwh_282x'})
    tabVerbr2 = tabVerbr2.rename(columns={'verbr_gas_2421':'verbr_gas_2421x'})
    tabVerbr2.columns
    
    tabVerbr2['timestamp'] = dfIn[1:]['timestamp'].tolist()
    #tabVerbr2['timestamp'] = dfIn['timestamp'].tolist()
    
    dfMerge = pd.merge(left=dfIn,right=tabVerbr2,how='left',on='timestamp')
    dfMerge.columns
    
    # calculate usage
    dfMerge = dfMerge.assign(verbr_kwh_x=(dfMerge.verbr_kwh_181-dfMerge.verbr_kwh_181x)+(dfMerge.verbr_kwh_182-dfMerge.verbr_kwh_182x))
    dfMerge = dfMerge.assign(gelvr_kwh_x=(dfMerge.gelvr_kwh_281-dfMerge.gelvr_kwh_281x)+(dfMerge.gelvr_kwh_282-dfMerge.gelvr_kwh_282x))
    dfMerge = dfMerge.assign(verbr_gas_x=(dfMerge.verbr_gas_2421-dfMerge.verbr_gas_2421x))
    dfMerge.columns
    dfMerge.drop(columns=['verbr_kwh_181x','verbr_kwh_182x','gelvr_kwh_281x','gelvr_kwh_282x','verbr_gas_2421x',],inplace=True) # delete columns
    dfMerge.columns
    
    # per time interval
    dfMerge = dfMerge.assign(act_verbr_kw_170=dfMerge.verbr_kwh_x/deltaT)
    dfMerge = dfMerge.assign(act_gelvr_kw_270=dfMerge.gelvr_kwh_x/deltaT)
    dfMerge = dfMerge.assign(act_verbr_gas=dfMerge.verbr_gas_x/deltaT)
    
    # retun
    return(dfMerge)
    
df1HistMin2 = funCalcUsage(dfIn=df1HistMin1.copy(deep=True),deltaT=1/60 )
#df1HistHour2 = funCalcUsage(dfIn=df1HistHour1.copy(deep=True),deltaT=1 )
#df1HistDay2 = funCalcUsage(dfIn=df1HistDay1.copy(deep=True),deltaT=24 )
#df1HistMonth2 = funCalcUsage(dfIn=df1HistMonth1.copy(deep=True),deltaT=365.25*24/12)
#df1HistYear2 = funCalcUsage(dfIn=df1HistYear1.copy(deep=True),deltaT=365.25*24)

#%% Adjust to save
# drop columns
df1HistMin2.drop(columns=['act_verbr_gas','verbr_gas_x',],inplace=True)

# drop first line with NAN values and incomplete last line
df1HistMin2 = df1HistMin2[1:-1]

#%% save          
HistoryMin.objects.bulk_create(ignore_conflicts=True,objs={HistoryMin(**vals) for vals in df1HistMin2.to_dict('records')})
##HistoryUur.objects.bulk_create(ignore_conflicts=True,objs={HistoryUur(**vals) for vals in df1HistHour2.to_dict('records')})
#HistoryDag.objects.bulk_create(ignore_conflicts=True,objs={HistoryDag(**vals) for vals in df1HistDay2.to_dict('records')})
#HistoryMaand.objects.bulk_create(ignore_conflicts=True,objs={HistoryMaand(**vals) for vals in df1HistMonth2.to_dict('records')})
#HistoryJaar.objects.bulk_create(ignore_conflicts=True,objs={HistoryJaar(**vals) for vals in df1HistYear2.to_dict('records')})

print("Converted to history: minutes")