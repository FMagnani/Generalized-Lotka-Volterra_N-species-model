#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 09:52:55 2020

@author: FMagnani
"""

import logging
import numpy as np

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
    
    @classmethod
    def create_data(cls):
        """
        

        Parameters
        ----------
        cls : TYPE
            DESCRIPTION.

        Returns
        -------
        An ordered tuple of arrays.
        return[0]: N  -number of species/ dimension of the system 
        return[1]: list of the species' names 
        return[2]: n0 -array of initial conditions
        return[3]: k  -array of k pars
        return[4]: K  -array of K pars
        return[5]: c  -array of c pars
        return[6]: A  -interaction Matrix
    
        The order of the values of each array is the same as the list of 
        species' name.
        So n0[0] refers to the species 'names[0]' and so on.
        """
        
        N = len(cls.species_list)


        n0 = []
        k = []
        K = []
        c = []
        for key in cls.species_list:
            n0.append(cls.species_pars[key][0])
            k.append(cls.species_pars[key][1])
            K.append(cls.species_pars[key][2])
            c.append(cls.species_pars[key][3])
        
        A = cls.dict_into_matrix(k, K, c)
        
        return (N, cls.species_list, n0, k, K, c, A)
        
    
    @classmethod
    def dict_into_matrix(cls, k, K, c):
        """
        This method takes the interaction matrix, that is a dict with keys 
        of shape (2,1), without "diagonal" entries, without "reciprocal" entries.
        "No diagonal entries" means the absence of keys = ('Name','Name').
        "No reciprocal entries" means that if ('Name1','Name2') is present,
        ('Name2','Name1') must be absent.
        Then the dictionary is converted into the square antysimmetric matrix
        needed by the system.
        Parameters k, K, c are needed in order to compute the diagonal 
        values.

        
        Returns
        -------
        A square antisymetric matrix, with diagonal entries obtained 
        with the formula:
            
            aii = int(ki>0)*(ci ki)/Ki 
            
        See the documentation for further informations.
        """
        
        N = len(cls.species_list)
        
        to_add = {}

        for key in Ecosystem.intMatrix:
            if not (key[0] == key[1]):
                to_add.update({(key[1], key[0]) : - Ecosystem.intMatrix[key]})
        
        cls.intMatrix.update(to_add)
        
        for i, key in zip(range(N), cls.species_list):
            
            aii = int(k[i]>0)*k[i]*K[i]/c[i]
            
            cls.intMatrix.update({(key,key):aii})
                
        A = np.zeros((N,N))
        
        for I, i in zip( cls.species_list, range(N) ):
            for J, j in zip( cls.species_list, range(N) ):     
                A[i][j] = cls.intMatrix[(I,J)]
    
        return A
    
    
class Species(Ecosystem):
    """
    Species(name, interaction, pars)
    
    Class representing a species. 
    
    ..note:: This class is not supposed to create instances, but to keep 
             updated the Ecosystem. Instances should be created from Predator 
             or Prey.

    Parameters
    ----------
    name: string
        The name of the Species created. It univocally identifies it.
    
    interaction: list. 
        Length should be equal to the number of species already implemented. 
        If smaller, it is padded with zeros.
        It defines the interaction coefficients of this species with respect
        to all the others. The order is the same as the species list of 
        Ecosystem.
        
        So if Ecosystem.species_list = [ 'A', 'B']
        and species 'C' is created with interactions = [1, 2]
        to the interaction matrix implemented will be added the following:
        {('C','A') : 1,
         ('C','B') : 2}
        
        Due to theoretical reasons, this values are bounded to very 
        specific ranges and sign.
        In the interaction matrix, a line as
        ('A','C') : 2
        means that 'A' beats 'C' ('C' is eaten by 'A'), while
        ('A','C'): -2
        means that 'C' eats 'A'.
        
        Thus when the list of interactions for a given species is created, 
        one should ask himself, for interactions[i]: "does this species eat 
        Ecosystem.species_list(i) (in such a case, a positive value should
        be inserted), or is this species eaten by Ecosystem.species_list[i]
        (negative value)?"
        
    pars: list. 
        It is the list of the parameters specific to this species.
        Length should be equal to 4. If smaller, it is padded with zeros.
        pars[0]: Initial value for population number (must be >0)
        pars[1]: growth/death rate (depending on the sign).
        pars[2]: carrying capacity.*
        pars[3]: Volterra equivalent number (must be >0).
        
        In the equation:
        
        dx/dt = (ki xi) - (ki xi xi/Ki) - 1/ci (SUM aij xi xj)

        pars[1] = ki
        pars[2] = Ki
        pars[3] = ci
        
        See the documentation for further information on the formula.
        
        *The carrying capacity is not used by the equations related to
        predators. It can be set to any number.
        
    See also
    --------
    Prey
    Predator
    
    Raise
    -----
    TypeError if the chosen name already exists.
    ValueError if the input lists are too long.
    Warning if the input lists are too short (then they are padded).
    
    """
    
    def __init__(self, name, interactions, pars):
        """
        This method creates the dictionary specifying the interaction of
        this species with respect to all the others, and then updates the 
        informations stored in the Ecosystem.
        It also check for the correctness of the inputs. 
        Itventually pads 'interactions' or 'pars' with default values.
        """
        
        other_species = len(Ecosystem.species_list)
        
        if (name in self.species_list):
            raise TypeError("""Name already existing. Species must have different names.""")


        if (len(interactions) > other_species):
            raise ValueError("""The length of 'interactions' should be equal to the number of the other species.""")

        if (len(pars) > SPECIES_PARS):
            raise ValueError('The length of "pars" should be equal to {}'.format(SPECIES_PARS))


        else:
            
             if (len(interactions) < other_species):
                 logging.warning("""The length of 'interactions' should be equal to the number of the other species. The missing values will be set to 0.""")
            
                 interactions = pad_list(interactions, other_species, 0)
        
             if (len(pars) < SPECIES_PARS):
                 logging.warning('The length of "pars" should be equal to {}. The missing value will be set to 0.5.'.format(SPECIES_PARS))
            
                 pars = pad_list(pars, SPECIES_PARS, 0.5)
        
             if (pars[0] < 0):
                  raise ValueError("The first parameter of 'pars' is the initial population number. Must be greater than 0.")

             if (pars[3] < 0):
                  logging.warning("Sign of pars[3] has been changed. It should be positive. See documentation of class 'Species' for further explanations.")
                  pars[3] = -1*pars[3]

        
             self.name = name
         
             Ecosystem.species_list.append(name)
    
             self.interactions = {}          
             
             for i, j in zip(Ecosystem.species_list, range(other_species)):
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
        
class Prey(Species):
    """
    This class is meant to be equivalent to the Species class, but with checks
    on the input parameters in order to help the user not to misunderstand
    their meaning.
    
    See also
    --------
    Species
    Predator
    
    """
    
    def __init__(self, name, interactions, pars):
    
        if (pars[1] < 0):
           logging.warning("Sign of pars[1] has been changed. It should be positive for preys. See documentation of class 'Species' for further explanations.")
           pars[1] *= -1
        
        if (pars[2] == 0):
            raise ValueError("pars[2] must be strictly positive. See documentation of class 'Species' for further explanations.")
        
        if (pars[2] < 0):
            logging.warning("Sign of pars[2] has been changed. It should be positive. See documentation of class 'Species' for further explanations.")
            pars[2] *= -1
                
        for i in range(len(interactions)):
            if (interactions[i] > 0):
                logging.warning("Interaction sign changed. All interactions should be eithr negative or zero for preys.")
                interactions[i] *= -1    
                
        super().__init__(name, interactions, pars)


class Predator(Species):
    """
    This class is meant to be equivalent to the Species class, but with checks
    on the input parameters in order to help the user not to misunderstand
    their meaning.
    
    See also
    --------
    Species
    Prey
    
    """
    
    def __init__(self, name, interactions, pars):
    
        if (pars[1] > 0):
           logging.warning("Sign of pars[1] has been changed. It should be negative for predators. See documentation of class 'Species' for further explanations.")
           pars[1] *= -1
        
        if (pars[2] == 0):
            raise ValueError("pars[2] must be different from zero. See documentation of class 'Species' for further explanations.")
                
        for i in range(len(interactions)):
            if (interactions[i] < 0):
                logging.warning("Interaction sign changed. All interactions should be eithr positive or zero for predators.")
                interactions[i] *= -1    
                
        super().__init__(name, interactions, pars)



        
#%%

def pad_list(list_to_pad, new_length, padding_value):
    """

    Parameters
    ----------
    list_to_pad : list
        This is the list to be padded with zeros up to length new_length.
    new_length : int
        Must be greater than the length of list_to_pad. It is the length of
        the returned list.
    padding_value: float
        The value used to pad the list.

    Returns
    -------
    list

    """
        
    if (len(list_to_pad) > new_length):
        raise ValueError("The new length of the list must be greater than the original length.")
    
    missing = new_length - len(list_to_pad)
        
    for i in range(missing):
        list_to_pad.append(padding_value)
            
    return list_to_pad       
        
        
    
    
        
        
        
        
        
        
        
        
        
        