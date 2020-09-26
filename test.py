#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:24:50 2020

@author: fede
"""

import system
from hypothesis import strategies as st
from hypothesis import given

#%%

@given(a=st.just(1),b=st.just(2),c=st.just(3), A=st.just('A'),B=st.just('B'))
def test_speciesCreation(a,b,c,A,B):
    """
    Create two Species and check that Ecosystem is correctly updated.
    """
    sp1_inter = []
    sp1_inter.append(a)
    sp2_inter=[]
    sp2_inter.append(b)
    sp2_inter.append(c)
    
    sp1 = system.Species(A, sp1_inter)
    sp2 = system.Species(B, sp2_inter)
    
    assert len(sp1.species_list) == len(sp2.species_list)
    assert len(sp1.species_list) == 2
    assert sp2.species_list == [A,B]
    assert sp1.intMatrix == {(A,A):1,
                             (B,A):2,
                             (B,B):3}




#%%