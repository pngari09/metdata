import os
import sys
import subprocess
import glob

# Confirm working directory
print("Running from directory:", os.getcwd())

print("Files in 'meteo':", glob.glob("meteo/*"))





# Install required packages if missing
required_packages = ["pandas", "scipy", "numpy", "xarray"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Import libraries
import xarray as xr
import numpy as np
import pandas as pd
import re


def get_VRXA_as_csv():
    patterns = [
        ("meteo/multi_target.VRXA00.*", r"\s+", "VRXA00_multi_target.csv", 0),
        ("meteo/multi_target.VRXA01.*", ";", "VRXA01_multi_target.csv", 0),
        ("meteo/multi_target_with_heading.VRXA00.*", r"\s+", "VRXA00_multi_target_with_heading.csv", 2),
        ("meteo/VRXA00.*", r"\s+", "VRXA00.csv", 2),
        ("meteo/VRXA01.*", ";", "VRXA01.csv", 2),
        ("meteo/VMSW43.*.zip", r"\s+", "VMSW43.csv", 2),
        ("meteo/VSRA02.*.zip", r"\s+", "VSRA02.csv", 2),
    ]

    for pattern, sep, output_file, header in patterns:
        all_files = glob.glob(pattern)
        print(f"Found {len(all_files)} files for pattern '{pattern}'")
        for f in all_files:
            try:
                print(f"Reading: {f}")
                df = pd.read_table(f, sep=sep, index_col=[0, 1], header=header,
                                   compression='zip' if f.endswith('.zip') else None)
                df.to_csv(output_file, mode='a', header=not os.path.exists(output_file))
                print(f"Appended {len(df)} rows to {output_file}")
            except Exception as e:
                print(f"Error processing file {f}: {e}")


# Run processing
get_VRXA_as_csv()





