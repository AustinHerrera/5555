import os, platform
import pypyodbc
import pandas as pd
import json
from flask_table import Table, Col

class laneResults(Table):
        org = Col('ORG')
        lane = Col('Lane')
        transactionCount = Col('Transactions by lane count')
        flushTags = Col('Flush Count by Lane')
        flushedPercentage = Col('Flushed Tags by Lane Percentage')
        secondTags = Col('Second Tag By Lane Count')
        violationCount = Col('Violations by Lane Count')
        violationPercentage = Col('Violations by Lane Percentage')
		

def dbconnect(dbip, user, pwd):
    dbip = dbip
    username = user
    pwd = pwd
    conn = pypyodbc.connect('DRIVER={FreeTDS};SERVER=%s;port=1433;uid=%s;pwd=%s' %(dbip, user, pwd))
    return conn


def dbquery(dbconnect, inputquery):
    connx = dbconnect
    results = pd.read_sql_query(inputquery, connx)
    connx.close()
    return results

	
def getDbServers(contract):
		dbip = contract
		username = 'rptuser'
		password = 'rptuser200804'
		dbServersQuery = open(os.path.join('./app/queries/','db-servers.txt')).read()
		dbservers = dbquery(dbconnect(dbip,username,password),dbServersQuery)
		return dbservers
		
def flushedTags(contract):
	pd.options.display.float_format == '0:.0%}'.format
	db = contract
	user = 'rptuser'
	password = 'rptuser200804'
	dbServersQuery = open(os.path.join('./app/queries/','db-servers.txt')).read()
	flushedTagsQuery = open(os.path.join('./app/queries/','flushtags.txt')).read()
	violQuery = open(os.path.join('./app/queries/', 'trans-viol-count.txt')).read()
	dbServers = dbquery(dbconnect(db,user,password),dbServersQuery)
	dbServers = dbServers.loc[(dbServers['machineip'] != '172.28.84.33') & (dbServers['machineip'] != '172.28.89.33') & (dbServers['machineip'] != '172.28.80.73')]
	results = []
	for d in dbServers.itertuples():
		ip = getattr(d, 'machineip')
		org = getattr(d, 'orgname')
		count = dbquery(dbconnect(ip, user, password), flushedTagsQuery)
		transactions = dbquery(dbconnect(ip, user, password), violQuery)
		secondTag = count[(count.secondtag == 'TRUE')]
		flushCount = count[(count.secondtag == 'FALSE')]
		secondTagCount = secondTag.groupby(['lanenumber'], as_index=False).count()
		flushCount2 = flushCount.groupby(['lanenumber'], as_index=False).count()
		flushCount2 = flushCount2.loc[(flushCount2['transdate'] >= 3)]
		for c in flushCount2.itertuples():
			flushCountByLane = c.transdate
			lane = getattr(c, "lanenumber")
			transactionByLane = transactions.loc[(transactions['lanenumber'] == lane)]
			transactionByLaneCount = len(transactionByLane)
			secondTagByLaneCount = secondTagCount[(secondTagCount['lanenumber'] == lane)]
			secondTagByLaneCount = secondTagByLaneCount.set_index('lanenumber')
			if secondTagByLaneCount.empty:
				secondTagByLaneCount = 0
			else:
				secondTagByLaneCount = secondTagByLaneCount.at[lane, 'transdate']
			violationsByLane = transactionByLane.loc[(transactionByLane['transtype'] == 'VIOL')]
			violationsByLaneCount = len(violationsByLane)
			flushedTagsByLanePercentage ='{0:.2%}'.format(  float(flushCountByLane) / transactionByLaneCount)
			violationsByLanePercentage = '{0:.2%}'.format(  float(violationsByLaneCount) /transactionByLaneCount)
			x = dict(org = org, lane = lane, transactionCount =  transactionByLaneCount, flushTags = flushCountByLane, flushedPercentage = flushedTagsByLanePercentage, secondTags = secondTagByLaneCount, violationCount = violationsByLaneCount, violationPercentage = violationsByLanePercentage)
			results.append(x)
	resultsOutput = pd.DataFrame()
	resultsOutput  = resultsOutput.from_dict(results)
	resultsOutput = resultsOutput[['org', 'lane', 'transactionCount', 'flushTags', 'flushedPercentage', 'secondTags', 'violationCount', 'violationPercentage',]]
	return resultsOutput

	
	
def autoClosed(contract):
	dbServers = getDbServers(contract)
	return dbServers