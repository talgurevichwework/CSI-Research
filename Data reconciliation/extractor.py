import string
import csv
from we_module.we import We
we = We(True)
import re
import pandas
import datetime
import time
import os

startdate = '2018-06-01'
enddate = '2018-06-03'
sf_won = '''
SELECT * from salesforce._opportunity o where o.stage_name = 'Closed Won' and o.close_date >= 'startsdate' and o.close_date < 'enddate'
'''
won_opps = we.get_tbl_query(sf_won)
