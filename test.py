#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:24:50 2020

@author: fede
"""

import system
from hypothesis import strategies as st
from hypothesis import given



@given(a=st.just(1),b=st.just(2),c=st.just(3), A=st.just('A'),B=st.just('B'))
def test_speciesCreation(a,b,c,A,B):
    """
    Create two Species and check that Ecosystem is correctly updated.
    """
    sp1_inter = [a]
    sp2_inter = [b]
    sp2_inter.append(c)

    sp1 = system.Species(A, sp1_inter, [])
    sp2 = system.Species(B, sp2_inter, [])
    
    assert len(sp1.species_list) == len(sp2.species_list)
    assert len(sp1.species_list) == 2
    assert sp2.species_list == [A,B]
    assert sp1.intMatrix == {(A,A):1,
                             (B,A):2,
                             (B,B):3}

@given(a=st.just(1),b=st.just(2),c=st.just(3), A=st.just('A'),B=st.just('B'))
def test_classVsInstanceInformation(a,b,c,A,B):
    """
    Are the updates visible to all the instances?
    """
    sp1_inter = [a]
    sp2_inter = [b]
    sp2_inter.append(c)

    sp1 = system.Species(A, sp1_inter, [])
    sp2 = system.Species(B, sp2_inter, [])
    
    assert len(sp1.species_list) == len(system.Ecosystem.species_list)
    assert len(system.Ecosystem.species_list) == 2
    assert system.Ecosystem.species_list == [A,B]
    assert system.Ecosystem.intMatrix == {(A,A):1,
                             (B,A):2,
                             (B,B):3}

#@given(A=st.text(min_size=1, max_size=2), B=st.text(min_size=3, max_size=4))
def test_speciesDestruction():    
    """
    Create and destroy two species and check that at every step the Ecosystem
    is correctly updated.
    """
    sp1_inter = [1]
    sp2_inter = [2]
    sp2_inter.append(3)
    sp3_inter = [4]
    sp3_inter.append(5)
    sp3_inter.append(6)

    sp1 = system.Species('A', sp1_inter, [])
    sp2 = system.Species('B', sp2_inter, [])
    sp3 = system.Species('C', sp3_inter, [])

    del sp1
    
    assert len(sp2.species_list) == len(system.Ecosystem.species_list)
    assert len(system.Ecosystem.species_list) == 2
    assert not ('A' in system.Ecosystem.species_list)
    for key in system.Ecosystem.intMatrix:
        assert not ('A' in key)
    
    del sp2
    
    assert system.Ecosystem.intMatrix == {('C','C'):6}
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
    
    zeros = []
    for i in range(system.SPECIES_PARS):
        zeros.append(0)
    
    sp1 = system.Species('A', [], [1])
    sp2 = system.Species('AA', [], [])
    
    assert sp1.species_pars == sp2.species_pars
    assert len(sp1.species_pars.keys()) == 2
    
    assert sp1.species_pars == { 'A' : [1], 'AA' : zeros }
    
    del sp1
    
    assert sp2.species_pars == { 'AA' : zeros }
    
    del sp2
    
    assert system.Ecosystem.species_pars == {}


















#%%