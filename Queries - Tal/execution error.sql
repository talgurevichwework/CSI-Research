---- execution errors --
select count(e.id)
from spaceman_public.membership_agreement_executions e
where e.requests_executed is null
and e.created_at > '2018-01-01'
and e.created_at < '2018-06-01'
;

select count(e.id)
from spaceman_public.membership_agreement_executions e
where e.requests_executed is null
and e.created_at > '2018-01-01'
and e.created_at < '2018-06-01'
;
