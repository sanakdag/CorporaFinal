'''
This will analyze the results of the GloVe model
After you run model.sh there were be vectors in the two folders male and female
within the GloVe folder
This program will read in those vectors and do cosine similarity of 20 nearest neighbors for up to 12 or so keywords that you can specificy in diff.txt
You can find interesting keywords by seeing what the corpora have in common
or not in common by using vocab.py and playing with some of the parameters


The first time you run this program it won't work because the GloVe model 
spits out the vectors with the wrong dimensions 

You will see an output like this:

" Detected dimensions: 3127  X  300
(3127, 300)
Detected dimensions: 2968  X  300
(2968, 300)

2019-12-09 13:54:12,336 : INFO : loading projection weights from ./GloVe-1.2/male/vectors.txt
Traceback (most recent call last):
  File "analyze.py", line 43, in <module>
    model_m = KeyedVectors.load_word2vec_format("./GloVe-1.2/male/vectors.txt", binary=False)
    
    ...

    vocab_size, vector_size = (int(x) for x in header.split())  # throws for invalid file format
ValueError: invalid literal for int() with base 10: 'and' "



Go to ./GloVe-1.2/male/vectors.txt and ./Glove-1.2/female/vectors.txt
and add a new line at the beginning
if the output above was:

" Detected dimensions: 3127  X  300
(3127, 300)                         ==> goes to ./GloVe-1.2/male/vectors.txt
Detected dimensions: 2968  X  300
(2968, 300)                         ==> goes to ./GloVe-1.2/female/vectors.txt
" 
IMPORTANT remove all other characters from the output 
    just the two numbers separated by whitespace on the first line
add the line: "3127 300" to the first line of the male vector file
and add "2968 300" to the first line of the female vector and run
analyze.py again and it will save teh graphs in the current directory


'''  


import numpy as np

from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,10)

from pylab import *

import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import models
from gensim.models import word2vec,KeyedVectors

# get dimensions of GloVe embedding

with open('./GloVe-1.2/male/vectors.txt', 'r') as m_embedding_file:
    m_embedding_content = m_embedding_file.readlines()
    m_embedding_content = [x.strip() for x in m_embedding_content] 

    m_num_lines = len(m_embedding_content)  #- 1 # skip the header
    m_num_dims = len(m_embedding_content[1].split()) - 1 # -1 because of the label column
    print("Detected dimensions:", m_num_lines, " X ", m_num_dims)

    m_placeholder = np.zeros((m_num_lines, m_num_dims))

with open('./GloVe-1.2/female/vectors.txt', 'r') as f_embedding_file:
    f_embedding_content = f_embedding_file.readlines()
    f_embedding_content = [x.strip() for x in f_embedding_content] 

    f_num_lines = len(f_embedding_content)  #- 1 # skip the header
    f_num_dims = len(f_embedding_content[1].split()) - 1 # -1 because of the label column
    print("Detected dimensions:", f_num_lines, " X ", f_num_dims)

    f_placeholder = np.zeros((f_num_lines, f_num_dims))



model_m = KeyedVectors.load_word2vec_format("./GloVe-1.2/male/vectors.txt", binary=False)



model_f = gensim.models.KeyedVectors.load_word2vec_format("./GloVe-1.2/female/vectors.txt", binary=False)


labels = []

m = dict()
f = dict()


print("making graph\n")

diff = open("diff.txt","r")
vocab = diff.readlines()
for i in range(0,len(vocab)):
    if (i%2==0):
        x = vocab[i].rstrip()
        x2 = vocab[i+1].rstrip()
        m[(x,x2)] = model_m.distance(x,x2)
        f[(x,x2)] = model_f.distance(x,x2)
        labels.append(x+" "+x2)




M = [m[x] for x in m]
F = [f[x] for x in f]
data = M+F



l = len(m)
men = data[:l]
women = data[l:]
w = 0.35
t = np.arange(len(labels))

# figure related code
fig,ax = plt.subplots()
r1 = ax.bar(t-(w/2),men,w,label="M")
r2 = ax.bar(t+(w/2),women,w,label="W")

ax.legend(["M","W"])

fig.suptitle('Distance between word pairs', fontsize=40, fontweight='bold')

ax.set_title(' ')
ax.set_xlabel('word pairs', fontsize=30)
ax.set_ylabel('distance')
xti = [x for x in range(0,int(len(data)/2))]
plt.xticks(xti,labels)


plt.savefig("distance.png")


print("\ncheckpoint\n")

print("Calculating word distances")

common = open("common.txt","r")
vocab = common.readlines()
m = dict()
f = dict()
l1 = len(vocab)
pairs = []

for i in range(0,l1):
    for j in range(i,l1):
        v1 = vocab[i]
        v2 = vocab[j]
        v1 = v1.rstrip()
        v2 =v2.rstrip()
        if v1 != v2:
            pairs.append((v1,v2))
            m[(v1,v2)] = model_m.distance(v1,v2)
            f[(v1,v2)] = model_f.distance(v1,v2)

print("\ncheckpoint\n")

print("find min/max distance")

m1 = []
f1 = []
cmin = 10
cmax = 0

for p in pairs:
    if abs(f[p]-m[p]) < cmin:
        cmin = abs(f[p]-m[p])
        print(p)
    if abs(f[p]-m[p]) > cmax:
        cmax = abs(f[p]-m[p])
        print(p)
    f1.append(f[p])
    m1.append(m[p])

c = list(zip(f1,m1))
c = sorted(c,key=lambda x:x[0])
print(c[:1])


m1 = [ i for i, j in c]
f1 = [ j for i, j in c]

print("\ncheckpoint\n")
print("linear regression")


m2 = np.array(m1).reshape((-1,1))
f2 = np.array(f1)

model_d = LinearRegression(n_jobs =-1)
model = model_d.fit(m2,f2)

r_sq = model.score(m2,f2)
print('coefficient of determination:', r_sq)