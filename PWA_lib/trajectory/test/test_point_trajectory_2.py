# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 18:06:20 2018

@author: sadra
"""

# External imports
import numpy as np

# My modules
from pypolycontain.lib.zonotope import zonotope
from pypolycontain.lib.polytope import polytope


# Internal imports
from PWA_lib.trajectory.system import system
from PWA_lib.trajectory.poly_trajectory import point_trajectory

sys=system()
sys.name="inverted pendulum with two walls"


sys.A[0,0]=np.array([[1,0.01],[0.1,1]])
sys.B[0,0]=np.array([[0,0.01]]).T
sys.c[0,0]=np.array([[0,0]]).T

sys.A[1,0]=np.zeros((2,2))
sys.B[1,0]=np.zeros((2,1))
sys.c[1,0]=np.zeros((2,1))
sys.A[1,1]=np.array([[0,0],[-10,0]])
sys.B[1,1]=np.array([[0,0]]).T
sys.c[1,1]=np.array([[0,1]]).T


sys.A[2,0]=np.zeros((2,2))
sys.B[2,0]=np.zeros((2,1))
sys.c[2,0]=np.zeros((2,1))
sys.A[2,1]=np.array([[0,0],[-10,0]])
sys.B[2,1]=np.array([[0,0]]).T
sys.c[2,1]=np.array([[0,-1]]).T

H=np.array([[1,0,0],[0,1,0],[-1,0,0],[0,-1,0],[0,0,1],[0,0,-1]])
h=np.array([[0.1,1,0.12,1,4,4]]).T   
sys.C[0,0]=polytope(H,h)
sys.C[1,0]=polytope(H,h)
sys.C[2,0]=polytope(H,h)

H=np.array([[1,0,0],[0,1,0],[-1,0,0],[0,-1,0],[0,0,1],[0,0,-1]])
h=np.array([[0.12,1,-0.1,1,4,4]]).T  
sys.C[1,1]=polytope(H,h)

H=np.array([[1,0,0],[0,1,0],[-1,0,0],[0,-1,0],[0,0,1],[0,0,-1]])
h=np.array([[-0.1,1,0.12,1,4,4]]).T  
sys.C[2,1]=polytope(H,h)

sys.goal=zonotope(np.array([0,0]).reshape(2,1),np.array([[0.0,0],[0,0.0]]))

sys.n=2
sys.m=1
sys.list_of_sum_indices=[0,1,2]
sys.list_of_modes={}
sys.list_of_modes[0]=[0]
sys.list_of_modes[1]=[0,1]
sys.list_of_modes[2]=[0,1]

sys.build()


import matplotlib.pyplot as plt

x0=np.array([0.0,0.69]).reshape(2,1)
T=50
(x,u,delta_PWA,mu)=point_trajectory(sys,x0,[sys.goal],T)

plt.plot([x[t][0,0] for t in range(T+1)],[x[t][1,0] for t in range(T+1)])
plt.plot([x[t][0,0] for t in range(T+1)],[x[t][1,0] for t in range(T+1)],'+')
plt.plot([0.1,0.1],[-1,1],'black')
plt.plot([-0.1,-0.1],[-1,1],'black')
plt.plot([0],[0],'o')
plt.plot([-0.05],[0.05],'o')