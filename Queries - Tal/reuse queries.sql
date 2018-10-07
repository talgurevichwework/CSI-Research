
---- research on  ----
select r.company_uuid, r.contract_event_type, r.contract_event_params, r.sf_response, r.step_found, t.name
from sales_api_public.opportunity_reuse_records r
join salesforce._account a on a.uuid___c = r.company_uuid
join salesforce._record_type t on t.id = a.record_type_id
where r.created_at >= '2018-08-01'
and r.created_at <= '2018-08-05'
--and r.opportunity_id_found is null
--and r.contract_event_type not in ('Contract Canceled', 'Contract Discarded', 'Contract Voided', 'Cancel Moveout', 'Contract Sent')
--and t.name not in ('Consumer')
--and r.sf_response not like '%Update%'
--and r.sf_response not like '%New Opportunity%'
--limit 1000;
;

--Yonah's Queries for reuse:
/*	1.	Salesforce creates a new opportunity and we update an existing opportunity
	2.	Salesforce updates an existing opportunity and we create a new opportunity
	3.	Salesforce updates one opportunity and we update a different opportunity */
--1.--
select * from sales_api_public.opportunity_reuse_records o where o.sf_response like '%New Opportunity :%' and o.opportunity_id_found is not null
--2.--
select * from sales_api_public.opportunity_reuse_records o where o.sf_response like '%Update Opportunity :%' and o.opportunity_id_found is null
--3.--
select * from sales_api_public.opportunity_reuse_records o where o.sf_response like '%Update Opportunity :%' and o.sf_response not like '%' + o.opportunity_id_found + '%' and o.opportunity_id_found is not null
-----------------------
select * from sales_api_public.opportunity_reuse_records r where r.opportunity_id_found is null and r.contract_event_type = 'Contract Signed' and r.company_uuid = '7de32cd0-26bb-418a-a2b8-75c268f0abd6'
