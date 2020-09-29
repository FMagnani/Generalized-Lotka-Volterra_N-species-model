#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:16:12 2020

@author: fede
"""

import system
import systemDynamicGenerator
import pandas as pd

sp1 = system.Prey('rabbit', [], [10, 1, 10000, 10])
sp2 = system.Predator('wolf', [1], [5, -1, 1, 20])



def create_dataSetUp():
    """
    Creates a DataFrame with the current status of the system.
    """
    
    df = pd.DataFrame()

    col_names = ['Species','n0','k','K','c']
    for i in range(5):
        df[col_names[i]] = system.Ecosystem.create_data()[i+1]

    N = len(df.Species)

    for i in range(N):
        col = 'A_row'+str(i)
        df[col] = system.Ecosystem.create_data()[6][i]
    
    return df

def save_dataSetUp(df, name =''):
    """
    Creates a csv file with the current status of the system.
    If the parameter 'name' is given, the state will be saved permanently 
    in the directory 'Saved_States'.
    """    
    df.to_csv(r'setUpData.csv', index=True, header=True)
    if not (name == ''):
        df.to_csv(r'/Saved_States/setUpData_{}'.format(name), 
                  index=True, header=True)    
    
def generate_Integrator():
    """
    Dynamical generation of Integrator.py.
    An example of the code is the file 'Integrator_Example.py', or can be 
    seen here:
        ---link---
    """
    N = len(system.Ecosystem.species_list)
    
    code = systemDynamicGenerator.merge_All(N)

    output = open("integrator.py","w") 
    output.write(code)
    output.close() 
      
def exe_Integrator():
    """    
    Execute the previously generated file 'Integrator.py'.
    It will output the file "solutionData.csv".
    """
    with open("integrator.py") as f:
        code = compile(f.read(), "integrator.py", 'exec')
        exec(code)


















