from we_module.we import We
import queries
import pandas as pd
from datetime import datetime as dt
we = We(True)

def check_hd_nomomi(reservation_uuid): # Returns True if reservation has move in before 01/01/2018
	hd_df = we.get_tbl_query(queries.create_hd_opp_query(reservation_uuid, 'movein'))
	if len(hd_df['close_date'].values) == 0:
		return False
	close_date = hd_df['close_date'].values[0] 
	return (close_date < dt.date(dt.strptime('2017-11-01', "%Y-%m-%d"))) # Need to understand from Tal what is correct date to start from

def check_hd_mimo_sametime(reservation_uuid): # Returns True if reservation has move in and move out at same time
	hd_df = we.get_tbl_query(queries.create_hd_res_query(reservation_uuid))
	if len(hd_df['date_reserved_local'].values) != 2:
		return False
	return (hd_df['date_reserved_local'].values[0] == hd_df['date_reserved_local'].values[1])

def label_sync_issue(row, vtrans_df):
	if type(row['Account Name']) == 'str' and "WeWork" in row['Account Name']: 
		return('WeWork account')
	if row['Country Code'] == 'CHN' and row['Vtrans Net Desk Change'] < 0: 
		return('China moveout')
	if pd.isnull(row['Contract UUID']):
		return ('No contract UUID')
	if row['Vtrans Net Desk Change'] == 0 and row['Sf Net Desk Change'] == 1 and check_hd_mimo_sametime(row['Contract UUID']): # HD move in and move out in same period
		return ('HD move in and move out at same time')
	if row['Vtrans Net Desk Change'] == -1 and row['Sf Net Desk Change'] == 0 and check_hd_nomomi(row['Contract UUID']): # HD move out missed by sf
		return ('Old HD missing move in and move out')
	else:
		return ("")