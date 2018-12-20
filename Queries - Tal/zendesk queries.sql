# Zendesk research #

select date(z.created_at) date, count(z.id)
from sf_zendesk.ticket z
where z.created_at > '2017-01-01'
and lower(z.subject) like '%merge%'
or lower(z.subject) like '%merging%'
group by date
order by date asc
;

select *
from sf_zendesk.ticket z
where z.created_at > '2017-01-01';

select date(o.created_date), count(o.id)
from salesforce._opportunity o
where o.merged_on_c is not null
group by date
order by date asc
;


select date_part(month, t.created_at) month_created, count(t.id)
from SF_zendesk.ticket t
where t.created_at > '2018-01-01'
and t.subject like '%missing%'
group by month_created;

;
select distinct t.created_at, t.updated_at
from digital_zendesk.ticket t
where t.created_at >= '2018-01-01'
and t.custom_digital_category = 'enterprise_dig_cat'
and status = 'solved'
;
select distinct *
from digital_zendesk.ticket t
where t.created_at >= '2017-01-01'
and t.custom_digital_category = 'enterprise_dig_cat'
and status = 'solved'
;

SELECT "tag", count(tg.ticket_id), avg(EXTRACT(HOURS FROM (t.updated_at - t.created_at))) as diff, date_part(month, t.created_at) date
FROM digital_zendesk.ticket_tag tg
join digital_zendesk.ticket t on t.id = tg.ticket_id
where t.created_at > '2018-01-01'
and lower("tag") = 'manual_paperwork_ent_cat' -- ('%enterprise%') or lower("tag") like '%manual%') or lower("tag") like '%contract%'
group by "tag", date
order by count DESC

;

select distinct count(t.id), t.custom_root_cause_category as root
from digital_zendesk.ticket t
group by root;
