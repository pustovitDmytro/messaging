import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

json_file = "secret.json"
with open('secret.json') as file:    
    secret = json.load(file)
login = secret["bots"]["yahoo"]["login"]
password = secret["bots"]["yahoo"]["password"]
to = secret["mine"]["test"]["login"]


message="""
This is an e-mail message to be sent in HTML format
<b>This is HTML message.</b>
<h1>This is headline.</h1>
"""
msg = MIMEMultipart('alternative')
text = "plaaaaaaaaaain text"

#part1 = MIMEText(text, 'plain')
#part2 = MIMEText(message, 'html')
#
#msg.attach(part1)
#msg.attach(part2)
msg = MIMEText(text)

msg['Subject'] = "SMTP HTML e-mail test"
msg['From'] = login
msg['To'] = to

print(login,password,to,msg)
smtpObj = smtplib.SMTP_SSL('smtp.mail.yahoo.com',465)
smtpObj.ehlo()
print(smtpObj.login(login,password))
print(smtpObj.sendmail(login,to,msg.as_string()))
smtpObj.quit()