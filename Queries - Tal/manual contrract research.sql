
-- select all accounts that ended signing with manual option
select count(a.id), pm.payment_method
from spaceman_public.payment_methods pm
join spaceman_public.accounts a on a.id=pm.account_id
where pm.created_at >= '2018-06-01'
and pm.created_at < '2018-07-01'
and a.created_at > '2018-06-01'
group by pm.payment_method;

select * -- t.subject, t.description, t.type, t.status, u.name, t.created_at created, t.updated_at updated, t. datediff(hour, created, updated)
from digital_zendesk.ticket t
join digital_zendesk.user u on u.id = t.assignee_id
where u.name = 'Hannah Plimack'
and (lower(subject) like '%agreement%' or lower(subject) like '%manual%' or lower(subject) like '%contract%');
