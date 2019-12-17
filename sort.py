#once all of the reviews are in folders sorted by professor,
#this program goes through all of the reviews and infers the gender of the 
#professor. Then the reviews for the professor are added to either 
#male.txt or female.txt which will end up in this folder

#to run the next step, put male.txt in a folder called male
#					   put female.txt in a folder called female
#					   put both files in the folder GloVe-1.2
#					   put the file model.sh into the GloVe-1.2 folder
#					   run model.sh and then to_tensorboard.py


import os 
import re
f = set()
f1 = 0
m = set()
m1 = 0
t = 0
gen = []
pname = ""

rootDir = './reviews'
for dirName, subdirList, fileList in os.walk(rootDir):
	male = 0
	female = 0
	#print("Found directory: " + dirName)
	for fname in fileList:
		
		try:
			with open(dirName+"/"+fname, "r") as fi:
				#print(fname)
				rs = fi.readlines()
				for r in rs:
					r = r.lower()
					p = fname.split('_')
					pname = p[0] +"_"+p[1]
					if (" he " in r or " his " in r or " him " in r):
						male = male + 1
					if (" she " in r or " her " in r):
						female = female + 1
			
			fi.close()
		except Exception as e:
			print()
	if male > female:
		m.add(pname)
		#print("M "+pname)
		m1+=1
	elif female > male:
		f.add(pname)
		#print("F "+pname)
		f1+=1
	else:
		t += 1
		#print("TIE")
		print(pname)
		#print(rs)
mcount = 0
fcount = 0

for p in m:
	f2 = open("male.txt","a+")
	for dirName, subdirList, fileList in os.walk("./reviews/"+p):
		for fname in fileList:
			#print(fname)
			with open(dirName+"/"+fname, "r") as fi:
				rs = fi.readlines()
				for r in rs:
					#r = r.lower()
					ws = r.split(" ")
					for w in ws:
						mcount+=1
						w = re.sub('[^A-Za-z]+', '', w)
						f2.write(w+" ")
						if (mcount > 150000):
							break
					f2.write("\n")
	f2.close()

for p in f:
	f3 = open("female.txt","a+")
	for dirName, subdirList, fileList in os.walk("./reviews/"+p):
		for fname in fileList:
			with open(dirName+"/"+fname, "r") as fi:
				p = fname.split('_')
				rs = fi.readlines()
				for r in rs:
					if p[0] in r:
						r = r.replace(p[0],'')
					if p[1] in r:
						r = r.replace(p[1],'')
					#r = r.lower()
					ws = r.split(" ")
					for w in ws:
						fcount+=1
						w = re.sub('[^A-Za-z]+', '', w)
						f3.write(w+" ")
						if (fcount > 150000):
							break
					f3.write("\n")
	f3.close()

print("M ", m1, " F ", f1, " T ", t)
