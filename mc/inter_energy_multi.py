#!/usr/bin/python
# -*- coding: utf-8 -*-

#import math
import numpy as np
from Elements import Elements
from EnergyTables import EnergyTables

def inter_energy_multi(ind,x,y,theta,typ,elements,inter_energy_tables):
    if elements.num_init == 0:
        return True, 0
    if elements.num_init != elements.num:
        input_mat = np.tile([x,y,theta,0],(elements.num_init,1))
        mol_mat = elements.conf[0:elements.num_init,0:4]
        dif_mat = np.zeros((elements.num_init,4))
    else:
        mol_mat = elements.conf[0:elements.num_init,0:4]
        if ind >= 0:
            input_mat = np.tile([x,y,theta,0],(elements.num_init-1,1))
            mol_mat = np.delete(mol_mat,ind,0)
            dif_mat = np.zeros((elements.num_init-1,4))
        else:
            input_mat = np.tile([x,y,theta,0],(elements.num_init,1))
            dif_mat = np.zeros((elements.num_init,4))
    # matrixing the input position
    # compute the difference of elements with input position
    #print elements.conf[0:elements.num_init,0:3]
    dif_mat[:,0:4] = mol_mat - input_mat
    #print dif_mat
    # remove the point that is already in there
    #dif_mat[:,3] = np.sqrt(np.power(dif_mat[:,0],2)+np.power(dif_mat[:,1],2))
    #if (dif_mat[:,0]<)&(dif_mat[:,1]<): return False,0
    dif_mat = dif_mat[(np.fabs(dif_mat[:,0]) < inter_energy_tables.x_range_max) & \
                      (np.fabs(dif_mat[:,1]) < inter_energy_tables.y_range_max)]
    #print dif_mat.shape
    if dif_mat.shape[0] == 0:
        return True, 0
    energies = np.zeros(dif_mat.shape[0])
    #print "input conf: %f, %f, %f" % (x,y,theta)
    #print dif_mat
    #print elements.print_conf()
    for i in range(0,dif_mat.shape[0]):
        #print dif_mat[i,:2]
        #print i
        energy_temp = fit_energy_multi(typ,dif_mat[i,:],inter_energy_tables)
        #print "energy_temp: %f" % energy_temp
        #var = raw_input("Please enter something: ")
        if energy_temp > 0:
            return False, 0
        else:
            energies[i] = energy_temp
    energy = energies.sum()
    return True, energy

def fit_energy_multi(typ,conf,e_tables):
    #print conf.shape
    #print conf
    #print typ
    assert len(conf.shape) < 2
    if int(conf[-1]) == 0:
        key = str(int(typ)) + str(int(typ))
    else:
        key = str(int(typ)) + str(int(conf[-1]))
    #print key
    energy_table = e_tables.get_energy_table(key)
    if conf[0] > energy_table.x_range or conf[1] > energy_table.y_range:
        return 0
    #x_ind = (np.floor((conf[0,0] - energy_table.x_min)/energy_table.x_step)).astype(int)
    #y_ind = (np.floor((conf[0,1] - energy_table.y_min)/energy_table.y_step)).astype(int)
    x_ind = int(np.floor((conf[0] - energy_table.x_min)/energy_table.x_step))
    y_ind = int(np.floor((conf[1] - energy_table.y_min)/energy_table.y_step))
    #print conf[0,0],x_ind,conf[0,1],y_ind,energy_table.table[x_ind,y_ind]
    return energy_table.table[x_ind,y_ind]

if __name__ == "__main__":
    elem = Elements(3,'C')
    elem.num_init = 3
    elem.conf[0,:] = [3,3,0,1]
    elem.conf[1,:] = [2,5,0,1]
    elem.conf[2,:] = [7,7,0,1]
    print elem.conf
    conf_1 = np.array([[3,4,0]])
    conf_2 = np.array([[3,3,0],[3,6,0]])
    e_tables = EnergyTables()
    e_tables.load_energy_table('11','inter_mol.txt')
    e_tables.load_energy_table('12','inter_mol_metal.txt')
    e_tables.load_energy_table('21','inter_metal_mol.txt')
    e_tables.load_energy_table('22','inter_metal.txt')
    #print e_tables.get_energy_table['11']
    e = inter_energy_multi(-1,8,8,0,1,elem,e_tables)
    print e
