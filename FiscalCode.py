from calendar import firstweekday
import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox
import csv

def ClearMask():
	TxtName.delete(0,'end')
	TxtSurname.delete(0,'end')
	TxtCity.delete(0,'end')
	ChkSex.deselect()
	LblCodice.config(text="Codice fiscale")

def ControlChar(code: str):
	OddTuple=(	1,0,5,7,9,13,15,17,19,
				21,1,0,5,7,9,13,15,17,
				19,21,2,4,18,20,11,3,6,
				8,12,14,16,10,22,25,24,23)
	c=1
	Sum=0
	for i in code:
		if (c%2==0):
			if(ord(i)>64):
				Sum+=(ord(i)-ord('A'))
			else:
				Sum+=(ord(i)-ord('0'))
		else:
			if (ord(i)>64):
				Sum+=OddTuple[ord(i)-55]
			else:
				Sum+=OddTuple[ord(i)-ord('0')]
		c+=1
	FinalChar=chr(ord('A')+(Sum%26))
	FinalCode=code+FinalChar
	return FinalCode

def GenerateCode():
	code=""
	Name=GetName(TxtName.get())
	Name=Name.upper()
	Surname=GetSurame(TxtSurname.get())
	Surname=Surname.upper()
	Birth=CalBirth.get_date()
	Birth=SetBirth(Birth)
	City=GetCity(TxtCity.get())
	if (City=='ZZZZ'):
		messagebox.showerror('Errore','Comune o stato estero di nascita non trovato\nAssicurarsi di aver digitato correttamente il nome completo del comune o stato estero')
		return -1
	code=Surname+Name+Birth+City
	code=code.upper()
	code=ControlChar(code)
	LblCodice.config(text=code)
	return 0

def GetCity(BirthTown: str):
	LineCounter=0
	TestCity=''
	BirthTown=BirthTown.upper()
	with open('Cities.csv','r',encoding='UTF-8') as CitiesFile:
		CitiesList=csv.reader(CitiesFile,delimiter=';')
		for row in CitiesList:
			if (LineCounter>0):
				if (row[0].upper()==BirthTown):
					return row[1]
			LineCounter+=1
	return 'ZZZZ'

def GetName(Name: str):
	vowels=('A','E','I','O','U')
	Letters=""
	outString=""
	Name=Name.upper()
	if (len(Name)<3):
		outString=Name.ljust(3,'X')
		return outString
	for i in Name:
		if (i==' '):
			continue
		for j in vowels:
			if (i==j):
				break
		if (i==j):
			continue
		Letters+=i
	if (len(Letters)>3):
		outString=Letters[0]+Letters[2]+Letters[3]
		return outString
	if (len(Letters)==3):
		outString=Letters
		return outString
	if (len(Letters)<3):
		for i in Name:
			for j in vowels:
				if (i==j):
					Letters+=i
					if (len(Letters)>=3):
						outString+=Letters
						return outString

def GetSurame(Name: str):
	Name=Name.upper()
	vowels=('A','E','I','O','U')
	Letters=0
	outString=""
	if (len(Name)<3):
		outString=Name.ljust(3,'X')
		return outString
	for i in Name:
		if (i==' '):
			continue
		for j in vowels:
			if (i==j):
				break
		if (i==j):
			continue
		outString+=i
		Letters+=1
		if (Letters==3):
			return outString
	for i in Name:
		for j in vowels:
			if (i==j):
				outString+=i
				Letters+=1
				if (Letters==3):
					return outString
	return outString

def SetBirth(DateOfBirth: str):
	months=('A','B','C','D','E','H','L','M','P','R','S','T')
	monthindex=int(DateOfBirth[3:5])-1
	isFemale=BolSex.get()
	if (isFemale):
		Day=str(int(DateOfBirth[0:2])+40)
	else:
		Day=DateOfBirth[0:2]
	return DateOfBirth[6:8]+months[monthindex]+Day
	

HomePage=tk.Tk()
HomePage.title("Codice Fiscale")
HomePage.iconbitmap('Icon.ico')
HomePage.geometry("400x400")

LblName=tk.Label(text="Nome: ")
LblName.grid(column=0,row=0)
TxtName=tk.Entry()
TxtName.grid(column=1,row=0,sticky='NSWE')

LblSurname=tk.Label(text="Cognome: ")
LblSurname.grid(column=0,row=1)
TxtSurname=tk.Entry()
TxtSurname.grid(column=1,row=1,sticky='NSWE')

LblBirth=tk.Label(text="Data di nascita: ")
LblBirth.grid(column=0,row=2)
CalBirth=Calendar(HomePage,selectmode="day",firstweekday="monday",locale="it_IT",date_patern="dd/mm/yy")
CalBirth.grid(column=1,row=2)

LblSex=tk.Label(text="Sesso: ")
LblSex.grid(column=0,row=3)
BolSex=tk.BooleanVar()
BolSex.set(False)
ChkSex=tk.Checkbutton(HomePage, text="Seleziona se donna",variable=BolSex)
ChkSex.grid(column=1,row=3,sticky='NSWE')
ChkSex.deselect()

LblCity=tk.Label(text="Comune di nascita: ")
LblCity.grid(column=0,row=4)
TxtCity=tk.Entry()
TxtCity.grid(column=1,row=4,sticky='NSWE')

CmdCalc=tk.Button(text="Calcola codice fiscale",command=GenerateCode)
CmdCalc.grid(column=1,row=5,sticky='NSWE')

CmdClear=tk.Button(text="Pulisci",command=ClearMask)
CmdClear.grid(column=0,row=5,sticky='NSWE')

LblCodice=tk.Label(text="Codice fiscale",font=("Consolas",25))
LblCodice.grid(column=0,row=6,columnspan=2,sticky='NSWE')

HomePage.mainloop()