#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:24:50 2020

@author: FMagnani
"""

import LVsystem
from hypothesis import strategies as st
from hypothesis import given



def test_speciesCreation():
    """
    Create two Species and check that Ecosystem is correctly updated.
    """
    
    sp1 = LVsystem.Species('A', [], [])
    sp2 = LVsystem.Species('B', [2], [])
    
    assert len(sp1.species_list) == len(sp2.species_list)
    assert len(sp1.species_list) == 2
    assert sp2.species_list == ['A','B']
    assert sp1.intMatrix == {('B','A'):2}

def test_classVsInstanceInformation():
    """
    Are the updates visible to all the instances?
    """

    sp1 = LVsystem.Species('A', [], [])
    sp2 = LVsystem.Species('B', [10], [])
    
    assert len(sp1.species_list) == len(LVsystem.Ecosystem.species_list)
    assert len(LVsystem.Ecosystem.species_list) == 2
    assert LVsystem.Ecosystem.species_list == ['A','B']
    assert LVsystem.Ecosystem.intMatrix == {('B','A'):10}

def test_speciesDestruction():    
    """
    Create and destroy two species and check that at every step the Ecosystem
    is correctly updated.
    """
    sp1 = LVsystem.Species('A', [], [])
    sp2 = LVsystem.Species('B', [], [])
    sp3 = LVsystem.Species('C', [], [])

    del sp1
    
    assert len(sp2.species_list) == len(LVsystem.Ecosystem.species_list)
    assert len(LVsystem.Ecosystem.species_list) == 2
    assert not ('A' in LVsystem.Ecosystem.species_list)
    for key in LVsystem.Ecosystem.intMatrix:
        assert not ('A' in key)
    
    del sp2
    
    assert LVsystem.Ecosystem.intMatrix == {}
    assert LVsystem.Ecosystem.species_list == ['C']
    for key in LVsystem.Ecosystem.intMatrix:
        assert not ('B' in key)
    
    del sp3
    
    assert LVsystem.Ecosystem.intMatrix == {}
    assert LVsystem.Ecosystem.species_list == []
    for key in LVsystem.Ecosystem.intMatrix:
        assert not ('C' in key)
    
def test_SpeciesPars():
    """
    Test if the dictionary species_pars in the Ecosystem class is updated
    correctly. 
    """
    
    default = []
    for i in range(LVsystem.SPECIES_PARS):
        default.append(0.5)
    
    sp1 = LVsystem.Species('A', [], [])
    sp2 = LVsystem.Species('AA', [], [])
    
    assert sp1.species_pars == sp2.species_pars
    assert len(sp1.species_pars.keys()) == 2
    
    assert sp1.species_pars == { 'A' : default, 'AA' : default }
    
    del sp1
    
    assert sp2.species_pars == { 'AA' : default }
    
    del sp2
    
    assert LVsystem.Ecosystem.species_pars == {}


def test_createData():
    """
    Tests if the method createData of the class Ecosystem returns correctly 
    the data stored.
    """

    pred1 = LVsystem.Predator('wolf', [], [1,-1,1,1])
    prey1 = LVsystem.Prey('rabbit', [-2], [2,2,2,2])
    pred2 = LVsystem.Predator('fox', [0,3], [3,-3,3,3])
    
    data = LVsystem.Ecosystem.create_data()
        
    assert data[0] == 3
    assert data[1] == ['wolf', 'rabbit', 'fox']
    assert data[2] == [1,2,3]
    assert data[3] == [-1,2,-3]    
    assert data[4] == [1,2,3]
    assert data[5] == [1,2,3]
    assert data[6][1][2] == -data[6][2][1]
    assert data[6][0][0] == 0
    assert data[6][1][1] == 2
    










