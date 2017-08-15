import pypyodbc
import pandas.io.sql as psql
import pandas as pd
import os, platform
from .Custom_functions import dbconnect, dbquery


pd.options.display.float_format = '{:,.0f}'.format

def MissingImages(contract):
    db = contract
    df = pd.DataFrame()
    query = open(os.path.join('./app/queries/', 'db-servers.txt')).read()
    user = 'rptuser'
    password = 'rptuser200804'
    dbServers = dbquery(dbconnect(db,user,password),query )
    dbServers = dbServers.loc[(dbServers['machineip'] != '172.28.84.33') & (dbServers['machineip'] != '172.28.89.33')] # & (dbServers['machineip'] != '172.28.86.33')]
    missingImageQuery = open(os.path.join('./app/queries/', 'missingImagePercentage.txt')).read()
    for d in dbServers.itertuples():
        ip = getattr(d, 'machineip')
        org = getattr(d, 'orgname')
        missingImageResults = dbquery(dbconnect(ip,user,password), missingImageQuery)
        df = df.append(missingImageResults, ignore_index=True)
    return df
        
