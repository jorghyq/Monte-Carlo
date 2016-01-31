# main class solver will be defined here
import sys
import random as rd
import numpy as np
import os
#from load_param import load_param
from elements import Elements

class Solver():
    def __init__(self, config_path):
        self.param = {}
        # default settings of the lattice
        # TODO finish the load param function
        #self.param = load_param(config_path)
        self.element_num = 20
        self.lattice_size = 20
        self.mol = Elements(self.element_num,'TPyP')
        self.step_counter = 0

    def init(self):
        for self.mols.init_num != self.mols.num:
            ind,x,y,theta = self.get_new_conf()
            state, energy = inter_energy(x,y,theta,self.mol)
            if state == 1:
                self.mol.update(self.mols.init_num,x,y,theta)
                self.mols.init_num = self.mols.init_num + 1
            else:
                continue
        # TODO: initialize the elements

    def step(self, step_num):
        if step_num <= 0:
            print "step number should be positve integer"
        else:
            while step_num > 0:
                # pick a molecule and its new random position and angle
                ind,x,y,theta = self.get_new_conf()
                # get its old position and angle
                x_old, y_old, theta_old = self.mol.conf[ind,:]
                # compute the energy of the old and new configuration,
                # respectively
                state_old, energy_old = inter_energy(x_old,y_old,theta_old,self.mol)
                state, energy = inter_energy(x,y,theta,self.mol)
                if state == 1:
                    # TODO: finish the metropolis part



    def load_inter_map(self, inter_map_path):
        # load intermolecular interaction energy map
        pass

    def load_surf_map(self, surf_map_path):
        # load surface interaction energy map
        pass

    def get_new_conf(self,INIT=False):
        ind_mol = rd.randint(0,self.element_num)
        x = rd.randint(0,self.lattice_size)
        y = rd.randint(0,self.lattice_size)
        theta = 0
        return ind_mol,x,y,theta
