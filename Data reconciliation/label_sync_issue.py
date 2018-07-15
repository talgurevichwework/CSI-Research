def label_sync_issue(row, vtrans_df):
	if row['Account Name'].str.contains("WeWork"): 
		return('WeWork account')
	if row['Country Code'] == 'CHN' & row['Looker Net Desk Change'] < 0: 
		return('China moveout')
	if row['Contract UUID'].isnull():
		return ('No contract UUID')
	if row['Vtrans Net Desk Change'] == 0 & row['Sf Net Desk Change'] == 1: # HD move in and move out in same period
		return ('HD move in and move out at same time')
	