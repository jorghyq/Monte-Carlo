import numpy as np
import re

class EnergyTable:
    def __init__(self,table_path):
        # x,y,theta,e
        print table_path
        self.x_low = None
        self.y_low = None
        with open(table_path,'r') as f:
            headers = f.readlines()
            for line in headers:
                #print line
                if re.search(r'theta range', line):
                    self.theta_range = float(line.split(':')[1].strip())
                if re.search(r'theta step', line):
                    self.theta_step = float(line.split(':')[1].strip())
                if re.search(r'x range', line):
                    self.x_range = float(line.split(':')[1].strip())
                if re.search(r'x step', line):
                    self.x_step = float(line.split(':')[1].strip())
                if re.search(r'y range', line):
                    self.y_range = float(line.split(':')[1].strip())
                if re.search(r'y step', line):
                    self.y_step = float(line.split(':')[1].strip())
                if re.search(r'x low', line):
                    self.x_low = float(line.split(':')[1].strip())
                if re.search(r'y low', line):
                    self.y_low = float(line.split(':')[1].strip())
                if re.search(r'TABLE START',line):
                    ind = headers.index(line)
                    #print ind+1
                    break
        if not self.x_low:
            self.x_low = 0
        if not self.y_low:
            self.y_low = 0
        self.table = np.loadtxt(table_path, skiprows=ind+1,delimiter=',')
        self.x_min = -self.x_range
        self.x_max = self.x_range
        self.y_min = -self.y_range
        self.y_max = -self.y_range

    def load_table(self,table_path):
        pass
        # TODO load table path

    def save_table(self,table_path):
        pass
        # TODO when needed, save the modified table

    def get_phi(self):
        return self.phi

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_energy(self):
        return self.energy

    def print_table(self):
        print self.table

    def print_header(self):
        print "theta range: %0.2f, step: %0.2f" % (self.theta_range, self.theta_step)
        print "x range: %0.2f, step: %0.2f, low: %0.2f" % (self.x_range, self.x_step, self.x_low)
        print "y range: %0.2f, step: %0.2f, low: %0.2f" % (self.y_range, self.y_step, self.y_low)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = './etables/inter_mol.txt'
    e_table = EnergyTable(file_name)
    e_table.print_table()
    e_table.print_header()
