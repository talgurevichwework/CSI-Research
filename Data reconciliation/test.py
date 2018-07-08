from we_module.we import We
import queries
we = We(True)
# s = '\'2018-03-28\''
# memberships = f''' SELECT * from spaceman_public.membership_agreements ma where ma.created_at > {s} and ma.created_at < '2018-04-01' '''
# ma_ag = we.get_tbl_query(memberships)
# print(memberships)
time_period = 'Week'
start_date = '2018-06-03'
end_date = '2018-06-10'
ma_ag = we.get_tbl_query(queries.create_salesforce_closedwon_query(time_period, start_date, end_date))
print(ma_ag)