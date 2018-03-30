#this is a KPI effort to establish benchmark between log failures of contracts to membership agreement numbers in a given time timeframe
# from we_module.we import We
# we = We(True)
import csv
import re
import pandas
import datetime
import time
import numpy
import os

#tiding the log file exported from leg entries, assuming it is filtered for a relevant time frame and "Failed sending Contract event"
logfile = open('/Users/tgurevich/Downloads/file.txt','r')
for row in logfile:
    a=str.find(row, 'Failed sending Contract event to SF with')
    failed_note=row[:a]
    b=str.find(row,'{')
    c=str.find(row,'}')
    payload=row[b+1:c]
    d=str.find(row, 'exception')
    exception=row[d+9:]
# print(failed_note)
# print('-----------')
# print(payload)
# print('-----------')
# print(exception)
