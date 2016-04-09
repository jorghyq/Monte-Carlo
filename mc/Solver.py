# main class solver will be defined here
import sys
import math
import random as rd
import numpy as np
import os
import matplotlib.pyplot as plt
#from load_param import load_param
from Elements import Elements
from EnergyTable import EnergyTable
from EnergyTables import EnergyTables
from inter_energy import inter_energy
from inter_energy_multi import inter_energy_multi

class Solver():
    def __init__(self, element_num, lattice_size):
        self.param = {}
        # default settings of the lattice
        # TODO finish the load param function
        #self.param = load_param(config_path)
        self.element_num = element_num
        self.lattice_size = lattice_size
        self.mol = Elements(self.element_num,'TPyP')
        self.step_counter = 0

    def init_single(self):
        while self.mol.num_init < self.mol.num:
            ind,x,y,theta = self.get_new_conf()
            state, energy = inter_energy(self.mol.num_init,x,y,theta,self.mol,self.energy_table)
            if state:
                self.mol.update(self.mol.num_init,x,y,0)
                self.mol.num_init = self.mol.num_init + 1
                #print x,y,theta,self.mol.conf
                #print state, energy
                #self.show()
            else:
                continue

    def init_multi(self,setting = None):
        if setting:
            self.element_settings = setting
            self.element_type_num = len(setting)
        while self.mol.num_init < self.mol.num:
            for typ,num in enumerate(self.element_settings):
                print "type # %d has %d element" % (typ, num)
                i = 0
                while i < num:
                    ind,x,y,theta = self.get_new_conf()
                    state, energy = inter_energy_multi(self.mol.num_init,x,y,theta,typ+1,self.mol,self.e_tables)
                    if state:
                        self.mol.update(self.mol.num_init,x,y,0,typ+1)
                        self.mol.num_init = self.mol.num_init + 1
                        i = i + 1
                #print x,y,theta,self.mol.conf
                #print state, energy
                #self.show()
            else:
                continue

    def step_single(self, step_num, SHOW_MODE=0):
        step_to_go = step_num
        hundredth = step_num/100
        if step_num <= 0:
            print "step number should be positve integer"
        else:
            while step_to_go > 0:
                # pick a molecule and its new random position and angle
                ind,x,y,theta = self.get_new_conf()
                # get its old position and angle
                x_old,y_old,theta_old = self.mol.conf[ind,:3]
                # compute the energy of the old and new configuration,
                # respectively
                state_old, energy_old = inter_energy(ind,x_old,y_old,theta_old,self.mol,self.energy_table)
                state_new, energy_new = inter_energy(-1,x,y,theta,self.mol,self.energy_table)
                if state_new:
                    p = min(math.exp(-(energy_new-energy_old)),1)
                    if p > rd.random():
                        # TODO: finish the metropolis part
                        self.mol.update(ind,x,y,theta)
                step_to_go = step_to_go - 1
                if step_to_go%hundredth == 0:
                    if step_to_go != step_num:
                        print "%d / %d done" % (100-step_to_go/hundredth,100)

    def step_multi(self, step_num, SHOW_MODE=0):
        step_to_go = step_num
        hundredth = step_num/100
        if step_num <= 0:
            print "step number should be positve integer"
        else:
            while step_to_go > 0:
                # pick a molecule and its new random position and angle
                ind,x,y,theta = self.get_new_conf()
                # get its old position and angle
                x_old,y_old,theta_old,typ_old = self.mol.conf[ind,:]
                # compute the energy of the old and new configuration,
                # respectively
                state_old, energy_old = inter_energy_multi(ind,x_old,y_old,theta_old,typ_old,self.mol,self.e_tables)
                state_new, energy_new = inter_energy_multi(-1,x,y,theta,typ_old,self.mol,self.e_tables)
                if state_new:
                    p = min(math.exp(-(energy_new-energy_old)),1)
                    if p > rd.random():
                        # TODO: finish the metropolis part
                        self.mol.update(ind,x,y,theta)
                step_to_go = step_to_go - 1
                if step_to_go%hundredth == 0:
                    if step_to_go != step_num:
                        print "%d / %d done" % (100-step_to_go/hundredth,100)


    def load_inter_map(self, inter_map_path):
        # load intermolecular interaction energy map
        self.energy_table = EnergyTable(inter_map_path)

    def load_inter_maps(self):
        self.e_tables = EnergyTables()


    def load_surf_map(self, surf_map_path):
        # load surface interaction energy map
        pass

    def get_new_conf(self,INIT=False):
        ind_mol = rd.randint(0,self.element_num-1)
        x = rd.randint(0,self.lattice_size-1)
        y = rd.randint(0,self.lattice_size-1)
        theta = 0
        return ind_mol,x,y,theta

    def show(self):
        #x = [-1.5,-0.5,-0.5,0.5,0.5,1.5,1.5,0.5,0.5,-0.5,-0.5,-1.5,-1.5]
        #y = [0.5,0.5,1.5,1.5,0.5,0.5,-0.5,-0.5,-1.5,-1.5,-0.5,-0.5,0.5]
        #xy1 = list(zip(x,y))
        marker_options = ['+','.','o','1']
        for typ,num in enumerate(self.element_settings):
            print typ, num
            print self.mol.conf
            conf = self.mol.conf[self.mol.conf[:,-1] == typ + 1]
            print conf
            plt.scatter(conf[:,0],conf[:,1],s=500,c='r',marker=marker_options[typ],linewidth=4)
            plt.xticks(range(0,self.lattice_size))
            plt.yticks(range(0,self.lattice_size))
            plt.grid(True)
            plt.hold(True)
        plt.show()

    def write_conf(self,path_to_write):
        np.savetxt(path_to_write,self.mol.conf,fmt='%0.1d',delimiter=',')


if __name__ == "__main__":
    SINGLE = False
    if SINGLE:
        solver = Solver(40,40)
        solver.load_inter_map('inter.txt')
        solver.init()
        print solver.mol.get_conf()
        solver.step_single(100000)
        solver.write_conf('test.txt')
        solver.show()
    else:
        solver = Solver(40,40)
        solver.load_inter_maps()
        solver.e_tables.load_energy_table('11','inter_mol.txt')
        solver.e_tables.load_energy_table('12','inter_mol_metal.txt')
        solver.e_tables.load_energy_table('21','inter_metal_mol.txt')
        solver.e_tables.load_energy_table('22','inter_metal.txt')
        solver.init_multi([20,20])
        print "######### INIT DONE ###########"
        solver.step_multi(10000000)
        solver.show()

