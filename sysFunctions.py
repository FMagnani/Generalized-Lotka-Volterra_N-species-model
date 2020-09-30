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
import shutil
import os

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

def save_data(data, name = datetime.now()):
    """
    Parameters
    ----------
        data: Dataframe to be saved
        name: str - Name given to the file
    Save permanently the current status of the system as csv in the 
    directory 'Saved_States'.
    """
    if (data == 'status'):    
        with open('setUpData.csv') as f:
            shutil.copy(f, '/Saved_States')
            os.rename('/Saved_States/dataname', 
                      '/Saved_States/setUpData_{}'.format(name))
    if (data == 'solution'):
         with open('solutionData.csv') as f:
            shutil.copy(f, '/Saved_Solutions')
            os.rename('/Saved_Solutions/dataname', 
                      '/Saved_Solutions/solutionData_{}'.format(name))
    if (data == 'plot'):
        with open('plotData.csv') as f:
            shutil.copy(f, '/Saved_Plots')
            os.rename('/Saved_Plots/dataname', 
                      '/Saved_Plots/plotData_{}'.format(name))
    
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


















