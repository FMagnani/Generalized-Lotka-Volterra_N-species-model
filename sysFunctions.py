#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:16:12 2020

@author: FMagnani
"""

import systemDynamicGenerator
import pandas as pd 

def pad_list(list_to_pad, new_length, padding_value):
    """

    Parameters
    ----------
    list_to_pad : list
        This is the list to be padded with zeros up to length new_length.
    new_length : int
        Must be greater than the length of list_to_pad. It is the length of
        the returned list.
    padding_value: float
        The value used to pad the list.

    Returns
    -------
    list

    """
        
    if (len(list_to_pad) > new_length):
        raise ValueError("The new length of the list must be greater than the original length.")
    
    missing = new_length - len(list_to_pad)
        
    for i in range(missing):
        list_to_pad.append(padding_value)
            
    return list_to_pad       
        
 
def create_dataSetUp(data, N):
    """
        N: int - dimension of the system (number of species)
    Creates a DataFrame with the current status of the system.
    """
    
    df = pd.DataFrame()

    col_names = ['Species','n0','k','K','c']
    for i in range(5):
        df[col_names[i]] = data.create_data()[i+1]

    for i in range(N):
        col = 'A_row'+str(i)
        df[col] = data.create_data()[6][i]
    
    return df

   
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


















