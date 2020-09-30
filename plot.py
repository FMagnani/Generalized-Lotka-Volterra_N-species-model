#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 16:54:06 2020

@author: fede
"""

import pandas as pd
import matplotlib.pyplot as plt


def plot():
    data = pd.read_csv('solutionData.csv')

    Species_names = list(data.columns[1:])
    N = len(Species_names)
    t = list(data['Unnamed: 0'])

    fig, ax = plt.subplots()
    for i, name in zip(range(N), Species_names):
        nt = list(data[name])
        ax.plot(t, nt, linewidth=4, label=name)

    ax.set_facecolor('white')
    ax.legend(loc='best')
