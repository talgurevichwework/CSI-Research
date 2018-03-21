#!/usr/bin/env python

from we_module.we import We
we = We(True)
import csv
import re
import pandas
import datetime
import time
import numpy
import os

# test commit message
# opportunities table
opportunities ='''
SELECT o.created_date, o.contract_signed_on_c, o.contract__sent__date___c, o.id, o.account_id, o.name, o.owner_id, a.uuid___c, o.contract_uuid_c
from salesforce._opportunity o
join salesforce._account a on a.id = o.account_id
where o.contract_signed_on_c > '2017-12-31'
and o.contract_signed_on_c < '2018-02-01'
'''
opp = we.get_tbl_query(opportunities)
opp.to_csv('opportunities_output.csv')

#memberships table
memberships = '''
SELECT *
from spaceman_public.membership_agreements ma
where ma.signed_at > '2017-12-31'
and ma.signed_at < '2018-02-01'
'''
ma_ag = we.get_tbl_query(memberships)
ma_ag.to_csv('memberships_output.csv')

#transations table (the looker table)
transations = '''
SELECT *
from dw.v_transaction v
where v.date_reserved_local > '2017-12-31'
and  v.date_reserved_local< '2018-02-01'
'''
trans = we.get_tbl_query(transations)
trans.to_csv('transations.csv')

# reservations table
reservations = '''
SELECT *
from spaceman_public.reservations r
where date(r.created_at) > '2017-12-31'
and date(r.created_at) < '2018-02-01'
'''
res = we.get_tbl_query(reservations)
res.to_csv('reservations_output.csv')

#spaceman account
spaceman_account = '''
SELECT *
from spaceman_public.accounts a
where a.updated_at > '2017-12-31'
and a.updated_at < '2018-02-01'
'''
space_accounts = we.get_tbl_query(spaceman_account)
space_accounts.to_csv('SMAccounts_output.csv')


no_sent=opp[opp['contract_sent_date_c'].isnull()] #all opps with no sent date for contract
no_contract = opp[opp['contract_uuid_c'].isnull()] #all opps with no contract uuid
no_signed= opp[opp['contract_signed_on_c'].isnull()] #all opps with no signed date

#extract opp accounts and transation accounts into sets
a=set(opp['uuid_c'])
b=set(trans['account_uuid'])
#find all accounts in opps but no i looker
c=a.difference(b)
print(len(c), 'accounts are missing from looker this timeframe')
for n in c:
    #run on each account, find if it is in any of the above variables (of no sent, no contract, or no signed)
    #extract the table to a new file

#search them for opportunities with no send, or contract or sign date
#find all account in looker that are not in SF tables
#look for account in SF, find recent opps, try to match?
