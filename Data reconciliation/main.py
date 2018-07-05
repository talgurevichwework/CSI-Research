from we_module.we import We
import queries
we = We(True)
import pandas as pd


# Variables:
start_date = '2018-06-03'
end_date = '2018-06-10'# Not inclusive 
time_period = 'Week'
output_file_destination = '~/Desktop/output.csv'

# Get query results as pandas dfs
looker_df = we.get_tbl_query(queries.create_looker_query(time_period, start_date, end_date))
cw_df = we.get_tbl_query(queries.create_salesforce_closedwon_query(time_period, start_date, end_date))
cl_df = we.get_tbl_query(queries.create_salesforce_closedlost_query(time_period, start_date, end_date))

# Merge closed won and closed lost tables
sf_df = cl_df.merge(cw_df, left_on=['account_uuid_c'], right_on=['account_uuid_c'], how='outer')
sf_df['net_desks_closedlost']= sf_df['net_desks_closedlost'].fillna(0)
sf_df['net_desks_closedwon']= sf_df['net_desks_closedwon'].fillna(0)
sf_df['Sf Net Desk Change'] = sf_df['net_desks_closedwon'] + sf_df['net_desks_closedlost']
sf_df = sf_df[['account_uuid_c', 'Sf Net Desk Change']]

# Merge salesforce table with looker table
comp_df = sf_df.merge(looker_df, how='outer', left_on='account_uuid_c', right_on='accounts_account_uuid')
comp_df['Sf Net Desk Change']= comp_df['Sf Net Desk Change'].fillna(0)
comp_df['new_sales_reporting_net_sales_1']= comp_df['new_sales_reporting_net_sales_1'].fillna(0)

comp_df['Sf Looker Difference'] = comp_df['Sf Net Desk Change'] - comp_df['new_sales_reporting_net_sales_1']
comp_df['Sf Looker Absolute Difference'] = abs(comp_df['Sf Looker Difference'])

comp_df['accounts_account_uuid'] = comp_df['accounts_account_uuid'].fillna(comp_df['account_uuid_c'])
comp_df = comp_df[['accounts_account_uuid', 'Sf Net Desk Change', 'new_sales_reporting_net_sales_1', 'Sf Looker Difference', 'Sf Looker Absolute Difference']]
comp_df.rename(index=str, columns={"accounts_account_uuid": "Account UUID", "new_sales_reporting_net_sales_1": "Looker Net Desk Change"}, inplace=True)

return_df = comp_df[comp_df['Sf Looker Absolute Difference'] != 0]
return_df.to_csv(output_file_destination, encoding='utf-8', index=False)
print(return_df)