#class elements will be defined here
import numpy as np

class Elements:
    def __init__(self, num, type_num):
        self.num = num
        self.init_num = 0
        self.type_num = type_num
        # 4 columns : x, y, theta, type
        self.conf = np.zeros((self.num,4))
        # correlation table, when two molecules are close, corr_table[i][j]=1
        self.corr_table = np.zeros((self.num, self.num))

    def load_energy_table(self,energy_table_path):
        self.energy_table = np.loadtxt('inter.txt',skiprows=6,delimiter=',')

    def init(self, shape):
        # initialize the molecules on the surface
        pass

    def update(self,ind,x,y,theta):
        # update the self.conf array
        pass

