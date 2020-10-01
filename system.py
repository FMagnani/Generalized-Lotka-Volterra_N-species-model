#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 09:52:55 2020

@author: FMagnani
GitHub repo: https://github.com/FMagnani/Lotka_Volterra_N_species_model
"""

import logging
from numpy import zeros
import systemDynamicGenerator
import sysFunctions
import pandas as pd
import matplotlib.pyplot as plt


SPECIES_PARS = 4



class Ecosystem:
    """
    Ecosystem()
    
    This class is used to store and manage the information about the whole
    system of interacting species. Such information is the list of all the 
    species, their parameters and the matrix of their binary interactions.
    Whenever a new species is created or deleted, all these are updated. 
    
    ..note:: This class is not supposed to create instances, but to store
             and manage the information about the system. 
 
    """
    
    species_list = []
    
    intMatrix = {}
    
    species_pars = {}
    
    @classmethod
    def create_data(cls):
        """
        Organizes the data in a single tuple.        
        
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
        of shape (2,1), without either "diagonal" or "reciprocal" entries.
        "No diagonal entries" means the absence of keys = ('Name','Name').
        "No reciprocal entries" means that if ('Name1','Name2') is present,
        ('Name2','Name1') is absent.
        Then the dictionary is converted into the square antysimmetric matrix
        needed by the system.
        Parameters k, K, c are needed in order to compute the diagonal 
        values.

        Returns
        -------
        A square antisymmetric matrix, with diagonal entries obtained 
        with the formula:
            
            aii = int(ki>0)*(ci ki)/Ki 
            
        See the documentation for further informations at
        https://github.com/FMagnani/Lotka_Volterra_N_species_model
        """
        
        N = len(cls.species_list)
        
        to_add = {}

        for key in Ecosystem.intMatrix:
            if not (key[0] == key[1]):
                to_add.update({(key[1], key[0]) : - Ecosystem.intMatrix[key]})
        
        cls.intMatrix.update(to_add)
        
        for i, key in zip(range(N), cls.species_list):
            
            aii = int(k[i]>0)*k[i]*c[i]/K[i]
            
            cls.intMatrix.update({(key,key):aii})
                
        A = zeros((N,N))
        
        for I, i in zip( cls.species_list, range(N) ):
            for J, j in zip( cls.species_list, range(N) ):     
                A[i][j] = cls.intMatrix[(I,J)]
    
        return A
    
    
class Species(Ecosystem):
    """
    Species(name, interaction, pars)
    
    Class representing a species. 

    Parameters
    ----------
    NAME: string
        The name of the Species created. It univocally identifies it.
    
    INTERACTION: list. 
        Length should be equal to the number of species already implemented. 
        If smaller, it is padded with zeros.
        It defines the interaction coefficients of this species with respect
        to all the others. The order is the same as the species list of 
        Ecosystem.
        
        So if Ecosystem.species_list = [ 'A', 'B']
        and species 'C' is created with interactions = [1, 2],
        the interaction matrix will be added with the following:
        {('C','A') : 1,
         ('C','B') : 2}
        
        In the interaction matrix, a line as
        ('A','C') : 2
        means that 'A' eats 'C' ('C' is eaten by 'A'), while
        ('A','C'): -2
        means that 'C' eats 'A'.
        
        Thus when the list of interactions for a given species is created, 
        one should ask himself, for interactions[i]: "does this species eat 
        Ecosystem.species_list(i) (in such a case, a positive value should
        be inserted), or is this species eaten by Ecosystem.species_list[i]
        (negative value)?"
        
    PARS: list. 
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
        
        See the documentation for further information on the formula, at
        https://github.com/FMagnani/Lotka_Volterra_N_species_model .
        
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
        This method updates the dictionary specifying the interaction of
        this species with respect to all the others.
        It also checks the the inputs, eventually padding 'interactions' 
        or 'pars' with default values.
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
            
                 interactions = sysFunctions.pad_list(interactions, other_species, 0)
        
             if (len(pars) < SPECIES_PARS):
                 logging.warning('The length of "pars" should be equal to {}. The missing value will be set to 0.5.'.format(SPECIES_PARS))
            
                 pars = sysFunctions.pad_list(pars, SPECIES_PARS, 0.5)
        
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
            
    def status(self):
        """
        Prints the current status of all the variables in the system.
        """
        print('\nCurrent species in the system:\n')
        print(self.species_list)
        print('\nSpecies parameters:')
        print(self.species_pars)
        print('\nCurrent interactions between species:\n')
        print(self.create_data()[6])
        print('\n\nCurrent ODE system:\n')
        print(systemDynamicGenerator.current_system(self))
        print('\n')
               
    def solve(self, max_time=20, t_steps=2**7+1):
        """
         Parameters
         ----------
         max_time : float
             Maximum time reached in the integration.
         t_steps : int
             Number of steps in which the time is divided.
             In the form 2**n +1 performance is increased.
        """
        N = len(self.species_list)
        df = sysFunctions.create_dfSetUp(self)
        df.to_csv(r'setup.csv', index=True, header=True)
        sysFunctions.generate_Integrator(N, max_time, t_steps)
        sysFunctions.exe_Integrator()

    @staticmethod
    def plot():
        """
        Generates the plot of the population number versus time, for all
        the species of the system.
        """
        data = pd.read_csv('solution.csv')

        Species_names = list(data.columns[1:])
        N = len(Species_names)
        t = list(data['Unnamed: 0'])

        fig, ax = plt.subplots()
        for i, name in zip(range(N), Species_names):
            nt = list(data[name])
            ax.plot(t, nt, linewidth=4, label=name)

        ax.set_facecolor('white')
        ax.legend(loc='best')
 
    def set_interaction(self, other_species, new_coeff):
        """        
        OTHER_SPECIES: string
            The name of the species with respect to which the interaction
            coefficient is to be changed.
        NEW_COEFF: float
            The new value of the coefficient.
        """
        
        for key in Ecosystem.intMatrix.keys():
            if (self.name in key) and (other_species in key):
                Ecosystem.intMatrix[key] = new_coeff
        
    def set_par(self, which, new_par):
        """
        WHICH: int
            t specifies which parameter is to be changed, with the same order used for the input:
            0 : Initial population
            1 : k (Growth/Death rate)
            2 : K (Carrying capacity)
            3 : c
        NEW_PAR: float
            The new value of the parameter.        
        """
        if (which==0) or (which==2) or (which==3):
            if (new_par<0):
                logging.warning("The sign of the inserted parameter has been changed. It should be positive. See documentation of class 'Species' for further explanations.")
                new_par *= -1
                
        
        for key in Ecosystem.species_pars.keys():
            if (self.name in key):
                Ecosystem.species_pars[key][which] = new_par
        
    
        
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


    def set_par(self, which, new_par):
        """
        WHICH: int
            From 0 to 3, it specifies which parameter is to be changed,
            with the same order used for the input:
            0 : Initial population
            1 : k (Growth/Death rate)
            2 : K (Carrying capacity)
            3 : c
        NEW_PAR: float
            The new value of the parameter.        
        """
        
        if (which==1) and (new_par<0):
           logging.warning("The sign of the parameter has been changed. It should be positive for preys. See documentation of class 'Species' for further explanations.")
           new_par *= -1
           
        if (which==2) and (new_par==0):
            raise ValueError("The carrying capacity must be strictly positive. See documentation of class 'Species' for further explanations.")

        
        super().set_par(which, new_par)
        
        

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

    def set_par(self, which, new_par):
        """
        WHICH: int
            From 0 to 3, it specifies which parameter is to be changed,
            with the same order used for the input:
            0 : Initial population
            1 : k (Growth/Death rate)
            2 : K (Carrying capacity)
            3 : c
        NEW_PAR: float
            The new value of the parameter.        
        """
        
        if (which==1) and (new_par>0):
           logging.warning("Sign of pars[1] has been changed. It should be negative for preys. See documentation of class 'Species' for further explanations.")
           new_par *= -1
        
        super().set_par(which, new_par)

        