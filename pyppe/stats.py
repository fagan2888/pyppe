import datetime as dt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from WindPy import *

from .periods import prds_per_year


# trans pandas Dataframe's first column to pandas Series
def df_to_series(df):
    """
    #Func:
    trans pandas Dataframe's first column to pandas Series
    
    #Params:
    df: pandas DataFrame
    
    #Return:
    pandas Series
    """ 

    if isinstance(df, (pd.DataFrame)):
        return pd.Series(df[df.columns[0]])
    else:
        return df


# return the maximum along columns
def maximum(x):
    """
    #Func:
        return the maximum along columns
    
    #Params:
        x: pd.DataFrame, pd.Series or np.ndarray
    
    #Return:
        the maximum
    """
    
    return x.max(axis=0)
    

# return the minimum along columns
def minimum(x):
    """
    #Func:
        return the minimum along columns
    
    #Params:
        x: pd.DataFrame, pd.Series or np.ndarray
    
    #Return:
        the minimum
    """
    
    return x.min(axis=0)
    

# return the median along columns
def median(x):
    """
    #Func:
        return the median along columns
    
    #Params:
        x: pd.DataFrame, pd.Series or np.ndarray
    
    #Return:
        the median
    """
    
    if isinstance(x, (pd.DataFrame, pd.Series)):
        return x.median(axis=0)
    else:
        # assume np.ndarray
        return np.median(x, axis=0)


# return the arithmetic average along columns
def arith_avg(x):
    """
    #Func:
        return the arithmetic average along columns
    
    #Params:
        x: pd.DataFrame, pd.Series or np.ndarray
    
    #Return:
        the arithmetic average
    """
    
    if isinstance(x, (pd.DataFrame, pd.Series)):
        return x.mean(axis=0)
    else:
        # assume np.ndarray
        return x.mean(axis=0)


# return the geometric mean along columns
def geo_avg(x):
    """
    #Func:
        return the geometric mean along columns
    
    #Params:
        x: pd.DataFrame, pd.Series or np.ndarray
    
    #Return:
        the geometric mean
    """
    
    if isinstance(x, (pd.DataFrame, pd.Series)):
        prod = x.product(axis=0)
    else:
        # assume np.ndarray
        prod = np.product(x, axis=0)
        
    return prod ** (1.0 / len(x))


# return the weighted average along columns
def wgt_avg(x, weights):
    """
    #Func:
        return the weighted average along columns
    
    #Params:
        x: pd.DataFrame (single column or multi columns), pd.Series or np.ndarray
        weights: pd.DataFrame (single column), pd.Series or np.ndarray
    
    #Return:
        the weighted average
    """
    
    if isinstance(weights, pd.DataFrame):
        weights = weights[weights.columns[0]]
    
    if isinstance(x, (pd.DataFrame, pd.Series)):
        wgt_mul = x.mul(weights, axis=0)
    else:
        # assume np.ndarray
        wgt_mul = np.multiply(x, weights)
    
    return wgt_mul.sum(axis=0) / weights.sum()


# calc standard deviation of series x
def std(x, dof=1):
    """
    #Func:
    calc standard deviation of series x
    
    #Params:
    x: pandas dataframe, pandas series or numpy array
    dof: degree of freedom

    #Return:
    standard deviation of series x
    """

    return np.std(x, ddof=dof)


# calc annulized standard deviation of series x
# e.g: returns series
def annl_std(x, period):
    """
    #Func:
    calc annulized standard deviation of series x
    e.g: returns series
    
    #Params:
    x: pandas dataframe, pandas series or numpy array
    period: freq of series x (daily, weekly, monthly...)

    #Return:
    annulized standard deviation of series x
    """

    n = prds_per_year(period)
    if n is None:
        return None
    else:
        return std(x) * (n ** 0.5)


# calc variance of series x
# e.g: returns series
def var(x, dof=1):
    """
    #Func:
    calc variance of series x
    
    #Params:
    x: pandas dataframe, pandas series or numpy array
    dof: degree of freedom

    #Return:
    variance of series x
    """

    return np.var(x, ddof=dof)


# calc covariance of series x and series y
# e.g: returns series
def cov(x,y):
    """
    #Func:
    calc covariance of series x
    e.g: returns series
    
    #Params:
    x, y: pandas dataframe, pandas series or numpy array

    #Return:
    covariance of series x and series y
    """

    x = df_to_series(x)
    y = df_to_series(y)
        
    cov_mat = np.cov(x, y)
    
    return cov_mat[0][1]


# calc correlation coefficient of series x and series y
# e.g: returns series
def cor(x, y):
    """
    #Func:
    calc correlation coefficient of series x and series y
    e.g: returns series
    
    #Params:
    x, y: pandas dataframe, pandas series or numpy array

    #Return:
    correlation coefficient of series x and series y
    """
    x = df_to_series(x)
    y = df_to_series(y)
        
    return cov(x, y) / (std(x) * std(y))


# calc coefficient of determination of series x and series y
# e.g: returns series
def r_sqr(x, y):
    """
    #Func:
    calc coefficient of determination of series x and series y
    e.g: returns series
    
    #Params:
    x, y: pandas dataframe, pandas series or numpy array

    #Return:
    coefficient of determination of series x and series y
    """

    x = df_to_series(x)
    y = df_to_series(y)
    
    return cor(x, y) ** 2


# return the elements above a paticular value in series x
def upside(x, line=0):
    """
    #Func:
    return the elements above a paticular value in series x
    
    #Params:
    x: pandas dataframe, pandas series or numpy array
    line: limited value

    #Return:
    series of x > line
    """
    
    return x[x > line]


# return the elements under a paticular value in series x
def downside(x, line=0):
    """
    #Func:
    return the elements under a paticular value in series x
    
    #Params:
    x: pandas dataframe, pandas series or numpy array
    line: limited value

    #Return:
    series of x < line
    """
    
    return x[x < line]


# calc downside standard deviation of series x
# e.g: returns series
def downside_std(x, period="d", line=0):
    """
    #Func:
    calc downside standard deviation of series x
    e.g: returns series
    
    #Params:
    x: pandas dataframe, pandas series or numpy array
    period: freq of series x (daily, weekly, monthly...)
    line: limited value

    #Return:
    downside standard deviation of series x
    """

    x = df_to_series(x)
    down_std = annl_std(downside(x, line), period)
    
    return down_std


# calc upside standard deviation of series x
# e.g: returns series
def upside_std(x, period="d", line=0):
    """
    #Func:
    calc upside standard deviation of series x
    e.g: returns series
    
    #Params:
    x: pandas dataframe, pandas series or numpy array
    period: freq of series x (daily, weekly, monthly...)
    line: limited value

    #Return:
    downside standard deviation of series x
    """

    x = df_to_series(x)
    up_std = annl_std(upside(x, line), period)
    
    return up_std 


# return rebased series x
# e.g: prices series
def rebase(x, base):
    """
    #Func:
    return rebased series x
    e.g: prices series
    
    #Params:
    x: pandas dataframe, pandas series or numpy array
    base: base

    #Return:
    rebased series x
    """

    if base == 0:
        return None
    if isinstance(x, (pd.DataFrame, pd.Series)):
        return x / x.iloc[0] * base
    else:
        return x / x[0] * base


# return simple rate of returns series from prices series
def to_simple_rets(prices):
    """
    #Func:
    return simple rate of returns series from prices series
    
    #Params:
    prices: prices series in pandas dataframe, pandas series or numpy array

    #Return:
    simple rate of returns series
    """

    if isinstance(prices, (pd.DataFrame, pd.Series)):
        rets = prices.pct_change().iloc[1:]
    else:
        # assume np.ndarray
        prices_dif = np.diff(prices, axis=0)
        rets = np.divide(prices_dif, p[:-1])

    return rets


# return log rate of returns series from prices series
def to_log_rets(prices):
    """
    #Func:
    return log rate of returns series from prices series
    
    #Params:
    prices: prices series in pandas dataframe, pandas series or numpy array

    #Return:
    log rate of returns series
    """

    if isinstance(prices, (pd.DataFrame, pd.Series)):
        rets = np.log(prices).diff().iloc[1:]
    else:
        # assume np.ndarray
        rets = np.diff(np.log(prices), axis=0)

    return rets


# return CAGR returns from prices series
def to_cagr_rets(prices):
    """
    #Func:
    return CAGR returns from prices series
    
    #Params:
    prices: prices series in pandas dataframe, pandas series or numpy array

    #Return:
    CAGR rate of return
    """

    if isinstance(prices, (pd.DataFrame, pd.Series)):
        rets = prices.iloc[-1] / prices.iloc[0] - 1
    else:
        # assume np.ndarray
        rets = prices[-1] / prices[0] - 1

    return rets


# return drawdown series from prices series
def prices_to_drawdown(prices):
    """
    #Func:
    return drawdown series from prices series
    
    #Params:
    prices: prices series in pandas dataframe, pandas series or numpy array

    #Return:
    drawdown series
    """

    roll_max = np.maximum.accumulate(prices)
    dd = p / roll_max - 1

    return dd


# return max drawdown of prices series
def prices_to_maxdrawdown(prices):
    """
    #Func:
    return max drawdown of prices series
    
    #Params:
    prices: prices series in pandas dataframe, pandas series or numpy array

    #Return:
    max drawdown
    """

    dd = prices_to_drawdown(prices)
    max_dd = np.min(dd)
    return max_dd
