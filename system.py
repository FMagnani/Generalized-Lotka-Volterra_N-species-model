#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 09:52:55 2020

@author: FMagnani
"""

import logging

#%%

SPECIES_PARS = 4

#%%

class Ecosystem:
    """
    Ecosystem()
    
    This class is used to store and manage the information about the whole
    system of interacting species. It's parent of the class Species, since
    alla its instances must have access to this information. 
    Such information is the list of all the species and the matrix of their
    binary interactions.
    Whenever a new species is created, both these are updated. 
    
    ..note:: This class is not supposed to create instances, but to store
             and manage the information about the system. 
 
    Parameters
    ----------
    none
    
    """
    
    species_list = []
    
    intMatrix = {}
    
    species_pars = {}
    
    
class Species(Ecosystem):
    """
    Species(name, interaction)
    
    Class representing a species, parent of classes Predator and Prey. 
    
    ..note:: This class is not supposed to create instances, but to keep 
             updated the Ecosystem. Instances should be created from Predator 
             or Prey.

    Parameters
    ----------
    name: string
        The name of the Species created. It univocally identifies it.
    
    interaction: array-like, of length equal to the number of species
                 already implemented +1
        It defines the interaction coefficients of this species with respect
        to all the others, and with respect to itself. The order is the same
        as the species list of Ecosystem, and the last value is the 
        ineraction with respect to itself.
        Due to theoretical reasons, this values are bounded to very 
        specific ranges and sign, depending on the type of species they 
        refers to.
        Nevertheless no control is performed by this class, since it is 
        delegated to the classes Predator and Prey. No instances of this
        class are supposed to be created. 

        
    See also
    --------
    Prey
    Predator
    
    Raise
    -----
    TypeError if the chosen name already exists.
    ValueError if the input lists are too long.
    Warning if the input lists are too short (then it is padded).
    
    """
    
    def __init__(self, name, interactions, pars):
        """
        This method creates the dictionary specifying the interaction of
        this species with respect to all the others, and then updates the 
        informations stored in the Ecosystem.
        It also check for the correctness of the inputs eventually padding
        'interactions' or 'pars' with zeros.
        """
        
        other_species = len(Ecosystem.species_list)
        
        if (name in self.species_list):
            raise TypeError("""Name already existing. Species must have different names.""")


        if (len(interactions) > other_species+1):
            raise ValueError("""The length of 'interactions' should be equal to the number of total species +1.""")

        if (len(pars) > SPECIES_PARS):
            raise ValueError('The length of "pars" should be equal to {}'.format(SPECIES_PARS))


        else:
            
             if (len(interactions) < other_species+1):
                 logging.warning("""The length of 'interactions' should be equal to the number of total species +1. The missing value will be set to 0.""")
            
                 interactions = pad_list(interactions, other_species+1)
        
             if (len(interactions) < other_species+1):
                 logging.warning('The length of "pars" should be equal to {}. The missing value will be set to 0.'.format(SPECIES_PARS))
            
                 interactions = pad_list(pars, SPECIES_PARS)
        
             self.name = name
         
             Ecosystem.species_list.append(name)
    
             self.interactions = {}          
             
             for i, j in zip(Ecosystem.species_list, range(other_species+1)):
                 self.interactions[(name, i)] = interactions[j]
                 
             Ecosystem.intMatrix.update(self.interactions)
            
             self.pars = {self.name : pars}
            
             Ecosystem.species_pars.update(self.pars)
            
    
    def __del__(self):
        """
        This method removes  all the interactions in which the instance 
        was involved, stored in the class Ecosystem.
        """
        
        Ecosystem.species_list.remove(self.name)
        
        key_blacklist =[]
        for key in Ecosystem.intMatrix.keys():
            if (self.name in key):
                key_blacklist.append(key)
        for key in key_blacklist:
            Ecosystem.intMatrix.pop(key)
            
        key_blacklist = []
        for key in Ecosystem.species_pars:
            if (self.name == key):
                key_blacklist.append(key)
        for key in key_blacklist:
            Ecosystem.species_pars.pop(key)
               
       

#%%
            
   
def pad_list(list_to_pad, new_length):
        
    missing = new_length - len(list_to_pad)
        
    for i in range(missing):
        list_to_pad.append(0)
            
    return list_to_pad
    
    
        
        
        
            
        


#%%     
        
class Prey(Species):
    pass

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        