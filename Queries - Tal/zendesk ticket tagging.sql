----- # 1
select listagg("tag",', ')
FROM digital_zendesk.ticket_tag
where ticket_id = 131561;    – ticket_id

----- #2
SELECT "tag",
ticket_id
FROM digital_zendesk.ticket_tag
WHERE ticket_id = 131561;    – ticket_id
