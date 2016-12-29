#!/usr/bin/env python

import sendgrid
from sendgrid.helpers.mail import *
import argparse
import psycopg2
import traceback
from sendgrid.helpers.mail import *
from sendgrid import *
import base64

parser = argparse.ArgumentParser(description='Runs specified query then sends query to email')
parser.add_argument('--host', help='ip address of db host', default='dbhost')
parser.add_argument('--user', help='db username', default='dbuser')
parser.add_argument('--dbpass', help='dp passwd', default='db_passwd')
parser.add_argument('queryfile', help='path to plaintext file that includes the sql formatted query')
parser.add_argument('--db', help="database to be queried", default='db_name')
parser.add_argument('--port', help="port that pgsql server is running on", default='5434')
parser.add_argument('--sender', help='sender email, defaults to do-not-reply@kentik.com', dest='sender', default='do-not-reply@kentik.com')
parser.add_argument('--recipient', help='recipient email, defaults to drohan@kentik.com', dest='recipient', default='your-email@example.com')
parser.add_argument('--subject', help='email subject, defaults to Scheduled Report', dest='subject', default='Scheduled Report')
args = parser.parse_args()


sg = sendgrid.SendGridAPIClient(apikey='send-grid api key')


def sendMail(sender, recipient, subject):
	body = "See attached report"
	with open ('resultsfile.csv', 'r') as f:
		data=f.read()
		attach_content = base64.urlsafe_b64encode(data)
	attachment = Attachment()
	attachment.set_content(attach_content)
	attachment.set_type('text/csv')
	attachment.set_filename('resultsfile.csv')
	attachment.set_disposition('attachment')
	attachment.set_content_id('request')
	mail = Mail(Email(sender), subject, Email(recipient), Content("text/plain", body))
	mail.add_attachment(attachment)
	try:
		response = sg.client.mail.send.post(request_body=mail.get())
		if (response.status_code == 202):
			return(0)
		else:
			print("Error:")
			print(response.status_code)
			print(response.body)
			print(response.headers)
	except:
		print traceback.format_exc()
		print("Unexpected error while sending mail")

	
def readQuery():
	with open(queryfile, 'r') as myfile:
		query = myfile.read()
	return(query)


def runQuery(query):
	conn_string = "host={} dbname={} user={} password={} port={}".format(host, dbname, user, dbpass, port)
	try:
		conn = psycopg2.connect(conn_string)
	except psycopg2.Error as e:
		print("Unable to connect to the database.")
	try:
		curs = conn.cursor()
		outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
		with open('resultsfile.csv', 'w') as f:
			curs.copy_expert(outputquery, f)
		conn.close()
	except psycopg2.Error as e:
		print traceback.format_exc()


if __name__ == "__main__":

	# Set up command line arguments	
	conn = None
	sender = args.sender
	recipient = args.recipient
	subject = args.subject
	queryfile = args.queryfile
	host=args.host
	dbname=args.db
	user=args.user
	dbpass=args.dbpass
	port=args.port
	resultsfile = 'resultsfile.csv'
	
	# do the things
	query = readQuery()
	results = runQuery(query)
	sendMail(sender, recipient, subject)
	

		
		
