# Lotka_Volterra_N_species_model
The software here developed allows to set up and integrate a [Lotka Volterra system with N species](https://en.wikipedia.org/wiki/Generalized_Lotka%E2%80%93Volterra_equation).

## Introduction to the model

In the field of population dynamics a very simple yet powerful model is based on the [Lotka Volterra equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations). 
It describes using two ordinary non linear differential equations the dynamics of biological systems in which two species interact, one as a predator and the other as a prey. The system arose in the early 1900s and since that time many generalizations have been developed, one of which is the case here under examination.

## Lotka Volterra Predator Prey model

In order to fix the ideas on the basic concepts, let's consider the original Predator-Prey model. 
We call x(t) the number of the preys and y(t) the number of predators, both at the time t. The simplest set of equation to describe their evolution is the following:

![equation1](<http://latex.codecogs.com/svg.latex?\frac{dx}{dt}&space;=&space;\alpha&space;x&space;-&space;\gamma&space;xy&space;>)

![equation2](<http://latex.codecogs.com/svg.latex?\frac{dy}{dt}&space;=-&space;\beta&space;x&space;+&space;\delta&space;xy&space;>)


Where dx/dt and dy/dt are the instantaneous growth rate of the two populations. 
α represents the natural birth rate of the preys, while γ represents their predation rate. If we interpret xy as the probability for a prey and a predator to meet and interact, γ can be read as the fraction of times in which the prey is actually caught. 
Overall, the change over time of the number of the preys is given by the balance between the rate at which they're born and the rate at which they're predated.  

Simmetrically β is the natural death rate of the predators, that are supposed to die if no predation occurs, while δ is their hunting efficiency. Note that γ and δ are different costants, since the gain percieved by predators can differ from the loss percieved by the preys. It can be roughly considered as the amount of preys needed to feed a predator. 

The system just described behaves in an oscillatory fashion, as shown in Fig.1.

FIG.1

Note that in absence of interaction, the predators are assumed to die while the preys are assumed to grow exponentially and with no limit. A development of the previous system is to limit the natural resources for the preys, with a term quadratic in x representing the intraspecific competition for the food ([Competitive Lotka Volterra](https://en.wikipedia.org/wiki/Competitive_Lotka%E2%80%93Volterra_equations)). The modified equations have the following form:

![equation3](<http://latex.codecogs.com/svg.latex?&space;\frac{dx}{dt}&space;=&space;\alpha&space;x&space;(&space;1&space;-&space;\frac{x}{K}&space;)&space;-&space;\gamma&space;xy&space;>)

![equation4](<http://latex.codecogs.com/svg.latex?\frac{dy}{dt}&space;=-&space;\beta&space;x&space;+&space;\delta&space;xy&space;>)


where K, called carrying capacity in ecology, here directly represents the maximum number of preys that the ecosystem in absence of predators can feed at once. This new scenario leads to solutions similar to that presented in Fig.2

FIG.2

Let's now analyze the N species generalization.

## Lotka Volterra N species model

The set of equations can be written

![equation5](<http://latex.codecogs.com/svg.latex?&space;\frac{dx_i}{dt}&space;=&space;k_i&space;x&space;(&space;1&space;-&space;\frac{x_i}{K_i}&space;\theta(k_i)&space;)&space;-&space;\frac{1}{c_i}&space;\sum_{i\neq&space;j}&space;a_i_j&space;x_i&space;x_j&space;&space;>)

The equation form is analogous to that of the simpler model.
θ(k) is the Heaviside function, defined as

θ(k) = 1    if    k > 0 <\br>
θ(k) = 0    if    k < 0

and it assures that the limited growth is applied only to preys, while predators have and no other limit in growth than the presence of preys. 
The summatory defines the interaction of the i-th species with all the others, both in intensity and in quality: a<sub>ij</sub> > 0 represents a loss for the species i against the species j. Simmetrically, the gain for the species j will be a<sub>ji</sub> = -a<sub>ij</sub>. Thus the interaction matrix A has to be antisymmetric. The 1/c<sub>i</sub> factors represent the relative velocity at which a particular species changes the number of its individuals, with respect to the number of interactions with all the other species. The interaction matrix coefficents can be interpreted as the coupling between the different species (0 coupling means total indifference).
Note that the intraspecific competition term (the quadratic term in x<sub>i</sub>) can be included into the summatory, through the definition

![equation6](<http://latex.codecogs.com/svg.latex?a_i_i&space;=&space;\frac{c_i&space;k_i}{K_i}\theta(k_i)&space;>)



