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

    
df = pd.DataFrame()

col_names = ['Species','n0','k','K','c']
for i in range(5):
    df[col_names[i]] = system.Ecosystem.create_data()[i+1]

N = len(df.Species)

for i in range(N):
    col = 'A_row'+str(i)
    df[col] = system.Ecosystem.create_data()[6][i]
    
df.to_csv(r'setUpData.csv', index=True, header=True)

code = systemDynamicGenerator.merge_All(N)

output = open("integrator.py","w") 
output.write(code)
output.close() 




















