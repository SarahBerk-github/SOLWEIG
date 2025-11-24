######################################################################################################
######## Code to break up a large raster DSM into smaller tiles, so it can be used in SOLWEIG ########
######################################################################################################
# Sarah Berk sberk@unc.edu

import os, os.path
import rasterio as rio
from rasterio.windows import Window
from osgeo import gdal
from osgeo.gdalconst import *
from matplotlib import pyplot as plt
import numpy as np
import time
import math
from rasterio.warp import calculate_default_transform, reproject

### For the tree canopy SVFs, need to use a dsm with only the trees, where there are no trees the dsm is 0, where there are trees it is tree height

# Input and output paths

#input_tif = '/nas/longleaf/home/sberk/SVF_for_Durham_ML/tree_dsms/Durham_Tree_DSM_with_DEM.tif'

#input_tif = '/nas/longleaf/home/sberk/SVF_for_Durham_ML/tree_dsms/Durham_Tree_Only_DSM.tif'

input_tif = '/nas/longleaf/home/sberk/SVF_for_Durham_ML/tree_dsms/Durham_Tree_DSM_EVI_Masked.tif'

#### !!!! Run the below code in bash to create the merged dsm ####
#gdalbuildvrt merged.vrt Durham_Building_DSM_*.tif

#vrt_path = '/nas/longleaf/home/sberk/SVF_for_Durham_ML/tree_canopy_dsms/merged.vrt'
output_folder = '/nas/longleaf/home/sberk/SVF_for_Durham_ML/evi_filtered_tree_dsm_tiles'

# Tile and buffer size in meters
tile_size_m = 1000 # note, the tile size ends up being 1000x1000 pixels, but its size in meters is actually 1300
buffer_m = 150

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Open the input raster (should be in EPSG:32617) 
with rio.open(input_tif) as src:
#with rio.open(vrt_path) as src:   # if you are only using one tif file you can replace vrt_path with input_tif and uncomment it above
    transform = src.transform
    crs = src.crs
    bounds = src.bounds
    minx, miny, maxx, maxy = bounds

    # Calculate number of tiles in X and Y directions
    num_tiles_x = int(np.ceil((maxx - minx - tile_size_m) / (tile_size_m - buffer_m)))
    num_tiles_y = int(np.ceil((maxy - miny - tile_size_m) / (tile_size_m - buffer_m)))

    print(f"Image size: {src.width} x {src.height} pixels")
    print(f"Total tiles: {num_tiles_x} x {num_tiles_y}")

    # Iterate over tiles
    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            x_off = minx + i * (tile_size_m - buffer_m)
            y_off = miny + j * (tile_size_m - buffer_m)
            x_end = min(maxx, x_off + tile_size_m)
            y_end = min(maxy, y_off + tile_size_m)

            # Get window in pixel coordinates
            window = src.window(x_off, y_off, x_end, y_end)

            # Read data in window
            tile_data = src.read(1, window=window)
            # Skip tile if any values are NaN - these will be tiles right at the edge so not important (as there was a buffer) and they mess up the svf calc code later
            if np.isnan(tile_data).any():
                print(f"Skipping tile {i}_{j} (contains NaN)")
                continue
            
            # Output path
            output_filename = os.path.join(output_folder, f"tile_{i}_{j}.tif")

            # Write tile
            with rio.open(
                output_filename, 'w',
                driver='GTiff',
                count=1,
                dtype=tile_data.dtype,
                width=tile_data.shape[1],
                height=tile_data.shape[0],
                crs=crs,
                transform=src.window_transform(window)
            ) as dst:
                dst.write(tile_data, 1)
                
                print(f"Size{tile_data.shape[1]} x {tile_data.shape[0]} pixels")
            print(f"Written tile {i}_{j} to {output_filename}")
            
print("Tiling completed")
