import pandas as pd

# Variables:
date_lower_bound = '2018-06-03'
date_upper_bound = '2018-06-10'# Not inclusive 
closed_won_filename = 'cw.xlsx'
closed_lost_filename = 'cl.xlsx'
looker_filename = '6:3-10 looker.csv'

cw_df = pd.read_excel(closed_won_filename, sheet_name=0, header=11)

cl_df = pd.read_excel(closed_lost_filename, sheet_name=0, header=13)

looker_df = pd.read_csv(looker_filename, header=0)

cw_df = cw_df.drop('Unnamed: 1', 1)
cl_df = cl_df.drop('Unnamed: 1', 1)

cl_df.drop(cl_df.columns[0:1],axis=1, inplace=True)
cl_df.drop(cl_df.columns[3:10], axis=1, inplace=True)
cl_df.drop(cl_df.columns[4:8], axis=1, inplace=True)
cw_df.drop(cw_df.columns[0:1],axis=1, inplace=True)
cw_df.drop(cw_df.columns[3:10], axis=1, inplace=True)
cw_df.drop(cw_df.columns[4:8], axis=1, inplace=True)

cw_df = cw_df[(cw_df['Close Date'] >= date_lower_bound) & (cw_df['Close Date'] < date_upper_bound)]
cl_df = cl_df[(cl_df['Close Date'] >= date_lower_bound) & (cl_df['Close Date'] < date_upper_bound)]
cw_df.drop('Close Date', 1)
cl_df.drop('Close Date', 1).head()

cl_df.groupby(['Account Name', 'UUID']).sum().sort_values(by='Total Desks Reserved (net)').reset_index()
cw_df.groupby(['Account Name', 'UUID']).sum().sort_values(by='No. of Desks (unweighted)', ascending=False).reset_index().head()

sf_df = cl_df.merge(cw_df, left_on=['UUID', 'Account Name'], right_on=['UUID', 'Account'                                                                                     ' Name'], how='outer')
sf_df['Total Desks Reserved (net)']= sf_df['Total Desks Reserved (net)'].fillna(0)
sf_df['No. of Desks (unweighted)']= sf_df['No. of Desks (unweighted)'].fillna(0)
sf_df['Net Desk Change'] = sf_df['Total Desks Reserved (net)'] + sf_df['No. of Desks (unweighted)']
sf_df.drop(sf_df.columns[[2,4]], axis=1, inplace=True)

# looker_df = looker_df.drop(['Unnamed: 0', 'Sales Reporting Location Type', 'Sales Reporting Desk Upgrades', 'Sales'\
#                             ' Reporting New Sales', 'Sales Reporting Total Desk Loss', \
#                             'Sales Reporting Total Desk Sales'], 1)

comp_df = sf_df.merge(looker_df, how='outer', left_on='UUID', right_on='Accounts Account UUID')
comp_df['Net Desk Change']= comp_df['Net Desk Change'].fillna(0)
comp_df['Sales Reporting Net Sales']= comp_df['Sales Reporting Net Sales'].fillna(0)

comp_df['Sf Looker Absolute Difference'] = abs(comp_df['Net Desk Change'] - comp_df['Sales Reporting Net Sales'])

comp_df['Sf Looker Absolute Difference'].sum()
comp_df['UUID'] = comp_df['UUID'].fillna(comp_df['Accounts Account UUID'])

comp_df = comp_df[['Account Name', 'UUID', 'Close Date_x', 'Net Desk Change', 'Sales Reporting Net Sales',                    'Sf Looker Absolute Difference']]
comp_df.rename(index=str, columns={"Close Date_x": "Close Date", "Net Desk Change": "SF Net Desk Change",                                  'Sales Reporting Net Sales':"Looker Net Desk Change"}, inplace=True)

return_df = comp_df[comp_df['Sf Looker Absolute Difference'] != 0]
return_df
