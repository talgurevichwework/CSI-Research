from we_module.we import We
import queries
we = We(True)
import pandas as pd
import csv
import label_sync_issue as lsi

# Variables:
start_date = '2018-06-12'
end_date = '2018-06-13'# Not inclusive
start_date_nextmonth = '2018-07-12'
end_date_nextmonth = '2018-07-13'
output_file_destination = f'./Reports/output{start_date}to{end_date}2.csv'
reuse_file_destination = f'./Reports/reuse{start_date}to{end_date}2.csv'
fulloutput_file_destination = f'./Reports/fulloutput{start_date}to{end_date}2.csv'

# Get query results as pandas dfs
vtrans_df = we.get_tbl_query(queries.create_vtrans_query_notrunc(start_date, end_date))
cw_df = we.get_tbl_query(queries.create_salesforce_closedwon_query_notrunc(start_date, end_date))
cl_df = we.get_tbl_query(queries.create_salesforce_closedlost_query_notrunc(start_date, end_date))
cl_nextmonth_df = we.get_tbl_query(f'''select o.reservation_uuid_c, o.total_desks_reserved_net_c, o.close_date 
	from salesforce_v2.opportunity o 
	where o.close_date >= TIMESTAMP '{start_date_nextmonth}' and o.close_date < TIMESTAMP '{end_date_nextmonth}' 
	''')
re_df = we.get_tbl_query(queries.create_sapi_reuserecords_query_notrunc(start_date, end_date))

# Merge closed won and closed lost tables
sf_df = cl_df.merge(cw_df, left_on=['contract_uuid_c'], right_on=['contract_uuid_c'], how='outer')
sf_df['net_desks_closedlost']= sf_df['net_desks_closedlost'].fillna(0)
sf_df['net_desks_closedwon']= sf_df['net_desks_closedwon'].fillna(0)
sf_df['Sf Net Desk Change'] = sf_df['net_desks_closedwon'] + sf_df['net_desks_closedlost']

sf_df['account_uuid_c_x'] = sf_df['account_uuid_c_x'].fillna(sf_df['account_uuid_c_y'])
sf_df['country_code_x'] = sf_df['country_code_x'].fillna(sf_df['country_code_y'])
sf_df['name_x'] = sf_df['name_x'].fillna(sf_df['name_y'])

sf_df = sf_df[['country_code_x', 'name_x', 'account_uuid_c_x', 'contract_uuid_c', 'Sf Net Desk Change']]
sf_df = sf_df.rename(index=str, columns={'name_x': 'name_c', 'account_uuid_c_x': 'account_uuid_c', 'country_code_x': 'country_code_c'})

sf_df['contract_uuid_c'] = sf_df['contract_uuid_c'].fillna('')
sf_df['country_code_c'] = sf_df['country_code_c'].fillna('')
sf_df = sf_df.groupby(['name_c', 'account_uuid_c', 'country_code_c', 'contract_uuid_c']).sum().reset_index()

# Get comparison table between sf and vtrans
comp_df = sf_df.merge(vtrans_df, how='outer', left_on='contract_uuid_c', right_on='contract_uuid')
comp_df['Sf Net Desk Change']= comp_df['Sf Net Desk Change'].fillna(0)
comp_df['desks_changed']= comp_df['desks_changed'].fillna(0)

comp_df['Sf Vtrans Difference'] = comp_df['Sf Net Desk Change'] - comp_df['desks_changed']
comp_df['Sf Vtrans Absolute Difference'] = abs(comp_df['Sf Vtrans Difference'])

comp_df['account_name'] = comp_df['account_name'].fillna(comp_df['name_c'])
comp_df['account_uuid'] = comp_df['account_uuid'].fillna(comp_df['account_uuid_c'])
comp_df['contract_uuid'] = comp_df['contract_uuid'].fillna(comp_df['contract_uuid_c'])
comp_df['country_code'] = comp_df['country_code'].fillna(comp_df['country_code_c'])

comp_df = comp_df[['account_name', 'account_uuid', 'country_code', 'contract_uuid', 'Sf Net Desk Change', 'desks_changed', 'Sf Vtrans Difference', 'Sf Vtrans Absolute Difference']]
comp_df = comp_df.rename(index=str, columns={"account_name": "Account Name","account_uuid": "Account UUID", "country_code": "Country Code", "contract_uuid": "Contract UUID", "desks_changed": "Vtrans Net Desk Change"})
return_df = comp_df[comp_df['Sf Vtrans Absolute Difference'] != 0]
return_df['Sync Issue'] = ""

# ==============================================================================================Sync Error Logic===========================================================================================================
return_df['Sync Issue'] = return_df.apply (lambda row: lsi.label_sync_issue (row, vtrans_df, cl_nextmonth_df),axis=1)

# =========================================================================================================================================================================================================
return_df.to_csv(output_file_destination, encoding='utf-8', index=False)
