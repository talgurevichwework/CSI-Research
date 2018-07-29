# README
This is an internal tool to quantify and segment the data reconciliation errors between Salesforce and Spaceman by type. 

### Scripts
There are two scripts: 
- **looker-sf&#46;py** quantifies the data reconciliation errors between the salesforce and Looker sales reports:

_output_ : the output of the comparison of both looker and SF reporting with all accounts and the number gaps

_reuse_ : the reuse records reason and event joined into the output file.

_fulloutput_ : a full right join of the output and the re-use entries


- **transaction-sf&#46;py** segments data reconciliation errors between salesforce and dw.v_transaction in spaceman by type:
_output_ : the output of the comparison of v_transaction reseqrvations with SF opportunities with all accounts, account information, opportunity information, reservation information, number gaps, and the error reason
_fulloutput_ : a full right join of the output and the re-use entries

### Other Files
##### queries&#46;py
Generates all relevant SQL queries. Queries are aplit up by relevant file. All queries use the [WeModule] library for accessing the redshift db.
##### label_sync_issues&#46;py
Contains the label_sync_issues function which attempts to diagnose the sync error of a single reservation. 

[WeModule]: <https://github.com/WeConnect/we_module>
