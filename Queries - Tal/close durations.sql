
----- close duration by account segment ----
select ma.created_at, ma.signed_at, a.name, a.record_type_id, r.name
from spaceman_public.membership_agreements ma
join salesforce._account a on a.uuid___c = ma.account_uuid
join salesforce.record_type r on r.id = a.record_type_id
where ma.created_at >= '2018-01-01'
and signed_at is not null
