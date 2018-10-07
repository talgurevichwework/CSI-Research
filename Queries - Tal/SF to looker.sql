
# Looker vs Salesforce queries #

with looker as (
select date_part(month, t.date_reserved) as month, --sum(t.desks_changed) as transaction_desks
count(DISTINCT t.account_uuid)
from dw.v_transaction t
where t.date_reserved > '2017-07-01'
and t.desks_changed > 0
group by month
),
salesforce as (
select date_part(month, o.close_date) as month, count(DISTINCT o.account_id)
from salesforce._opportunity o
where o.close_date > '2017-07-01'
and o.stage_name = 'Closed Won'
group by month)

select salesforce.month, salesforce.count as SF, looker.count as Looker, sf-looker
from salesforce
join looker on looker.month=salesforce.month;















;
