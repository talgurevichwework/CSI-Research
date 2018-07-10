from we_module.we import We
import queries
we = We(True)
import pandas as pd
import csv

# Variables:
start_date = '2018-06-03'
end_date = '2018-06-10'# Not inclusive
time_period = 'Week'
output_file_destination = f'./Reports/output{start_date}to{end_date}.csv'
reuse_file_destination = f'./Reports/reuse{start_date}to{end_date}.csv'
fulloutput_file_destination = f'./Reports/fulloutput{start_date}to{end_date}.csv'

# Get query results as pandas dfs
vtrans_df = we.get_tbl_query(queries.create_vtrans_query_notrunc(start_date, end_date))
cw_df = we.get_tbl_query(queries.create_salesforce_closedwon_query(time_period, start_date, end_date))
cl_df = we.get_tbl_query(queries.create_salesforce_closedlost_query(time_period, start_date, end_date))
re_df = we.get_tbl_query(queries.create_sapi_reuserecords_query(time_period, start_date, end_date))
# res_df = we.get_tbl_query(queries.create_spaceman_reservations_query(time_period, start_date, end_date))
# ma_df = we.get_tbl_query(queries.create_spaceman_membershipagreements_query(time_period, start_date, end_date))
# sm_df = we.get_tbl_query(queries.create_spaceman_r_cr_ma_query(time_period, start_date, end_date))	

# Merge closed won and closed lost tables
sf_df = cl_df.merge(cw_df, left_on=['account_uuid_c'], right_on=['account_uuid_c'], how='outer')
sf_df['net_desks_closedlost']= sf_df['net_desks_closedlost'].fillna(0)
sf_df['net_desks_closedwon']= sf_df['net_desks_closedwon'].fillna(0)
sf_df['Sf Net Desk Change'] = sf_df['net_desks_closedwon'] + sf_df['net_desks_closedlost']
sf_df = sf_df[['account_uuid_c', 'Sf Net Desk Change']]

# Merge salesforce table with looker table
comp_df = sf_df.merge(vtrans_df, how='outer', left_on='account_uuid_c', right_on='account_uuid')
comp_df['Sf Net Desk Change']= comp_df['Sf Net Desk Change'].fillna(0)
comp_df['desks_changed']= comp_df['desks_changed'].fillna(0)

comp_df['Sf V-Trans Absolute Difference'] = abs(comp_df['Sf Net Desk Change'] - comp_df['desks_changed'])
comp_df['Sf V-Trans Difference'] = comp_df['Sf Net Desk Change'] - comp_df['desks_changed']

comp_df['account_uuid'] = comp_df['account_uuid'].fillna(comp_df['account_uuid_c'])
comp_df = comp_df[['account_uuid', 'Sf Net Desk Change', 'desks_changed', 'Sf V-Trans Difference', 'Sf V-Trans Absolute Difference']]
comp_df.rename(index=str, columns={"account_uuid": "Account UUID", "desks_changed": "V-Trans Net Desk Change"}, inplace=True)

return_df = comp_df[comp_df['Sf V-Trans Absolute Difference'] != 0]
return_df.to_csv(output_file_destination, encoding='utf-8', index=False)

vtrans_sum = comp_df['V-Trans Net Desk Change'].sum()
sf_sum = comp_df['Sf Net Desk Change'].sum()
sums = [vtrans_sum, sf_sum]
with open(output_file_destination, 'a', newline='') as f:
	fieldnames = ['V-Trans Net Desk Change', 'Sf Net Desk Change']
	writer = csv.writer(f)
	writer.writerow(fieldnames)
	writer.writerow([vtrans_sum, sf_sum])

re_comp_df = re_df.merge(return_df, how='right', left_on='company_uuid', right_on='Account UUID')
re_comp_df.to_csv(reuse_file_destination, encoding='utf-8', index=False)

# sm_df.columns = [sm_df.columns[i]+str(i) for i in range(len(sm_df.columns))]
# re_comp_df = re_comp_df.merge(sm_df, how='left', left_on='Account UUID', right_on='account_uuid14')
# re_comp_df.to_csv(fulloutput_file_destination, encoding='utf-8', index=False)

