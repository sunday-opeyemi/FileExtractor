from tkinter import *
from tkinter.filedialog import askopenfilename
import re
import mysql.connector
from os.path import exists
root = None
in_path = ''
coursedesc = ''
fword = ''
rword = []
cdescription = None
mcontent = None
cunit = None
count = 1
scount = 2
searchobj = None
infile =''
enters = 0
desc = " "
mylist = []

def chooseFile():
	global in_path, mcontent
	try:
		root = Tk().withdraw()
		in_path = askopenfilename()
		if exists(in_path):
			with open(in_path) as infile:
				content = infile.read()
				mcontent.insert(END, content)
	except Exception as e:
		Label(root, text = "No file selected").grid(row = 2, column = 0)

def submitFile():
	submitheader()
	submitdescription()

def headers():
	global description, unit, count, scount, coursedesc, in_path, searchobj, fword, enters, mylist
	coursedesc2 = []
	coursedesc3 = []
	ful_description = ''
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
						print("the line enters continue")
					else:
						fword = myfile[0]+" "+ myfile[1]
						rword = myfile[2].split("[")
					if len(rword) <=1:
						continue
					else:
						unit = rword[1].split()
						mylist.append(fword)
	
					mydb = mysql.connector.connect(host = 'localhost', user = 'root', password = '', database = 'sylabus_db')
					mycursor = mydb.cursor()
					sql = "insert into courses_tb (title, s_desc, unit, status) value('%s', '%s', '%s', '%s')"\
						%(fword, rword[0], unit[0], "C")
					if sql:
						mycursor.execute(sql)
						mydb.commit()
						enters += mycursor.rowcount
						Label(root, text = str(enters)+" inserted successfully").grid(row = 2, column = 0)
					else:
						Label(root, text = "Sending failed").grid(row = 2, column = 0)

					count +=1
	else:
		Label(root, text = "NO file detected").grid(row = 2, column = 0)

def description():
	global description, unit, count, scount, coursedesc, in_path, searchobj, infile, fword, enters, mylist, desc
	coursedesc2 = []
	coursedesc3 = []
	if exists(in_path):
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
				Label(root, text = str(enters)+" Updated successfully").grid(row = 2, column = 0)
			else:
				Label(root, text = "Updating failed").grid(row = 2, column = 0)
	else:
		Label(root, text = "NO file detected").grid(row = 2, column = 0)

def submitheader():
	for line in range(1, 2):	
		headers()

def submitdescription():
	global scount, count, mylist, desc
	count = 1
	for desc in mylist:
		description()
		print(desc)
		scount +=1
		count +=1

def component(root):
	global mcontent
	
	mcontent = Text(root, height = 30, width = 60)
	mcontent.grid(row = 0, column = 0)
	scroll = Scrollbar(root, orient = "vertical", command = mcontent.yview)
	scroll.grid(row = 0, column = 1, sticky = 'ns')
	mcontent.configure(yscrollcommand = scroll.set)
	bpanel = Frame(root)
	Button(bpanel, text="Selct File", command = chooseFile).pack(side=LEFT, padx=5)
	Button(bpanel, text="Uploade Course", command = submitFile).pack(side=LEFT)
	bpanel.grid(row = 1, column = 0)
	bpanel.grid_propagate(0)

def main():
	global root
	root = Tk()
	component(root)
	root.title('File Extraction')
	root.mainloop()

main()
