def tdays_per_prd(prd):
    apx_tdays_per_1w = 5
    apx_tdays_per_1m = 21
    apx_tdays_per_3m = 63
    apx_tdays_per_6m = 125
    apx_tdays_per_1y = 250

    apx_tdays = {
                 "w":apx_tdays_per_1w,
                 "m":apx_tdays_per_1m,
                 "q":apx_tdays_per_3m,
                 "s":apx_tdays_per_6m,
                 "y":apx_tdays_per_1y
                }

    if prd in apx_tdays:
        return apx_tdays[prd]
    else:
        return None

def prds_per_year(prd):
    d_per_1y = 250
    w_per_1y = 52
    m_per_1y = 12
    q_per_1y = 4
    s_per_1y = 2
    y_per_1y = 1

    apx_prds = {
                "d":d_per_1y,
                "w":w_per_1y,
                "m":m_per_1y,
                "q":q_per_1y,
                "s":s_per_1y,
                "y":y_per_1y
               }

    if prd in apx_prds:
        return apx_prds[prd]
    else:
        return None
