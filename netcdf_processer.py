import os
import netCDF4 as nc
import numpy as np
import pandas as pd
from datetime import datetime

# --- Config ---
folder_path = r"D:/test_netcdf"
output_csv = os.path.join(folder_path, "point_extract.csv")
target_lat = -1.2
target_lon = 36.2

# --- Helpers ---


def extract_date_from_filename(filename):
    try:
        parts = filename.split('_')
        for part in parts:
            if part.isdigit() and len(part) == 8:
                return datetime.strptime(part, "%Y%m%d").date()
    except:
        pass
    return None


def find_nearest(array, value):
    return (np.abs(array - value)).argmin()


# --- Main ---
records = []

for filename in sorted(os.listdir(folder_path)):
    if not filename.endswith(".nc"):
        continue

    file_date = extract_date_from_filename(filename)
    if not file_date:
        print(f"Skipping {filename}: could not extract date")
        continue

    filepath = os.path.join(folder_path, filename)
    print(f"Processing {filename}...")

    try:
        ds = nc.Dataset(filepath)

        # Detect temperature variable (first one starting with 't')
        temp_var_name = next(
            (v for v in ds.variables if v.lower().startswith("t")), None)
        if not temp_var_name:
            print(f"Skipping {filename}: no temperature variable found.")
            continue

        temp_data = ds.variables[temp_var_name]
        dims = temp_data.dimensions

        # Try direct lat/lon
        lat_var = ds.variables.get("lat") or ds.variables.get("latitude")
        lon_var = ds.variables.get("lon") or ds.variables.get("longitude")

        # If missing, try coordinates attribute
        if lat_var is None or lon_var is None and hasattr(temp_data, "coordinates"):
            coord_names = temp_data.coordinates.split()
            for name in coord_names:
                var = ds.variables.get(name)
                if var is not None:
                    if "lat" in name.lower():
                        lat_var = var
                    elif "lon" in name.lower():
                        lon_var = var

        if lat_var is None or lon_var is None:
            print(f"Skipping {filename}: could not find lat/lon.")
            continue

        lats = lat_var[:]
        lons = lon_var[:]

        lat_idx = find_nearest(lats, target_lat)
        lon_idx = find_nearest(lons, target_lon)

        # Extract value
        if temp_data.ndim == 3:
            value = float(temp_data[0, lat_idx, lon_idx])
        elif temp_data.ndim == 2:
            value = float(temp_data[lat_idx, lon_idx])
        else:
            print(f"Unsupported data shape in {filename}")
            continue

        lat_val = float(lats[lat_idx])
        lon_val = float(lons[lon_idx])

        records.append({
            "date": file_date.isoformat(),
            "lat": lat_val,
            "lon": lon_val,
            "temperature": value,
            "filename": filename
        })

        ds.close()

    except Exception as e:
        print(f"Error reading {filename}: {e}")

# --- Save ---
if records:
    df = pd.DataFrame(records)
    df.sort_values("date", inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Extracted {len(df)} records.")
    print(f"📄 Saved to {output_csv}")
else:
    print("⚠️ No data extracted.")
