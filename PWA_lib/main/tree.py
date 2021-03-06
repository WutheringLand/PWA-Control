#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 00:04:20 2018

@author: sadraddini
"""
import numpy as np
from random import random,choice,randint
from gurobipy import Model

### Internal imports
import sys
sys.path.append('..')
sys.path.append('../..')

from main.trajectory import polytope_trajectory,make_state_trajectory_state_end
from main.auxilary_methods import sample
from main.tree_locator import array_tree,inside_tree,sorted_distance_states,all_vertices_out_of_tree
from main.simulate import simulate_0
from main.ana_system import cost_state
from main.polytope import sample_from_polytope

from Convex_Hull.trajectory_disjunctive import polytopic_trajectory_to_set_of_polytopes


def intitialize_tree(s,T=20,alpha_start=0):
    goal=s.goal
    s.goal.successor=(s.goal,"null","null")
    x0=s.goal.x
    (x,u,G,theta,z,flag)=polytope_trajectory(s,x0,goal,T,alpha_start,coin=0.5)
    if flag==True:
        print("Initilization Successfull!")
        make_state_trajectory_state_end(s,x,u,z,G,theta,T,goal)
        s.X.append(s.goal)
        array_tree(s)
        s.tree_iterations+=1
        s.tree_size[s.tree_iterations]=len(s.X)
    else:
        raise("Error! Initilization NOT successfull!")

def extend_RRT(s,T,alpha_start=10**5,eps=0.1):
    i=choice(s.modes)
    x_sample=sample(s.l[i],s.u[i])
    array_tree(s)
    if inside_tree(s,x_sample)==True:
        print("inside X_tree")
        return False
    else:
        (x_zero,T)=simulate_0(s,x_sample,T)
        STATES=sorted_distance_states(s,x_zero)
        for state_end in STATES:
            (x,u,G,theta,z,flag)=polytope_trajectory(s,x_sample,state_end,T,alpha_start,eps)
            if flag==True:
                if all_vertices_out_of_tree(s,x[0],G[0])==True:
                    make_state_trajectory_state_end(s,x,u,z,G,theta,T,state_end)
                    print("+"*80,"Connected to Tree","+"*80)
                    return True
                
def extend_RRT_MILP(s,T,eps,K,x_sample_list):
    i=choice(s.modes)
    #x_sample=sample(s.l[i],s.u[i])
    if x_sample_list==[]:
        x_sample=sample_from_mode(s,i)
    else:
        x_sample=x_sample_list[0]
    array_tree(s)
    if inside_tree(s,x_sample)==True:
        print("inside X_tree")
        return False
    else:
        (x_zero,T)=simulate_0(s,x_sample,T)
        STATES=sorted_distance_states(s,x_zero)
        # using list comprehension
        chunck_list = [STATES[i * K:(i + 1) * K] for i in range((len(STATES) + K - 1) // K )] 
        for list_of_states in chunck_list:
            (x,u,G,theta,z,flag,state_end)=polytopic_trajectory_to_set_of_polytopes(s,x_sample,T,list_of_states,eps,method="chull")
            if flag==True:
                if all_vertices_out_of_tree(s,x[0],G[0])==True:
                    make_state_trajectory_state_end(s,x,u,z,G,theta,T,state_end)
                    print("+"*80,"Connected to Tree, size=%d"%len(s.X),"+"*80)
                    return True
        
                
def Random_Tree_of_Polytopes(s,T_max=10,eps_max=1,method="MILP",x_sample_list=[]):
    for t in range(0,500):
        print("*"*100,"iteration",t)
        T=randint(1,T_max)
        if method=="one_by_one":
            flag=extend_RRT(s,T,alpha_start=-1,eps=random()*eps_max)
        elif method=="MILP":
            flag=extend_RRT_MILP(s,T,eps=random()*eps_max,K=30,x_sample_list=[])
        else:
            raise(method, "is not one of known extend_RRT methods, try 'MILP' or 'one_by_one'")
        if flag==True:
            s.tree_iterations+=1
            s.tree_size[s.tree_iterations]=len(s.X)
                       
def rewiring(s,x):
    pass

def tree_construct(s,goal,max_iterations):
    pass

def tree_value_function(s):
    """
        Solve a linear program
    """
    model=Model("cost_to_go")
    V={}
    for state_considered in s.X:
        V[state_considered]=model.addVar(lb=0,obj=1)
    model.update()
    for state_considered in s.X:
        if state_considered==s.goal:
            model.addConstr(V[state_considered]==0)
        else:
            model.addConstr(V[state_considered]>=V[state_considered.successor[0]]+cost_state(s,state_considered,s.Q,s.R,s.g))
    model.optimize()
    for state_considered in s.X:
        state_considered.cost_to_go=V[state_considered].X


def sample_from_mode(s,mode):
    """
    This is rejection sampling, remove it at next commit
    """
    p=s.mode_polytope[mode]
    return sample_from_polytope(p)
        
def sample_from_mode_old(s,mode,max_iterations=1000):
    """
    This is rejection sampling, remove it at next commit
    """
    i=0
    while i<max_iterations:
        x=sample(s.l[mode],s.u[mode])
        a=np.dot(s.H[mode],x)<=s.h[mode]
        if sum(a)==s.h[mode].shape[0]:
            return x
        else:
            i+=1
    raise("reached maximum iterations of sampling. Either increase maximum iterations, reshape the bounding box, or design a better sampler")