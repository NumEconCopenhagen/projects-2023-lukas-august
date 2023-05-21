import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

def SS_simulation():

    # Define parameter values
    alpha = 1/3  # Production function parameter
    s = 0.8  # Savings rate
    sr = 0.2  # Share of output invested in research
    delta = 0.1  # Depreciation rate
    n = 0.01  # Labor force growth rate
    rho = 0.5 # Productivity parameter
    phi = 0.9 # Elasticity of existing knowledge
    _lambda_ = 0.9 # Efficiency of researchers

    # Define production function
    def production_function(K, A, L):
        return K**alpha*(A*L)**(1-alpha)

    # Set up variables for simulation
    T = 300
    Ks = np.zeros(T)
    Ys = np.zeros(T)
    Ls = np.zeros(T)
    As = np.zeros(T)
    Zs = np.zeros(T)

    # Define starting period values
    Ks[0] = 0.5
    Ls[0] = 1.0
    As[0] = 1.0
    Ys[0] = production_function(Ks[0], As[0], Ls[0]) # Call production_function to calculate Y_0

    # Iteration by for-loop from 1 to periode T (ending period)
    for t in range(1,T):
        Ks[t] = s*Ys[t-1] + (1-delta)*Ks[t-1]
        Ls[t] = (1+n)*Ls[t-1]

        L_A = sr*Ls[t] # Share of labor working in research
        L_Y = (1-sr)*Ls[t] # Residual labor force

        As[t] = rho*As[t-1]**phi*L_A**_lambda_+As[t-1] # Calculate A_t
        Ys[t] = production_function(Ks[t], As[t], L_Y) # Call production_function to calculate Y_t

    k_tilde = Ks/(As*Ls) # Calculate K per capita
    y_tilde = Ys/(As*Ls) # Calculate Y per capita

    return Ks, Ys, Ls, As, k_tilde, y_tilde
