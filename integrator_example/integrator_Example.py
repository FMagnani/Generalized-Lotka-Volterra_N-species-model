# This is the file "integrator.py" which is created in the case with 2 speceies in the system.
# Similar files are created and then executed by the software for different number of species.

from scipy.integrate import odeint
import pandas as pd
import numpy as np

data =pd.read_csv("setup.csv")

t = np.linspace(0,20,129)

names = list(data['Species'])
n0 = list(data['n0'])
k = list(data['k'])
K = list(data['K'])
c = list(data['c'])
N = len(k)
A = []
for i in (range(N)):
    A.append( list(data['A_row'+str(i)]) )
def system (y, t, k0,k1,K0,K1,c0,c1,A00,A01,A11):

    n0,n1 = y

    dn0dt = k0*n0 + A00*n0*n0/c0 + A01*n0*n1/c0
    dn1dt = k1*n1 + A11*n1*n1/c1 - A01*n1*n0/c1

    dydt = [dn0dt,dn1dt]

    return dydt

sol = odeint(system,(n0[0],n0[1]), t, args=(k[0],k[1],K[0],K[1],c[0],c[1],A[0][0],A[0][1],A[1][1]))

sol_unzip = list(zip(*sol))
data = pd.DataFrame()
for i, name in zip(range(N), names):
    data[name] = sol_unzip[i]
    
data.to_csv(r'solution.csv', index=True, header=True)
