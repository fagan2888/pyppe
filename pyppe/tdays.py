import datetime as dt
import pandas as pd
from WindPy import *

# return today's date
def today():
    return dt.datetime.today().date()

# return yesterday's date
def yesterday():
    return today() - dt.timedelta(days=1)

# return tomorrow's date
def tomorrow():
    return today() - dt.timedelta(days=-1)

# trans date format from string to datetime.date
def to_date(date):
    if isinstance(date, str):
        date = dt.datetime.strptime(date, "%Y-%m-%d").date()
        
    return date

# return previous(most recent) trading day's date
# from today or a paticular date
def tdays_prev(date=None, **kwargs):
    date = to_date(date)
    options = ";".join([k + "=" + v for k, v in kwargs.items()])
    
    wind_data = w.tdays("ED-0TD", date, options)
    tdate = wind_data.Times[0]
    
    return tdate

# return previous(most recent) trading day's date
# from a [offset] of a paticular date
def tdays_offset(offset, date, **kwargs):
    if offset[-2:].upper() == "TD":
        prd = "TD"
        offset = int(offset[:-2])
    else:
        prd = offset[-1:].upper()
        offset = int(offset[:-1])
    
    date = to_date(date)
    options = ";".join([k + "=" + v for k, v in kwargs.items()])
    options = options + ";period=" + prd
    
    wind_data = w.tdaysoffset(offset, date, options)
    tdate = wind_data.Times[0]
    
    return tdate

# return the nearest trading day's date
def tdays_nearest(date=None, **kwargs):
    date = today() if date is None else to_date(date)
    options = ";".join([k + "=" + v for k, v in kwargs.items()])
    
    prev_tdate = tdays_offset("-0TD", date, **kwargs)
    next_tdate = tdays_offset("1TD", date, **kwargs)

    prev_delta = date - prev_tdate
    next_delta = next_tdate - date
    
    if prev_delta.days == next_delta.days == 1:
        return date
    elif prev_delta <= next_delta:
        return prev_tdate
    else:
        return next_tdate
    
# return a date series of trading day from start date to end date
def tdays_series(s_date, e_date=None, **kwargs):
    s_date = to_date(s_date)
    e_date = today() if e_date is None else to_date(e_date)
    options = ";".join([k + "=" + v for k, v in kwargs.items()])
    
    wsd_data = w.tdays(s_date, e_date, options)
    
    if wsd_data.Data:
        return pd.Series(wsd_data.Data[0], index=wsd_data.Times)
    else:
        return None
    
# count how many trading days from start date to end date
def tdays_count(s_date, e_date=None, **kwargs):
    s_date = to_date(s_date)
    e_date = today() if e_date is None else to_date(e_date)
    options = ";".join([k + "=" + v for k, v in kwargs.items()])
    
    wsd_data = w.tdayscount(s_date, e_date, options)
    count = wsd_data.Data[0][0]
    
    return count
