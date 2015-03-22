import sys
sys.path.append("C:\\users\\benson\\desktop\\cs53")
import smtplib
import time
import benson
import os
import pickle
from copy import deepcopy

FNAME = 'hafiz.txt'
PICKLE_PATH = 'parsed.pkl'
LOGPATH = 'hafizlog.txt'
MSG = """From: Hafizbot <hafizbot>
To: You
MIME-Version: 1.0
Content-type: text/html
Subject: HAFIZBOT

"""

HEADER_TERMS = ["POEMS FROM THE","DIVAN OF HAFIZ"]
SPLITTER_TERMS = ["I","V","X","L","M"]

def get_structured_corpus():
	"""
	Either gets titles from pickle path or re-parses
	"""
	if os.path.isfile(PICKLE_PATH):
		with open(PICKLE_PATH, 'rb') as pfk:
			tdict = pickle.load(pkf)
			tlist = pickle.load(pkf)
		return tdict, tlist

	tdict = {}
	tlist = []
	
	# organize poems by line number
	with open(FNAME, "r") as f:
		llist = f.readlines()
		llist = [line.rstrip(' \n') for line in llist]
		for i in range(len(llist)):
			if len(llist[i]) < 8:
				if any(word in llist[i] for word in SPLITTER_TERMS):
					tdict[llist[i]] = i
					tlist.append(llist[i])
	return tdict, tlist


def construct_message_dictionary(tdict, tlist):
	# all this stuff is super convoluted, but this just adds style based on content of lines
	# i think i was feeling pretty 'digital humanities' at the time
	msgdict = {}
	for i in range(len(tlist)-1):
		msglist = []
		for j in range(tdict[tlist[i]],tdict[tlist[i+1]]):
			ital = 0
			bold = 0
			if any(word in llist[j] for word in HEADER_TERMS + map(str, range(10))):
				continue
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
				msgdict[i] = msglist
	return msgdict

"""
This is the 'log' implementation which is so ugly I just must comment it out..
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
"""

def get_msg_idx():
	with open(LOGPATH,'r+') as logfile:
		logfile.seek(0)
		logint = int(logfile.readline().split(",")[0])
	return logint


def update_log(msg_idx):
	with open(LOGPATH,'r+') as logfile:
		logfile.seek(0)
		logfile.write(str(msg_idx + 1) + ", \r\n")


def send_mail(msg):
	server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('bensontucker@gmail.com',benson.gmail())
	server.sendmail('bensontucker@gmail.com', benson.FRIENDS,msg)
	server.close()
	return True

if __name__ == '__main__':
	msg = deepcopy(MSG)
	msgdict = construct_message_dictionary(*get_structured_corpus())
	msg_idx = get_msg_idx()
	for i in range(len(msgdict[msg_idx])):
		if i == 0:
			msg = msg + " <br> "
		if i == 1:
			msg = msg + " <br> "
		if len(msgdict[msg_idx][i]) > 0:
			if "<" in msgdict[msg_idx][i]:
				msg = msg + msgdict[msg_idx][i]
			else:
				msg = msg + msgdict[msg_idx][i] + " <br> "
		
	if send_mail(msg):
		update_log(msg_idx)

