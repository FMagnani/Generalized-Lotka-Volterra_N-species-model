#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:24:50 2020

@author: FMagnani
"""

import system
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


















#%%