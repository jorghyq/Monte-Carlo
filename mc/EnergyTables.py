import numpy as np
import re
from EnergyTable import EnergyTable

class EnergyTables:
    def __init__(self):
        self.table_num = 0
        self.energy_tables = {}
        self.x_range_max = 0
        self.y_range_max = 0

    def load_energy_table(self,key,table_path):
        # x,y,theta,e
        energy_table = EnergyTable(table_path)
        self.energy_tables[key] = energy_table
        self.table_num = self.table_num + 1
        if self.energy_tables[key].x_range > self.x_range_max:
            self.x_range_max = self.energy_tables[key].x_range
        if self.energy_tables[key].y_range > self.y_range_max:
            self.y_range_max = self.energy_tables[key].y_range

    def remove_energy_table(self,key):
        del self.energy_tables[key]

    def get_energy_table(self,key):
        return self.energy_tables[key]

if __name__ == "__main__":
    e_table = EnergyTables()
    e_table.load_energy_table('11','inter_mol.txt')
    e_table.load_energy_table('12','inter_mol_metal.txt')
    e_table.load_energy_table('21','inter_metal_mol.txt')
    e_table.load_energy_table('22','inter_metal.txt')
    print e_table.table_num
    print type(e_table.energy_tables)
    for key,value in e_table.energy_tables.iteritems():
        print key
