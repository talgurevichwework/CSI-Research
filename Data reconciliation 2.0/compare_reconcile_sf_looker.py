from we_module.we import We
import queries_sf
import queries_sm
import queries_looker
we = We(True)
import pandas as pd
import csv

# Variables:
start_date = '2018-08-01'
end_date = '2018-09-01'# Not inclusive
time_period = 'month'
output_file_destination = f'./Reports/looker_output{start_date}to{end_date}.csv'
reuse_file_destination = f'./Reports/looker_reuse{start_date}to{end_date}.csv'
fulloutput_file_destination = f'./Reports/looker_fulloutput{start_date}to{end_date}.csv'
printoutput_file_destination = f'./Reports/looker_printoutput{start_date}to{end_date}.txt'
test = f'./Reports/test{start_date}to{end_date}.csv'
output_file_sf_won = f'./Reports/sf_won{start_date}to{end_date}.csv'
output_file_sf_lost = f'./Reports/sf_lost{start_date}to{end_date}.csv'
output_file_sf_net = f'./Reports/sf_net{start_date}to{end_date}.csv'
output_file_looker = f'./Reports/looker{start_date}to{end_date}.csv'
output_file_looker_sf_merge = f'./Reports/outer_looker_sf_merge{start_date}to{end_date}.csv'


# Get query results as pandas dfs
looker_df = we.get_tbl_query(queries_looker.create_looker_query(time_period, start_date, end_date))
cw_df = we.get_tbl_query(queries_sf.create_salesforce_closed_won_query(time_period, start_date, end_date))
cl_df = we.get_tbl_query(queries_sf.create_salesforce_closed_lost_query(time_period, start_date, end_date))
#re_df = we.get_tbl_query(queries.create_sapi_reuserecords_query(time_period, start_date, end_date))
#sm_df = we.get_tbl_query(queries-sm.create_spaceman_r_cr_ma_query(time_period, start_date, end_date))
#org_df = we.get_tbl_query(queries.create_orgs_from_billing(start_date, end_date))

# Merge closed won and closed lost tables
sf_df = cl_df.merge(cw_df, left_on=['uuid_c'], right_on=['uuid_c'], how='outer')
sf_df['net_desks_closedlost']= sf_df['net_desks_closedlost'].fillna(0)
sf_df['net_desks_closedwon']= sf_df['net_desks_closedwon'].fillna(0)
sf_df['Sf Net Desk Change'] = sf_df['net_desks_closedwon'] + sf_df['net_desks_closedlost']
sf_df = sf_df[['uuid_c', 'Sf Net Desk Change']]

# Merge salesforce table with looker table
comp_df = sf_df.merge(looker_df, how='outer', left_on='uuid_c', right_on='accounts_account_uuid') #simple innitial outer merge on uuid
comp_df['Sf Net Desk Change']= comp_df['Sf Net Desk Change'].fillna(0)
comp_df['new_sales_reporting_net_sales_1']= comp_df['new_sales_reporting_net_sales_1'].fillna(0)
comp_df['Sf Looker Difference'] = comp_df['Sf Net Desk Change'] - comp_df['new_sales_reporting_net_sales_1']
comp_df['Sf Looker Absolute Difference'] = abs(comp_df['Sf Looker Difference'])
comp_df['accounts_account_uuid'] = comp_df['accounts_account_uuid'].fillna(comp_df['uuid_c'])
comp_df = comp_df[['accounts_account_uuid', 'new_sales_reporting_account_name', 'Sf Net Desk Change', 'new_sales_reporting_net_sales_1', 'Sf Looker Difference', 'Sf Looker Absolute Difference']]
comp_df.rename(index=str, columns={"new_sales_reporting_account_name": "Billing Account Name", "accounts_account_uuid": "Account UUID", "new_sales_reporting_net_sales_1": "Looker Net Desk Change"}, inplace=True)

return_df = comp_df[comp_df['Sf Looker Absolute Difference'] != 0]
return_df.to_csv(output_file_destination, encoding='utf-8', index=False)

with open(printoutput_file_destination, "w") as text_file:
	text_file.write('Date Frame: %s - %s\n' % (start_date, end_date))
	text_file.write('Transaction Total: %d\n' % comp_df['Looker Net Desk Change'].sum())
	text_file.write('Salesforce Total: %d\n' % comp_df['Sf Net Desk Change'].sum())
	text_file.write('Net Gap: %d\n' % comp_df['Sf Looker Difference'].sum())
	text_file.write('Absolute Gap: %d\n' % comp_df['Sf Looker Absolute Difference'].sum())
	text_file.write('Accounts Affected: %d\n' % comp_df['Account UUID'].nunique())

# test file outputs
sf_df.to_csv(output_file_sf_net , encoding='utf-8', index=False) #sf agregation
looker_df.to_csv(output_file_looker , encoding='utf-8', index=False) #looker_df
cw_df.to_csv(output_file_sf_won, encoding='utf-8', index=False) # sf opps
cl_df.to_csv(output_file_sf_lost, encoding='utf-8', index=False) # sf opps
comp_df.to_csv(output_file_looker_sf_merge, encoding='utf-8', index=False) #looker sf Merge
