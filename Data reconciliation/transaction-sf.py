from we_module.we import We
import queries
we = We(True)
import pandas as pd
import csv
import label_sync_issue as lsi
from dateutil.relativedelta import relativedelta as rd
from datetime import datetime as dt

# Variables:
start_date = '2018-06-12'
end_date = '2018-06-13'# Not inclusive
start_date_nextmonth = str((dt.strptime(start_date, "%Y-%m-%d") + rd(months=+1)).date())
end_date_nextmonth = str((dt.strptime(end_date, "%Y-%m-%d") + rd(months=+1)).date())
output_file_destination = f'./Reports/transaction_output{start_date}to{end_date}.csv'
reuse_file_destination = f'./Reports/transaction_reuse{start_date}to{end_date}.csv'
fulloutput_file_destination = f'./Reports/transaction_fulloutput{start_date}to{end_date}.csv'
printoutput_file_destination = f'./Reports/transaction_printoutput{start_date}to{end_date}.txt'

# Get query results as pandas dfs
vtrans_df = we.get_tbl_query(queries.create_vtrans_query_notrunc(start_date, end_date))
cw_df = we.get_tbl_query(queries.create_salesforce_closedwon_query_notrunc(start_date, end_date))
cl_df = we.get_tbl_query(queries.create_salesforce_closedlost_query_notrunc(start_date, end_date))
cl_nextmonth_df = we.get_tbl_query(f'''select o.reservation_uuid_c, o.contract_uuid_c, o.total_desks_reserved_net_c, o.close_date 
	from salesforce_v2.opportunity o
	where o.close_date >= TIMESTAMP '{start_date_nextmonth}' and o.close_date < TIMESTAMP '{end_date_nextmonth}' and o.total_desks_reserved_net_c < 0
	''')
re_df = we.get_tbl_query(queries.create_sapi_reuserecords_query_notrunc(start_date, end_date))

# Merge closed won and closed lost tables
sf_df = cl_df.merge(cw_df, left_on=['contract_uuid_c'], right_on=['contract_uuid_c'], how='outer')
sf_df['net_desks_closedlost']= sf_df['net_desks_closedlost'].fillna(0)
sf_df['net_desks_closedwon']= sf_df['net_desks_closedwon'].fillna(0)
sf_df['Salesforce Count'] = sf_df['net_desks_closedwon'] + sf_df['net_desks_closedlost']

sf_df['account_uuid_c_x'] = sf_df['account_uuid_c_x'].fillna(sf_df['account_uuid_c_y'])
sf_df['country_code_x'] = sf_df['country_code_x'].fillna(sf_df['country_code_y'])
sf_df['name_x'] = sf_df['name_x'].fillna(sf_df['name_y'])
sf_df['opp_name_x'] = sf_df['opp_name_x'].fillna(sf_df['opp_name_y'])

sf_df = sf_df[['opp_name_x', 'country_code_x', 'name_x', 'account_uuid_c_x', 'contract_uuid_c', 'Salesforce Count']]
sf_df = sf_df.rename(index=str, columns={'opp_name_x': 'opp_name_c', 'name_x': 'name_c', 'account_uuid_c_x': 'account_uuid_c', 'country_code_x': 'country_code_c'})

sf_df['contract_uuid_c'] = sf_df['contract_uuid_c'].fillna('')
sf_df['country_code_c'] = sf_df['country_code_c'].fillna('')
sf_df = sf_df.groupby(['opp_name_c', 'name_c', 'account_uuid_c', 'country_code_c', 'contract_uuid_c']).sum().reset_index()

# Get comparison table between sf and vtrans
comp_df = sf_df.merge(vtrans_df, how='outer', left_on='contract_uuid_c', right_on='contract_uuid')
comp_df['Salesforce Count']= comp_df['Salesforce Count'].fillna(0)
comp_df['desks_changed']= comp_df['desks_changed'].fillna(0)

comp_df['Net Gap'] = comp_df['Salesforce Count'] - comp_df['desks_changed']
comp_df['Absolute Gap'] = abs(comp_df['Net Gap'])

comp_df['opp_name_c'] = comp_df['opp_name_c'].fillna('')
comp_df['account_name'] = comp_df['account_name'].fillna(comp_df['name_c'])
comp_df['account_uuid'] = comp_df['account_uuid'].fillna(comp_df['account_uuid_c'])
comp_df['contract_uuid'] = comp_df['contract_uuid'].fillna(comp_df['contract_uuid_c'])
comp_df['country_code'] = comp_df['country_code'].fillna(comp_df['country_code_c'])

comp_df = comp_df[['account_name', 'account_uuid', 'opp_name_c', 'country_code', 'contract_uuid', 'Salesforce Count', 'desks_changed', 'Net Gap', 'Absolute Gap']]
comp_df = comp_df.rename(index=str, columns={"account_name": "Account Name","account_uuid": "Account UUID", "opp_name_c": "Opportunity Name", "country_code": "Country Code", "contract_uuid": "Contract UUID", "desks_changed": "Vtrans Count"})
return_df = comp_df[comp_df['Net Gap'] != 0]
return_df['Reason'] = ""

return_df['Reason'] = return_df.apply (lambda row: lsi.label_sync_issue(row, cl_nextmonth_df, re_df), axis=1)

full_output = return_df.merge(re_df, how='left', left_on=['Contract UUID', 'Account UUID'], right_on=['membership_agreement_uuid', 'company_uuid'])

return_df.to_csv(output_file_destination, encoding='utf-8', index=False)
full_output.to_csv(fulloutput_file_destination, encoding='utf-8', index=False)

with open(printoutput_file_destination, "w") as text_file:
	text_file.write('Date Frame: %s - %s' % (start_date, end_date))
	text_file.write('Transaction Total: %d' % comp_df['Vtrans Count'].sum())
	text_file.write('Salesforce Total: %d' % comp_df['Salesforce Count'].sum())
	text_file.write('Net Gap: %d' % comp_df['Net Gap'].sum())
	text_file.write('Absolute Gap: %d' % comp_df['Absolute Gap'].sum())
	text_file.write('Accounts Affected: %d' % comp_df['Account UUID'].nunique())

