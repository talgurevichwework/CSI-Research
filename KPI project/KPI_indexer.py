from we_module.we import We
we = We(True)
import csv
import re
import pandas
import datetime
import time
import numpy
import os

# opening unique companies with contract sync error file from running log_vs_contract.py file
with open('unique_contracts.csv', 'r') as contracts:
    error_contracts = 0
    for row in contracts:
        error_contracts = error_contracts +1

# SQL find all spaceman accounts with contracts that month
memberships = '''
SELECT distinct count(uuid)
from spaceman_public.membership_agreements ma
where ma.created_at > '2018-02-28'
and ma.created_at < '2018-04-01'
'''
ma_ag = we.get_tbl_query(memberships)
#divide this number by the length of unbique companies to get the KPI


print('contracts created during this time:', ma_ag)
print('sync errors during this time:', error_contracts)
print('ratio:', error_contracts / ma_ag *100, '%')
