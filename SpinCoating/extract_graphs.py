
# coding: utf-8

# In[54]:
# $a

import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

h = 6.626 * 10**(-34) *(10**19)/1.6
c = 299792458

fig = plt.figure()
k = 0.20

if(len(sys.argv)!=5 and len(sys.argv)!=3 ): #and len(sys.argv)!=5):
    sys.exit("usage:\nInput: <text or csv file> <value of thickness in nm> \nOutput: \n1. graph of func = (alpha*hc/lambda)^2 vs E(eV)\n2. graph of E against derivative of func\n3. CSV file containing output table \nThe function graph will be displayed, \nWatch the graph and enter the appropriate range \nOf energy value in eV")

# $d
def derivative(x,y):
    ly = len(y)
    lx = len(x)
    if(ly != lx):
        print('derivative error')
    diff = [0]
    for i in range(ly-1):
        diff.append((y[i+1]-y[i])/(x[i+1]-x[i]))
    return diff
# $h

# extracting the name of the file
filename = sys.argv[1]
temp = filename.split(".")
output = 'output_'+temp[0]+'.csv'

# Variables to be computed
W = [] # wavelength
Tp = [] # tramittance percentage
T = [] # tramittance
lnT = [] # log tranmittance
D = np.float64(sys.argv[2]) # distance in nanometers


# $i
# get the key given the value inside any sorted array
def extract_key(value, array):
    for i in range(len(array)-1):
        #print(value,array[i],array[i+1],i)
        if(value>min(array[i],array[i+1]) and value<max(array[i],array[i+1])):
            return i
        continue
        
# get data from file
def getWTp(filename):
    W = []
    Tp = []
    with open(filename,'r') as fi:
        csv_reader = csv.reader(fi)
        for row in csv_reader:
            try:
                Tp.append(float(row[1]))
                W.append(float(row[0]))
                continue
            except:
                continue
        return W,Tp

# get intercept function
def getIntercept(e,f1):
    #print(e)
    while(True):
        x1 = np.float64(input('Enter first energy value: '))
        x2 = np.float64(input('Enter second energy value: '))
        k1 = extract_key(x1,e)
        k2 = extract_key(x2,e)
        y1 = f1[k1]
        y2 = f1[k2]
        m = (y2-y1)/(x2-x1)
        intercept = x1 - y1/m
        print("intercept in eV:")
        print(intercept)
        reply = input("Redo? [y/n]: ")
        if(reply=='n'):
            return m,intercept
        continue

def stLine(x,x_intercept, slope):
	return slope*(x - x_intercept)
# $s

W, Tp = getWTp(filename)

W = np.array(W)
Tp = np.array(Tp)

# Extract Data from the array
if(np.max(Tp[0])>1): T = Tp/100
else: 
    T = Tp
    Tp = Tp*100

# Logarithmic Transmittance
lnT = np.log(T) # natural logarithm

# Alpha
alpha = -(lnT)/D

# Energy
e = (h*c/W)*(10**(9))

# Choose the right function:

#f1 = alpha*(e**(1/2))
#f1 = (alpha*e)**(1/2)
f1 = (alpha*e)**(2)
der = derivative(e,f1)
# $h

# Write it all into a csv
with open(output,'w') as fo:
    csv_writer = csv.writer(fo)
    csv_writer.writerow(['wavelength (nm)',
                         'Percentage Transmittance',
                         'Transmittance',
                         'logarithmic transmittance lnT',
                         'Thickness (nm)','alpha = lnT/D (per nm)',
                         'energy(J)','parameter','derivative'])
    for i in range(len(T)):
        row = [W[i],Tp[i],T[i],lnT[i],D,alpha[i],e[i],f1[i],der[i]]
        csv_writer.writerow(row)

# save the energy vs function plot
plt.plot(e,f1,label = '$y = (alpha*(E))^2, $x = E (J)')
plt.grid(color='r',linestyle='-',linewidth=0.1)
plt.show()
name1 = temp[0]+'_graph.png'
fig.savefig(name1)
"""
# superimpose the derivative plot
d1 = der#[key_start:key_last]
plt.plot(e,der,label = '$y = (alpha*sqrt(E))^2, $x = E (J)')
name2 = temp[0]+'_derivative.png'
fig.savefig(name2)
"""
# get start and end values for derivative
while(True):
	m, intercept = getIntercept(e,f1)
	# k = extract_key(intercept,e)
	line = []
	line1 = []
	for i in range(len(e)):
		line1.append(0)
		line_value = stLine(e[i],intercept,m)
		if(line_value<0):
			line.append(0)
			continue
		line.append(line_value)
	

	plt.plot(e,line,label = '$y = (alpha*(E))^2, $x = E (J)')
	plt.plot(e,f1)
	plt.plot(e,line1)
	name3 = temp[0]+'_FINAL.png'
	# fig.savefig(name3)
	plt.ylim(0,max(f1))
	plt.xlabel('Photon energy in eV')
	plt.ylabel('(alpha*energy) squared in sq.(eV/m)')
	plt.title(name3)
	plt.show()
	fig.savefig(name3)
	answer = input('Exit? [y/n]: ')
	if(answer=='y'):
		break

sys.exit('Auf Wiedersehen')