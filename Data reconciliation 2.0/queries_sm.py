# Gets reservations, change_requests, membership_agreements over time period in data_trunc format
def create_spaceman_r_cr_ma_query(time_period, start_date, end_date):
	return(f'''
		with ma as (
			select *
			from spaceman_public.membership_agreements ma),
		r as (
			select *
			from spaceman_public.reservations r),
		cr as (
			select *
			from spaceman_public.change_requests cr)
		select cr.account_uuid as account_uuid,
			ma.created_at as ma_created,
			cr.created_at as cr_created,
			r.created_at as reservation_created,
			r.uuid as reservation_uuid,
			ma.uuid as ma_uuid,
			cr.sf_opportunity_id,
			ma.signed_at,
			cr.reservation_started_on,
			cr.reservation_ended_on,
			r.description as reservable
		from cr
		full join ma on ma.id = cr.membership_agreement_id
		full join r on r.id = cr.reservation_id
		where date_trunc(lower('{time_period}'), ma.created_at)::date>=TIMESTAMP '{start_date}' and date_trunc (lower('{time_period}'), ma.created_at)::date<TIMESTAMP '{end_date}'
		and cr.reservation_type = 'PrimaryReservation'
		''')
