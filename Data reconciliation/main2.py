from we_module.we import We
import queries
we = We(True)
import pandas as pd
import csv

# Variables:
start_date = '2018-06-03'
end_date = '2018-06-10'# Not inclusive
output_file_destination = f'./Reports/output{start_date}to{end_date}.csv'
reuse_file_destination = f'./Reports/reuse{start_date}to{end_date}.csv'
fulloutput_file_destination = f'./Reports/fulloutput{start_date}to{end_date}.csv'

# Get query results as pandas dfs
vtrans_df = we.get_tbl_query(queries.create_vtrans_query_notrunc(start_date, end_date))
cw_df = we.get_tbl_query(queries.create_salesforce_closedwon_query_notrunc(start_date, end_date))
cl_df = we.get_tbl_query(queries.create_salesforce_closedlost_query_notrunc(start_date, end_date))
re_df = we.get_tbl_query(queries.create_sapi_reuserecords_query_notrunc(start_date, end_date))

# Merge closed won and closed lost tables
sf_df = cl_df.merge(cw_df, left_on=['contract_uuid_c'], right_on=['contract_uuid_c'], how='outer')
sf_df['net_desks_closedlost']= sf_df['net_desks_closedlost'].fillna(0)
sf_df['net_desks_closedwon']= sf_df['net_desks_closedwon'].fillna(0)
sf_df['Sf Net Desk Change'] = sf_df['net_desks_closedwon'] + sf_df['net_desks_closedlost']

sf_df['account_uuid_c_x'] = sf_df['account_uuid_c_x'].fillna(sf_df['account_uuid_c_y'])
sf_df = sf_df[['account_uuid_c_x', 'contract_uuid_c', 'Sf Net Desk Change']]
sf_df = sf_df.rename(index=str, columns={'account_uuid_c_x': 'account_uuid_c'})

sf_df = sf_df.groupby(['account_uuid_c','contract_uuid_c']).sum().reset_index()

# Get comparison table between sf and vtrans
comp_df = sf_df.merge(vtrans_df, how='outer', left_on='contract_uuid_c', right_on='contract_uuid')
comp_df['Sf Net Desk Change']= comp_df['Sf Net Desk Change'].fillna(0)
comp_df['desks_changed']= comp_df['desks_changed'].fillna(0)

comp_df['Sf Looker Difference'] = comp_df['Sf Net Desk Change'] - comp_df['desks_changed']
comp_df['Sf Looker Absolute Difference'] = abs(comp_df['Sf Looker Difference'])

comp_df['account_uuid'] = comp_df['account_uuid'].fillna(comp_df['account_uuid_c'])
comp_df['contract_uuid'] = comp_df['contract_uuid'].fillna(comp_df['contract_uuid_c'])

comp_df = comp_df[['account_uuid', 'contract_uuid', 'Sf Net Desk Change', 'desks_changed', 'Sf Looker Difference', 'Sf Looker Absolute Difference']]
comp_df = comp_df.rename(index=str, columns={"account_uuid": "Account UUID", "contract_uuid": "Contract UUID", "desks_changed": "Looker Net Desk Change"})