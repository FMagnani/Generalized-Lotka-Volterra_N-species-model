#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 14:18:35 2020

@author: FMagnani
GitHub repo: https://github.com/FMagnani/Lotka_Volterra_N_species_model

"""

def merge_All(N, max_time, t_steps):

    """
    Creates the string containing the whole code of integartor.py.
    You can see the example of a possible code created in the file
    'Integrator_Example.py', or here:
    https://github.com/FMagnani/Generalized-Lotka-Volterra_N-species-model/tree/master/integrator_example

    Parameters
    ----------
    N: int 
        Number of species (i.e. of equations in the system)
    max_time: float
        Maximum time reached in the integration
    t_steps: int
        Number of steps in which the time is divided. 
        In the form 2**n +1 performance is increased.
    """
    
    max_time = str(max_time)
    t_steps = str(t_steps)
    
    intro = \
"""from scipy.integrate import odeint
import pandas as pd
import numpy as np

data =pd.read_csv("setup.csv")

t = np.linspace(0,"""+ max_time +','+ t_steps +""")

names = list(data['Species'])
n0 = list(data['n0'])
k = list(data['k'])
K = list(data['K'])
c = list(data['c'])
N = len(k)
A = []
for i in (range(N)):\n    A.append( list(data['A_row'+str(i)]) )"""

    outro =\
"""\nsol_unzip = list(zip(*sol))
data = pd.DataFrame()
for i, name in zip(range(N), names):
    data[name] = sol_unzip[i]
    
data.to_csv(r'solution.csv', index=True, header=True)
"""

    code = intro + create_Module(N) + outro

    return code    


def current_system(data):
    """
    Returns the system of equations with current variables values, as a string.
    """
    
    k = data.create_data()[3]
    c = data.create_data()[5]
    A = data.create_data()[6]
    N = len(k)
    
    sys =[]
    string_sys = ''
    
    for i in range(N):
        sys.append( '    dn'+str(i)+'dt = '+str(k[i])+'*n'+str(i)+' + '+str(A[i][i])
                   +('*n'+str(i))*2+'/'+str(c[i]) )
               
    for i in range(N):
        for j in range(N)[i:]:
            if not (i==j):
                sys[i] +=' + '+str(A[i][j])+'*n'+str(i)+'*n'+str(j)+'/'+str(c[i])
                sys[j] +=' - '+str(A[i][j])+'*n'+str(j)+'*n'+str(i)+'/'+str(c[j])
    
    for i in range(N):
        string_sys += sys[i] + '\n'     
        
    return string_sys

    
    

def create_Module(N):
    """
    It creates the main module of the generated code, that depends on
    the current dimension of the system.
    """
    
    str0 = create_Strings(N)[0]
    str2 = create_Strings(N)[2]
    str4 = create_Strings(N)[4]
    str3 = create_Strings(N)[3]
    str1 = create_Strings(N)[1]
    str5 = create_Strings(N)[5]
    
    module = '\ndef system (y, t, '+ str0 +'):\n' \
             +'\n    '+ str2 +' = y\n' \
             +'\n'+ str4 \
             +'\n    dydt = ['+ str3 +']\n' \
             +'\n    return dydt\n' \
             +'\nsol = odeint(system,('+ str5 +'), t, args=('+ str1 +'))\n'
    
    return module




def create_Strings(N):
    """
    Creates the strings needed for the dynamical generation. They depends
    on the current dimension of the system.
    
    Parameters
    ----------
        N: int
    The dimension of the system.

    Returns
    -------
        A tuple with 5 strings.
        return[0]: The string specifying the arguments for the function 
                   'system'.
        return[1]: The string specifying the arguments for the function
                   'odeint'.
        return[2]: The string for the definition of the variables inside the
                   function 'system'.
        return[3]: The string for the definition of the solution dydt inside
                   function 'system'.
        return[4]: The string defining the system of equations itself.
        return[5]: The string defining the second argument (initial values) 
                   for odeint.
    
    """
    
    string_vars = ''
    string_args = ''
    string_n = ''
    string_dndt = ''
    string_sys = ''
    string_n0 = ''
    
    for i in range(N):
        string_vars += 'k' + str(i) + ','
        
        string_args += 'k[' + str(i) + '],'
        
        string_n += 'n' + str(i) + ','
        
        string_n0 += 'n0[' + str(i) + '],'
        
        string_dndt += 'dn' + str(i) + 'dt,' 
    
        
    for i in range(N):
        string_vars += 'K' + str(i) + ','
        
        string_args += 'K[' + str(i) + '],'
        
    for i in range(N):
        string_vars += 'c' + str(i) + ','
        
        string_args += 'c[' + str(i) + '],'
        
    sys = []    
    
    for i in range(N):
        sys.append( '    dn'+str(i)+'dt = k'+str(i)+'*n'+str(i)+' + A'+str(i)*2
                   +('*n'+str(i))*2+'/c'+str(i) )
        
    
        
    for i in range(N):
        for j in range(N)[i:]:
            string_vars += 'A' + str(i) + str(j) + ','
        
            string_args += 'A[' + str(i) + '][' + str(j) + '],'
            
            if not (i==j):
                sys[i] +=' + A'+str(i)+str(j)+'*n'+str(i)+'*n'+str(j)+'/c'+str(i)
                sys[j] +=' - A'+str(i)+str(j)+'*n'+str(j)+'*n'+str(i)+'/c'+str(j)
     
    for i in range(N):
        string_sys += sys[i] + '\n'          
    
        
    return (string_vars[:-1], string_args[:-1], string_n[:-1], 
            string_dndt[:-1], string_sys, string_n0[:-1])
    
    
    
    
    
  
