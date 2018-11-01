----- # 1
select listagg("tag",', ')
FROM digital_zendesk.ticket_tag
where ticket_id = 131561;    – ticket_id

----- #2
SELECT "tag",
ticket_id
FROM digital_zendesk.ticket_tag
WHERE ticket_id = 131561;    – ticket_id


--hours spent per tag
SELECT "tag", count(tg.ticket_id), avg(EXTRACT(HOURS FROM (t.updated_at - t.created_at))) as diff
FROM digital_zendesk.ticket_tag tg
join digital_zendesk.ticket t on t.id = tg.ticket_id
where t.created_at > '2018-01-01'
and (lower("tag") like ('%enterprise%') or lower("tag") like '%manual%'
group by "tag"
order by count DESC
