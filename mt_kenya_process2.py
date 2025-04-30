import os
import re
import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Settings ---
folder_path = r"D:/test_netcdf"
output_csv = os.path.join(folder_path, "data.csv")
output_plot = os.path.join(folder_path, "plot.png")

target_lon = 36.1
target_lat = -1.2432
