# send-report
A quick script to run an sql query, parse the results into a csv and ship the file via the sendgrid API. 

# usage

```
$ ./send-report.py
usage: send-report.py [-h] [--host HOST] [--user USER] [--dbpass DBPASS]
                      [--db DB] [--port PORT] [--sender SENDER]
                      [--recipient RECIPIENT] [--subject SUBJECT]
                      queryfile
```
