with executed as(
select ma.created_at, ma.id, ma.status
from spaceman_public.reservations r
join spaceman_public.change_requests cr on cr.reservation_id = r.id
join spaceman_public.membership_agreements ma on ma.id = cr.membership_agreement_id
where r.description = 'Global Access'
and ma.status = 'executed'
and r.created_at >= '2018-01-01' ),
 sent as (
select ma.created_at, ma.id, ma.status
from spaceman_public.reservations r
join spaceman_public.change_requests cr on cr.reservation_id = r.id
join spaceman_public.membership_agreements ma on ma.id = cr.membership_agreement_id
where r.description = 'Global Access'
and ma.status = 'sent'
and r.created_at >= '2018-01-01')

select executed.id
from executed
join sent on sent.id = executed.id;
;
select date_part(month, ma.created_at) as datepart, count(ma.id), ma.status
from spaceman_public.reservations r
join spaceman_public.change_requests cr on cr.reservation_id = r.id
join spaceman_public.membership_agreements ma on ma.id = cr.membership_agreement_id
where r.description = 'Global Access'
--and ma.status = 'executed'
and r.created_at >= '2018-01-01'
group by datepart, ma.status
order by datepart ASC;
