from tabulate import tabulate 
from pprint import pprint
from f5.bigip import ManagementRoot
from datetime import datetime
from jinja2 import Template,Environment, FileSystemLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

todays_date=datetime.now().date()

mgmt = ManagementRoot('127.0.0.1', 'admin', 'password')
ltm = mgmt.tm.ltm
sys= mgmt.tm.sys
client_ssl_profiles=ltm.profile.client_ssls
ssl_certs= sys.file.ssl_certs

vips=[]
#get list of virtual servers 
virtuals = ltm.virtuals.get_collection()

#loop through virtual servers and append  data to  list 
for virtual in virtuals:
    client_ssl = None
    for profile in virtual.profiles_s.get_collection():
        if profile.context == "clientside":
            	client_ssl = profile.name 
		vips.append({"name":virtual.name,"destination":virtual.destination,"ssl_profile":client_ssl})

#obtain certificate information from profile
#loop through list and append  certificate info to  list 

for vip in vips:
	if vip['ssl_profile'] != None:
		for client_ssl_profile in client_ssl_profiles.get_collection():
			if client_ssl_profile.name ==vip['ssl_profile']:
        			cert= client_ssl_profile.cert
    				vip['cert']= client_ssl_profile.cert

		for ssl_cert in ssl_certs.get_collection():
    			if vip['cert'] == ssl_cert.fullPath:
        	           	vip['expire']= ssl_cert.expirationString
        	 		vip['subject']=ssl_cert.subject

#print(tabulate(vips,headers='keys'))

#pprint(vips)
#loop through list and  create list for certs expiring in  days 

vips_30_days=[]
for vip in vips:
	cert_expiration=datetime.strptime(vip['expire'], '%b %d  %H:%M:%S %Y %Z')
	delta=cert_expiration.date()-todays_date
        if delta.days < 29:
		vips_30_days.append({"name":vip['name'],"destination":vip['destination'],"ssl_profile":vip['ssl_profile'],"cert":vip['cert'],"subject":vip['subject']})

#send email notification

env = Environment(loader=FileSystemLoader('/etc/ansible/templates/'))
template = env.get_template('f5_ssl_table.html')
vips_30_days= {'vips_30_days':vips_30_days}
output= template.render(vips_30_days)

#print(vips_30_days)
if len(vips_30_days) > 0: 
	gmail_user = 'user@gmail.com'
	gmail_password = 'password'
	to_email= 'user@gmail.com'

	message = MIMEMultipart()
	message['Subject'] = 'SSL certificates expiring in 30 days'
	message['From'] = gmail_user
	message['To'] = to_email
	message.attach(MIMEText(output, "html"))
	msgBody = message.as_string()

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(gmail_user, gmail_password)
	server.sendmail(gmail_user,to_email,msgBody)
	server.close()
