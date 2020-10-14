# Lotka_Volterra_N_species_model
The software here developed allows to set up and integrate a generalized [Lotka Volterra system](https://en.wikipedia.org/wiki/Generalized_Lotka%E2%80%93Volterra_equation), either via the IPython Console or using a script.

## Introduction to the model

In the field of population dynamics a very simple yet powerful model is based on the [Lotka Volterra equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations). 
It describes, using two ordinary non linear differential equations, the dynamics of biological systems in which two species interact, one as a predator and the other as a prey. The system arose in the early 1900s and since that time many generalizations have been developed, one of which is the case here under examination.

### Lotka Volterra Predator Prey model

In order to fix the ideas on the basic concepts, let's consider the original Predator-Prey model. 
We call x(t) the number of the preys and y(t) the number of predators, both at the time t. The simplest set of equation to describe their evolution is the following:

![equation1](<http://latex.codecogs.com/svg.latex?\frac{dx}{dt}&space;=&space;\alpha&space;x&space;-&space;\gamma&space;xy&space;>)

![equation2](<http://latex.codecogs.com/svg.latex?\frac{dy}{dt}&space;=-&space;\beta&space;x&space;+&space;\delta&space;xy&space;>)


Where dx/dt and dy/dt are the instantaneous growth rate of the two populations. 
α represents the natural birth rate of the preys, while γ represents their predation rate. If we interpret xy as the probability for a prey and a predator to meet and interact, γ can be read as the fraction of times in which the prey is actually caught. 
Overall, the change over time of the number of the preys is given by the balance between the rate at which they're born and the rate at which they're predated.  

Simmetrically β is the natural death rate of the predators, that are supposed to die if no predation occurs, while δ is their hunting efficiency. Note that γ and δ are different costants, since the gain percieved by predators can differ from the loss percieved by the preys. It can be roughly considered as the amount of preys needed to feed a predator. 

The system just described behaves in an oscillatory fashion, as shown in the following figure.

![config](./images/LV_normal.png)

Note that in absence of interaction, the predators are assumed to die while the preys are assumed to grow exponentially and with no limit. A development of the previous system is to limit the natural resources for the preys, with a term quadratic in x representing the intraspecific competition for the food. The modified equations have the following form:

![equation3](<http://latex.codecogs.com/svg.latex?&space;\frac{dx}{dt}&space;=&space;\alpha&space;x&space;(&space;1&space;-&space;\frac{x}{K}&space;)&space;-&space;\gamma&space;xy&space;>)

![equation4](<http://latex.codecogs.com/svg.latex?\frac{dy}{dt}&space;=-&space;\beta&space;x&space;+&space;\delta&space;xy&space;>)


where K, called carrying capacity in ecology, here directly represents the maximum number of preys that the ecosystem in absence of predators can feed at once.
This new scenario leads to different solutions. Let's now analyze the N species generalization.

### Lotka Volterra N species model

The set of equations can be written

![equation5](<http://latex.codecogs.com/svg.latex?&space;\frac{dx_i}{dt}&space;=&space;k_i&space;x&space;(&space;1&space;-&space;\frac{x_i}{K_i}&space;\theta(k_i)&space;)&space;-&space;\frac{1}{c_i}&space;\sum_{i\neq&space;j}&space;a_i_j&space;x_i&space;x_j&space;&space;>)

The equation form is analogous to that of the simpler model.
θ(k) is the Heaviside function, defined as

θ(k) = 1    if    k > 0  
θ(k) = 0    if    k < 0

and it assures that the limited growth is applied only to preys, while predators have and no other limit in growth than the presence of preys. 
The summatory defines the interaction of the i-th species with all the others, both in intensity and in quality: a<sub>ij</sub> > 0 represents a loss for the species i against the species j. Simmetrically, the gain for the species j will be a<sub>ji</sub> = -a<sub>ij</sub>. Thus the interaction matrix A has to be antisymmetric. The 1/c<sub>i</sub> factors represent the relative velocity at which a particular species changes the number of its individuals, with respect to the number of interactions with all the other species. The interaction matrix coefficents can be interpreted as the coupling between the different species (0 coupling means total indifference).
Note that the intraspecific competition term (the quadratic term in x<sub>i</sub>) can be included into the summatory, through the definition

![equation6](<http://latex.codecogs.com/svg.latex?a_i_i&space;=&space;\frac{c_i&space;k_i}{K_i}\theta(k_i)&space;>)

## Software structure

The software is made up of three main modules:  
***sysFunctions***, that implements simple functions used in system.  
***LVsystem***, where the objects exploited by the user to set up the system are defined.  
***systemDynamicGenerator***, that generates a new module ***integrator*** for the system integration.  
Thus the dataflow is the following:  
***LVsystem*** ---setup data--->***systemDynamicGenerator***---dynamical generation--->***integrator***--->solution  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|______________________________________________________^  

## Usage 

The file ***LVsystem*** is run and the system is set up and solved even from command line, through the object **Ecosystem**. It contains all the methods needed in order to set up the system up to an arbitrary number of species, solve it, plot the results and eventually save permanently either the setup or the solution. Previusly saved setups can be loaded into the system as a starting point. Each species is univocally identified with a name.  
Below the list of all the available methods is shown, with the specification of their arguments and the explanation of their function.  

| **Method**     	| **Parameter**                                                              	| **Function**                                                                                                                                                                                                                                      	|
|----------------	|----------------------------------------------------------------------------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| addSpecies     	| *name*: string                                                               	| *Name* is added to the current list of species.                                                                                                                                                                                      	|
| setInteraction 	| *name1*: string <br>*name2*: string<br>*value*: float                            	| This method is used to specify the kind of interaction of *name1* with respect to *name2*. The interaction matrix is updated with *value*.  <br>A positive *value* means that *name1* eats *name2*.  <br>A negative *value* means that *name1* is eaten by *name2*. 	|
| setInitialCond 	| *name*: string   <br>*value*: float                                            	| This method sets the initial population of species *name* equal to *value*.                                                                                                                                                                       	|
| setGrowthRate  	| *name*: string   <br>*value*: float                                            	| This method sets the growth rate of species *name* equal to *value*.                                                                                                                                                                              	|
| setCarrCap     	| *name*: string <br>*value*: float                                              	| This method sets the carrying capacity of species *name* equal to *value*.                                                                                                                                                                        	|
| setChangeRate  	| *name*: string <br>*value*: float                                              	| This method sets the change rate of species *name* equal to *value*.                                                                                                                                                                              	|
| removeSpecies  	| *name*: string                                                               	| This method removes from the system the species *name* and all its interactions with the other species.                                                                                                                                           	|
| status         	| *name*: string<br>(optional)                                                 	| This method prints the status of the system, if no arguments are given.  <br>If the name of a species is given, the method prints the current value of its parameters and interactions.                                                           	|
| solve          	| *max_time*: float  <br>(default: 20)<br><br>*t_steps*: int  <br>(default: 129) 	| *max_time* specifies the maximum time reached in the integration.  <br>  <br>*t_steps* specifies the number of steps in which the time is divided.  <br>In the form 2^n +1 performance is increased.                                                  	|
| plot           	|                                                                            	| This method plots the solution contained in the file solution.csv.                                                                                                                                                                                	|
| saveSetup      	| *name*: string<br>(optional)                                                 	| The current setup of the system is saved into the folder 'saved_setups'.  <br>If *name* is not given, it will be saved in the format setup_day-month-year-hour:min:sec.                                                                            	|
| saveSolution   	| *name*: string<br>(optional)                                                 	| The solution of the system is saved into the folder 'saved_solutions'.  <br>If *name* is not given, it will be saved in the format setup_day-month-year-hour:min:sec.                                                                              	|
| loadSetup      	| *name*: string                                                               	| The system is initialized with the status given by the file *name*, that should be a setup present in the folder 'saved_setups'.                                                                                      	|

### Examples

As a reference, below is shown the code needed to replicate the Prey Predator model.  

    sys = Ecosystem()
    
    sys.addSpecies('rabbit')
    sys.addSpecies('fox')

    sys.setInitialCond('rabbit', 10)
    sys.setInitialCond('fox', 5)
    sys.setGrowthRate('rabbit', 1)
    sys.setGrowthRate('fox', -1)
    sys.setCarrCap('rabbit', 10000)
    sys.setCarrCap('fox', 1)
    sys.setChangeRate('rabbit', 10)
    sys.setChangeRate('fox', 20)

    sys.setInteraction('rabbit', 'fox', -1)
    sys.setInteraction('fox', 'rabbit', 1)

    sys.solve()
    sys.plot()

The result of the code above is a file *setup.csv*, a file *solution.csv*, and the following figure plot on the terminal.

![config](./images/LV_normal.png)

In order to save the setup just built, the following line can be run:  

    sys.saveSetup('PreyPredator')

Let's now see briefly how to load an already saved setup, how to check its status and variables and eventually modify and solve it. We will use the setup *2Prey1Predator*, already present in the folder of saved setups as a reference.  

    sys.loadSetup('2Prey1Predator')
    sys.status()
    
Output:

    Current species in the system:
    ['rabbit', 'hen', 'fox']

    Current interactions between species:
    [[ 0.0036  0.     -1.    ]
     [ 0.      0.0035 -1.    ]
     [ 1.      1.     -0.    ]]


    Current ODE system:

    dn0dt = 0.09*n0 + 0.0036*n0*n0/400 + 0.0*n0*n1/400 + -1.0*n0*n2/400
    dn1dt = 0.07*n1 + 0.0035*n1*n1/500 - 0.0*n1*n0/500 + -1.0*n1*n2/500
    dn2dt = -0.06*n2 + -0.0*n2*n2/250 - -1.0*n2*n0/250 - -1.0*n2*n1/250
    
A deeper inspection for a particular species is possible:  

    sys.status('fox')  
    
Output:

    Species name:  fox

    Initial condition:  20
    Growth rate:  -0.06
    Carrying capacity:  -0.06
    Change rate:  250

    Interactions: 
    ('rabbit', 'fox') :  -1.0
    ('hen', 'fox') :  -1.0
    ('fox', 'rabbit') :  1.0
    ('fox', 'hen') :  1.0
    ('fox', 'fox') :  -0.0

If needed, the user can add new species to this setup or modify their parameters and eventually save the new situation. To solve and plot up to a time = 500, the following line are required:

    sys.solve(500)  
    sys.plot()  

Output:

![config](./images/LV_2Prey1Pred.png)  
  
