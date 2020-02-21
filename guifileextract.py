from tkinter import *
from tkinter.filedialog import askopenfilename
import re
import mysql.connector
from os.path import exists
root = None
in_path = 'No File'
coursedesc = ''
cid = None
code = None
cdescription = None
cunit = None
count = 1
scount = 2
course_id = None
course_code = None
description = None
unit = None
fd = ''
ful_description = None

def chooseFile():
	global in_path
	try:
		root = Tk().withdraw()
		in_path = askopenfilename()
		if exists(in_path):
			with open(in_path) as infile:
				content = infile.read()
				mcontent = Text(root, height = 30, width = 60)
				mcontent.grid(row = 4, column = 2)
				scroll = Scrollbar(root, orient = "vertical", command = mcontent.yview)
				scroll.grid(row = 4, column = 3, sticky = 'ns')
				mcontent.configure(yscrollcommand = scroll.set)
				mcontent.insert(END, content)
	except Exception as e:
		Label(root, text = "No file selected").grid(row = 6, column = 0)
		
def extractFile():
	global cid, code, cdescription, cunit, count, scount, fd, coursedesc, in_path, unit
	coursedesc2 = []
	coursedesc3 = ''
	fword = ''
	rword = ""
	if exists(in_path):
		with open(in_path) as infile:
			for line in infile:	
				searchobj = re.search(r'\(', line, re.M|re.I)
				if searchobj:
					infile2 = line
					myfile = infile2.split(" ", 2)
					if len(myfile) <=2:
						continue
					else:
						fword = myfile[0]+ myfile[1]
						rword = myfile[2].split("(")
					if len(rword) <=1:
						continue
					else:
						unit = rword[1].split()
				if not searchobj:	
					if line.startswith(str(scount)):	
						break
					else:
						if count == 1:
							fd = Text(root, height = 15, width = 50, bg = 'green', fg = 'white')
							fd.grid(row = 4, column = 2)
							coursedesc2.append(line)
							coursedesc = ''.join(coursedesc2)
							fd.insert(END, coursedesc)
						else:
							fd = Text(root, height = 15, width = 50, bg = 'green', fg = 'white')
							fd.grid(row = 4, column = 2)
							coursedesc2.append(line)
							coursedesc = ''.join(coursedesc2)
							coursedesc3 = coursedesc.split(str(count))
							if len(coursedesc3) == 2:
								fd.insert(END, coursedesc3[1])

			cid.set(count)
			code.set(fword)	
			cdescription.set(rword[0])
			cunit.set(unit[0])
			scount+=1
			count +=1	
	else:
		Label(root, text = "No file selected to extract.").grid(row = 6, column = 0)

def submitfile():
	global course_id, course_code, description, unit, fd, cid, code, cdescription, ful_description, cunit
	cid2 = cid.get()
	code2 = code.get()
	cdescription2 = cdescription.get()
	ful_description = fd.get("1.0", "end-1c")
	cunit2 = cunit.get()
	
	mydb = mysql.connector.connect(host = 'localhost', user = 'root', password = '', database = 'sylabus_db')
	mycursor = mydb.cursor()
	sql = "insert into courses_tb (co_id, title, s_desc, f_desc, unit, status) value('%d', '%s', '%s', '%s', '%d', '%s')"\
		%(cid2, code2, cdescription2, ful_description, cunit2, "C")
	if sql:
		mycursor.execute(sql)
		mydb.commit()
		Label(root, text = "Record inserted successfully.").grid(row = 6, column = 0)
	else:
		Label(root, text = "Record insertion failed.").grid(row = 6, column = 0)
	
def moveBack():
	global count, scount, cid

	count -=1
	scount -=1
	cid.set(count)

def component(root):
	global cid, code, cdescription, cunit
	cid = IntVar()
	cdescription = StringVar()
	code = StringVar()
	cunit = IntVar()
	
	Label(root, text = "Course Id").grid(row = 0)
	course_id = Entry(root, text = cid)
	course_id.grid(row = 0, column = 1)

	Label(root, text = "Course Code").grid(row = 1, column = 0)
	course_code = Entry(root, text = code)
	course_code.grid(row = 1, column = 1)

	Label(root, text = "Code Title").grid(row = 2, column = 0)
	description = Entry(root, text = cdescription)
	description.grid(row = 2, column = 1)

	Label(root, text = "Course Unit").grid(row = 3, column = 0)
	unit = Entry(root, text = cunit)
	unit.grid(row = 3, column = 1)

	Button(root, text="Submit File", command = submitfile).grid(row = 5, column = 0)
	Button(root, text="Extract File", command = extractFile).grid(row = 5, column = 1)
	Button(root, text="←", command = moveBack).grid(row = 5, column = 3)
	Button(root, text="Selct File", command = chooseFile).grid(row = 5, column = 2)

def main():
	global root
	root = Tk()
	component(root)
	root.title('File Extraction')
	root.mainloop()

main()