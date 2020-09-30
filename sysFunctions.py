#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:16:12 2020

@author: FMagnani
"""

import system
import systemDynamicGenerator
import pandas as pd
from datetime import datetime

def solve(max_time=20, t_steps=2**7+1):
    """
    Parameters
    ----------
    t_steps : int
        Number of steps in which the time is divided.
        In the form 2**n +1 performance is increased.
    max_time : float
        Maximum time reached in the integration.

    """
    N = len(system.Ecosystem.species_list)
    df = create_dataSetUp(N)
    df.to_csv(r'setUpData.csv', index=True, header=True)
    generate_Integrator(N, max_time, t_steps)
    exe_Integrator()

def create_dataSetUp(N):
    """
        N: int - dimension of the system (number of species)
    Creates a DataFrame with the current status of the system.
    """
    
    df = pd.DataFrame()

    col_names = ['Species','n0','k','K','c']
    for i in range(5):
        df[col_names[i]] = system.Ecosystem.create_data()[i+1]

    for i in range(N):
        col = 'A_row'+str(i)
        df[col] = system.Ecosystem.create_data()[6][i]
    
    return df

def save_dataSetUp(df, name = datetime.now()):
    """
    Parameters
    ----------
        df: Dataframe to be saved
        name: str - Name given to the file
    Save permanently the current status of the system as csv in the 
    directory 'Saved_States'.
    """
    df.to_csv(r'/Saved_States/setUpData_{}'.format(name), 
                  index=True, header=True)

    
def generate_Integrator(N, t_max, t_step):
    """
        N: int - dimension of the system (number of species)
    Dynamical generation of Integrator.py.
    An example of the code is the file 'Integrator_Example.py', or can be 
    seen here:
        ---link---
    """
    
    code = systemDynamicGenerator.merge_All(N, t_max, t_step)

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


















