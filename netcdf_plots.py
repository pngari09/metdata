import os
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# --- Settings ---
folder_path = r"D:\test_netcdf"
output_plot = r"D:\test_netcdf\plot.png"
output_csv = r"D:\test_netcdf\values.csv"
target_lon = 36.1
target_lat = 0
variable_name = None  # Set to a specific variable name or leave None to auto-detect

# --- Helper functions ---


def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx


def extract_date_from_filename(filename):
    try:
        digits = ''.join(filter(str.isdigit, filename))
        return datetime.strptime(digits[:8], "%Y%m%d")
    except:
        return None


# --- Data extraction ---
records = []

for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".nc"):
        file_path = os.path.join(folder_path, filename)
        date = extract_date_from_filename(filename)
        if not date:
            print(f"Skipping {filename} (no date found)")
            continue

        try:
            ds = nc.Dataset(file_path)

            lat_var = 'lat' if 'lat' in ds.variables else 'latitude'
            lon_var = 'lon' if 'lon' in ds.variables else 'longitude'

            lats = ds.variables[lat_var][:]
            lons = ds.variables[lon_var][:]

            lat_idx = find_nearest(lats, target_lat)
            lon_idx = find_nearest(lons, target_lon)

            # Auto-detect variable if needed
            if variable_name is None:
                for var in ds.variables:
                    if var not in [lat_var, lon_var, 'time']:
                        variable_name = var
                        break

            if variable_name not in ds.variables:
                print(f"{variable_name} not in {filename}, skipping.")
                continue

            data_var = ds.variables[variable_name]

            if data_var.ndim == 3:
                value = data_var[0, lat_idx, lon_idx]
            elif data_var.ndim == 2:
                value = data_var[lat_idx, lon_idx]
            else:
                print(f"Unsupported variable shape in {filename}")
                continue

            records.append({'Date': date, 'Value': float(value)})

            ds.close()

        except Exception as e:
            print(f"Error reading {filename}: {e}")

# --- Save & Plot ---
if records:
    df = pd.DataFrame(records)
    df.sort_values('Date', inplace=True)

    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"CSV saved to {output_csv}")

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Value'], marker='o')
    plt.title(f"{variable_name} at lon={target_lon}, lat={target_lat}")
    plt.xlabel("Date")
    plt.ylabel(variable_name)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_plot)
    plt.close()
    print(f"Plot saved to {output_plot}")
else:
    print("No data extracted.")
