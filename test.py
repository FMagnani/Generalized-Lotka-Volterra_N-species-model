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
    
    sys = LVsystem.Ecosystem()
    sys.addSpecies('rabbit')
    sys.addSpecies('fox')
    sys.setInteraction('rabbit', 'fox', -1)
    sys.setInteraction('fox', 'rabbit',  1)
    sys.setInitialCond('rabbit', 10)
    sys.setInitialCond('fox', 5)
    sys.setGrowthRate('rabbit', 1)
    sys.setGrowthRate('fox', -1)
    sys.setCarrCap('rabbit', 10000)
    sys.setCarrCap('fox', 10000)
    sys.setChangeRate('rabbit', 10)
    sys.setChangeRate('fox', 20)        
    
    assert len(sys.species_list) == 2
    assert sys.species_list == ['rabbit','fox']
    assert sys.intMatrix == {('rabbit','fox'):-1, ('fox','rabbit'):1}

    sys.removeSpecies('rabbit')
    sys.removeSpecies('fox')


def test_speciesDestruction():    
    """
    Create and destroy two species and check that at every step the Ecosystem
    is correctly updated.
    """
    sys = LVsystem.Ecosystem()
    sys.addSpecies('rabbit')
    sys.addSpecies('fox')
    sys.addSpecies('wolf')
    
    sys.removeSpecies('fox')
    
    assert len(sys.species_list) == 2
    assert not ('fox' in sys.species_list)
    for key in sys.intMatrix:
        assert not ('fox' in key)
    
    sys.removeSpecies('wolf')
    
    assert sys.species_list == ['rabbit']
    for key in sys.intMatrix:
        assert not ('wolf' in key)
    
    sys.removeSpecies('rabbit')        
    
    assert sys.intMatrix == {}
    assert sys.species_list == []
    for key in sys.intMatrix:
        assert not ('rabbit' in key)
        

def test_createData():
    """
    Tests if the method createData of the class Ecosystem returns correctly 
    the data stored.
    """

    sys = LVsystem.Ecosystem()

    sys.addSpecies('rabbit')
    sys.setInteraction('rabbit', 'hen', 0)
    sys.setInteraction('rabbit', 'fox', -1)
    sys.setInitialCond('rabbit', 30)
    sys.setGrowthRate('rabbit', 0.09)
    sys.setCarrCap('rabbit', 10000)
    sys.setChangeRate('rabbit', 400)

    sys.addSpecies('hen')
    sys.setInteraction('hen', 'rabbit', 0)
    sys.setInteraction('hen', 'fox', -1)
    sys.setInitialCond('hen', 10)
    sys.setGrowthRate('hen', 0.07)
    sys.setCarrCap('hen', 10000)
    sys.setChangeRate('hen', 500)

    sys.addSpecies('fox')
    sys.setInteraction('fox', 'rabbit', 1)
    sys.setInteraction('fox', 'hen', 1)
    sys.setInitialCond('fox', 20)
    sys.setGrowthRate('fox', -0.06)
    sys.setCarrCap('fox', 1)
    sys.setChangeRate('fox', 250)

    
    data = sys.create_data()
        
    assert data[0] == 3
    assert data[1] == ['rabbit', 'hen', 'fox']
    assert data[2] == [30,10,20]
    assert data[3] == [0.09,0.07,-0.06]    
    assert data[4] == [10000,10000,1]
    assert data[5] == [400,500,250]
    assert data[6][1][2] == -data[6][2][1]
    assert data[6][2][2] == 0
    
    sys.removeSpecies('rabbit')
    sys.removeSpecies('fox')
    sys.removeSpecies('hen')


def test_loadData():
    """Loads a known setup and checks if it has been loaded correctly."""
    
    sys = LVsystem.Ecosystem()
    
    sys.loadSetup('2Prey1Predator')
    
    
    data = sys.create_data()
    
    assert data[0] == 3
    assert data[1] == ['rabbit', 'hen', 'fox']
    assert data[2] == [30,10,20]
    assert data[3] == [0.09,0.07,-0.06]    
    assert data[4] == [10000,10000,1]
    assert data[5] == [400,500,250]
    assert data[6][1][2] == -data[6][2][1]
    assert data[6][2][2] == 0

    sys.removeSpecies('rabbit')
    sys.removeSpecies('fox')
    sys.removeSpecies('hen')



