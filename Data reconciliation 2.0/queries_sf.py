# sf closed lost query with date in data_trunc (i.e Looker) format (combine with sf closed won query to create sfdc report)
def create_salesforce_closed_lost_query(time_period, start_date, end_date):
	return(f'''
		select
			billing.uuid_c,
			sum(opportunities.no_of_desks_unweighted_c) as net_desks_closedlost,
			date_trunc (lower('{time_period}'),
			opportunities.close_date)::date as date
		from salesforce_v2.opportunity as opportunities
		left join (select uuid_c, id
					from salesforce_v2.billing_account_c
					group by uuid_c,id) as billing on opportunities.billing_account_c=billing.id
		where stage_name='Closed Lost' and date_trunc (lower('{time_period}'), opportunities.close_date)::date>=TIMESTAMP '{start_date}' and date_trunc (lower('{time_period}'), opportunities.close_date)::date<TIMESTAMP '{end_date}' and opportunities.total_desks_reserved_net_c<0 and opportunities.region_name_c<>'India'
		group by billing.uuid_c, date_trunc (lower('{time_period}'), opportunities.close_date)
		''')

# sf closed won query with date in data_trunc (i.e Looker) format (combine with sf closed lost query to create sfdc report)
def create_salesforce_closed_won_query(time_period, start_date, end_date):
	return(f'''
	select
		billing.uuid_c,
		sum(opportunities.no_of_desks_unweighted_c) as net_desks_closedwon,
		date_trunc (lower('{time_period}'),
		opportunities.close_date)::date as date
	from salesforce_v2.opportunity as opportunities
	left join (select uuid_c, id
				from salesforce_v2.billing_account_c
				group by uuid_c, id) as billing on opportunities.billing_account_c=billing.id
	where stage_name='Closed Won' and date_trunc (lower('{time_period}'), opportunities.close_date)::date>=TIMESTAMP '{start_date}' and date_trunc (lower('{time_period}'), opportunities.close_date)::date<TIMESTAMP '{end_date}' and (lower(opportunities.contract_type_c) not like '%upgrade%' or opportunities.contract_type_c is null) and opportunities.region_name_c<>'India'
	group by billing.uuid_c, date_trunc (lower('{time_period}'), opportunities.close_date)
		''')

# sf closed lost query with date in normal format
def create_salesforce_closedlost_query_notrunc(start_date, end_date):
	return(f'''
		select
			billing.uuid_c as account_uuid_c,
			billing.name,
			l.country_code,
			opportunities.name as opp_name,
			case
				when (((opportunities.type_c='Hot Desk' and opportunities.type_c is not null) or (opportunities.segment_c='Enterprise Solutions'
					and opportunities.other_lost_reason_c='Hot Desk Contract Canceled New Opportunity' and opportunities.other_lost_reason_c is not null))
				and ((l.country_code<>'CHN' and l.country_code<>'ARG' and l.country_code<>'COL'
					and l.country_code<>'PER' and l.country_code<>'IND' and l.country_code<>'RUS' and l.country_code<>'CHL' and l.country_code<>'KOR') or l.country_code is null))
				then opportunities.reservation_uuid_c
				else opportunities.contract_uuid_c
			end as contract_uuid_c,
			sum(opportunities.total_desks_reserved_net_c) as net_desks_closedlost
		from salesforce_v2.opportunity as opportunities
		left join spaceman_public.locations l on l.uuid=opportunities.building_uuid_c
		left join (select
					uuid_c,
					id,
					name
					from salesforce_v2.billing_account_c
					group by name, uuid_c, id) as billing on opportunities.billing_account_c=billing.id
		where stage_name='Closed Lost' and opportunities.close_date >= TIMESTAMP '{start_date}' and opportunities.close_date < TIMESTAMP '{end_date}' and opportunities.total_desks_reserved_net_c < 0
		group by
			billing.uuid_c,
			opportunities.contract_uuid_c,
			opportunities.type_c,
			reservation_uuid_c,
			opportunities.portfolio_name_c,
			opportunities.region_name_c,
			l.country_code,
			billing.name,
			opportunities.other_lost_reason_c, opportunities.segment_c, opportunities.name
		''')

# sf closed won query with date in normal format
def create_salesforce_closedwon_query_notrunc(start_date, end_date):
	return(f'''
		select billing.uuid_c as account_uuid_c,
		billing.name,
		l.country_code,
		opportunities.name as opp_name,
		case
			when (opportunities.type_c='Hot Desk' and opportunities.type_c is not null and ((l.country_code<>'CHN' and l.country_code<>'ARG' and l.country_code<>'COL'
				and l.country_code<>'PER' and l.country_code<>'IND' and l.country_code<>'RUS' and l.country_code<>'CHL' and l.country_code<>'KOR') or l.country_code is null))
			then opportunities.reservation_uuid_c
			else opportunities.contract_uuid_c
		end as contract_uuid_c,
		sum(opportunities.no_of_desks_unweighted_c) as net_desks_closedwon
		from salesforce_v2.opportunity as opportunities
		left join spaceman_public.locations l on l.uuid=opportunities.building_uuid_c
		left join (select uuid_c, id, name from salesforce_v2.billing_account_c group by name, uuid_c, id) as billing on opportunities.billing_account_c=billing.id
		where stage_name='Closed Won' and opportunities.close_date >= TIMESTAMP '{start_date}' and opportunities.close_date < TIMESTAMP '{end_date}' and (lower(opportunities.contract_type_c) not like '%downgrade%' or opportunities.contract_type_c is null)
		group by
			billing.uuid_c,
			opportunities.contract_uuid_c,
			opportunities.type_c,
			reservation_uuid_c,
			opportunities.portfolio_name_c,
			opportunities.region_name_c,
			l.country_code,
			billing.name,
			opportunities.name
		''')


# Returns date frame with opportunities connected to given reservation uuid
def create_hd_opp_query(reservation_uuid, move_type):
	stage = 'Closed Lost' if move_type == 'moveout' else 'Closed Won'
	return(f'''
			select o.reservation_uuid_c, o.name, o.region_name_c, o.territory_name_c, o.building_city_c, o.no_of_desks_unweighted_c, o.total_desks_reserved_net_c, o.close_date, o.stage_name
			from salesforce_v2.opportunity o
			where o.reservation_uuid_c='{reservation_uuid}' and o.stage_name='{stage}'
		''')
