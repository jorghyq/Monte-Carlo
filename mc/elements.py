#class elements will be defined here
import numpy as np

class Elements:
    def __init__(self, num, symbol):
        self.num = num
        self.symbol = symbol
        # 3 columns : x, y, theta
        self.conf = np.zeros((self.num,3))
        # correlation table, when two molecules are close, corr_table[i][j]=1
        self.corr_table = np.zeros((self.num, self.num))

    def init(self, shape):
        # initialize the molecules on the surface
        pass

    def update(self):
        # update the self.conf array
        pass

