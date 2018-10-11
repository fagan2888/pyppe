import numpy as np
import pandas as pd
from WindPy import *
w.start()

from .tdays import tdays_prev, to_date


# fetch time series data via Wind API
def wind_series(wcodes, fields, sdate, edate, **kwargs):
    """
    #Func: fetch time series data via Wind API
    
    #Params:
    wcodes: Wind code, e.g: 000300.SH, 000011.OF
    fields: data field, e.g: "close", "nav", "nav_adj"
    sdate: start date, e.g: "2018-10-10", datetime.date(2018, 10, 10)
    edate: end date, e.g: "2018-10-15", datetime.date(2018, 10, 15)
    
    #Return:
    time series data in pandas DataFrame with date index and Wind code columns name
    """
    
    sdate = tdays_prev(to_date(sdate), **kwargs) # most recent trading day of start date
    edate = tdays_prev(to_date(edate), **kwargs) # most recent trading day of end date
    options = ";".join([k + "=" + v for k, v in kwargs.items()])
    
    if sdate < edate:
        wind_data = w.wsd(wcodes, fields, sdate, edate, options)
        series = pd.DataFrame(wind_data.Data, index=wind_data.Codes, columns=wind_data.Times).T
        return series
    else:
        return None
