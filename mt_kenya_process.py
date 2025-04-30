import re
import pandas as pd
import numpy as np
import glob
import xarray as xr
import os
import sys
import subprocess

# List of required packages
required_packages = ["pandas", "scipy", "numpy", "xarray"]

# Install missing packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package])

# Import libraries


def get_tei49_as_csv():
    for folder in ["tei49c", "tei49i"]:
        all_files = glob.glob(os.path.join(folder, "*.zip"))
        for f in all_files:
            if 'all' not in f:
                try:
                    df = pd.read_table(
                        f, sep=r"\s+", index_col=[0, 2], header=0, compression='zip')
                    df.drop(columns=["pctime", "date"], errors="ignore").to_csv(
                        f"{folder}.csv", mode='a', header=not os.path.exists(f"{folder}.csv"))
                except Exception as e:
                    print(f"Error processing file {f}: {e}")


def get_VRXA_as_csv():
    patterns = [
        ("meteo/multi_target.VRXA00.*", r"\s+", "VRXA00_multi_target.csv", 0),
        ("meteo/multi_target.VRXA01.*", ";", "VRXA01_multi_target.csv", 0),
        ("meteo/multi_target_with_heading.VRXA00.*",
         r"\s+", "VRXA00_multi_target_with_heading.csv", 2),
        ("meteo/VRXA00.*", r"\s+", "VRXA00.csv", 2),
        ("meteo/VRXA01.*", ";", "VRXA01.csv", 2),
        ("meteo/VMSW43.*.zip", r"\s+", "VMSW43.csv", 2),
        ("meteo/VSRA02.*.zip", r"\s+", "VSRA02.csv", 2),
    ]

    for pattern, sep, output_file, header in patterns:
        all_files = glob.glob(pattern)
        for f in all_files:
            try:
                df = pd.read_table(f, sep=sep, index_col=[0, 1], header=header,
                                   compression='zip' if f.endswith('.zip') else None)
                df.to_csv(output_file, mode='a',
                          header=not os.path.exists(output_file))
            except Exception as e:
                print(f"Error processing file {f}: {e}")


def get_g2401_as_csv():
    all_files = glob.glob(os.path.join("g2401", "*.zip"))
    for f in all_files:
        try:
            df = pd.read_table(
                f, sep=r"\s+", index_col=[0, 1], header=0, compression='zip')
            df.to_csv("g2401.csv", mode='a',
                      header=not os.path.exists("g2401.csv"))
        except Exception as e:
            print(f"Error processing file {f}: {e}")


# Run the processing functions
get_tei49_as_csv()
get_VRXA_as_csv()
get_g2401_as_csv()
