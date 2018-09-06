# sf closed lost query with date in data_trunc (i.e Looker) format (combine with sf closed won query to create sfdc report)
def create_salesforce_closed_lost_query(time_period, start_date, end_date):
	return(f'''
		select
			accounts.uuid_c,
			sum(opportunities.no_of_desks_unweighted_c) as net_desks_closedwon,
			date_trunc (lower('{time_period}'),
			opportunities.close_date)::date as date
		from salesforce_v2.opportunity as opportunities
		left join (select uuid_c
					from salesforce_v2.billing_account_c
					group by uuid_c, parent_account_c) as accounts on opportunities.billing_account_c=accounts.id
		where stage_name='Closed Lost' and date_trunc (lower('{time_period}'), opportunities.close_date)::date>=TIMESTAMP '{start_date}' and date_trunc (lower('{time_period}'), opportunities.close_date)::date<TIMESTAMP '{end_date}' and (lower(opportunities.contract_type_c) not like '%downgrade%' or opportunities.contract_type_c is null) and opportunities.region_name_c<>'India'
		group by accounts.parent_account_c, date_trunc (lower('{time_period}'), opportunities.close_date)
		''')

# sf closed won query with date in data_trunc (i.e Looker) format (combine with sf closed lost query to create sfdc report)
def create_salesforce_closed_won_query(time_period, start_date, end_date):
	return(f'''
		select
			accounts.uuid_c,
			sum(opportunities.no_of_desks_unweighted_c) as net_desks_closedwon,
			date_trunc (lower('{time_period}'),
			opportunities.close_date)::date as date
		from salesforce_v2.opportunity as opportunities
		left join (select uuid_c
					from salesforce_v2.billing_account_c
					group by uuid_c, parent_account_c) as accounts on opportunities.billing_account_c=accounts.id
		where stage_name='Closed Won' and date_trunc (lower('{time_period}'), opportunities.close_date)::date>=TIMESTAMP '{start_date}' and date_trunc (lower('{time_period}'), opportunities.close_date)::date<TIMESTAMP '{end_date}' and (lower(opportunities.contract_type_c) not like '%downgrade%' or opportunities.contract_type_c is null) and opportunities.region_name_c<>'India'
		group by accounts.parent_account_c, date_trunc (lower('{time_period}'), opportunities.close_date)
		''')
