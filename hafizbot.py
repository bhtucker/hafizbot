import sys
sys.path.append("C:\\users\\benson\\desktop\\cs53")
import smtplib
import time
import benson

fname = "hafiz.txt"

tdict = {}
tlist = []

file = open(fname)
llist = file.readlines()
llist = [line.rstrip(' \n') for line in llist]
for i in range(len(llist)):
	if len(llist[i]) < 8:
		if any(word in llist[i] for word in ["I","V","X","L","M"]):
			tdict[llist[i]] = i
			tlist.append(llist[i])

file.close()

msglist = []
msgdict = {}
for i in range(len(tlist)-1):
	msglist = []
	for j in range(tdict[tlist[i]],tdict[tlist[i+1]]):
		ital = 0
		bold = 0
		if any(word in llist[j] for word in ["POEMS FROM THE","DIVAN OF HAFIZ"]):
			pass
		else:
			if any(word in llist[j] for word in ["1","2","3","4","5","6","7","8,","9","0"]):
				pass
			else:
				if "!" in llist[j]:
					bold = 1
					msglist.append("<b>")
				if "'" in llist[j]:
					ital = 1
					msglist.append("<i>")
				msglist.append(llist[j])
				if bold == 1:
					msglist.append("</b>")
				if ital == 1:
					msglist.append("</i>")
				msgdict[i]=msglist
		
msg = """From: Hafizbot <hafizbot>
To: You
MIME-Version: 1.0
Content-type: text/html
Subject: HAFIZBOT

"""

logfile = open("hafizlog.txt",'r+')
logfile.seek(0)
logint = int(logfile.readline().split(",")[0])
loglines = logfile.readlines()

#check log to make sure HAFIZBOT didn't already run today
splitLL = loglines[len(loglines)-1].split(",")
monstr = splitLL[2].strip()
daystr = splitLL[3].strip()
if monstr == "tm_mon=" + str(time.localtime()[1]):
	if daystr == "tm_mday=" + str(time.localtime()[2]):
		logfile.seek(0,2)
		logfile.write("attempt # " + str(logint) + " aborted at, " + str(time.localtime()) + ", \r\n")
		logfile.close
		sys.exit()
		
#if this isn't a dup run, update the log and proceed
logfile.seek(0)
logfile.write(str(logint+1) + ", \r\n")
logfile.seek(0,2)
logfile.write("run # " + str(logint) + " at, " + str(time.localtime()) + ", \r\n")
logfile.close


for i in range(len(msgdict[logint])):
	if i == 0:
		msg = msg + " <br> "
	if i == 1:
		msg = msg + " <br> "
	if len(msgdict[logint][i]) > 0:
		if "<" in msgdict[logint][i]:
			msg = msg + msgdict[logint][i]
		else:
			msg = msg + msgdict[logint][i] + " <br> "

#print(logint)
#print(msg)

server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
server.ehlo()
server.starttls()
server.ehlo()
server.login('bensontucker@gmail.com',benson.gmail())
server.sendmail('bensontucker@gmail.com',["sophia_renda@brown.edu","jonathan_storch@brown.edu","adamfoldi@gmail.com","ronaldkevinlewis@gmail.com","william_mack-crane@brown.edu","bensontucker@gmail.com","tnassau@gmail.com","lizzie_davis@brown.edu","r.j.sandler@gmail.com","serena.putterman@gmail.com","heyredhat@gmail.com","colin.ocon@gmail.com","tcleslie@bsu.edu"],msg)

#server.sendmail('bensontucker@gmail.com','bensontucker@gmail.com',msg)

server.close()