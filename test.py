#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:24:50 2020

@author: FMagnani
"""

import system
import systemDynamicGenerator
from hypothesis import strategies as st
from hypothesis import given



def test_speciesCreation():
    """
    Create two Species and check that Ecosystem is correctly updated.
    """
    
    sp1 = system.Species('A', [], [])
    sp2 = system.Species('B', [2], [])
    
    assert len(sp1.species_list) == len(sp2.species_list)
    assert len(sp1.species_list) == 2
    assert sp2.species_list == ['A','B']
    assert sp1.intMatrix == {('B','A'):2}

def test_classVsInstanceInformation():
    """
    Are the updates visible to all the instances?
    """

    sp1 = system.Species('A', [], [])
    sp2 = system.Species('B', [10], [])
    
    assert len(sp1.species_list) == len(system.Ecosystem.species_list)
    assert len(system.Ecosystem.species_list) == 2
    assert system.Ecosystem.species_list == ['A','B']
    assert system.Ecosystem.intMatrix == {('B','A'):10}

def test_speciesDestruction():    
    """
    Create and destroy two species and check that at every step the Ecosystem
    is correctly updated.
    """
    sp1 = system.Species('A', [], [])
    sp2 = system.Species('B', [], [])
    sp3 = system.Species('C', [], [])

    del sp1
    
    assert len(sp2.species_list) == len(system.Ecosystem.species_list)
    assert len(system.Ecosystem.species_list) == 2
    assert not ('A' in system.Ecosystem.species_list)
    for key in system.Ecosystem.intMatrix:
        assert not ('A' in key)
    
    del sp2
    
    assert system.Ecosystem.intMatrix == {}
    assert system.Ecosystem.species_list == ['C']
    for key in system.Ecosystem.intMatrix:
        assert not ('B' in key)
    
    del sp3
    
    assert system.Ecosystem.intMatrix == {}
    assert system.Ecosystem.species_list == []
    for key in system.Ecosystem.intMatrix:
        assert not ('C' in key)
    
def test_SpeciesPars():
    """
    Test if the dictionary species_pars in the Ecosystem class is updated
    correctly. 
    """
    
    default = []
    for i in range(system.SPECIES_PARS):
        default.append(0.5)
    
    sp1 = system.Species('A', [], [])
    sp2 = system.Species('AA', [], [])
    
    assert sp1.species_pars == sp2.species_pars
    assert len(sp1.species_pars.keys()) == 2
    
    assert sp1.species_pars == { 'A' : default, 'AA' : default }
    
    del sp1
    
    assert sp2.species_pars == { 'AA' : default }
    
    del sp2
    
    assert system.Ecosystem.species_pars == {}



def test_PreyPredatorInput():
    """
    Test if the classes Prey and Predators correctly changes the given input.
    """
    
    pred = system.Species('wolf', [], [])
    prey = system.Prey('rabbit', [5], [1,-1,-1,-1])
    
    assert system.Ecosystem.intMatrix == { ('rabbit', 'wolf') : -5 }
    assert prey.pars == {'rabbit' : [1,1,1,1]}

    del pred
    
    pred = system.Predator('wolf', [0], [1,1,-1,-1])
    
    assert system.Ecosystem.intMatrix == { ('wolf', 'rabbit') : 0 }
    assert pred.pars == {'wolf' : [1,-1,-1,1]}


def test_createData():
    """
    Tests if the method createData of the class Ecosystem returns correctly 
    the data stored.
    """

    pred1 = system.Predator('wolf', [], [1,-1,1,1])
    prey1 = system.Prey('rabbit', [-2], [2,2,2,2])
    pred2 = system.Predator('fox', [0,3], [3,-3,3,3])
    
    data = system.Ecosystem.create_data()
        
    assert data[0] == 3
    assert data[1] == ['wolf', 'rabbit', 'fox']
    assert data[2] == [1,2,3]
    assert data[3] == [-1,2,-3]    
    assert data[4] == [1,2,3]
    assert data[5] == [1,2,3]
    assert data[6][1][2] == -data[6][2][1]
    assert data[6][0][0] == 0
    assert data[6][1][1] == 2
    
    

#%%















