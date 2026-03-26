#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 08:48:19 2026

@author: baf739
"""

import GPRClass as gpr #Custom built class for handling the tree GPR Data
import matplotlib.pyplot as plt #For Plotting
import ProcessingMethods as pm
import pandas as pd
from scipy import interpolate
import numpy as np


#SET FONT STYLE FOR PLOTS
font = {'family' : 'Times New Roman',
    'weight' : 'regular',
    'size'   : 14}
plt.rc('font', **font)

import warnings
warnings.filterwarnings('ignore')


#Figure 1a

# Line numbers to highlight in the plot
ELEVATION_GEO_TIFF = '../ElevationData/SCBG_2cm_DEM_shift.tif'
HILL_SHADE_TIFF = '../ElevationData/SCBG_2cm_HS_shift.tif'
TOTAL_STATION_CSV = '../Data/locations_all.csv'
TOTAL_STATION_FILE = '../Data/08122024_cor.txt'
OUTPUT_IMAGE = 'Fig01a_SCBG_oak_map.png'
HIGHLIGHTED_LINES = [21, 35, 55]
LINE_COLORS = ['tab:blue', 'tab:orange', 'tab:purple']

elev_shfit = -1.9
# Read elevation and hillshade data from GeoTIFF files
easting_hs, northing_hs, hs = pm.getDataFromGeoTiff(HILL_SHADE_TIFF)
easting, northing, elev = pm.getDataFromGeoTiff(ELEVATION_GEO_TIFF)
elev += elev_shfit
# Create an interpolator for elevation data
#f = interpolate.interp2d(easting, northing, elev, kind='linear')
EEE,NNN = np.meshgrid(easting,northing)
points = np.column_stack([EEE.ravel(),NNN.ravel()])
f = interpolate.LinearNDInterpolator(points, elev.ravel())
#f = interpolate.RectBivariateSpline(easting, northing, elev_2d.T, kx=1, ky=1, s=0)

# Read total station data from CSV file
df_locs = pd.read_csv(TOTAL_STATION_CSV)

# Read canopy location data from the total station file
xGrid, yGrid, zGrid = pm.read_total_station_output(TOTAL_STATION_FILE)
totalStation_df = pd.read_csv(TOTAL_STATION_FILE)

# Extract canopy coordinates
ind3 = totalStation_df['name'].str.startswith('CANOPY')
canopy_x = totalStation_df['x'][ind3].to_numpy()
canopy_y = totalStation_df['y'][ind3].to_numpy()
canopy_x = np.append(canopy_x, canopy_x[0])
canopy_y = np.append(canopy_y, canopy_y[0])

#%%
# Initialize the figure and axis
fig = plt.figure(constrained_layout=True, figsize=[10, 10])
ax = fig.add_subplot(111)

# Plot elevation and hillshade background
cbar = ax.pcolormesh(easting, northing, elev, cmap='Spectral_r', vmin=-2, vmax=2)
ax.pcolormesh(easting, northing, hs, cmap='gray', vmin=0, vmax=255, alpha=0.2)

# Initialize arrays to store start and end coordinates for each line
start_x_all = np.zeros(df_locs.shape[0])
start_y_all = np.zeros(df_locs.shape[0])
end_x_all = np.zeros(df_locs.shape[0])
end_y_all = np.zeros(df_locs.shape[0])

gridLines_x = []
gridLines_y = []

# Iterate through the dataset to plot survey lines
for i in range(df_locs.shape[0]):
    start_x = df_locs['start_x'][i]
    start_y = df_locs['start_y'][i]
    end_x = df_locs['end_x'][i]
    end_y = df_locs['end_y'][i]
    
    # Highlight specific lines with different colors
    if df_locs['Line'][i] in HIGHLIGHTED_LINES:
        color_index = HIGHLIGHTED_LINES.index(df_locs['Line'][i])
        #ax.plot([start_x, end_x], [start_y, end_y], lw=3, c=LINE_COLORS[color_index])
        ax.plot([start_x, end_x], [start_y, end_y],  lw=0.5, c='k')

    else:
        ax.plot([start_x, end_x], [start_y, end_y], lw=0.5, c='k')
        
    
    # Store coordinates
    start_x_all[i] = start_x
    start_y_all[i] = start_y
    end_x_all[i] = end_x
    end_y_all[i] = end_y

# Generate grid lines at every third point
for i in range(0, len(xGrid), 3):
    ux, uy, mag = pm.calcUnitVector([xGrid[i], yGrid[i]], [xGrid[i+2], yGrid[i+2]])
    L = np.linspace(0, 12.5, 10)
    xPlot = ux * L + xGrid[i]
    yPlot = uy * L + yGrid[i]
    gridLines_x.append(xPlot)
    gridLines_y.append(yPlot)
    ax.plot(xPlot, yPlot, c='k', lw=2)

plt.colorbar(cbar,label='Relative Elevation (m)', shrink=0.8)
# Configure plot axes and grid
major_ticks = np.arange(-15, 15, 5)
minor_ticks = np.arange(-15, 15, 0.5)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Distance (m)')
ax.grid(which='both')
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)
ax.set_xlim([-15, 13.5])
ax.set_ylim([-15, 13.5])
ax.set_aspect(1)

# Save the figure
fig.savefig(OUTPUT_IMAGE, dpi=600, transparent=True)

#%% Figure 1b
save_file = 'Fig01b_SCBG_oak_map_polar.png'

tree_center = [0, -1.2]
lineNumber_1 = 21
lineNumber_2 = 35
lineNumber_3 = 55
angle_1 = 97 * np.pi / 180
angle_2 = 238 * np.pi / 180
angle_3 = 303 * np.pi / 180

# Compute polar coordinates
EE, NN = np.meshgrid(easting_hs - tree_center[0], northing_hs - tree_center[1])
tr = np.arctan2(NN, EE)
rr = np.sqrt(EE**2 + NN**2)

EE2, NN2 = np.meshgrid(easting - tree_center[0], northing - tree_center[1])
tr2 = np.arctan2(NN2, EE2)
rr2 = np.sqrt(EE2**2 + NN2**2)

# Create figure and polar plot
fig = plt.figure(figsize=[10, 10], constrained_layout=True)
ax1 = fig.add_subplot(111, polar=True)

ax1.pcolormesh(tr2, rr2, elev, cmap='Spectral_r', vmin=-2, vmax=2)
ax1.pcolormesh(tr, rr, hs, cmap='gray', vmin=0, vmax=255, alpha=0.2)

# Plot grid lines
for i in range(len(gridLines_y)):
    grid_angle = np.arctan2(gridLines_y[i] - tree_center[1], gridLines_x[i] - tree_center[0])
    grid_r = np.sqrt((gridLines_y[i] - tree_center[1])**2 + (gridLines_x[i] - tree_center[0])**2)
    ax1.plot(grid_angle, grid_r, c='k', lw=2,alpha=0.2)

# Plot survey lines
for i in range(len(start_x_all)):
    grid_angle_s = np.arctan2(start_y_all[i] - tree_center[1], start_x_all[i] - tree_center[0])
    grid_r_s = np.sqrt((start_y_all[i] - tree_center[1])**2 + (start_x_all[i] - tree_center[0])**2)
    grid_angle_e = np.arctan2(end_y_all[i] - tree_center[1], end_x_all[i] - tree_center[0])
    grid_r_e = np.sqrt((end_y_all[i] - tree_center[1])**2 + (end_x_all[i] - tree_center[0])**2)
    
    if df_locs['Line'][i] == lineNumber_1:
        ax1.plot([grid_angle_s, grid_angle_e], [grid_r_s, grid_r_e], c='tab:blue', lw=3)
    elif df_locs['Line'][i] == lineNumber_2:
        ax1.plot([grid_angle_s, grid_angle_e], [grid_r_s, grid_r_e], c='tab:orange', lw=3)
    elif df_locs['Line'][i] == lineNumber_3:
        ax1.plot([grid_angle_s, grid_angle_e], [grid_r_s, grid_r_e], c='tab:purple', lw=3)
    else:
        pass
        ax1.plot([grid_angle_s, grid_angle_e], [grid_r_s, grid_r_e], c='k', lw=0.5,alpha=0.2)

# Plot reference angles
ax1.plot([angle_1, angle_1], [1, 12], c='tab:red', lw=3)
ax1.plot([angle_2, angle_2], [1, 12], c='tab:gray', lw=3)
ax1.plot([angle_3, angle_3], [1, 12], c='tab:cyan', lw=3)

# Set axis limits and ticks
ax1.set_ylim([0, 14])
ax1.set_yticks(np.arange(0, 15, 15))
ax1.set_yticklabels([])
ax1.set_xticks(np.arange(0, 2 * np.pi, 20 * np.pi / 180))
ax1.grid(False)  # simplest
# Save the figure
fig.savefig(save_file, dpi=600, transparent=True)