--- membership note research ---
select id, created_at, uuid, executed_at, membership_agreement_id, cr.sf_opportunity_id , account_uuid, notes
from spaceman_rest_of_world.change_requests cr
where cr.created_at > '2018-01-01'
and notes is not null;



with notes as (
select date_part(month, cr.created_at) as date, count(id) as id
from spaceman_rest_of_world.change_requests cr
where cr.created_at > '2018-01-01'
and cr.notes is not null
and cr.reservation_type = 'PrimaryReservation'
group by date),
total as (
select date_part(month, cr.created_at) as date, count(id) as id
from spaceman_rest_of_world.change_requests cr
where cr.created_at > '2018-01-01'
and cr.reservation_type = 'PrimaryReservation'
-- and cr.exception_type is not null
group by date)

select total.date, sum(total.id), sum(notes.id)
from total
join notes on notes.date=total.date
group by total.date
order by total.date asc
;


select count(cr.id)
from spaceman_rest_of_world.change_requests cr
where cr.created_at >= '2017-07-01'
and cr.created_at < '2018-01-01'
and cr.reservation_type = 'PrimaryReservation'
and notes is not null;
