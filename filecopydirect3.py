import re
import mysql.connector
from os.path import exists
root = None
in_path = 'COURSE DESCRIPT2.txt'
coursedesc = ''
fword = []
rword = []
cdescription = None
cunit = None
count = 1
scount = 2
searchobj = None
mylist = []
desc = ""

def headers():
	global description, unit, count, scount, coursedesc, in_path, searchobj
	coursedesc2 = []
	coursedesc3 = []
	ful_description = ''
	fword = ''
	rword = ""
	if exists(in_path):
		with open(in_path) as infile:
			for line in infile:	
				searchobj = re.search(r'\[', line, re.M|re.I)
				if searchobj:
					infile2 = line
					myfile = infile2.split(" ", 2)
					if len(myfile) <=2:
						continue
					else:
						fword = myfile[0]+ myfile[1]
						rword = myfile[2].split("[")
					if len(rword) <=1:
						continue
					else:
						unit = rword[1].split()
						mylist.append(fword)
					print(count, fword, rword[0], rword[1])
	
					mydb = mysql.connector.connect(host = 'localhost', user = 'root', password = '', database = 'sylabus_db')
					mycursor = mydb.cursor()
					sql = "insert into courses_tb (co_id, title, s_desc, unit, status) value('%d', '%s', '%s', '%s', '%s')"\
						%(count, fword, rword[0], unit[0], "C")
					if sql:
						mycursor.execute(sql)
						mydb.commit()
						print(count, fword, rword[0], unit[0])
					else:
						print("file failed to submit")
					count +=1
	else:
		print("File does not exits.")

def description():
	global description, unit, count, scount, coursedesc, in_path, searchobj, mylist, desc
	coursedesc2 = []
	coursedesc3 = []
	with open(in_path) as infile:
		for line in infile:
			if not searchobj:
				coursedesc2.append(line)
				if line.startswith('('+str(scount)+')'):
					break
		contents = " ".join(coursedesc2)
		description3 = contents.split('('+str(count)+')')
		mydb = mysql.connector.connect(host = 'localhost', user = 'root', password = '', database = 'sylabus_db')
		mycursor = mydb.cursor()
		sql = 'update courses_tb set f_desc = "%s" where title = "%s"' %(description3[1], desc)
		if sql:
			mycursor.execute(sql)
			mydb.commit()
			print(str(count) +' file updeated successfully')
		else:
			print("file failed to submit")
def submitheader():
	for line in range(1, 2):	
		headers()

def submitdescription():
	global scount, count, desc
	count = 1
	for desc in mylist: 
	    description()
	    scount +=1
	    count +=1

submitheader()
submitdescription()