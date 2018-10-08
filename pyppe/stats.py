import datetime as dt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from WindPy import *

from .periods import prds_per_year

def df_to_series(data):
    if isinstance(data, (pd.DataFrame)):
        return pd.Series(data[data.columns[0]])
    else:
        return data


def std(x, dof=1):
    return np.std(x, ddof=dof)


def annl_std(x, period):
    n = prds_per_year(period)
    if n is None:
        return None
    else:
        return std(x) * (n ** 0.5)

def var(x, dof=1):
    return np.var(x, ddof=dof)


def cov(x,y):
    x = df_to_series(x)
    y = df_to_series(y)
        
    cov_mat = np.cov(x,y)
    
    return cov_mat[0][1]

def cor(x, y):
    x = df_to_series(x)
    y = df_to_series(y)
        
    return cov(x, y) / (std(x) * std(y))

def r_sqr(x, y):
    x = df_to_series(x)
    y = df_to_series(y)
    
    return cor(x, y) ** 2

def upside(x, line=None):
    if line is None:
        line = 0
    
    return x[x > line]

def downside(x, line=None):
    if line is None:
        line = 0
    
    return x[x < line]

def downside_std(x, period="d", line=None):
    x = df_to_series(x)
    down_std = annl_std(downside(x, line), period)
    
    return down_std
    
def upside_std(x, period="d", line=None):
    x = df_to_series(x)
    up_std = annl_std(upside(x, line), period)
    
    return up_std 


def rebase(x, base):
    if base == 0:
        return None
    if isinstance(x, (pd.DataFrame, pd.Series)):
        return x / x.iloc[0] * base
    else:
        return x / x[0] * base


def to_simple_rets(prices):
    if isinstance(prices, (pd.DataFrame, pd.Series)):
        rets = prices.pct_change().iloc[1:]
    else:
        prices_dif = np.diff(prices, axis=0)
        rets = np.divide(prices_dif, p[:-1])

    return rets


def to_log_rets(prices):
    if isinstance(prices, (pd.DataFrame, pd.Series)):
        rets = np.log(prices).diff().iloc[1:]
    else:
        rets = np.diff(np.log(prices), axis=0)

    return rets

def prices_to_drawdown(prices):
    roll_max = np.maximum.accumulate(prices)
    dd = p / roll_max - 1

    return dd

def prices_to_maxdrawdown(prices):
    dd = prices_to_drawdown(prices)
    max_dd = np.min(dd)
    return max_dd


def single_index_model(x, benchmark):
    x = df_to_series(x)
    benchmark = df_to_series(benchmark)
        
    beta, alpha, rvalue, pvalue, stderr = stats.linregress(benchmark, x)
    
    result_dict = {
        "alpha":alpha,
        "beta":beta,
        "rvalue":rvalue,
        "pvalue":pvalue,
        "stderr":stderr
    }

    return result_dict


def treynor_mazuy_model(r, benchmark, risk_free):
    def tm_model(r, alpha, beta, gamma):
        return alpha + beta * r + gamma * r * r
    
    r = df_to_series(r) - risk_free
    benchmark = df_to_series(benchmark) - risk_free
    
    (alpha, beta, gamma), pcov = curve_fit(tm_model, benchmark, r)
    
    result_dict = {
        "alpha":alpha,
        "beta":beta,
        "gamma":gamma,
        "stderr":np.sqrt(np.diag(pcov))
    }
    
    return result_dict
