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


message="""\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""
msg = MIMEMultipart('related')
msgAlt = MIMEMultipart('alternative')
text = "plaaaaaaaaaain text"

part1 = MIMEText(text, 'plain')
part2 = MIMEText(message, 'html')

msg['Subject'] = "SMTP HTML e-mail test"
msg['From'] = login
msg['To'] = to

msgAlt.attach(part1)
msgAlt.attach(part2)
msg.attach(msgAlt)

print(msg.as_string())
#print(login,password,to,msg)
smtpObj = smtplib.SMTP_SSL('smtp.mail.yahoo.com',465)
smtpObj.ehlo()
print(smtpObj.login(login,password))
print(smtpObj.sendmail(login,to,msg.as_string()))
smtpObj.quit()