import datetime as dt
import pandas as pd
from WindPy import *

w.start()


# return today's date
def today():
    return dt.datetime.today().date()


# return yesterday's date
def yesterday():
    return today() - dt.timedelta(days=1) # today-1


# return tomorrow's date
def tomorrow():
    return today() - dt.timedelta(days=-1) # today+1


# trans date format from string to datetime.date
def to_date(date):
    """
    #Func:
        trans date format from string to datetime.date
    
    #Params:
        date: date in string format like "2018-03-24"
    
    #Return:
        date in datetime.date format
    """
    
    if isinstance(date, str):
        date = dt.datetime.strptime(date, "%Y-%m-%d").date() # YYYY-MM-DD
        
    return date


# return previous(most recent) trading day's date
# from today or a paticular date
def tdays_prev(date=None, **kwargs):
    """
    #Func:
        return previous(most recent) trading day's date
        from today or a paticular date
    
    #Params:
        date: e.g: "20181010", "2018/10/10", "2018-10-10", datetime.date(2018, 10, 10)
        **kwargs: ref: https://www.windquant.com/
    
    #Return:
        date in datetime.date format
    """
    
    edate = to_date(date) # end date
    
    # ED-0TD is Wind date macro, ref: https://www.windquant.com/
    # 0 trading day before end date
    wind_data = w.tdays("ED-0TD", edate, **kwargs)

    return wind_data.Times[0] # datetime.date


# return next trading day's date
# from today or a paticular date
def tdays_next(date=None, **kwargs):
    """
    #Func:
        return next trading day's date
        from today or a paticular date
    
    #Params:
        date: e.g: "20181010", "2018/10/10", "2018-10-10", datetime.date(2018, 10, 10)
        **kwargs: ref: https://www.windquant.com/
    
    #Return:
        date in datetime.date format
    """
    
    sdate = to_date(date) # start date
    
    # SD+1TD is Wind date macro, ref: https://www.windquant.com/
    # 1 trading day after start date
    wind_data = w.tdays(sdate, "SD+1TD", **kwargs)
    
    return wind_data.Times[0] # datetime.date


# return previous(most recent) trading day's date
# from a [offset] of a paticular date
def tdays_offset(offset, date, **kwargs):
    """
    #Func:
        return previous(most recent) trading day's date
        from a [offset] of a paticular date
    
    #Params:
        offset: offset in Wind date macro, e.g: "-1W", "-2M"
        date: e.g: "20181010", "2018/10/10", "2018-10-10", datetime.date(2018, 10, 10)
        **kwargs: ref: https://www.windquant.com/
    
    #Return:
        date in datetime.date format
    """
    
    # parsing offset
    if offset[-2:].upper() == "TD":
        prd = "TD"  # trading day
        offset = int(offset[:-2])
    else:
        prd = offset[-1:].upper()
        offset = int(offset[:-1])
    
    date = to_date(date)
    options = ";".join([k + "=" + v for k, v in kwargs.items()])
    options = options + ";period=" + prd
    
    wind_data = w.tdaysoffset(offset, date, options)
    
    return wind_data.Times[0] # datetime.date
    

# return the nearest trading day's date
# e.g: Sat -> Fri, Sun -> Mon
def tdays_nearest(date=None, **kwargs):
    """
    #Func:
        return the nearest trading day's date
        e.g: Sat -> Fri, Sun -> Mon
    
    #Params:
        date: e.g: "20181010", "2018/10/10", "2018-10-10", datetime.date(2018, 10, 10)
        **kwargs: ref: https://www.windquant.com/
    
    #Return:
        date in datetime.date format
    """
    
    date = today() if date is None else to_date(date) # if None, today
    
    prev_tdate = tdays_prev(date, **kwargs)
    next_tdate = tdays_next(date, **kwargs)

    # prev_tdate <- prev_delta -> date <- next_delta -> next_tdate
    prev_delta = date - prev_tdate
    next_delta = next_tdate - date
    
    if prev_delta.days == next_delta.days == 1:
        return date
    elif prev_delta <= next_delta:
        return prev_tdate
    else:
        return next_tdate


# return a date series of trading day from start date to end date
def tdays_series(sdate, edate=None, **kwargs):
    """
    #Func:
        return a date series of trading day from start date to end date
    
    #Params:
        sdate, edate: e.g: "20181010", "2018/10/10", "2018-10-10", datetime.date(2018, 10, 10)
        **kwargs: ref: https://www.windquant.com/
    
    #Return:
        date series in pandas Series
    """
    
    sdate = to_date(sdate) # start date
    edate = today() if edate is None else to_date(edate) # end date, if None, today
    
    wsd_data = w.tdays(sdate, edate, **kwargs)
    
    if wsd_data.Data:
        return pd.Series(wsd_data.Data[0], index=wsd_data.Times)
    else:
        return None

    
# count how many trading days from start date to end date
def tdays_count(sdate, edate=None, **kwargs):
    """
    #Func:
        count how many trading days from start date to end date
    
    #Params:
        sdate, edate: e.g: "20181010", "2018/10/10", "2018-10-10", datetime.date(2018, 10, 10)
        **kwargs: ref: https://www.windquant.com/
    
    #Return:
        a number
    """
    
    return len(tdays_series(sdate, edate=None, **kwargs))
