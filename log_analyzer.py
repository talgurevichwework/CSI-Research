import string
import csv
from we_module.we import We
we = We(True)
import re
import pandas
import datetime
import time
import numpy
import os

# analyzign a log file to produce only the errors from contracts sf comms, and filtering out the retries

mylog = open('file.txt', 'r')
unique_exceptions = []
all_exceptions = []
for row in mylog:
    a=str.find(row,'exception')
    b=str.find(row,'id:')
    c=row[a:b]
    d=str.find(c,'records:')
    e=c[:d]
    if e.find('retry') == -1:
        all_exceptions.append(e)
        if e not in unique_exceptions:
            unique_exceptions.append(e)

print('unique exceptions:', len(unique_exceptions))
print('total non-retry exceptions:', len(all_exceptions))

# making a CSV out it
# with open('exceptions.csv', 'w') as csvfile:
#     writer=csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter='\n')
#     writer.writerow(myexceptions)
