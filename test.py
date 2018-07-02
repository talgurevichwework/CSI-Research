
import csv
import re
import pandas
import datetime
import time
import numpy
import os
from we_module.we import We
we = We(True)

memberships = '''
SELECT distinct count(uuid)
from spaceman_public.membership_agreements ma
where ma.created_at > '2018-02-28'
and ma.created_at < '2018-04-01'
'''
ma_ag = we.get_tbl_query(memberships)

print(ma_ag)
print('test')
