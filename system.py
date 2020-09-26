#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 09:52:55 2020

@author: FMagnani
"""


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
    
    """
    
    def __init__(self, name, interactions):
        """
        This method creates the dictionary specifying the interaction of
        this species with respect to all the others, and updates the 
        informations stored in the Ecosystem.
        """
        
        if (name in self.species_list):
            raise TypeError("Name already existing. Species must have different names.")

        else:
            self.name = name
        
            Ecosystem.species_list.append(name)
    
            self.interactions = {}
    
            for i, j in zip(self.species_list, range(len(self.species_list))):
                self.interactions[(name, i)] = interactions[j]
    
            Ecosystem.intMatrix.update(self.interactions)
    

            
        
#%%     
        

        
        
        
        
        
        
        
        
        
        
        