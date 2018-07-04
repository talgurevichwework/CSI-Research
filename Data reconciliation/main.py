from we_module.we import We
import queries
we = We(True)
import pandas as pd


# Variables:
date_lower_bound = '2018-06-03'
date_upper_bound = '2018-06-10'# Not inclusive 
time_period = 'Week'

# Get query results as pandas dfs
cw_df = we.get_tbl_query(queries.create_salesforce_closedwon_query(time_period, start_date, end_date))
cl_df = we.get_tbl_query(queries.create_salesforce_closedlost_query(time_period, start_date, end_date))

sf_df = cl_df.merge(cw_df, left_on=['account_uuid_c', 'close_date'], right_on=['account_uuid_c', 'close_date'], how='outer')
sf_df['net_desks_closedlost']= sf_df['net_desks_closedlost'].fillna(0)
sf_df['net_desks_closedwon']= sf_df['net_desks_closedwon'].fillna(0)
sf_df['Net Desk Change'] = sf_df['net_desks_closedwon'] + sf_df['net_desks_closedlost']

sf_df = sf_df[['account_uuid_c', 'close_date', 'Net Desk Change']]






sf_df = cl_df.merge(cw_df, left_on=['UUID', 'Account Name'], right_on=['UUID', 'Account Name'], how='outer')
sf_df['Total Desks Reserved (net)']= sf_df['Total Desks Reserved (net)'].fillna(0)
sf_df['No. of Desks (unweighted)']= sf_df['No. of Desks (unweighted)'].fillna(0)
sf_df['Net Desk Change'] = sf_df['Total Desks Reserved (net)'] + sf_df['No. of Desks (unweighted)']
sf_df.drop(sf_df.columns[[2,4]], axis=1, inplace=True)

# looker_df = looker_df.drop(['Unnamed: 0', 'Sales Reporting Location Type', 'Sales Reporting Desk Upgrades', 'Sales'\
#                             ' Reporting New Sales', 'Sales Reporting Total Desk Loss', \
#                             'Sales Reporting Total Desk Sales'], 1)

comp_df = sf_df.merge(looker_df, how='outer', left_on='account_uuid_c', right_on='accounts_account_uuid')
comp_df['Net Desk Change']= comp_df['Net Desk Change'].fillna(0)
comp_df['new_sales_reporting_net_sales_1']= comp_df['new_sales_reporting_net_sales_1'].fillna(0)

comp_df['Sf Looker Absolute Difference'] = abs(comp_df['Net Desk Change'] - comp_df['new_sales_reporting_net_sales_1'])

comp_df['accounts_account_uuid'] = comp_df['accounts_account_uuid'].fillna(comp_df['account_uuid_c'])
comp_df['close_date_x'] = comp_df['close_date_x'].fillna(comp_df['close_date_y'])

comp_df = comp_df[['accounts_account_uuid', 'close_date_x', 'Net Desk Change', 'new_sales_reporting_net_sales_1', 'Sf Looker Absolute Difference']]
comp_df.rename(index=str, columns={"accounts_account_uuid": "Account UUID","close_date_x": "Close Date", "Net Desk Change": "SF Net Desk Change", 'new_sales_reporting_net_sales_1':"Looker Net Desk Change"}, inplace=True)

return_df = comp_df[comp_df['Sf Looker Absolute Difference'] != 0]
return_df
