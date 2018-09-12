from we_module.we import We
import queries
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
we = We(True)

# input : reservation uuid (string)
# output : true if reservation_uuid has move in before 2017-11-01
def check_hd_nomomi(reservation_uuid): 
	hd_df = we.get_tbl_query(queries.create_hd_opp_query(reservation_uuid, 'movein'))
	if len(hd_df['close_date'].values) == 0:
		return False
	close_date = hd_df['close_date'].values[0] 
	return (close_date < dt.date(dt.strptime('2017-11-01', "%Y-%m-%d")))

# input : reservation uuid (string)
# output : true if reservation has move in and move out on same day
def check_hd_mimo_sametime(reservation_uuid):
	hd_df = we.get_tbl_query(queries.create_hd_res_query(reservation_uuid))
	return (len(hd_df['date_reserved_local'].values) == 2 and hd_df['date_reserved_local'].values[0] == hd_df['date_reserved_local'].values[1])

# input : reservation uuid (string), salesforce_v2.opportunity table covering from one month + start date to one month + end date
# output : true if reservation has move in and move out on same day
def check_mo_nextmonth(reservation_uuid, cl_nextmonth_df): # Returns True if the move out opportunity is one month late
	res_df = cl_nextmonth_df[(cl_nextmonth_df['reservation_uuid_c']==reservation_uuid) | (cl_nextmonth_df['contract_uuid_c']==reservation_uuid)]
	return(len(res_df['total_desks_reserved_net_c'].values) >= 1 and res_df['total_desks_reserved_net_c'].values[0] == -1)

# input : 
# 1) pandas row from return_df - must contain row['Account Name'], row['Contract UUID'], row['Country Code'], row['Vtrans Count'], row['Salesforce Count']
# 2) salesforce_v2.opportunity table covering from one month + start date to one month + end date
# 3) sales_api_public.opportunity_reuse_records table within given time frame
# output : string containing sync error reason 
def label_sync_issue(row, cl_nextmonth_df, re_df):
	if type(row['Account Name']) == 'str' and "WeWork" in row['Account Name']: 
		return ('WeWork account')
	# if row['Country Code'] == 'CHN' and row['Vtrans Count'] < 0:
		return('China moveout')
	if row['Contract UUID']=='':
		return ('Unable to connect reservation to a membership agreement')
	if row['Vtrans Count'] < row['Salesforce Count'] and check_mo_nextmonth(row['Contract UUID'], cl_nextmonth_df):
		return ('HD move out one month late')
	if row['Vtrans Count'] == 0 and row['Salesforce Count'] == 1 and check_hd_mimo_sametime(row['Contract UUID']): # HD move in and move out in same period
		return ('HD move in and move out at same time')
	if row['Vtrans Count'] == -1 and row['Salesforce Count'] == 0 and check_hd_nomomi(row['Contract UUID']): # HD move out missed by sf
		return ('Old HD missing move in and move out')
	if row['Contract UUID'] in re_df['membership_agreement_uuid'].values: # reservation is in reuse logic table
		return('Possible issue with reuse logic')
	else:
		return ("")