# Gets reuse logic records over given time period in data_trunc format
def create_sapi_reuserecords_query_notrunc(start_date, end_date):
	return(f'''
		select *
		from sales_api_public.opportunity_reuse_records as opr
		where opr.created_at >= TIMESTAMP '{start_date}' and opr.created_at < TIMESTAMP '{end_date}'
	''')
