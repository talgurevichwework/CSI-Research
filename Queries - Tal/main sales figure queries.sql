
with
leads as(
select date_part(month, l.created_date) month_, count(id) leads
from salesforce_v2.lead l
where l.created_date >='2018-01-01'
and l.created_date < '2018-10-01'
group by date_part(month, l.created_date)
order by date_part(month, l.created_date) ASC
),
opps_open as(
select date_part(month, o.created_date) month_, count(o.id) opps_open--, sum(o.net_desks_c)
from salesforce_v2.opportunity o
where o.created_date >= '2018-01-01'
and o.created_date < '2018-10-01'
group by date_part(month, o.created_date)
order by date_part(month, o.created_date) ASC
),
opps_won as(
select date_part(month, o.created_date) month_, count(o.id)--, sum(o.net_desks_c)
from salesforce_v2.opportunity o
where o.created_date >= '2018-01-01'
and o.created_date < '2018-10-01'
and o.stage_name = 'Closed Won'
group by date_part(month, o.created_date)
order by date_part(month, o.created_date) ASC
),
ma_total as(
select date_part(year, ma.created_at), date_part(month,ma.created_at) month_, count(ma.id) MSAs
from spaceman_public.membership_agreements ma
where ma.created_at >='2018-01-01'
and ma.created_at < '2018-10-01'
--and ma.signed_at is null
group by date_part(year, ma.created_at), date_part(month,ma.created_at)
),
ma_signed as(
select date_part(year, ma.created_at), date_part(month,ma.created_at) month_, count(ma.id) signed
from spaceman_public.membership_agreements ma
where ma.created_at >='2018-01-01'
and ma.created_at < '2018-10-01'
and ma.signed_at is not null
group by date_part(year, ma.created_at), date_part(month,ma.created_at)
),
Tours as (
select date_part(year, t.created_at), date_part(month,t.created_at) month_, count(t.id)
from sales_api_public.tours t
where t.created_at >='2018-01-01'
and t.created_at < '2018-10-01'
group by date_part(year, t.created_at), date_part(month,t.created_at)
)

SELECT l.month_, l.leads, t.count as tours, o.opps_open, ow.count as won, ma_total.MSAs, ma_signed.signed
from leads l
join opps_open o on o.month_=l.month_
join opps_won ow on ow.month_ = l.month_
join ma_total on ma_total.month_=l.month_
join ma_signed on ma_signed.month_=l.month_
join tours t on t.month_=l.month_
;
