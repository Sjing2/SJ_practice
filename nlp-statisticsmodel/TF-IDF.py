import pandas as pd
import numpy as np

d1 = "The cat sat on my face I hate a cat"
d2 = "The dog sat on my bed I love a dog"

docs = [d1, d2]

d_N = len(docs)
# d_N

## 토크나이징
d1_token = d1.split(" ")
d2_token = d2.split(" ")
# print(d1_token)
# print(d2_token)

## TF
word_list = np.unique(d1_token + d2_token)
# print(word_list)

# d1 count

d1_count=[]
for word in word_list:
    d1_count.append(d1_token.count(word))

print(d1_count)

# d1 토큰개수

d1_len = len(d1_token)
print(d1_len)

# d1 TF

d1_TF = []

for i in d1_count:
    a = i/d1_len
    d1_TF.append(a)

# print(d1_TF)

# d2 count

d2_count=[]
for word in word_list:
    d2_count.append(d2_token.count(word))

# print(d2_count)

# d2 토큰개수

d2_len = len(d2_token)
# print(d2_len)

# d2 TF

d2_TF = []

for z in d2_count:
    a = z/d2_len
    d2_TF.append(a)

# print(d2_TF)

## IDF
from numpy import log as ln

word_list = np.unique(d1_token + d2_token)
# print(word_list)

# print("---------------------------------------------------------------")

dn1_count = []

for e in d1_count:
    if e != 0:
        print(e)
        e=1
    else:
        print(0)
    dn1_count.append(e)

# print(dn1_count)

# print("---------------------------------------------------------------")

dn2_count = []

for r in d2_count:
    if r != 0:
        print(r)
        r=1
    else:
        print(0)
    dn2_count.append(r)

# print(dn2_count)

# print("---------------------------------------------------------------")

dn1_result = np.array(dn1_count)
# print(dn1_result)

dn2_result = np.array(dn2_count)
# print(dn2_result)

# print("---------------------------------------------------------------")

dn_result = dn1_result + dn2_result
# print(dn_result) # 토큰이 등장한 문서수

# print("---------------------------------------------------------------")

d_N_array = np.array(d_N)
# print(d_N_array)

# IDF

IDF = []

for t in dn_result:
    a = ln(d_N_array/t)
    IDF.append(a)

# print(IDF)

## TF-IDF

# d1 TF-IDF

d1_TF1 = np.array(d1_TF)
# print(d1_TF1)

IDF1 = np.array(IDF)
# print(IDF1)

d1_TF_IDF = d1_TF1*IDF1
# print(d1_TF_IDF)

# d2 TF-IDF

d2_TF2 = np.array(d2_TF)
# print(d2_TF2)

d2_TF_IDF = d2_TF2*IDF1
# print(d2_TF_IDF)