# created by Adhish on 21-01-2019

import numpy as np
import sys


# In[12]:


def usage():
    if(len(sys.argv) != 6):
        sys.exit("Usage:\nInput: <i12> <v34> <i14> <v23> <d> \nOutput: resistivity")


# In[13]:


usage()
i12 = float(sys.argv[1])
v34 = float(sys.argv[2])
i14 = float(sys.argv[3])
v23 = float(sys.argv[4])
d = float(sys.argv[5])


# In[7]:


def f(x,R1234,R1423):
    return np.exp(-3.14*R1234/x) + np.exp(-3.14*R1423/x)


# In[8]:


def getR(i12,v34,i14,v23):
    R1234 = v34/i12
    R1423 = v23/i14
    ub = float(100*(R1234+R1423)/2)
    lb = float(0)
    while(np.abs(ub-lb)>0.01):
        mid = (lb+ub)/2
        print(mid)
        ex = f(mid,R1234,R1423)
        if(ex>1):
            ub = mid
        elif(ex<1):
            lb = mid
    return mid


# In[9]:


R = getR(i12,v34,i14,v23)
rho = R*d
print("Rs obtained:")
print(R)
print("resistivity obtained:")
print(rho)


