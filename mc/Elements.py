#class elements will be defined here

import numpy as np

class Elements:
    def __init__(self, num, type_num):
        self.num = num
        self.num_init = 0
        self.type_num = type_num
        # 4 columns : x, y, theta, type
        self.conf = np.zeros((self.num,4))
        #self.conf[:,-1] = 1
        # correlation table, when two molecules are close, corr_table[i][j]=1
        self.corr_table = np.zeros((self.num, self.num))

    #def load_energy_table(self,energy_table_path):
    #    self.energy_table = np.loadtxt('inter.txt',skiprows=6,delimiter=',')

    #def init(self, shape):
    #    # initialize the molecules on the surface
    #    pass

    def update(self,ind,x,y,theta,typ=None):
        # update the self.conf array
        if typ:
            self.conf[ind,:] = [x,y,theta,typ]
        else:
            self.conf[ind,:-1] = [x,y,theta]

    def get_conf(self):
        if self.num_init == self.num:
            return self.conf
        else:
            return self.conf[:self.num_init,:]

