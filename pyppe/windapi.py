import pandas as pd
from WindPy import *

from .tdays import tdays_prev, to_date

w.start()

# fetch time series data via Wind API
def wind_series(wcodes, fields, sdate, edate, **kwargs):
    """
    #Func:
        fetch time series data via Wind API
        multi-codes with multi-indicators is supported
    
    #Params:
        wcodes: Wind code, e.g: "000300.SH", "000011.of", ["000300.SH", "000985.CSI"]
        fields: data field, e.g: "close", "NAV", "nav_adj", ["high", "low"]
        sdate: start date, e.g: "20180710", "2018/07/01", "2018-07-10", datetime.date(2018, 07, 10)
        edate: end date, e.g: "20181015", "2018/10/15", "2018-10-15", datetime.date(2018, 10, 15)
        **kwargs: ref: https://www.windquant.com/
    
    #Return:
        time series data in pandas DataFrame
        with date index and Wind code + fields columns (hierarchical columns)
    """
    
    sdate = tdays_prev(to_date(sdate), **kwargs) # most recent trading day of start date
    edate = tdays_prev(to_date(edate), **kwargs) # most recent trading day of end date

    # formatting parameters
    if isinstance(wcodes, str):
        # wcodes is a list of one Wind code like ["000300.SH"]
        wcodes = [wcodes]

    if isinstance(fields, list):
        # fields is a list like ["high", "low"]
        fields_len = len(fields)
    else:
        # fields is a string like "high"
        fields_len = 1

    df = pd.DataFrame()
    
    for code in wcodes:
        wind_data = w.wsd(code, fields, sdate, edate, **kwargs) # raw wind data
        
        if wind_data.ErrorCode != 0:
            # Error Code: ref: https://www.windquant.com/
            raise Exception("Wind Error Code:" + str(wind_data.ErrorCode))
        
        wcodes_col = [code.upper()] * fields_len # like ["000300.SH", "000300.SH"]

        idx = pd.MultiIndex.from_arrays([wcodes_col, wind_data.Fields])
        sub_df = pd.DataFrame(wind_data.Data, index=idx, columns=wind_data.Times).T
        
        df = pd.concat([df, sub_df], axis=1)

    return df
