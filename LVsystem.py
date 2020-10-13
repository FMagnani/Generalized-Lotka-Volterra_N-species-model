#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 09:52:55 2020

@author: FMagnani
GitHub repo: https://github.com/FMagnani/Lotka_Volterra_N_species_model
"""

from numpy import zeros
import systemDynamicGenerator
import sysFunctions
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import shutil

class Ecosystem:
    """
    Ecosystem()
    
    This class is used to store and manage the information about the
    system. 
    
    Methods
    -------
    addSpecies(name)
    removeSpecies(name)
    setInteraction(name1, name2, value)
    setInitialCond(name, value)
    setGrowthRate(name, value)
    setCarrCap(name, value)
    setChangeRate(name, value)
    status(name = '')
    solve(max_time=20, t_steps=129)
    plot()
    saveSetup(name = '')
    saveSolution(name = '')
    loadSetup(name)
    
    Further information are given by the documentation of each method.
    
    """
    
    species_list = []
    
    intMatrix = {}
  
    InitialCond = {}
    GrowthRate = {}
    CarrCap = {}
    ChangeRate = {}
  
    def create_data(self):
        """
        Organizes the data in a single tuple.        
        
        Returns
        -------
        An ordered tuple of arrays.
        return[0]: N  -number of species/ dimension of the system 
        return[1]: list of the species' names 
        return[2]: n0 -array of initial conditions
        return[3]: k  -array of k parameters
        return[4]: K  -array of K parameters
        return[5]: c  -array of c parameters
        return[6]: A  -interaction Matrix
    
        The order of the values of each array is the same as the list of 
        species' name.
        """
        
        N = len(self.species_list)

        n0 = []
        k = []
        K = []
        c = []
        for key in self.species_list:
            n0.append(self.InitialCond[key])
            k.append(self.GrowthRate[key])
            K.append(self.CarrCap[key])
            c.append(self.ChangeRate[key])
        
        A = self.dict_into_matrix(k, K, c)
        
        return (N, self.species_list, n0, k, K, c, A)
        
    
    
    def dict_into_matrix(self, k, K, c):
        """
        This method converts the intMatrix, that is a dictionary,
        into a square matrix.
        Parameters k, K, c are needed in order to compute the diagonal 
        values.
        
        """
        
        for key1 in self.species_list:
            for key2 in self.species_list:
                if (key1 != key2) and ( (key1,key2) not in self.intMatrix ):
                    raise KeyError("The interaction of "+key1+" with respect to "+key2+" is missing.")            
        
        for key in self.species_list:
            if not (key in self.InitialCond.keys()):
                raise KeyError("Missing initial condition for "+key+".")                
            if not (key in self.GrowthRate.keys()):
                raise KeyError("Missing growth rate for "+key+".")
            if not (key in self.CarrCap.keys()):
                raise KeyError("Missing carrying capacity for "+key+".")
            if not (key in self.ChangeRate.keys()):
                raise KeyError("Missing change rate for "+key+".")
        
        N = len(self.species_list)
        
        # Diagonal entries
        for i, key in zip(range(N), self.species_list):
            
            aii = int(k[i]>0)*k[i]*c[i]/K[i]
            
            self.intMatrix.update({(key,key):aii})
                
        A = zeros((N,N))
        
        for I, i in zip( self.species_list, range(N) ):
            for J, j in zip( self.species_list, range(N) ):     
                A[i][j] = self.intMatrix[(I,J)]
    
        return A
    

    def load_from_setup(self):
        """
        This method initializes the system with the data stored in the
        setup file currently present in the directory.
        """
        
        data =pd.read_csv("setup.csv")
        
        N = len(list(data['Species']))
        
        for i in range(N):
            name = list(data['Species'])[i]
            n0 = list(data['Initial cond'])[i]
            k = list(data['Growth rate'])[i]
            K = list(data['Carrying cap'])[i]
            c = list(data['Change rate'])[i]
            
            interactions = list(data['A_row'+str(i)])
        
            self.addSpecies(name)
            self.setInitialCond(name, n0)
            self.setGrowthRate(name, k)
            self.setCarrCap(name, K)
            self.setChangeRate(name, c)
            
            for j in range(N):
                if not (i==j):
                    self.setInteraction(name, list(data['Species'])[j], interactions[j])


    def addSpecies(self, name):
        """
        name: string. The species' name.
        
        The list of species of the system is updated with this name.
        
        """
       
        if (name in self.species_list):
            raise TypeError("""Name already existing. Species must have different names.""")

        self.species_list.append(name)
 
        
    def setInteraction(self, name1, name2, value):
        """
        name1: string. 
        name2: string.
        value: float.
        
        This method is used to specify the kind of interaction of name1
        with respect of name2. The interaction matrix is updated with
        value.
        
        A positive value means that name1 eats name2.
        A negative value means that name1 is eaten by name2.
        
        """
        
        if not ( (name1) in self.species_list ):
            raise TypeError("""Species not found.""")
            
        self.intMatrix[(name1, name2)] = value  
        
        
    def setInitialCond(self, name, value):
        """
        name: string. 
        value: float.
        
        This method sets the initial population of species 'name'
        equal to 'value'.
        
        """
        
        if not ( (name) in self.species_list ):
            raise TypeError("""Species not found.""")
        
        self.InitialCond.update({name:value})
        
    def setGrowthRate(self, name, value):
        """
        name: string. 
        value: float.
        
        This method sets the growth rate of species 'name'
        equal to 'value'.
        
        """
        
        if not ( (name) in self.species_list ):
            raise TypeError("""Species not found.""")
        
        self.GrowthRate.update({name:value})
            
    def setCarrCap(self, name, value):
        """
        name: string. 
        value: float.
        
        This method sets the carrying capacity of species 'name'
        equal to 'value'.
        
        """
        
        if not ( (name) in self.species_list ):
            raise TypeError("""Species not found.""")
        
        self.CarrCap.update({name:value})    

    def setChangeRate(self, name, value):
        """
        name: string. 
        value: float.
        
        This method sets the change rate of species 'name'
        equal to 'value'.
        
        """
        
        if not ( (name) in self.species_list ):
            raise TypeError("""Species not found.""")
        
        self.ChangeRate.update({name:value})
    
    
    def status(self, name=''):
        """
        name: string. 
        
        This method prints the status of the system, if no arguments are
        given.
        If the name of a species is given, the method prints the current
        value of its parameters and interactions.
        
        """
        
        if not (name == ''):
            print("\nSpecies name: ", name)
            print("\nInitial condition: ", self.InitialCond[name]) 
            print("Growth rate: ", self.GrowthRate[name])
            print("Carrying capacity: ", self.GrowthRate[name])
            print("Change rate: ", self.ChangeRate[name])
            print("\nInteractions: ")
            for key in self.intMatrix.keys():
                if (name in key):
                    print(key, ": ", self.intMatrix[key])
            print('\n')
        
        else:
            print('\nCurrent species in the system:')
            print(self.species_list)
            print('\nCurrent interactions between species:')
            print(self.create_data()[6])
            print('\n\nCurrent ODE system:\n')
            print(systemDynamicGenerator.current_system(self))
            print('\n')

     
    def solve(self, max_time=20, t_steps=2**7+1):
        """
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
        This method plots the solution contained in the file solution.csv.
        
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
 
 
    def removeSpecies(self, name):
        """
        name: string. 
        
        This method removes from the system the species 'name' and all
        its interactions with the other species.
        
        """
                
        if not ( name in self.species_list ):
            raise TypeError("""Species not found.""")
        
        self.species_list.remove(name)
   
        if name in self.InitialCond.keys():
            self.InitialCond.pop(name)
        if name in self.GrowthRate.keys():
            self.GrowthRate.pop(name)
        if name in self.CarrCap.keys():
            self.CarrCap.pop(name)
        if name in self.ChangeRate.keys():
            self.ChangeRate.pop(name)
        
        # Needed an external key list since it's not possible to remove
        # elements from a dictionary while iterating over it.
        
        key_blacklist =[]
        for key in self.intMatrix.keys():
            if (name in key):
                key_blacklist.append(key)
        for key in key_blacklist:
            self.intMatrix.pop(key)
        
    
    def saveSetup(self, name = ''):
        """
        name: string.
        
        The current setup of the system is saved into the folder 
        'saved_setups'. If 'name' is not given, it will be saved with 
        the current date and time inside the name.
        
        """
        df = sysFunctions.create_dfSetUp(self)
        df.to_csv(r'setup.csv', index=True, header=True)
        
        if (name == ''):
            name = datetime.now().strftime("setup_%d-%m-%Y-%H:%M:%S")
        
        path = "saved_setups/"
        os.rename('setup.csv', path+name)

    def saveSolution(self, name = ''):
        """
        name: string.
        
        The current solution of the system is saved into the folder 
        'saved_solutions'. If 'name' is not given, it will be saved with 
        the current date and time inside the name.
        
        """
        self.solve()
        
        if (name == ''):
            name = datetime.now().strftime("solution_%d-%m-%Y-%H:%M:%S")
                
        path = "saved_solutions/"
        os.rename('solution.csv', path+name)
    
    def loadSetup(self, name):
        """
        name: string.
        
        The system is initialized with the status given by the file 
        'name', that should be a setup previously saved or already 
        present in the folder 'saved_setups'.
        
        """        
        if (os.path.isfile('setup.csv')):
            os.remove('setup.csv')

        name = 'saved_setups/'+name
        shutil.copy(name, 'setup.csv')
        
        self.load_from_setup()
    
    
