#once you finish the steps for sort.py and the corpora are in their respective 
# folders in the GloVe directory, we can run this program to see what
# differences there are in terms of frequency

import re
import operator


#uncomment one of these lines at a time to play with the two options
#IN_COMMON = True
IN_COMMON = False


# will print the same list without the numbers so you can run 
# python vocab.py > diff.txt 
# which lets you use those words for analyze.py

NO_NUMS = False
#NO_NUMS = True

# appears at least this many times between the two corpora
FREQ = 500

# how big the difference in frequency should be
# i.e. -20 < m_freq(x) - f_freq(x) < 20
RANGE = 30



#words in the female review corpus
f = dict()
#words in the male review corpus
m = dict()

#words that appear in BOTH
diff = dict()




with open("./GloVe-1.2/female/vocab.txt", "r") as fv:
	with open("./GloVe-1.2/male/vocab.txt", "r") as fm:
		m_vocab = fm.readlines()
		f_vocab = fv.readlines()

for i in m_vocab:
	x = len(i)
	i = i[:x-1]
	i = i.split(" ")
	m[i[0]]=int(i[1])

for i in f_vocab:
	x = len(i)
	i = i[:x-1]
	i = i.split(" ")
	f[i[0]]=int(i[1])


common = []
for x in m:
	if x in f:
		common.append(x)
		print(x)


'''

		if m[x]+f[x] > FREQ:
			# if difference is positive it appears more in the male corpus
			diff[x] = m[x]-f[x]

for x in f:
	if x in m and x not in diff:
		if m[x]+f[x] > FREQ:
			# if difference is negative it appears more in the female corpus
			diff[x] = m[x]-f[x]

sorted_x = sorted(diff.items(), key=operator.itemgetter(1), reverse=True)



if not NO_NUMS:
	if not IN_COMMON:
		for k,v in sorted_x:
			if v < RANGE and v > (0-RANGE):
				print(k+ " "+str(v))
	else:
		for k,v in sorted_x:
			if v == 0:
				print(k+" "+str(v))
else:
	if not IN_COMMON:
		for k,v in sorted_x:
			if v < RANGE and v > (0-RANGE):
				print(k)
	else:
		for k,v in sorted_x:
			if v == 0:
				print(k)
'''