
# coding: utf-8

# In[1]:


import pandas as pd


# In[6]:


# Variables:
date_lower_bound = '2018-06-03'
date_upper_bound = '2018-06-10'# Not inclusive 
closed_won_filename = 'cw.xlsx'
closed_lost_filename = 'cl.xlsx'
looker_filename = '6:3-10 looker.csv'


# In[12]:


cw_df = pd.read_excel(closed_won_filename, sheet_name=0, header=11)


# In[13]:


cl_df = pd.read_excel(closed_lost_filename, sheet_name=0, header=13)


# In[30]:


looker_df = pd.read_csv(looker_filename, header=0)


# In[15]:


cw_df = cw_df.drop('Unnamed: 1', 1)
cl_df = cl_df.drop('Unnamed: 1', 1)


# In[16]:


cl_df.drop(cl_df.columns[0:1],axis=1, inplace=True)
cl_df.drop(cl_df.columns[3:10], axis=1, inplace=True)
cl_df.drop(cl_df.columns[4:8], axis=1, inplace=True)
cw_df.drop(cw_df.columns[0:1],axis=1, inplace=True)
cw_df.drop(cw_df.columns[3:10], axis=1, inplace=True)
cw_df.drop(cw_df.columns[4:8], axis=1, inplace=True)


# In[26]:


cw_df = cw_df[(cw_df['Close Date'] >= date_lower_bound) & (cw_df['Close Date'] < date_upper_bound)]
cl_df = cl_df[(cl_df['Close Date'] >= date_lower_bound) & (cl_df['Close Date'] < date_upper_bound)]
cw_df.drop('Close Date', 1)
cl_df.drop('Close Date', 1).head()


# In[27]:


cl_df.groupby(['Account Name', 'UUID']).sum().sort_values(by='Total Desks Reserved (net)').reset_index()
cw_df.groupby(['Account Name', 'UUID']).sum().sort_values(by='No. of Desks (unweighted)', ascending=False).reset_index().head()


# In[28]:


sf_df = cl_df.merge(cw_df, left_on=['UUID', 'Account Name'], right_on=['UUID', 'Account'                                                                                     ' Name'], how='outer')
sf_df['Total Desks Reserved (net)']= sf_df['Total Desks Reserved (net)'].fillna(0)
sf_df['No. of Desks (unweighted)']= sf_df['No. of Desks (unweighted)'].fillna(0)
sf_df['Net Desk Change'] = sf_df['Total Desks Reserved (net)'] + sf_df['No. of Desks (unweighted)']
sf_df.drop(sf_df.columns[[2,4]], axis=1, inplace=True)


# In[33]:


# looker_df = looker_df.drop(['Unnamed: 0', 'Sales Reporting Location Type', 'Sales Reporting Desk Upgrades', 'Sales'\
#                             ' Reporting New Sales', 'Sales Reporting Total Desk Loss', \
#                             'Sales Reporting Total Desk Sales'], 1)


# In[36]:


comp_df = sf_df.merge(looker_df, how='outer', left_on='UUID', right_on='Accounts Account UUID')
comp_df['Net Desk Change']= comp_df['Net Desk Change'].fillna(0)
comp_df['Sales Reporting Net Sales']= comp_df['Sales Reporting Net Sales'].fillna(0)


# In[47]:


comp_df['Absolute Desk Difference'] = abs(comp_df['Net Desk Change'] - comp_df['Sales Reporting Net Sales'])


# In[49]:


comp_df['Absolute Desk Difference'].sum()


# In[52]:


comp_df

