import datetime as dt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from scipy.optimize import minimize 
from scipy.optimize import nnls 
from WindPy import *

from .periods import prds_per_year
from .windapi import wind_series


# calc trailing return based style analysis(rbsa)
def trailing_rbsa(rets, style, period="m"):
    if isinstance(period, str):
        period = tdays_per_prd(period)
        
    if isinstance(rets, (pd.DataFrame)):
        rets = rets[rets.columns[0]].values
    if isinstance(style, (pd.DataFrame)):
        idx = style.index[period:]
        cols = style.columns
        style = style.values
        
    length = len(rets)
    num_style = style.shape[1]
    
    def fn(x, A, b):
        return np.linalg.norm(A.dot(x) - b)

    cons = {'type': 'eq', 'fun': lambda x:  np.sum(x)-1} # constraints
    bds = [[0.0, None]] * num_style # bounds
    
    factors = []
    
    for i in range(0, length-period):
        x0, rnorm = nnls(style[i: i+period-1], rets[i: i+period-1])
        minout = minimize(fn, x0, args=(style[i: i+period-1], rets[i: i+period-1]),
                          method='SLSQP', bounds=bds, constraints=cons)
        
        factors.append(minout.x)

    return pd.DataFrame(factors, index=idx, columns=cols)
