import numpy as np
import pandas as pd
from WindPy import *

from .tdays import tdays_prev, to_date

def wind_series(wcodes, fields, s_date, e_date, **kwargs):
    s_date = tdays_prev(to_date(s_date), **kwargs)
    e_date = tdays_prev(to_date(e_date), **kwargs)
    options = ";".join([k + "=" + v for k, v in kwargs.items()])
    
    if s_date == e_date:
        series = quote_value(wcodes, fields, s_date, **kwargs)
    else:
        wind_data = w.wsd(wcodes, fields, s_date, e_date, options)
        series = pd.DataFrame(wind_data.Data, index=wind_data.Codes, columns=wind_data.Times).T
        
    return series
