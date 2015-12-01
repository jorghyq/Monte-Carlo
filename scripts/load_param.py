# This function load configuration file

import os
import re
import pandas as pd

def load_param(conf_path, skiprows, seperator):
    if os.path.isfile(conf_path):


