select date_part('year', o.created_date) as year, date_part('month', o.created_date) as month, count(o.id), t.name as deal_type, o.type_c as product_type, avg(EXTRACT(DAYS FROM (o.Close_date - o.created_date))) as avg_duration
from salesforce_v2.opportunity o
join salesforce_v2.record_type t on t.id = o.record_type_id
where o.stage_name = 'Closed Won'
and o.created_date > '2017-01-01'
group by year, month, type_c, t.name
order by year, month ASC;
