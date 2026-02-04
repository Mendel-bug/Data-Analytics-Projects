'''Proving the schrodinger equation for an infifnite square well using python By Montle Fredah Segomotso 202107060   '''
#Import necessary libraries


import numpy as np #For numerical operations
import matplotlib.pyplot as plt #For plotting
from mpl_toolkits.mplot3d import Axes3D #For 3D plotting
from scipy.linalg import eigh #For eigenvalue problems

#Define function
def schrodinger_hamiltonian (N, W, E):
    #Constants
    M = 1 #Mass in AMU
    Hbar = 1 # Reduced Planck's constant in AMU

    #The differential operator
    dx = (W/N-1) #Grid spacing
    D = -(Hbar**2/2*M*dx**2)#Coefficient of the Hamiltonian matrix

    #Defining the Hamiltonian as a zero matrix
    H = np.zeros((N-1,N-1))

    #Constructing the Hamiltonian matrix using Central differene 
    for x in range (0, N-2):
        H[x,x-1] = D #Lower diagonal
        H[x,x]= 2*(-D)-E #Main diagonal with Energy term
        H[x,x-1] =D #Upper diagonal

    #Applying infinite potential boundaries by equating H to higher value for the first and last diagonal
    H[0,0] =1e10
    H[N-2,N-2] =1e10
    return H

#Finding energy using bisection method
def bisection_energy (N, W, E_min, E_max, E_mid,tolerance = 1e-10, max_iterations = 1000):
    for iteration in range (max_iterations):
        E_mid = (E_max + E_min)/2
        #Update the Hamiltonian for E =E_mid
        H = schrodinger_hamiltonian(N, W, E_mid)
        eigenvalues,_ =eigh(H) #Computes the values
        eigenvalues.sort()

        #Handling special cases to check if the lowest eigenvalue is negative
        if eigenvalues[0]<0:
            E_min = E_mid #The midpoint energy becomes the lower bound
        else:
            E_max = E_mid #The midpoint becomes the upper bound

            #Check for convergence
        if abs (E_max -E_min)<tolerance:
            break #Exit the loop within tolerence
    return E_mid, iteration

#Parameters
E_min =0 #Energy Lower Bound
E_max =10 #Energy Upper Bound
E_mid = (E_min + E_max)/2
W = 2 #Infinite Square Well Width
N = 100 #Number of grid points

#Compute energy eigen values
energy_levels = []
iterations_list = []
for i in range(4): #Calculate the firts 3 energy levels
    energy, iterations = bisection_energy(N, W, E_min, E_max, E_mid)#Find energy using bisection
    energy_levels.append(energy)#Store the found energy
    iterations_list.append(iterations)#Store the nuber of iterations
    E_min = energy #Update E_min for the next iteration
print(f'Found energy eigenvalue:{energy_levels} after {iterations_list} iterations')

#3D Visualization
x = np.linspace(0, W, N-1) #Define x as a linear space from 0 to W with N-1 points in the grid
X, Y = np.meshgrid(x, energy_levels) #Creating meshgrid for 3D plotting
Z = np.zeros_like(X)#Initializing Z for probability density

#Update the Hamiltonian and calculate wavefunctions for each energy level
for i, energy in enumerate(energy_levels):
    H = schrodinger_hamiltonian (N,W, energy)
    eigenvalues, eigenvectors = eigh(H)
    eigenvalues.sort()
    wavefunction = eigenvectors[:,i] #ith eigen vector corresponds to ith nergy level#Normalization of the wavefunction

    #Normalization of the wavefunction
    wavefunction /= np.sqrt(np.sum(wavefunction**2)*(W/(N-1)))
    Z[i, :] = wavefunction**2 #storing the probability density

#3D Visualization
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')#111 shows 1row, 1column for the first subplot
ax.plot_surface(X, Y, Z, cmap='Greens')#Plot a 3D surface using the X,Y,Z data arrays and cmap argument specifies thecolorpam to use for coloring

#Plot each wave function seperately with differnt color
for i in range(len(energy_levels)):
               ax.plot(x,[energy_levels[i]]*len(x), Z[i, :], label=f'n={i+1}',linewidth=2)


ax.set_title('3D Wave Function Probability Density For Infinite Square Well')
ax.set_xlabel('Position (x)')
ax.set_ylabel('Energy Levels')
ax.set_zlabel('Probability Density')
ax.legend()
plt.tight_layout()
plt.show()

# Also plot 2D versions for clarity
plt.figure(figsize=(10, 6))
for i in range(len(energy_levels)):
    plt.plot(x, Z[i, :], label=f'n={i+1}')
plt.title('Wave Function Probability Density for Infinite Square Well')
plt.xlabel('Position (x)')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
