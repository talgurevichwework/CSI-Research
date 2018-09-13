# Gets v_transaction records over given time period in normal date format as well as contract uuid from corresponding membership agreement
def create_vtrans_query_notrunc(start_date, end_date):
	return(f'''
with vtrans as (select v.account_name,
		v.account_uuid,
		l.country_code,
		sum(v.desks_changed) as desks_changed,
			case
				when (v.reservable_type='HotDesk' and l.country_code<>'CHN' and l.country_code<>'ARG' and l.country_code<>'COL'
				and l.country_code<>'PER' and l.country_code<>'IND' and l.country_code<>'RUS' and l.country_code<>'CHL' and l.country_code<>'KOR')
			then v.reservation_uuid
			else ma.uuid
			end as contract_uuid
		from dw.v_transaction v
	left join spaceman_public.locations l on l.uuid=v.location_uuid
	left join (select r.uuid, r.id from spaceman_public.reservations r group by r.uuid, r.id) r on r.uuid=v.reservation_uuid
	left join (select cr.reservation_id, cr.membership_agreement_id, cr.reservation_started_on, cr.reservation_ended_on from spaceman_public.change_requests cr
		where cr.executed_at >= DATEADD(day , -1 , '2018-06-01') and cr.executed_at < DATEADD(day, 1, '2018-07-01')
		group by cr.reservation_id, cr.membership_agreement_id, cr.reservation_started_on, cr.reservation_ended_on) cr on cr.reservation_id=r.id
			and (((v.action_type='Transfer In' or v.action_type='Move In') and cr.reservation_started_on is not null) or
			(v.action_type='Transfer Out' or v.action_type='Move Out') and cr.reservation_ended_on is not null)
	left join (select ma.id, ma.uuid from spaceman_public.membership_agreements ma group by ma.id, ma.uuid) ma on ma.id=cr.membership_agreement_id
		where date_reserved_local >=TIMESTAMP '{start_date}' and date_reserved_local <TIMESTAMP '{end_date}'
		group by v.account_name, v.account_uuid, v.reservable_type, v.city, v.reservation_uuid, ma.uuid, l.country_code)
			select account_name, account_uuid, country_code, sum(desks_changed) as desks_changed, contract_uuid
				from vtrans
				group by account_name, account_uuid, contract_uuid, country_code
		''')

# Returns date frame with reservations connected to given reservation uuid
def create_hd_res_query(reservation_uuid):
	return(f'''
			select * from dw.v_transaction v where v.reservation_uuid='{reservation_uuid}'
		''')
