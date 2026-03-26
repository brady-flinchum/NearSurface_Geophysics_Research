#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 11:40:26 2026

@author: baf739
"""

import matplotlib.pyplot as plt #For Plotting
import ProcessingMethods as pm
import pandas as pd
import numpy as np
from scipy import stats
from matplotlib.colors import ListedColormap, BoundaryNorm


FONT_PROPERTIES = {
        'family': 'Times New Roman',
        'weight': 'regular',
        'size': 18
    }

import warnings
warnings.filterwarnings('ignore')

# Line numbers to highlight in the plot
ELEVATION_GEO_TIFF = '../ElevationData/SCBG_2cm_DEM_shift.tif'
HILL_SHADE_TIFF = '../ElevationData/SCBG_2cm_HS_shift.tif'
TOTAL_STATION_CSV = '../Data/locations_all.csv'
TOTAL_STATION_FILE = '../Data/08122024_cor.txt'
HIGHLIGHTED_LINES = [21, 35, 55]
LINE_COLORS = ['tab:blue', 'tab:orange', 'tab:purple']
OUTFILE = 'Fig04_SCBG_oak_map_withVel_real2Mean.png'  # Output file name for the saved figure
velFile = '../Data/GPR_Velocites.txt'
tree_center = [0, -1.2]  # Reference point for calculations


#Read in total station data
df_locs = pd.read_csv(TOTAL_STATION_CSV)

elev_shfit = -1.9
# Read elevation and hillshade data from GeoTIFF files
easting_hs, northing_hs, hs = pm.getDataFromGeoTiff(HILL_SHADE_TIFF)
easting, northing, elev = pm.getDataFromGeoTiff(ELEVATION_GEO_TIFF)
elev += elev_shfit

# Initialize figure and axis
fig = plt.figure(constrained_layout=True, figsize=[10, 10])
ax = fig.add_subplot(111)

# Plot the base map using elevation and hillshade data
ax.pcolormesh(easting, northing, elev, cmap='gray', vmin=-2, vmax=2)
ax.pcolormesh(easting, northing, hs, cmap='gray', vmin=0, vmax=255, alpha=0.2)

# Load velocity data from a text file
df_vels = pd.read_csv(velFile, delimiter=' ')
df_vels.columns = ['file', 'pick number', 'distance', 'twtt', 'velocity']
meanVel = df_vels['velocity'].mean()  # Compute the mean velocity

# Initialize arrays for storing computed values
allDepths = np.zeros(df_vels.shape[0])
allVels = np.zeros(df_vels.shape[0])
all_e = np.zeros(df_vels.shape[0])
all_n = np.zeros(df_vels.shape[0])

# Process each velocity record and compute relevant spatial properties
for i in range(df_vels.shape[0]):
    ind = df_locs['File Name'].str.startswith(df_vels['file'][i])
    start_x = df_locs['start_x'][ind].to_numpy()[0]
    start_y = df_locs['start_y'][ind].to_numpy()[0]
    end_x = df_locs['end_x'][ind].to_numpy()[0]
    end_y = df_locs['end_y'][ind].to_numpy()[0]
    
    SoL = [start_x, start_y]  # Start of line
    EoL = [end_x, end_y]  # End of line
    dist = df_vels['distance'][i]
    vel = df_vels['velocity'][i]
    twtt = df_vels['twtt'][i]
    
    depth = twtt / 2 * vel  # Calculate depth
    r, theta, e, n = pm.calcLoc(SoL, EoL, dist, tree_center)  # Compute spatial coordinates
    
    # Store computed values
    allVels[i] = vel
    allDepths[i] = depth
    all_e[i] = e
    all_n[i] = n

# Compute average velocity and scale point sizes based on depth
meanVel = np.mean(allVels)
size = ((allDepths / np.max(allDepths) + 0.3) * 18) ** 2

# Scatter plot showing velocity differences
cbar = ax.scatter(all_e, all_n, c=(allVels - meanVel) / meanVel * 100,
                  vmin=-50, vmax=50, cmap='coolwarm',
                  s=size, edgecolors='k')

# cbar = ax.scatter(all_e, all_n, c=allVels,
#                   vmin=0.06, vmax=0.15, cmap='turbo_r',
#                   s=size, edgecolors='k')

# Add colorbar
plt.colorbar(cbar, ax=ax, label='EM Velocity Difference (%)', shrink=0.5, location='top', orientation='horizontal')

# Configure axis ticks and grid
major_ticks = np.arange(-15, 15, 5)
minor_ticks = np.arange(-15, 15, 0.5)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Distance (m)')
ax.grid(which='both', alpha=0.5)
ax.grid(which='minor', alpha=0.2)
ax.set_xlim([-15, 13.5])
ax.set_ylim([-15, 13.5])
ax.set_aspect(1)

# Save the figure
fig.savefig(OUTFILE, dpi=600, transparent=True)

#%% VEL BY AZIMUTH
#CLEANED UP WITH AI


# =========================================================
# ============= User inputs / hard-coded values ===========
# =========================================================
# Expected input arrays (provide these before running)
# all_n, all_e : arrays of N and E components (same length)
# allVels      : array of velocities (m/ns), same length as all_n/all_e

# Example:
# all_n = np.array([...], dtype=float)
# all_e = np.array([...], dtype=float)
# allVels = np.array([...], dtype=float)

# Binning and plot ranges
BINS_THETA = np.linspace(0, 360, 10)  # azimuth bins (degrees)
YLIM = (0.06, 0.15)
XLIM = (0, 360)

# Day sectors (azimuth ranges in degrees). If t2 < t1, the range wraps across 360.
# Four day blocks to classify points into Day 1..4 (1-based).
DAY_SECTORS = [
    (46.3, 132.7),      # Day 1
    (132.7, 229.3),     # Day 2
    (229.3, 336.5),     # Day 3
    (336.5, 46.3),      # Day 4 (wraps: 336.5→360 and 0→46.3)
]

# Vertical reference line (e.g., precipitation event) in azimuth degrees
PRECIP_EVENT_AZ = 132.7

# Error bars: choose 'std' (standard deviation) or 'sem' (standard error of the mean)
ERROR_METRIC = 'std'

# Discrete colour palette for days 1..4 (in order)
DAY_COLORS = ['tab:blue', 'tab:orange', 'tab:purple', 'tab:red']

# Output figure file
FIG_OUT = 'Fig05_vel_with_azimuth.png'
FIG_DPI = 300

# =========================================================
# ===================== Helper functions ==================
# =========================================================
def angles_deg(n, e):
    """
    Return azimuths (degrees, 0–360) from North/East components using arctan2(N, E).
    """
    th = np.degrees(np.arctan2(n, e))
    return np.mod(th, 360.0)

def assign_days(theta_deg, sectors):
    """
    Assign day indices (1..len(sectors)) based on azimuth sectors.
    Sectors can wrap 360 if t2 < t1.
    Returns an array 'days' (float) with 0 for unassigned, else 1..K.
    """
    days = np.zeros(theta_deg.size, dtype=float)
    for i, (t1, t2) in enumerate(sectors, start=1):
        if t2 >= t1:
            mask = (theta_deg >= t1) & (theta_deg < t2)
        else:
            # wrap-around sector: [t1, 360) U [0, t2)
            mask = (theta_deg >= t1) | (theta_deg < t2)
        days[mask] = i
    return days

def binned_stats(x_deg, y, bins_deg, err_metric='std'):
    """
    Compute bin-wise mean and error (std or sem) of y in azimuth bins of x_deg.
    Returns (bin_mids, y_mean, y_err).
    """
    x_deg = np.asarray(x_deg)
    y = np.asarray(y)
    mids = 0.5 * (bins_deg[:-1] + bins_deg[1:])
    y_mean = np.full(mids.shape, np.nan)
    y_err  = np.full(mids.shape, np.nan)

    for i in range(1, len(bins_deg)):
        t1, t2 = bins_deg[i-1], bins_deg[i]
        idx = np.where((x_deg >= t1) & (x_deg < t2))[0]
        if idx.size == 0:
            continue
        vals = y[idx]
        y_mean[i-1] = np.mean(vals)
        if err_metric == 'sem':
            y_err[i-1] = np.std(vals, ddof=1) / np.sqrt(vals.size) if vals.size > 1 else np.nan
        else:  # 'std'
            y_err[i-1] = np.std(vals, ddof=1) if vals.size > 1 else 0.0
    return mids, y_mean, y_err

# =========================================================
# ====================== Main computation =================
# =========================================================
# 1) Compute azimuths (0–360°)
theta = angles_deg(all_n, all_e)

# 2) Classify each sample into Day 1..4 based on azimuth sectors
days = assign_days(theta, DAY_SECTORS)

# 3) Sort by theta (primary) then day (secondary) for nicer plotting/order if desired
indSort = np.lexsort((days, theta))  # primary = last key = theta
theta_sort = theta[indSort]
allVels_sort = allVels[indSort]
days_sort = days[indSort]

print('Day 1: ', np.round(np.mean(allVels_sort[days_sort==1]),3), np.round(np.std(allVels_sort[days_sort==1]),3))
print('Day 2: ', np.round(np.mean(allVels_sort[days_sort==2]),3), np.round(np.std(allVels_sort[days_sort==2]),3))
print('Day 3: ', np.round(np.mean(allVels_sort[days_sort==3]),3), np.round(np.std(allVels_sort[days_sort==3]),3))
print('Day 4: ', np.round(np.mean(allVels_sort[days_sort==4]),3), np.round(np.std(allVels_sort[days_sort==4]),3))

# 4) Bin statistics across azimuth
theta_mids, meanVel_theta, meanVel_err = binned_stats(theta_sort, allVels_sort, BINS_THETA, err_metric=ERROR_METRIC)

# 5) Build discrete colormap/norm for Day labels
cmap_days = ListedColormap(DAY_COLORS)
bounds = [0.5, 1.5, 2.5, 3.5, 4.5]  # map 1→color0, 2→color1, etc.
norm_days = BoundaryNorm(bounds, cmap_days.N)
valid = days > 0  # mask points that do not fall into any defined day sector

# 6) Shift azimuth so Day 1 starts at 0° (for ordered collection view)
shift0 = DAY_SECTORS[0][0]  # start of Day 1
theta_shifted = (theta - shift0) % 360.0
theta_mids_shifted = (theta_mids - shift0) % 360.0
precip_shifted = (PRECIP_EVENT_AZ - shift0) % 360.0

# =========================================================
# ======================= Plotting ========================
# =========================================================
plt.rcParams.update({'figure.constrained_layout.use': True})
fig = plt.figure()
ax  = fig.add_subplot(211)
ax2 = fig.add_subplot(212, sharex=ax, sharey=ax)

# --- Top: true azimuth ---
sc1 = ax.scatter(theta[valid], allVels[valid], s=10, c=days[valid],
                 cmap=cmap_days, norm=norm_days, ec='tab:gray', linewidths=0.3, zorder=2)
ax.errorbar(theta_mids, meanVel_theta, yerr=meanVel_err, ls='', ecolor='k', color='k', zorder=3)
ax.scatter(theta_mids, meanVel_theta, s=30, c='k', zorder=3)
ax.axvline(PRECIP_EVENT_AZ, color='tab:blue', lw=2, label='Precipitation Event', zorder=1)
ax.text(3,0.062,'(a)',size='large',color='k',ha='left',va='bottom',weight='regular')

ax.set_xlabel('Azimuth (degrees)')
ax.set_ylabel('Velocity (m/ns)')
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)

# --- Bottom: shifted azimuth (ordered by collection) ---
sc2 = ax2.scatter(theta_shifted[valid], allVels[valid], s=10, c=days[valid],
                  cmap=cmap_days, norm=norm_days, ec='tab:gray', linewidths=0.3, zorder=2)
ax2.errorbar(theta_mids_shifted, meanVel_theta, yerr=meanVel_err, ls='', ecolor='k', color='k', zorder=3)
ax2.scatter(theta_mids_shifted, meanVel_theta, s=30, c='k', zorder=3)
ax2.axvline(precip_shifted, color='tab:blue', lw=2, label='Precipitation Event', zorder=1)

ax2.set_xlabel('Shifted Azimuth (degrees)')
ax2.set_ylabel('Velocity (m/ns)')
ax2.text(3,0.062,'(b)',size='large',color='k',ha='left',va='bottom',weight='regular')

# --- One shared discrete colourbar with Day labels ---
sm = plt.cm.ScalarMappable(cmap=cmap_days, norm=norm_days)
sm.set_array([])
cbar = fig.colorbar(sm, ax=[ax, ax2], fraction=0.046, pad=0.04)
cbar.set_ticks([1, 2, 3, 4])
cbar.set_ticklabels(['Day 1', 'Day 2', 'Day 3', 'Day 4'])
cbar.set_label('Acquisition Day')

# Optional: shaded day sectors on the top subplot (uncomment to use)
# shade_styles = [
#     dict(facecolor='tab:blue',   alpha=0.15, edgecolor='none', zorder=0),
#     dict(facecolor='tab:orange', alpha=0.15, edgecolor='none', zorder=0),
#     dict(facecolor='tab:purple', alpha=0.15, edgecolor='none', zorder=0),
#     dict(facecolor='tab:red',    alpha=0.15, edgecolor='none', zorder=0),
# ]
# for (t1, t2), style in zip(DAY_SECTORS, shade_styles):
#     if t2 >= t1:
#         ax.axvspan(t1, t2, **style)
#     else:
#         ax.axvspan(t1, 360, **style)
#         ax.axvspan(0, t2, **style)

# Save figure
fig.savefig(FIG_OUT, dpi=FIG_DPI, transparent=True)
plt.show()


#OLD SCRIPT THAT I WROTE
# bins_v = np.linspace(0.05,0.15,20)
# bins_theta = np.linspace(0,360,10)


# theta = np.arctan2(all_n,all_e)*180/np.pi
# ind_neg = np.where(theta<0)[0]
# theta[ind_neg] = 180 + (180 + theta[ind_neg])

# pairs = [[46.3,132.7],
#          [132.7,229.3],
#          [229.3,336.5],
#          [336.5,360,0,46.3]]
# days = np.zeros(len(allVels))

# for i in range(0,len(pairs)):
#     tmp = pairs[i]
#     if len(tmp)>2:
#         t1 = tmp[0]
#         t2 = tmp[1]
#         ind1 = np.where(np.logical_and(theta>=t1,theta<t2))[0]
#         t3 = tmp[2]
#         t4 = tmp[3]
#         ind2 = np.where(np.logical_and(theta>=t3,theta<t4))[0]
#         ind = np.concatenate((ind1,ind2))
#         days[ind] = i+1
#     else:
#         t1 = tmp[0]
#         t2 = tmp[1]
#         ind = np.where(np.logical_and(theta>=t1,theta<t2))[0]
#         days[ind] = i+1


# indSort = np.lexsort((days, theta))

# days_sort = days[indSort]
# theta_sort = theta[indSort]
# allVels_sort = allVels[indSort]
# print(days_sort[0],theta_sort[0])

# meanVel_theta = np.zeros(len(bins_theta)-1)
# meanVel_stdErr = np.zeros(len(bins_theta)-1)
# theta_mids = np.zeros(len(bins_theta)-1)


# for i in range(1,len(bins_theta)):
#     t1 = bins_theta[i-1]
#     t2 = bins_theta[i]
#     ind = np.where(np.logical_and(theta_sort>=t1,theta_sort<t2))[0]
    
#     print(len(ind))
#     meanVel_theta[i-1] = np.mean(allVels_sort[ind])
#     meanVel_stdErr[i-1] = stats.sem(allVels_sort[ind])
#     meanVel_stdErr[i-1] = np.std(allVels_sort[ind])

#     theta_mids[i-1] = (t1 + t2)/2


# fig = plt.figure(constrained_layout=True)
# ax = fig.add_subplot(211)
# ax.scatter(theta,allVels,s=10,c=days,cmap='cool',ec='tab:gray')
# ax.errorbar(theta_mids,meanVel_theta,yerr=meanVel_stdErr,ls='',ecolor='black',color='k')
# ax.scatter(theta_mids,meanVel_theta,s=30,c='k')

# ax2 = fig.add_subplot(212,sharex=ax,sharey=ax)
# tmp_theta = theta-pairs[0][0]
# tmp_theta[tmp_theta<0] = -tmp_theta[tmp_theta<0] + (360-pairs[0][0])

# tmp_theta_mids = theta_mids-pairs[0][0]
# tmp_theta_mids[tmp_theta_mids<0] = -tmp_theta_mids[tmp_theta_mids<0] + (360-pairs[0][0])

# ax2.scatter(tmp_theta,allVels,s=10,c=days,cmap='cool',ec='tab:gray')
# ax2.errorbar(tmp_theta_mids,meanVel_theta,yerr=meanVel_stdErr,ls='',ecolor='black',color='k')
# ax2.scatter(tmp_theta_mids,meanVel_theta,s=30,c='k')


# ax.plot([132.7,132.7],[0.05,0.15],c='tab:blue',lw=2,label='Precipitation Event')
# ax2.plot([132.7-pairs[0][0],132.7-pairs[0][0]],[0.05,0.15],c='tab:blue',lw=2,label='Precipitation Event')


# ax.set_xlabel('Azimuth (degrees)')
# ax.set_ylabel('Velocity (m/ns)')
# ax.set_ylim([0.06,0.15])
# ax.set_xlim([0,360])


# ax2.set_xlabel('Shifted Azimuth (degrees)')
# ax2.set_ylabel('Velocity (m/ns)')


# fig.savefig('Fig05_vel_with_azimuth.png',dpi=300,transparent=True)



    

# fig = plt.figure()
# ax = fig.add_subplot(111)
# distros = []
# for i in range(0,len(pairs)):
#     tmp = pairs[i]
#     if len(tmp)>2:
#         t1 = tmp[0]
#         t2 = tmp[1]
#         ind1 = np.where(np.logical_and(theta>=t1,theta<t2))[0]
#         t3 = tmp[2]
#         t4 = tmp[3]
#         ind2 = np.where(np.logical_and(theta>=t3,theta<t4))[0]
#         ind = np.concatenate((ind1,ind2))
#         print(i)
#         print(np.mean(allVels[ind]),stats.sem(allVels[ind]))
#         ax.hist(allVels[ind],bins=bins_v,density=True)
#         distros.append(allVels[ind])        
#     else:
#         t1 = tmp[0]
#         t2 = tmp[1]
#         ind = np.where(np.logical_and(theta>=t1,theta<t2))[0]
#         print(i)
#         print(np.mean(allVels[ind]),stats.sem(allVels[ind]))
#         ax.hist(allVels[ind],bins=bins_v,density=True)
#         distros.append(allVels[ind])
        
        
    # t_stat, p_val = stats.ttest_ind(distros[0], distros[1])
    # print(p_val)
        

#%% ABSOLUTE VELS

# Line numbers to highlight in the plot
ELEVATION_GEO_TIFF = '../ElevationData/SCBG_2cm_DEM_shift.tif'
HILL_SHADE_TIFF = '../ElevationData/SCBG_2cm_HS_shift.tif'
TOTAL_STATION_CSV = '../Data/locations_all.csv'
TOTAL_STATION_FILE = '../Data/08122024_cor.txt'
HIGHLIGHTED_LINES = [21, 35, 55]
LINE_COLORS = ['tab:blue', 'tab:orange', 'tab:purple']
OUTFILE = 'Fig04_SCBG_oak_map_withVel_absVels.png'  # Output file name for the saved figure
velFile = '../Data/GPR_Velocites.txt'
tree_center = [0, -1.2]  # Reference point for calculations


#Read in total station data
df_locs = pd.read_csv(TOTAL_STATION_CSV)

elev_shfit = -1.9
# Read elevation and hillshade data from GeoTIFF files
easting_hs, northing_hs, hs = pm.getDataFromGeoTiff(HILL_SHADE_TIFF)
easting, northing, elev = pm.getDataFromGeoTiff(ELEVATION_GEO_TIFF)
elev += elev_shfit

# Initialize figure and axis
fig = plt.figure(constrained_layout=True, figsize=[10, 10])
ax = fig.add_subplot(111)

# Plot the base map using elevation and hillshade data
ax.pcolormesh(easting, northing, elev, cmap='gray', vmin=-2, vmax=2)
ax.pcolormesh(easting, northing, hs, cmap='gray', vmin=0, vmax=255, alpha=0.2)

# Load velocity data from a text file
df_vels = pd.read_csv(velFile, delimiter=' ')
df_vels.columns = ['file', 'pick number', 'distance', 'twtt', 'velocity']
meanVel = df_vels['velocity'].mean()  # Compute the mean velocity

# Initialize arrays for storing computed values
allDepths = np.zeros(df_vels.shape[0])
allVels = np.zeros(df_vels.shape[0])
all_e = np.zeros(df_vels.shape[0])
all_n = np.zeros(df_vels.shape[0])

# Process each velocity record and compute relevant spatial properties
for i in range(df_vels.shape[0]):
    ind = df_locs['File Name'].str.startswith(df_vels['file'][i])
    start_x = df_locs['start_x'][ind].to_numpy()[0]
    start_y = df_locs['start_y'][ind].to_numpy()[0]
    end_x = df_locs['end_x'][ind].to_numpy()[0]
    end_y = df_locs['end_y'][ind].to_numpy()[0]
    
    SoL = [start_x, start_y]  # Start of line
    EoL = [end_x, end_y]  # End of line
    dist = df_vels['distance'][i]
    vel = df_vels['velocity'][i]
    twtt = df_vels['twtt'][i]
    
    depth = twtt / 2 * vel  # Calculate depth
    r, theta, e, n = pm.calcLoc(SoL, EoL, dist, tree_center)  # Compute spatial coordinates
    
    # Store computed values
    allVels[i] = vel
    allDepths[i] = depth
    all_e[i] = e
    all_n[i] = n

# Compute average velocity and scale point sizes based on depth
meanVel = np.mean(allVels)
size = ((allDepths / np.max(allDepths) + 0.3) * 18) ** 2

# Scatter plot showing velocity differences
# cbar = ax.scatter(all_e, all_n, c=(allVels - meanVel) / meanVel * 100,
#                   vmin=-50, vmax=50, cmap='coolwarm',
#                   s=size, edgecolors='k')

cbar = ax.scatter(all_e, all_n, c=allVels,
                  vmin=0.06, vmax=0.15, cmap='turbo_r',
                  s=size, edgecolors='k')

# Add colorbar
plt.colorbar(cbar, ax=ax, label='EM Velocity Difference (%)', shrink=0.5, location='top', orientation='horizontal')

# Configure axis ticks and grid
major_ticks = np.arange(-15, 15, 5)
minor_ticks = np.arange(-15, 15, 0.5)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Distance (m)')
ax.grid(which='both', alpha=0.5)
ax.grid(which='minor', alpha=0.2)
ax.set_xlim([-15, 13.5])
ax.set_ylim([-15, 13.5])
ax.set_aspect(1)

# Save the figure
fig.savefig(OUTFILE, dpi=600, transparent=True)

VELFILE = '../Data/GPR_Velocites.txt'  # Path to velocity data file
output_fig = 'VelocityDepthPicks.png'  # Output file path
font_settings = {'family': 'Times New Roman', 'weight': 'regular', 'size': 18}  # Font settings for plots
velocity_range = (0.08, 0.13)  # Range for velocity percentage calculation (m/ns)
depth_range = (0, 1)  # Depth range for percentage calculation (m)
depths2Avg = np.arange(0.05, 1.5, 0.15)  # Depth bins for averaging velocity
nbins = 20  # Number of bins for histogram


# ---------------- Load Data ---------------- #
data_df = pd.read_csv(VELFILE, header=None, delimiter=' ')
xPickList = data_df[2].to_numpy()
tPickList = data_df[3].to_numpy()
vPickList = data_df[4].to_numpy()

# ---------------- Compute Additional Parameters ---------------- #
meanVel = np.mean(vPickList)
allDepths = tPickList / 2 * vPickList  # Convert time picks to depth
size = ((allDepths / np.max(allDepths) + 0.3) * 18) ** 2  # Scale marker size by depth
D = tPickList / 2 * vPickList  # Depth calculation

# ---------------- Data Statistics ---------------- #
N = len(vPickList)
n = len(np.where((vPickList >= velocity_range[0]) & (vPickList <= velocity_range[1]))[0])
print(f'Percentage of Data between {velocity_range[0]} and {velocity_range[1]} m/ns:', np.round(n / N * 100, 1))

N = len(D)
n = len(np.where((D >= depth_range[0]) & (D <= depth_range[1]))[0])
print(f'Percentage of Data less than {depth_range[1]} m:', np.round(n / N * 100, 1))

# ---------------- Create Figure and Subplots ---------------- #
fig = plt.figure(figsize=(10, 10))
gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                      left=0.2, right=0.9, bottom=0.1, top=0.9,
                      wspace=0.1, hspace=0.05)
ax = fig.add_subplot(gs[1, 0])  # Main scatter plot
ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)  # Histogram for velocity
ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)  # Histogram for depth

# ---------------- Scatter Plot ---------------- #
ax.scatter(vPickList, D, c=(vPickList - meanVel) / meanVel * 100,
           vmin=-50, vmax=50, cmap='coolwarm',
           s=size, edgecolors='k')

# ---------------- Depth Averaging ---------------- #
depthMidPoints = (depths2Avg[1:] + depths2Avg[:-1]) / 2
meanVelDepth = np.zeros(len(depths2Avg) - 1)
stdDevVelDepth = np.zeros(len(depths2Avg) - 1)
stdErrVelDepth = np.zeros(len(depths2Avg) - 1)

for i in range(len(depths2Avg) - 1):
    ind = np.where((D >= depths2Avg[i]) & (D < depths2Avg[i + 1]))[0]
    meanVelDepth[i] = np.mean(vPickList[ind])
    stdDevVelDepth[i] = np.std(vPickList[ind])
    stdErrVelDepth[i] = stats.sem(vPickList[ind])

ax.fill_betweenx(depthMidPoints, meanVelDepth - 2 * stdErrVelDepth, meanVelDepth + 2 * stdErrVelDepth, facecolor='k', alpha=0.4)
ax.plot(meanVelDepth, depthMidPoints, lw=4, c='k')

# ---------------- Axis Labels and Limits ---------------- #
ax.set_xlabel('EM Velocity (m/ns)')
ax.set_ylabel('Depth (m)')
ax.set_xlim([0.05, 0.16])
ax.set_ylim([0, 1.6])
ax.invert_yaxis()

# ---------------- Histograms ---------------- #
ax_histx.hist(vPickList, bins=nbins, density=True, color='tab:blue')
ax_histx.xaxis.tick_top()
ax_histx.xaxis.set_label_position("top")
ax_histx.set_xlabel('EM Velocity (m/ns)')

ax_histy.hist(D, bins=nbins, orientation='horizontal', density=True, color='tab:blue')
ax_histy.yaxis.tick_right()
ax_histy.yaxis.set_label_position("right")
ax_histy.set_ylabel('Depth (m)')

# ---------------- Save Figure ---------------- #
fig.savefig(output_fig, dpi=600, transparent=True)

#%% STATS
VELFILE = '../Data/GPR_Velocites.txt'  # Path to velocity data file
output_fig = 'Fig04_VelocityDepthPicks.png'  # Output file path
font_settings = {'family': 'Times New Roman', 'weight': 'regular', 'size': 18}  # Font settings for plots
velocity_range = (0.08, 0.13)  # Range for velocity percentage calculation (m/ns)
depth_range = (0, 1)  # Depth range for percentage calculation (m)
depths2Avg = np.arange(0.05, 1.5, 0.15)  # Depth bins for averaging velocity
nbins = 20  # Number of bins for histogram


# ---------------- Load Data ---------------- #
data_df = pd.read_csv(VELFILE, header=None, delimiter=' ')
xPickList = data_df[2].to_numpy()
tPickList = data_df[3].to_numpy()
vPickList = data_df[4].to_numpy()

# ---------------- Compute Additional Parameters ---------------- #
meanVel = np.mean(vPickList)
allDepths = tPickList / 2 * vPickList  # Convert time picks to depth
size = ((allDepths / np.max(allDepths) + 0.3) * 18) ** 2  # Scale marker size by depth
D = tPickList / 2 * vPickList  # Depth calculation

# ---------------- Data Statistics ---------------- #
N = len(vPickList)
n = len(np.where((vPickList >= velocity_range[0]) & (vPickList <= velocity_range[1]))[0])
print(f'Percentage of Data between {velocity_range[0]} and {velocity_range[1]} m/ns:', np.round(n / N * 100, 1))

N = len(D)
n = len(np.where((D >= depth_range[0]) & (D <= depth_range[1]))[0])
print(f'Percentage of Data less than {depth_range[1]} m:', np.round(n / N * 100, 1))

print('Mean = ', meanVel)
print('Stdev = ', np.std(vPickList))

print('Standard Error = ', stats.sem(vPickList))
# ---------------- Create Figure and Subplots ---------------- #
fig = plt.figure(figsize=(10, 10))
gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                      left=0.2, right=0.9, bottom=0.1, top=0.9,
                      wspace=0.1, hspace=0.05)
ax = fig.add_subplot(gs[1, 0])  # Main scatter plot
ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)  # Histogram for velocity
ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)  # Histogram for depth

# ---------------- Scatter Plot ---------------- #
ax.scatter(vPickList, D, c=(vPickList - meanVel) / meanVel * 100,
           vmin=-50, vmax=50, cmap='coolwarm',
           s=size, edgecolors='k')

# ---------------- Depth Averaging ---------------- #
depthMidPoints = (depths2Avg[1:] + depths2Avg[:-1]) / 2
meanVelDepth = np.zeros(len(depths2Avg) - 1)
stdDevVelDepth = np.zeros(len(depths2Avg) - 1)
stdErrVelDepth = np.zeros(len(depths2Avg) - 1)

for i in range(len(depths2Avg) - 1):
    ind = np.where((D >= depths2Avg[i]) & (D < depths2Avg[i + 1]))[0]
    meanVelDepth[i] = np.mean(vPickList[ind])
    stdDevVelDepth[i] = np.std(vPickList[ind])
    stdErrVelDepth[i] = stats.sem(vPickList[ind])

ax.fill_betweenx(depthMidPoints, meanVelDepth - 2 * stdErrVelDepth, meanVelDepth + 2 * stdErrVelDepth, facecolor='k', alpha=0.4)
ax.plot(meanVelDepth, depthMidPoints, lw=4, c='k')

# ---------------- Axis Labels and Limits ---------------- #
ax.set_xlabel('EM Velocity (m/ns)')
ax.set_ylabel('Depth (m)')
ax.set_xlim([0.05, 0.16])
ax.set_ylim([0, 1.6])
ax.invert_yaxis()

# ---------------- Histograms ---------------- #
ax_histx.hist(vPickList, bins=nbins, density=True, color='tab:blue')
ax_histx.xaxis.tick_top()
ax_histx.xaxis.set_label_position("top")
ax_histx.set_xlabel('EM Velocity (m/ns)')

ax_histy.hist(D, bins=nbins, orientation='horizontal', density=True, color='tab:blue')
ax_histy.yaxis.tick_right()
ax_histy.yaxis.set_label_position("right")
ax_histy.set_ylabel('Depth (m)')

# ---------------- Save Figure ---------------- #
fig.savefig(output_fig, dpi=600, transparent=True)

