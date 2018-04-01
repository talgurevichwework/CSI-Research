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

#borrowed code for text clean up
def clean_up(text, strip_chars=[], replace_extras={}):
    """
    :type text str
    :type strip_chars list
    :type replace_extras dict
    *************************
    strip_chars: optional arg
    Accepts passed list of string objects to iter through.
    Each item, if found at beginning or end of string, will be
    gotten rid of.
    example:
    text input: '       ,  ,      , .,.,.,.,,,......test, \t  this\n.is.a\n.test...,,,         , .'
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^------^^^^----^^-----^^-----^^^^^^^^^^^^^^^^^^
    strip_chars arg: [',', '.']
    output: 'test, this .is.a .test'
    *************************
    replace_extras: optional arg
    Accepts passed dict of items to replace in the standard
    clean_up_items dict or append to it.
    example:
    text_input: ' this is one test\n!\n'
                 ^--------^^^-----^^-^^
    replace_extras arg: {'\n': '', 'one': '1'}
    output: 'this is 1 test!'
    *************************
    DEFAULT REPLACE ITEMS
    ---------------------
    These can be overridden and/or appended to using the replace_extras
    argument.
    replace item      |   with
    <\\n line ending> - <space>
    <\\r line ending> - <space>
    <\\t tab>         - <space>
    <  double-space>  - <space>
    <text-input>      - <stripped>
    *************************
    """
    clean_up_items = {'\n': ' ', '\r': ' ', '\t': ' ', '  ': ' ', '"':'', ',':''}
    clean_up_items.update(replace_extras)

    text = text.strip()

    change_made = True
    while change_made:
        text_old = text
        for x in strip_chars:
            while text.startswith(x) or text.endswith(x):
                text = text.strip(x).strip()

        for key, val in clean_up_items.items():
            while key in text:
                text = text.replace(key, val)

        change_made = False if text_old == text else True

    return text.strip()


#tiding the log file exported from leg entries, assuming it is filtered for a relevant time frame and "Failed sending Contract event"
with open('logfile.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['event', 'exception', 'company', 'contract'])
logfile = open('/Users/tgurevich/Downloads/file.txt','r')
for row in logfile:
    a=str.find(row, 'Failed sending Contract event to SF with')
    failed_note=row[:a]
    b=str.find(row,'{')
    c=str.find(row,'}')
    payload=row[b+1:c]
    d=str.find(row, 'exception')
    exception=row[d+9:]
    e=str.find(row,'retry')
    retrytext = row[e:]
    f=str.find(row, 'company_uuid')
    company=row[f+17:f+60]
    g=str.find(row,'membership_agreement_uuid')
    contract = row[g+30:g+70]
    contract = clean_up(contract)
    company = clean_up(company)
    has_event = str.find(payload, 'event_name')
    event = payload[has_event+16:has_event+36]
    event = clean_up(event)
    if e == -1:
        retry= False
    else:
        retry = True

    if retry == False and has_event !=-1:
        with open('logfile.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([event, exception, company, contract])
# print(failed_note)
# print('-----------')
# print(payload)
# print('-----------')
# print(exception)
