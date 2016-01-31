
import numpy as np
from elements import Elements

def inter_energy(x,y,theta,elements,inter_energy_table):
    # get the minima and maxima of the interaction distance
    r_min = inter_energy_table[0,1]
    r_max = inter_energy_table[0,-1]
    print r_min, r_max
    # matrixing the input position
    input_mat = np.tile([x,y,theta],(elements.init_num,1))
    print input_mat
    #print input_mat.shape
    dif_mat = np.zeros((elements.init_num,4))
    # compute the difference of elements with input position
    print elements.conf[0:elements.init_num,0:3]
    dif_mat[:,0:3] = elements.conf[0:elements.init_num,0:3] - input_mat
    print dif_mat
    # remove the point that is already in there
    #dif_mat = dif_mat[~np.array([0,0,0,0])]
    dif_mat[:,3] = np.sqrt(np.power(dif_mat[:,0],2)+np.power(dif_mat[:,1],2))
    print dif_mat
    if (dif_mat[:,3] <= r_min).sum() > 0:
        return False,0
    elif (dif_mat[:,3] <= r_max).sum() < 0:
        return True,0
    else:
        neighbours = dif_mat[dif_mat[:,3]<=r_max]
        print neighbours
        energies = np.zeros(neighbours.shape[0])
        #for i in range(0,neighbours.shape[1]):
        energies = fit_energy(neighbours[:,2:4],inter_energy_table)
        energy = energies.sum()
        return True, energy

def fit_energy(conf,energy_table):
    theta_input = conf[:,0]
    theta_min = energy_table[1,0]
    r_input = conf[:,1]
    r_min = energy_table[0,1]
    print r_min, theta_min
    r = energy_table[0,1:]
    print r
    r_dr = r[1] - r[0]
    theta = energy_table[1:,0]
    print theta
    theta_dtheta = theta[1] - theta[0]
    e = energy_table[1:,1:]
    r_ind = (np.floor((r_input - r_min)/r_dr)).astype(int)
    theta_ind = (np.floor((theta_input - theta_min)/theta_dtheta)).astype(int)
    print r_ind, theta_ind
    return e[theta_ind,r_ind]

if __name__ == "__main__":
    elem = Elements(3,'C')
    elem.init_num = 3
    elem.conf[0,:] = [3,3,0,0]
    elem.conf[1,:] = [2,5,0,0]
    elem.conf[2,:] = [9,3,0,0]
    print elem.conf
    conf_1 = np.array([[3,3,0],[2,5,0]])
    conf_2 = np.array([[3,3,0],[3,6,0]])
    energy_table = np.loadtxt('inter.txt',skiprows=6,delimiter=',')
    e = inter_energy(3,2,0,elem,energy_table)
    print e
