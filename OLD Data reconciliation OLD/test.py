from we_module.we import We
import queries
we = We(True)
import pandas as pd
import csv

# Variables:
start_date = '2018-08-01'
end_date = '2018-09-01'# Not inclusive
time_period = 'Day'
output_file_destination = f'./Reports/looker_output{start_date}to{end_date}.csv'
reuse_file_destination = f'./Reports/looker_reuse{start_date}to{end_date}.csv'
fulloutput_file_destination = f'./Reports/looker_fulloutput{start_date}to{end_date}.csv'
printoutput_file_destination = f'./Reports/looker_printoutput{start_date}to{end_date}.txt'
test = f'./Reports/test{start_date}to{end_date}.csv'

# Get query results as pandas dfs
#looker_df = we.get_tbl_query(queries.create_looker_query(time_period, start_date, end_date))
cw_df = we.get_tbl_query(queries_sf.create_salesforce_closed_won_query(time_period, start_date, end_date))
#cl_df = we.get_tbl_query(queries.create_salesforce_closedlost_query(time_period, start_date, end_date))
#re_df = we.get_tbl_query(queries.create_sapi_reuserecords_query(time_period, start_date, end_date))
#sm_df = we.get_tbl_query(queries.create_spaceman_r_cr_ma_query(time_period, start_date, end_date))
#org_df = we.get_tbl_query(queries.create_orgs_from_billing(start_date, end_date))

cw_df.to_csv(test, encoding='utf-8', index=False)
