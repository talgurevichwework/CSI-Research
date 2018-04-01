how to export the log file:
1. log into logentries
2. filter for sales api prod
3. place time frame
4. search for "Failed sending Contract event"
5. export in log format, save to this program's directory as file.log
6. success


unique company (and unique_contracts) csvs will be re-written every timeframe
logfile.csv is opened to append and will have to be deleted before each py run to avoid bloating.

happy hunting

Tal 
