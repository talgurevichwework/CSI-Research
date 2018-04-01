from we_module.we import We
we = We(True)
import csv
import re
import pandas
import datetime
import time
import numpy
import os

# contract sync error file from running log_vs_contract.py file
with open('unique_contracts.csv', 'r') as contracts:
    error_contracts = 0
    for row in contracts:
        error_contracts = error_contracts +1

# SQL find all agreements on time period
memberships = '''
SELECT distinct count(uuid)
from spaceman_public.membership_agreements ma
where ma.created_at > '2018-02-28'
and ma.created_at < '2018-04-01'
'''
ma_ag = we.get_tbl_query(memberships)

print('contracts created during this time:', ma_ag)
print('sync errors during this time:', error_contracts)
print('ratio:', error_contracts / ma_ag *100, '%')
