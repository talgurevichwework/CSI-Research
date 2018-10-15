--opps by type
select date_part(month, o.created_date) month_, count(o.id) opps, o.record_type_id, r.name

from salesforce_v2.opportunity o
join salesforce_v2.record_type r on r.id=o.record_type_id

where o.created_date >= '2018-01-01'
and o.created_date < '2018-10-01'

group by date_part(month, o.created_date), o.record_type_id, r.name
order by date_part(month, o.created_date) ASC

-----

-- desks closed by type


select date_part(month, o.created_date) month_, sum(o.no_of_desks_unweighted_c) opps, o.record_type_id, r.name

from salesforce_v2.opportunity o
join salesforce_v2.record_type r on r.id=o.record_type_id

where o.created_date >= '2018-01-01'
and o.created_date < '2018-10-01'
and o.stage_name = 'Closed Won'

group by date_part(month, o.created_date), o.record_type_id, r.name
order by date_part(month, o.created_date) ASC
