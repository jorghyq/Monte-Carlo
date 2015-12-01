# main class solver will be defined here
import sys
import random as rd
import numpy as np
import os
from load_param import load_param


class Solver():
    def __init__(self, config_path):
        self.param = {}
        # default settings of the lattice
        self.param = load_param(config_path)
        self.step_counter = 0

    def init(self):
        # TODO: initialize the elements

    def step(self, step_num):
        if step_num <= 0:
            print "step number should be positve integer"
        else:
            while step_num > 0:
                pass

    def load_inter_map(self, inter_map_path):
        # load intermolecular interaction energy map
        pass

    def load_surf_map(self, surf_map_path):
        # load surface interaction energy map
        pass

