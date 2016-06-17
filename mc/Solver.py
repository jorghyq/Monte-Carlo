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
from inter_energy_real import inter_energy_real

class Solver():
    def __init__(self, setting_path):
        self.param = {}
        # default settings of the lattice
        self.element_num = element_num
        self.lattice_size = lattice_size
        self.mol = Elements(self.element_num,'TPyP')
        self.step_counter = 0

    def load_params(self, setting_path):
        if os.path.isfile(setting_path):
            with open(setting_path,'r') as f:
                lines = f.readlines()
            for line in lines:
                temp = line.split(':')
                self.param[temp[0].strip()] = temp[1].strip()

    def init_single(self):
        self.element_settings = [self.element_num]
        while self.mol.num_init < self.mol.num:
            ind,x,y,theta = self.get_new_conf_real()
            state, energy = inter_energy_real(self.mol.num_init,x,y,theta,self.mol,self.energy_table)
            if state:
                self.mol.update(self.mol.num_init,x,y,theta,1)
                self.mol.num_init = self.mol.num_init + 1
                print "element # %d is done" % self.mol.num_init
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
        tenth = step_num/10
        if step_num <= 0:
            print "step number should be positve integer"
        else:
            while step_to_go > 0:
                # pick a molecule and its new random position and angle
                ind,x,y,theta = self.get_new_conf_real()
                # get its old position and angle
                x_old,y_old,theta_old = self.mol.conf[ind,:3]
                # compute the energy of the old and new configuration,
                # respectively
                state_old, energy_old = inter_energy_real(ind,x_old,y_old,theta_old,self.mol,self.energy_table)
                state_new, energy_new = inter_energy_real(-1,x,y,theta,self.mol,self.energy_table)
                if state_new:
                    p = min(math.exp(-(energy_new-energy_old)),1)
                    if p > rd.random():
                        # TODO: finish the metropolis part
                        self.mol.update(ind,x,y,theta,1)
                step_to_go = step_to_go - 1
                if step_to_go%hundredth == 0:
                    if step_to_go != step_num:
                        print "%d / %d done" % (100-step_to_go/hundredth,100)
                if step_to_go%tenth == 0:
                    if step_to_go != step_num:
                        self.write_conf('temp/test_%d_%d.txt'%(100-step_to_go/tenth,step_num))
                        print "%d / %d is written to file" % (step_to_go/tenth,100)

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
                        self.write_conf('test.txt')


    def load_inter_map(self, inter_map_path):
        if self.param['etable_pre']:
            if self.param['element_type'] == 1:
                self.energy_table = EnergyTable(self.param['etable_pre']+'11'+self.param['etable_post'])
                print 'Energy table loaded'
            else:
                self.e_tables = EnergyTables()
                for i in range(self.param['element_type']):
                    for j in range(self.param['element_type']):
                        ind = ('%d%d') % (i+1,j+1)
                        self.e_tables.load_energy_table(ind,self.param['etable_pre']+ind+self.param ['etable_post'])
                        print 'Energy table %s loaded' % ind

    def load_surf_map(self, surf_map_path):
        # load surface interaction energy map
        pass

    def get_new_conf(self,INIT=False):
        if self.param[real]:
            ind_mol = rd.randint(0,self.element_num-1)
            x = rd.uniform(0,self.lattice_size-1)
            y = rd.uniform(0,self.lattice_size-1)
            #theta = rd.randint(0,12)*30
            theta = 0
            #theta = rd.randint(0,360)
        else:
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

    def show_real(self):
        x_coor = self.mol.conf[:,0]
        y_coor = self.mol.conf[:,1]
        theta = self.mol.conf[:,2]
        print theta
        arm_length = 16
        x_min = x_coor - arm_length * np.cos(theta/180*np.pi)
        x_max = x_coor + arm_length * np.cos(theta/180*np.pi)
        y_min = y_coor - arm_length * np.sin(theta/180*np.pi)
        y_max = y_coor + arm_length * np.sin(theta/180*np.pi)
        theta_comp = theta + 90
        x_min2 = x_coor - arm_length * np.cos(theta_comp/180*np.pi)
        x_max2 = x_coor + arm_length * np.cos(theta_comp/180*np.pi)
        y_min2 = y_coor - arm_length * np.sin(theta_comp/180*np.pi)
        y_max2 = y_coor + arm_length * np.sin(theta_comp/180*np.pi)
        #plt.plot(x_coor,y_min)
        for i in range(x_coor.size):
            #plt.axhline(y=y_coor[i],xmin=x_min[i],xmax=x_max[i],linewidth=4)
            #plt.axvline(x=x_coor[i],ymin=y_min[i],ymax=y_max[i],linewidth=4)
            #plt.hold(True)
            #plt.plot([x_coor[i],x_coor[i]],[y_min[i],y_max[i]],linewidth=4)
            #plt.plot([x_min[i],x_max[i]],[y_coor[i],y_coor[i]],linewidth=4)
            plt.arrow(x_min[i],y_min[i],x_max[i]-x_min[i],y_max[i]-y_min[i],fc='b',ec='b',linewidth=4,head_width=0.05,head_length=0.1)
            plt.plot([x_min2[i],x_max2[i]],[y_min2[i],y_max2[i]],'b',linewidth=4)
            plt.hold(True)
        plt.axes().set_aspect('equal', 'datalim')
        plt.scatter(x_coor,y_coor,s=50,c='r',marker='o',linewidth=4)
        plt.xlim([-20,self.lattice_size+20])
        plt.ylim([-20,self.lattice_size+20])
        plt.show()

    def write_conf(self,path_to_write):
        np.savetxt(path_to_write,self.mol.conf,fmt='%0.1d',delimiter=',')


if __name__ == "__main__":
    SINGLE = True
    import sys
    if len(sys.argv) > 1:
        RUNS = float(sys.argv[1])
    else:
        RUNS = 1000000
    if SINGLE:
        solver = Solver('settings.ini')
        solver.load_inter_map()
        solver.init_single()
        print solver.mol.get_conf()
        solver.step_single(RUNS)
        solver.write_conf('test.txt')
        solver.show_real()
    else:
        solver = Solver(40,40)
        solver.load_inter_maps()
        solver.e_tables.load_energy_table('11','./etables/inter_mol.txt')
        solver.e_tables.load_energy_table('12','./etables/inter_mol_metal.txt')
        solver.e_tables.load_energy_table('21','./etables/inter_metal_mol.txt')
        solver.e_tables.load_energy_table('22','./etables/inter_metal.txt')
        solver.init_multi([20,20])
        print "######### INIT DONE ###########"
        solver.step_multi(RUNS)
        solver.show()

