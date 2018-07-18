#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:55:26 2018

@author: sadra
"""
import numpy as np

def find_mode(s,x,eps=10**-9):
    """
    Description: Given system s and state x
    """
    for mode in s.modes:
        if np.amin(s.h[mode]-np.dot(s.H[mode],x))>=-eps:
            return mode
    raise(ValueError("Error! out of state space:",x.T))

def valuation(x):
    """
    Description: given a set of Gurobi variables, output a similar object with values
    Input:
        x: dictionary, each val an numpy array, each entry a Gurobi variable
        output: x_n: dictionary with the same key as, each val an numpy array, each entry a float 
    """
    x_n={}
    for key,val in x.items():
        x_n[key]=np.ones(val.shape)
        (n_r,n_c)=val.shape
        for row in range(n_r):
            for column in range(n_c):
                x_n[key][row,column]=x[key][row,column].X   
    return x_n

def mode_sequence(s,z):
    seq={}
    for key,val in z.items():
        t=key[0]
        if round(val.X)==1:
            if t in seq.keys():
                raise(ValueError("Two modes are assigned to time %d: %d and %d"%(t,seq[t],key[1])))
            seq[t]=key[1]
    return seq

def vertices_cube(T):
    """
    Description: 2**n * n array of vectors of vertices in unit cube in R^n
    """
    from itertools import product 
    v=list(product(*zip([-1]*T,[1]*T)))
    return np.array(v)

def sample(l,u):
    """
    Description: sample from box of l:lower corner, u: upper corner, with uniform distribution
    """
    return l+(u-l)*np.random.random_sample(l.shape)

def inside_X(s,x,eps=10**-9):
    """
    Description: x inside state-space: True, Otherwise: False
    """
    for mode in s.modes:
        if np.amin(s.h[mode]-np.dot(s.H[mode],x))>=-eps:
            return True
    return False
        
            