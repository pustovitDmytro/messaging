import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import re

def get_authentication(filename , option='yahoo-bot'):
    with open(filename) as file:
        secret = json.load(file)
        if option=='yahoo-bot':
            data = secret["bots"]["yahoo"]
        elif option=='gmail-test':
            data = secret["mine"]["test"]
        return (data['host'],data['port'],data['login'],data['password'])

def html_to_plain(html):
    msg = re.sub(r'<br>','\n',html.strip())
    bs = BeautifulSoup(msg,"html.parser")
    list = []
    for a in bs.findAll('a'):
        href = a.attrs['href']
        list.append(a.text + ": " + href)
    msg = bs.text
    if len(list)>0:
        msg+="\nhidden links:\n"
        for item in list:
            msg+=item+"\n"
    return msg

def add_body(msg,html,plain=0):
    if plain==0:
        plain = html_to_plain(html)
    part1 = MIMEText(plain, 'plain')
    part2 = MIMEText(html, 'html')
    altMsg = MIMEMultipart('alternative')
    altMsg.attach(part1)
    altMsg.attach(part2)
    msg.attach(altMsg)

def add_header(msg,Subject,From,To):
    msg['Subject'] = Subject
    msg['From'] = From
    msg['To'] = To

def sendMessage(authentication,msg,To):
    if authentication[1]==465:
        smtpObj = smtplib.SMTP_SSL(authentication[0], authentication[1])
        smtpObj.ehlo()
    else:
        smtpObj = smtplib.SMTP(authentication[0], authentication[1])
        smtpObj.ehlo()
        smtpObj.starttls()
    smtpObj.login(authentication[2],authentication[3])
    smtpObj.sendmail(authentication[2],To,msg.as_string())
    smtpObj.quit()

authentication=get_authentication('secret.json')
msg = MIMEMultipart('related')
html="""

<h1> this is title </h1>
<p> first <b>paragraph</b> </p>
<p> second<br> paragraph </p>
<p> third paragraph <a href="google">somwere</a></p>
<ol>
<li>item1</li>
<li>item2</li>
<li>item3</li>
</ol>

"""
add_header(msg,"Test python module",authentication[2], 'pustic@gmail.com')
add_body(msg,html)
sendMessage(authentication,msg,'pustic@gmail.com')


