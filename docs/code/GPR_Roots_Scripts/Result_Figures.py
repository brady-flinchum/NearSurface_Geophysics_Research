#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 12:44:41 2026

@author: baf739
"""

import GPRClass as gpr
import numpy as np
from scipy.interpolate import griddata
from opendtect_colormaps import OpendtectColormaps
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import pyvista as pv
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

saveDir = '../Data/savedProcessedFiles/'
locInfoFile = '../Data/locations_all.csv'
nFiles = 1170
deWowVal = 1
meanTraceVal = 150
tPowVal = 1.5
lpVal = 400 
hpVal = 1000
filtOrder = 1
gprVel = 0.105
dz = 0.005
z0 = 0
zf = 1.5
treeCenter = [0,-1.2]

readData = True

#CREATE INSTANCE
allGPRData = gpr.treeGPRStructure() 


#GET SPATIAL INFORMATION
allGPRData.initalizeData(locInfoFile,treeCenter)
#SET PROCESSING PARAMETERS
allGPRData.setProcessingParms(saveDir, deWowVal, meanTraceVal,
                              hpVal, lpVal, filtOrder,
                              gprVel)

#This will save a lot of time
if readData:
    #PROCESS DATA
    print('Reading in Data')
    allGPRData.readProcessedGPR_all()
    print('Spatially Locating Profiles')
    allGPRData.spatiallyLocateProfiles()
    print('Reading depth amplitudes')
    allGPRData.readEnvNormVals()
    print('Calculating Radial Coordinates')
    allGPRData.calcRadialCoordinates()
    print('Calculating All Locations')
    allGPRData.getAllLocs()
else:
    #Read in and Process Data
    envVal = 1 #1 = mean, 2 = max, 3 = median
    allGPRData.processGPR_all(z0,zf,dz)
    print('Spatially Locating Profiles')
    allGPRData.spatiallyLocateProfiles()
    print('Working on depth amplitudes')
    allGPRData.getEnvNormVals(envVal)
    print('Calculating Radial Coordinates')
    allGPRData.calcRadialCoordinates()
    print('Calculating All Locations')
    allGPRData.getAllLocs()

# Read in Elevaiton data 
elevGeoTiff = '../ElevationData/SCBG_2cm_DEM_shift.tif'
hsGeoTiff = '../ElevationData/SCBG_2cm_HS_shift.tif'
easting_hs,northing_hs,hs = gpr.getDataFromGeoTiff(hsGeoTiff)
easting,northing,elev = gpr.getDataFromGeoTiff(elevGeoTiff)
elev_shfit = -1.9
elev += elev_shfit

#Resample the elevation data for data cube
# e_resamp = np.arange(-15,15,0.03)
# n_resamp = np.arange(-15,15,0.03)
# depths = np.arange(0.01,1.2,0.01)

e_resamp = np.arange(-15,15,0.05)
n_resamp = np.arange(-15,15,0.05)
depths = np.arange(0.01,1.2,0.01)


ee,nn = np.meshgrid(easting,northing)
EE,NN = np.meshgrid(e_resamp,n_resamp)
ELV_resamp = griddata(np.column_stack([ee.ravel(),nn.ravel()]),elev.ravel(),(EE,NN),method='nearest')
HS_resamp = griddata(np.column_stack([ee.ravel(),nn.ravel()]),hs.ravel(),(EE,NN),method='nearest')

TT = np.arctan2(NN,EE)
RR = np.sqrt(EE**2 + NN**2)
ELV_resamp_polar = griddata(np.column_stack([ee.ravel()-treeCenter[0],nn.ravel()-treeCenter[1]]),elev.ravel(),(EE,NN),method='nearest')
HS_resamp_polar = griddata(np.column_stack([ee.ravel()-treeCenter[0],nn.ravel()-treeCenter[1]]),hs.ravel(),(EE,NN),method='nearest')


#%% Visualize the Gain of the data for depth sections
# FIGURE 6 of the paper
plotGray = False

powerVal = 1
lineNumber = 21
VE = 3
vMin = 0
vMax = 15


depths = allGPRData.gpr_depths[0]
day1 = allGPRData.hilbertNormAmps[0]
day2 = allGPRData.hilbertNormAmps[1]
day3 = allGPRData.hilbertNormAmps[2]
day4 = allGPRData.hilbertNormAmps[3]

dist,theta,radius,preMig,postMig,postEnv = allGPRData.getRadialProfile_byLine(lineNumber,powerVal)

x0_1 = 9.9
ind_x0_1 = np.argmin((dist-x0_1)**2)
x0_2 = 3.3
ind_x0_2 = np.argmin((dist-x0_2)**2)

x0_3 = 18.23
ind_x0_3 = np.argmin((dist-x0_3)**2)

avgAllDays = (day1+day2+day3+day4)/4


day1_ind = np.where(np.logical_and(theta>=46.3,theta<132.7))[0]

day2_ind = np.where(np.logical_and(theta>=132.7,theta<229.3))[0]

day3_ind = np.where(np.logical_and(theta>=229.3,theta<=336.4))[0]

day4_ind = np.where(np.logical_and(theta>=336.5,theta<360))[0]
day4_ind2 = np.where(np.logical_and(theta>=0,theta<46.3))[0]

#day3_ind = np.concatenate((day3_ind,day3_ind2))


OUTFILE = 'Fig06_GPR_Roots_Results_proifle_notGray'+str(lineNumber)+'.png'

dist,theta,radius,preMig,postMig,postEnv = allGPRData.getRadialProfile_byLine(lineNumber,powerVal)

#TILE THE DATA for PCOLOR MESH this prevents the uniform angle and plots the true data
THETA = np.tile(theta, (preMig.shape[0],1))
DEPTHS = np.tile(allGPRData.gpr_depths[0],(preMig.shape[1],1)).T
DIST = np.tile(dist, (preMig.shape[0],1))
R = np.tile(radius, (preMig.shape[0],1))

od_cmaps = OpendtectColormaps(filename='/Users/baf739/Library/CloudStorage/OneDrive-TheUniversityofNewcastle/Documents/Research/Manuscripts/GPR_Roots/DataRepository/PythonScripts/opendtect_colormaps/ColTabs')
ODcmap = od_cmaps("Seismics")


fig = plt.figure(constrained_layout=True,figsize=[10.3,7])
gs = fig.add_gridspec(4, 5)
ax2 = fig.add_subplot(gs[0, 1:])
ax1 = fig.add_subplot(gs[0, 0],sharey=ax2)
ax3 = fig.add_subplot(gs[1, 0],sharey=ax2)
ax4 = fig.add_subplot(gs[1, 1:],sharey=ax2)
ax5 = fig.add_subplot(gs[2, 0],sharey=ax2)
ax6 = fig.add_subplot(gs[2, 1:],sharey=ax2)
ax7 = fig.add_subplot(gs[3, 0],sharey=ax2)
ax8 = fig.add_subplot(gs[3, 1:],sharey=ax2)




ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax4.yaxis.set_label_position("right")
ax4.yaxis.tick_right()
ax6.yaxis.set_label_position("right")
ax6.yaxis.tick_right()
ax8.yaxis.set_label_position("right")
ax8.yaxis.tick_right()

ax1.plot(day1,depths,c='tab:blue')
ax1.plot(day2,depths,c='tab:orange')
ax1.plot(day3,depths,c='tab:purple')
ax1.plot(day4,depths,c='tab:red')
ax1.set_xscale('log')
ax1.set_xlabel('Average Section Envelopes',size='x-small')
ax1.set_ylabel('Depth (m)')
ax1.text(0.3,0.05,'(a)',size='large',color='k',ha='left',va='top',weight='bold')



#cmap='gray'
if plotGray:
    cbar1 = ax2.pcolormesh(DIST,DEPTHS,preMig,cmap='gray',vmin=-5,vmax=5)
else:
    cbar1 = ax2.pcolormesh(DIST,DEPTHS,preMig,cmap=ODcmap,vmin=-5,vmax=5)
    
ax2.plot(dist[day1_ind],np.zeros(len(day1_ind))-0.0,c='tab:blue',lw=5)
ax2.plot(dist[day2_ind],np.zeros(len(day2_ind))-0.0,c='tab:orange',lw=5)
ax2.plot(dist[day3_ind],np.zeros(len(day3_ind))-0.0,c='tab:purple',lw=5)
ax2.plot(dist[day4_ind],np.zeros(len(day4_ind))-0.0,c='tab:red',lw=5)
ax2.plot(dist[day4_ind2],np.zeros(len(day4_ind2))-0.0,c='tab:red',lw=5)

ax2.text(0.1,1.4,'(b)',size='large',color='k',ha='left',va='bottom',weight='bold')
ax2.set_aspect(VE)
ax2.set_xlabel('Distance (m)')
ax2.set_ylabel('Depth (m)')
ax2.set_ylim([0,1.5])
ax2.invert_yaxis()
plt.colorbar(cbar1,ax=ax2,label='',orientation='vertical',shrink=0.8)


ax3.plot(postMig[:,ind_x0_1],depths,c='k',lw=0.5)
ax3.plot(postMig[:,ind_x0_2],depths,c='gray',lw=0.5)
ax3.plot(postMig[:,ind_x0_3],depths,c='tab:cyan',lw=0.5)
ax3.set_xlim([-5,5])
ax3.set_xlabel('Amplitude')
ax3.set_ylabel('Depth (m)')
ax3.text(-4.5,0.05,'(c)',size='large',color='k',ha='left',va='top',weight='bold')

if plotGray:
    cbar2 = ax4.pcolormesh(DIST,DEPTHS,postMig,cmap='gray',vmin=-5,vmax=5)
else:
    cbar2 = ax4.pcolormesh(DIST,DEPTHS,postMig,cmap=ODcmap,vmin=-5,vmax=5)
ax4.text(0.1,1.45,'(d)',size='large',color='k',ha='left',va='bottom',weight='bold')

ax4.plot(dist[day1_ind],np.zeros(len(day1_ind))-0.0,c='tab:blue',lw=5)
ax4.plot(dist[day2_ind],np.zeros(len(day2_ind))-0.0,c='tab:orange',lw=5)
ax4.plot(dist[day3_ind],np.zeros(len(day3_ind))-0.0,c='tab:purple',lw=5)
ax4.plot(dist[day4_ind],np.zeros(len(day4_ind))-0.0,c='tab:red',lw=5)
ax4.plot(dist[day4_ind2],np.zeros(len(day4_ind2))-0.0,c='tab:red',lw=5)

ax4.plot([x0_1,x0_1],[0,1.5],c='k')
ax4.plot([x0_2,x0_2],[0,1.5],c='gray')
ax4.plot([x0_3,x0_3],[0,1.5],c='cyan')

ax4.set_aspect(VE)
ax4.set_xlabel('Distance (m)')
ax4.set_ylabel('Depth (m)')
plt.colorbar(cbar2,ax=ax4,label='',orientation='vertical',shrink=0.8)

ax5.plot(postEnv[:,ind_x0_1],depths,c='k',lw=0.5)
ax5.plot(postEnv[:,ind_x0_2],depths,c='gray',lw=0.5)
ax5.plot(postEnv[:,ind_x0_3],depths,c='tab:cyan',lw=0.5)
ax5.set_xlim([-5,5])
ax5.set_xlabel('Envelope')
ax5.set_ylabel('Depth (m)')
ax5.text(-4.5,0.05,'(e)',size='large',color='k',ha='left',va='top',weight='bold')


cbar3 = ax6.pcolormesh(DIST,DEPTHS,postEnv,cmap='seismic',vmin=-5,vmax=5)
ax6.plot(dist[day1_ind],np.zeros(len(day1_ind))-0.0,c='tab:blue',lw=5)
ax6.plot(dist[day2_ind],np.zeros(len(day2_ind))-0.0,c='tab:orange',lw=5)
ax6.plot(dist[day3_ind],np.zeros(len(day3_ind))-0.0,c='tab:purple',lw=5)
ax6.plot(dist[day4_ind],np.zeros(len(day4_ind))-0.0,c='tab:red',lw=5)
ax6.plot(dist[day4_ind2],np.zeros(len(day4_ind2))-0.0,c='tab:red',lw=5)

ax6.plot([x0_1,x0_1],[0,1.5],c='k')
ax6.plot([x0_2,x0_2],[0,1.5],c='gray')
ax6.plot([x0_3,x0_3],[0,1.5],c='cyan')
ax6.text(0.1,1.45,'(f)',size='large',color='k',ha='left',va='bottom',weight='bold')
ax6.set_aspect(VE)
ax6.set_xlabel('Distance (m)')
ax6.set_ylabel('Depth (m)')
plt.colorbar(cbar3,ax=ax6,label='',orientation='vertical',shrink=0.8)


ax7.plot(postEnv[:,ind_x0_1]**2,depths,c='k',lw=0.5)
ax7.plot(postEnv[:,ind_x0_2]**2,depths,c='gray',lw=0.5)
ax7.plot(postEnv[:,ind_x0_3]**2,depths,c='tab:cyan',lw=0.5)
ax7.set_xlim([0,25])
ax7.set_xlabel('(Envelope)$^2$')
ax7.set_ylabel('Depth (m)')
ax7.text(24,0.05,'(g)',size='large',color='k',ha='right',va='top',weight='bold')


cbar4 = ax8.pcolormesh(DIST,DEPTHS,postEnv**2,cmap='cubehelix_r',vmin=vMin,vmax=vMax)
ax8.plot(dist[day1_ind],np.zeros(len(day1_ind))-0.0,c='tab:blue',lw=5)
ax8.plot(dist[day2_ind],np.zeros(len(day2_ind))-0.0,c='tab:orange',lw=5)
ax8.plot(dist[day3_ind],np.zeros(len(day3_ind))-0.0,c='tab:purple',lw=5)
ax8.plot(dist[day4_ind],np.zeros(len(day4_ind))-0.0,c='tab:red',lw=5)
ax8.plot(dist[day4_ind2],np.zeros(len(day4_ind2))-0.0,c='tab:red',lw=5)

ax8.text(0.1,1.45,'(h)',size='large',color='k',ha='left',va='bottom',weight='bold')
ax8.plot([x0_1,x0_1],[0,1.5],c='k')
ax8.plot([x0_2,x0_2],[0,1.5],c='gray')
ax8.plot([x0_3,x0_3],[0,1.5],c='cyan')
ax8.set_aspect(VE)
ax8.set_xlabel('Distance (m)')
ax8.set_ylabel('Depth (m)')
plt.colorbar(cbar4,ax=ax8,label='',orientation='vertical',shrink=0.8)
fig.savefig(OUTFILE,dpi=300,transparent=True)

#%% FIGURE 7
powerVal = 2
    
HIGHLIGHTED_LINES = np.array([21, 35, 55])
HIGHLIGHTED_ANGLES = np.array([97,238,303])*np.pi/180
VE = 2
tol = 0.01
N = 1000      


r_4 = np.linspace(0,13,N)
theta_4 = np.ones(len(r_4))*HIGHLIGHTED_ANGLES[0]
path_4 = np.column_stack([theta_4,r_4])
DIST_4,DEPTHS_4,THETA_4,postEnv_4,postMig_4 = allGPRData.getRadialProfile(path_4,N,tol,powerVal)
ZZ_4 = np.zeros(THETA_4.shape)
xi = DIST_4[0,:]*np.cos(THETA_4[0,:]) + treeCenter[0]
yi = DIST_4[0,:]*np.sin(THETA_4[0,:]) + treeCenter[1]
zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
for i in range(0,DEPTHS_4.shape[1]):
    ZZ_4[:,i] = zElev[i] - DEPTHS_4[:,i]
    
r_5 = np.linspace(0,13,N)
theta_5 = np.ones(len(r_5))*HIGHLIGHTED_ANGLES[1]
path_5 = np.column_stack([theta_5,r_5])
DIST_5,DEPTHS_5,THETA_5,postEnv_5,postMig_5 = allGPRData.getRadialProfile(path_5,N,tol,powerVal)
ZZ_5 = np.zeros(THETA_5.shape)
xi = DIST_5[0,:]*np.cos(THETA_5[0,:]) + treeCenter[0]
yi = DIST_5[0,:]*np.sin(THETA_5[0,:]) + treeCenter[1]
zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
for i in range(0,DEPTHS_5.shape[1]):
    ZZ_5[:,i] = zElev[i] - DEPTHS_5[:,i]

r_6 = np.linspace(0,13,N)
theta_6 = np.ones(len(r_6))*HIGHLIGHTED_ANGLES[2]
path_6 = np.column_stack([theta_6,r_6])
DIST_6,DEPTHS_6,THETA_6,postEnv_6,postMig_6 = allGPRData.getRadialProfile(path_6,N,tol,powerVal)
ZZ_6 = np.zeros(THETA_6.shape)
xi = DIST_6[0,:]*np.cos(THETA_6[0,:]) + treeCenter[0]
yi = DIST_6[0,:]*np.sin(THETA_6[0,:]) + treeCenter[1]
zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
for i in range(0,DEPTHS_6.shape[1]):
    ZZ_6[:,i] = zElev[i] - DEPTHS_6[:,i]

#TILE THE DATA for PCOLOR MESH this prevents the uniform angle and plots the true data
dist_0,theta_0,radius_0,preMig_0,postMig_0,postEnv_0 = allGPRData.getRadialProfile_byLine(HIGHLIGHTED_LINES[0],powerVal)
THETA_0 = np.tile(theta_0, (preMig_0.shape[0],1))
DEPTHS_0 = np.tile(allGPRData.gpr_depths[0],(preMig_0.shape[1],1)).T
DIST_0 = np.tile(dist_0, (preMig_0.shape[0],1))
R_0 = np.tile(radius_0, (preMig_0.shape[0],1))  
e_0 = allGPRData.gpr_E[HIGHLIGHTED_LINES[0]]
n_0 = allGPRData.gpr_N[HIGHLIGHTED_LINES[0]]
xi = R_0[0,:]*np.cos(THETA_0[0,:]*np.pi/180) + treeCenter[0]
yi = R_0[0,:]*np.sin(THETA_0[0,:]*np.pi/180) + treeCenter[1]
meanRad_0 = np.mean(np.sqrt(xi**2+yi**2))
ZZ = np.zeros(R_0.shape)
zElev = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (xi,yi),method='nearest')
ZZ_0 = np.zeros(R_0.shape)
zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
for i in range(0,DEPTHS_0.shape[1]):
    ZZ_0[:,i] = zElev[i] - DEPTHS_0[:,i]
ang2dist_a_0 = dist_0[np.argmin((theta_0-HIGHLIGHTED_ANGLES[0]*180/np.pi)**2)]
ang2dist_b_0 = dist_0[np.argmin((theta_0-HIGHLIGHTED_ANGLES[1]*180/np.pi)**2)]
ang2dist_c_0 = dist_0[np.argmin((theta_0-HIGHLIGHTED_ANGLES[2]*180/np.pi)**2)]
print('Line = ',HIGHLIGHTED_LINES[0],meanRad_0)


dist_1,theta_1,radius_1,preMig_1,postMig_1,postEnv_1 = allGPRData.getRadialProfile_byLine(HIGHLIGHTED_LINES[1],powerVal)
THETA_1 = np.tile(theta_1, (preMig_1.shape[0],1))
DEPTHS_1 = np.tile(allGPRData.gpr_depths[0],(preMig_1.shape[1],1)).T
DIST_1 = np.tile(dist_1, (preMig_1.shape[0],1))
R_1 = np.tile(radius_1, (preMig_1.shape[0],1))  
e_1 = allGPRData.gpr_E[HIGHLIGHTED_LINES[1]]
n_1 = allGPRData.gpr_N[HIGHLIGHTED_LINES[1]]
xi = R_1[0,:]*np.cos(THETA_1[0,:]*np.pi/180) + treeCenter[0]
yi = R_1[0,:]*np.sin(THETA_1[0,:]*np.pi/180) + treeCenter[1]
meanRad_1 = np.mean(np.sqrt(xi**2+yi**2))
zElev = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (xi,yi),method='nearest')
ZZ_1 = np.zeros(R_1.shape)
zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
for i in range(0,DEPTHS_1.shape[1]):
    ZZ_1[:,i] = zElev[i] - DEPTHS_1[:,i]
ang2dist_a_1 = dist_1[np.argmin((theta_1-HIGHLIGHTED_ANGLES[0]*180/np.pi)**2)]
ang2dist_b_1 = dist_1[np.argmin((theta_1-HIGHLIGHTED_ANGLES[1]*180/np.pi)**2)]
ang2dist_c_1 = dist_1[np.argmin((theta_1-HIGHLIGHTED_ANGLES[2]*180/np.pi)**2)]
print('Line = ',HIGHLIGHTED_LINES[1],meanRad_1)



dist_2,theta_2,radius_2,preMig_2,postMig_2,postEnv_2 = allGPRData.getRadialProfile_byLine(HIGHLIGHTED_LINES[2],powerVal)
THETA_2 = np.tile(theta_2, (preMig_2.shape[0],1))
DEPTHS_2 = np.tile(allGPRData.gpr_depths[0],(preMig_2.shape[1],1)).T
DIST_2 = np.tile(dist_2, (preMig_2.shape[0],1))
R_2 = np.tile(radius_2, (preMig_2.shape[0],1))  
e_2 = allGPRData.gpr_E[HIGHLIGHTED_LINES[1]]
n_2 = allGPRData.gpr_N[HIGHLIGHTED_LINES[1]]
xi = R_2[0,:]*np.cos(THETA_2[0,:]*np.pi/180) + treeCenter[0]
yi = R_2[0,:]*np.sin(THETA_2[0,:]*np.pi/180) + treeCenter[1]
meanRad_2 = np.mean(np.sqrt(xi**2+yi**2))
zElev = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (xi,yi),method='nearest')
ZZ_2 = np.zeros(R_2.shape)
zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
for i in range(0,DEPTHS_2.shape[1]):
    ZZ_2[:,i] = zElev[i] - DEPTHS_2[:,i]
ang2dist_a_2 = dist_2[np.argmin((theta_2-HIGHLIGHTED_ANGLES[0]*180/np.pi)**2)]
ang2dist_b_2 = dist_2[np.argmin((theta_2-HIGHLIGHTED_ANGLES[1]*180/np.pi)**2)]
ang2dist_c_2 = dist_2[np.argmin((theta_2-HIGHLIGHTED_ANGLES[2]*180/np.pi)**2)]
print('Line = ',HIGHLIGHTED_LINES[2],meanRad_2)


    #%%
fig = plt.figure(layout='constrained',figsize=[14,7])
gs = GridSpec(3, 8, figure=fig)
ax1 = fig.add_subplot(gs[0, 0:3])
ax1.spines['bottom'].set(lw=2,color='tab:red')
ax1.spines['top'].set(lw=2,color='tab:red')
ax1.spines['left'].set(lw=2,color='tab:red')
ax1.spines['right'].set(lw=2,color='tab:red')

ax1.pcolormesh(DIST_4,ZZ_4,postEnv_4,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
ax1.plot(DIST_4[0,:],ZZ_4[0,:],c='k')
ax1.plot([meanRad_0,meanRad_0],[-3,3],c='tab:blue',lw=1,ls='--')
ax1.plot([meanRad_1,meanRad_1],[-3,3],c='tab:orange',lw=1,ls='--')
ax1.plot([meanRad_2,meanRad_2],[-3,3],c='tab:purple',lw=1,ls='--')
ax1.text(1.7,-2.9,'(a)',size='large',color='k',ha='left',va='bottom',weight='regular')

ax1.set_aspect(VE)
ax1.set_ylim([-3,0])
ax1.set_xlabel('Distance (m)')
ax1.set_ylabel('Relative Elevation (m)')

ax2 = fig.add_subplot(gs[1, 0:3])
ax2.spines['bottom'].set(lw=2,color='tab:gray')
ax2.spines['top'].set(lw=2,color='tab:gray')
ax2.spines['left'].set(lw=2,color='tab:gray')
ax2.spines['right'].set(lw=2,color='tab:gray')

ax2.pcolormesh(DIST_5,ZZ_5,postEnv_5,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
ax2.plot(DIST_5[0,:],ZZ_5[0,:],c='k')
ax2.plot([meanRad_0,meanRad_0],[-3,3],c='tab:blue',lw=1,ls='--')
ax2.plot([meanRad_1,meanRad_1],[-3,3],c='tab:orange',lw=1,ls='--')
ax2.plot([meanRad_2,meanRad_2],[-3,3],c='tab:purple',lw=1,ls='--')
ax2.text(1.7,-1.9,'(b)',size='large',color='k',ha='left',va='bottom',weight='regular')

ax2.set_aspect(VE)
ax2.set_ylim([-2,0.5])
ax2.set_xlabel('Distance (m)')
ax2.set_ylabel('Relative Elevation (m)')


ax3 = fig.add_subplot(gs[2, 0:3])
ax3.spines['bottom'].set(lw=2,color='tab:cyan')
ax3.spines['top'].set(lw=2,color='tab:cyan')
ax3.spines['left'].set(lw=2,color='tab:cyan')
ax3.spines['right'].set(lw=2,color='tab:cyan')

ax3.pcolormesh(DIST_6,ZZ_6,postEnv_6,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
ax3.plot(DIST_6[0,:],ZZ_6[0,:],c='k')
ax3.plot([meanRad_0,meanRad_0],[-2,3],c='tab:blue',lw=1,ls='--')
ax3.plot([meanRad_1,meanRad_1],[-2,3],c='tab:orange',lw=1,ls='--')
ax3.plot([meanRad_2,meanRad_2],[-2,3],c='tab:purple',lw=1,ls='--')
ax3.text(1.5,-1.9,'(c)',size='large',color='k',ha='left',va='bottom',weight='regular')

ax3.set_aspect(VE)
ax3.set_ylim([-2,1])
ax3.set_xlabel('Distance (m)')
ax3.set_ylabel('Relative Elevation (m)')


ax4 = fig.add_subplot(gs[0, 3:8])
ax4.spines['bottom'].set(lw=2,color='tab:blue')
ax4.spines['top'].set(lw=2,color='tab:blue')
ax4.spines['left'].set(lw=2,color='tab:blue')
ax4.spines['right'].set(lw=2,color='tab:blue')
ax4.yaxis.set_label_position("right")
ax4.yaxis.tick_right()

ax4.pcolormesh(DIST_0,ZZ_0,postEnv_0,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
ax4.plot(DIST_0[0,:],ZZ_0[0,:],c='k')
ax4.plot([ang2dist_a_0,ang2dist_a_0],[-2,3],c='tab:red',lw=1,ls='--')
ax4.plot([ang2dist_b_0,ang2dist_b_0],[-2,3],c='tab:gray',lw=1,ls='--')
ax4.plot([ang2dist_c_0,ang2dist_c_0],[-2,3],c='tab:cyan',lw=1,ls='--')
ax4.text(0.2,-1.5,'(d)',size='large',color='k',ha='left',va='top',weight='regular')

ax4.set_aspect(VE)
ax4.set_ylim([-2,0.5])
ax4.set_xlabel('Distance (m)')
ax4.set_ylabel('Relative Elevation (m)')


ax5 = fig.add_subplot(gs[1, 3:8])
ax5.spines['bottom'].set(lw=2,color='tab:orange')
ax5.spines['top'].set(lw=2,color='tab:orange')
ax5.spines['left'].set(lw=2,color='tab:orange')
ax5.spines['right'].set(lw=2,color='tab:orange')
ax5.yaxis.set_label_position("right")
ax5.yaxis.tick_right()

ax5.pcolormesh(DIST_1,ZZ_1,postEnv_1,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
ax5.plot(DIST_1[0,:],ZZ_1[0,:],c='k')
ax5.set_aspect(VE)
ax5.plot([ang2dist_a_1,ang2dist_a_1],[-3,3],c='tab:red',lw=1,ls='--')
ax5.plot([ang2dist_b_1,ang2dist_b_1],[-3,3],c='tab:gray',lw=1,ls='--')
ax5.plot([ang2dist_c_1,ang2dist_c_1],[-3,3],c='tab:cyan',lw=1,ls='--')
ax5.text(0.1,-1.9,'(e)',size='large',color='k',ha='left',va='bottom',weight='regular')

ax5.set_ylim([-2,0.5])
ax5.set_xlabel('Distance (m)')
ax5.set_ylabel('Relative Elevation (m)')


ax6 = fig.add_subplot(gs[2, 3:8])
ax6.spines['bottom'].set(lw=2,color='tab:purple')
ax6.spines['top'].set(lw=2,color='tab:purple')
ax6.spines['left'].set(lw=2,color='tab:purple')
ax6.spines['right'].set(lw=2,color='tab:purple')
ax6.yaxis.set_label_position("right")
ax6.yaxis.tick_right()
cmap = ax6.pcolormesh(DIST_2,ZZ_2,postEnv_2,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
ax6.plot(DIST_2[0,:],ZZ_2[0,:],c='k')
ax6.set_aspect(VE)
ax6.plot([ang2dist_a_2,ang2dist_a_2],[-3,3],c='tab:red',lw=1,ls='--')
ax6.plot([ang2dist_b_2,ang2dist_b_2],[-3,3],c='tab:gray',lw=1,ls='--')
ax6.plot([ang2dist_c_2,ang2dist_c_2],[-3,3],c='tab:cyan',lw=1,ls='--')
ax6.text(0.2,-2.9,'(f)',size='large',color='k',ha='left',va='bottom',weight='regular')

ax6.set_ylim([-3,0.75])
ax6.set_xlabel('Distance (m)')
ax6.set_ylabel('Relative Elevation (m)')
plt.colorbar(cmap,ax=ax6,label='',orientation='horizontal',shrink=0.5)
fig.savefig('Fig07_Amplitude_Profiles.png',dpi=300,transparent=True)

#%% Make GIFS for radial sections
path2Save = './RadialProfiles_Images/'
makeSections = False

angles4Vid = np.linspace(0,2*np.pi,360)
r = np.linspace(0,13,N)

VE = 2

if makeSections:

    for i in range(0,len(angles4Vid)):
        fileName = 'Radial_Angle_' + str(np.round(angles4Vid[i]*180/np.pi,1)) + '.png'
        print(fileName)
        theta = np.ones(len(r))*angles4Vid[i]
        path = np.column_stack([theta,r])
        DIST,DEPTHS,THETA,postEnv,postMig = allGPRData.getRadialProfile(path,N,tol,powerVal)
        ZZ = np.zeros(THETA.shape)
        xi = DIST[0,:]*np.cos(THETA[0,:]) + treeCenter[0]
        yi = DIST[0,:]*np.sin(THETA[0,:]) + treeCenter[1]
        zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
        for i in range(0,DEPTHS.shape[1]):
            ZZ[:,i] = zElev[i] - DEPTHS[:,i]
            
            
        fig = plt.figure(constrained_layout=True,figsize=[7,5])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122,polar=True)
        cbar = ax1.pcolormesh(DIST,ZZ,postEnv,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
        ax1.plot(DIST[0,:],ZZ[0,:],c='k')
        ax1.set_aspect(VE)
        #ax1.set_ylim([-3,2.75])
        #ax1.set_ylim([-1.5,2.5])
        ax1.set_xlabel('Radial Distance (m)')
        ax1.set_ylabel('Relative Elevation (m)')

        
        ax2.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray')
        ax2.plot(THETA[0,:],DIST[0,:],c='k')
        ax2.set_ylim([0, 14])
        #ax2.set_xlim([1, 13.5])

        ax2.set_yticks(np.arange(0, 15, 1))
        ax2.set_yticklabels([])
        ax2.set_xticks(np.arange(0, 2 * np.pi, 20 * np.pi / 180))
        ax2.set_aspect(1)
        plt.colorbar(cbar,ax=ax2,label='',orientation='horizontal',shrink=0.8)

        fig.savefig(path2Save+fileName,dpi=300,transparent=True)
        plt.close('all')
        
#%%Make ciruclar profiles (DISTANCE)
path2Save = './CircularProfilesDist_Images/'
makeSections = False
VE = 2
lineNumbers = np.arange(0,65,1).astype(int)

if makeSections:
    for i in range(0,len(lineNumbers)):
        fileName = 'circular_line_' + str(np.round(lineNumbers[i],0)) + '.png'

        dist,theta,radius,preMig,postMig,postEnv = allGPRData.getRadialProfile_byLine(int(lineNumbers[i]),powerVal)
        THETA = np.tile(theta, (preMig.shape[0],1))
        DEPTHS = np.tile(allGPRData.gpr_depths[0],(preMig.shape[1],1)).T
        DIST = np.tile(dist, (preMig.shape[0],1))
        R = np.tile(radius, (preMig.shape[0],1))  
        e = allGPRData.gpr_E[lineNumbers[i]]
        n = allGPRData.gpr_N[lineNumbers[i]]
        xi = R[0,:]*np.cos(THETA[0,:]*np.pi/180) + treeCenter[0]
        yi = R[0,:]*np.sin(THETA[0,:]*np.pi/180) + treeCenter[1]
        meanRad = np.mean(np.sqrt(xi**2+yi**2))
        zElev = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (xi,yi),method='nearest')
        ZZ = np.zeros(R.shape)
        zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
        for i in range(0,DEPTHS.shape[1]):
            ZZ[:,i] = zElev[i] - DEPTHS[:,i]
    
        fig = plt.figure(constrained_layout=True,figsize=[13,4])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        cmap = ax1.pcolormesh(DIST,ZZ,postEnv,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
        ax1.plot(DIST[0,:],ZZ[0,:],c='k')
        #ax1.set_ylim([-3,2.75])
        #ax1.set_xlim([0,50])
        ax1.set_xlabel('Distance (m)')
        ax1.set_ylabel('Relative Elevation (m)')
        ax1.set_aspect(VE)
        
        ax2.pcolormesh(EE,NN,HS_resamp,cmap='gray')
        ax2.plot(xi,yi,c='k',lw=1)
        ax2.set_xlim([-15, 13.5])
        #ax2.set_ylim([-15, 13.5])
        ax2.set_aspect(1)
        ax2.set_xlabel('Distance (m)')
        ax2.set_ylabel('Distance (m)')
        plt.colorbar(cbar,ax=ax2,label='',orientation='horizontal',shrink=0.8)
        fig.savefig(path2Save+fileName,dpi=300,transparent=True)
        plt.close('all')
        
#%% Make GIFS for circular sections: Angle
VE = 2
path2Save = './CircularProfilesAngle_Images/'

lineNumbers = np.arange(0,65,1).astype(int)
makeSections = False

if makeSections:
    for i in range(0,len(lineNumbers)):
        fileName = 'circular_line_' + str(np.round(lineNumbers[i],0)) + '.png'

        dist,theta,radius,preMig,postMig,postEnv = allGPRData.getRadialProfile_byLine(int(lineNumbers[i]),powerVal)
        THETA = np.tile(theta, (preMig.shape[0],1))
        DEPTHS = np.tile(allGPRData.gpr_depths[0],(preMig.shape[1],1)).T
        DIST = np.tile(dist, (preMig.shape[0],1))
        R = np.tile(radius, (preMig.shape[0],1))  
        e = allGPRData.gpr_E[lineNumbers[i]]
        n = allGPRData.gpr_N[lineNumbers[i]]
        xi = R[0,:]*np.cos(THETA[0,:]*np.pi/180) + treeCenter[0]
        yi = R[0,:]*np.sin(THETA[0,:]*np.pi/180) + treeCenter[1]
        meanRad = np.mean(np.sqrt(xi**2+yi**2))
        zElev = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (xi,yi),method='nearest')
        ZZ = np.zeros(R.shape)
        zElev = griddata(np.column_stack([ee.ravel(),nn.ravel()]), elev.ravel(), (xi,yi),method='nearest')
        for i in range(0,DEPTHS.shape[1]):
            ZZ[:,i] = zElev[i] - DEPTHS[:,i]
    
        fig = plt.figure(constrained_layout=True,figsize=[13,4])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122,polar=True)

        cmap = ax1.pcolormesh(THETA,ZZ,postEnv,vmin=vMin,vmax=vMax,cmap='cubehelix_r')
        ax1.plot(THETA[0,:],ZZ[0,:],c='k')
        #ax1.set_ylim([-1,2.75])
        #ax1.set_xlim([0,50])
        ax1.set_xlabel('Angle (degrees)')
        ax1.set_ylabel('Relative Elevation (m)')
        aspect = 1/(np.max(dist)/360)*VE
        ax1.set_aspect(aspect)
        
        ax2.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray')
        ax2.plot(theta*np.pi/180,radius,c='k')
        ax2.set_ylim([0, 14])
 
        ax2.set_yticks(np.arange(0, 15, 1))
        ax2.set_yticklabels([])
        ax2.set_xticks(np.arange(0, 2 * np.pi, 20 * np.pi / 180))
        ax2.set_aspect(1)
        plt.colorbar(cmap,ax=ax2,label='',orientation='horizontal',shrink=0.8)

        fig.savefig(path2Save+fileName,dpi=300,transparent=True)
        plt.close('all')
        
#%% BUILD ARRAYS FOR BUILDING VOLUMES ETC.
avgWindow = 5
thresh = 2.25 #1.5x greater than mean
powerVal = 2

allDepths = np.array([])
allThetas = np.array([])
allRadii = np.array([])
allEast = np.array([])
allNorth = np.array([])
allAmps = np.array([])

#FOR RESAMPLED PV Grid
x = np.array([])
y = np.array([])
z = np.array([])
a = np.array([])

index = 0
for depth in depths:
    east,north,angle,radius,amp = allGPRData.getDepthSection(depth, avgWindow, powerVal, thresh)
    print(index+1, 'of',len(depths), np.round(depth,3),len(east))

    allDepths = np.append(allDepths,np.ones(len(east))*depth)
    allThetas = np.append(allThetas,angle)
    allRadii = np.append(allRadii,radius)
    allEast = np.append(allEast,east)
    allNorth = np.append(allNorth,north)
    allAmps = np.append(allAmps,amp)
    
    points = np.column_stack([east,north])
    grid_z0 = griddata(points, amp, (EE, NN), method='nearest')
    grid_z0[RR>=112] = 0
    x = np.append(x,EE.flatten())
    y = np.append(y, NN.flatten())
    z = np.append(z,np.ones(NN.size)*depth)
    a = np.append(a,grid_z0.flatten())
    
    index += 1
    
#%% DEPTH SECTION Figure 8a
d0 = 0.05
df = 0.25
fileName = 'Fig08a_DepthSection_' + str(d0) + 'to' + str(df) + '_.png'    
ind2Keep = np.where(np.logical_and(allDepths>d0,allDepths<=df))[0]

avgAmp = allAmps[ind2Keep]
avgDepth = allDepths[ind2Keep]
avgTheta = allThetas[ind2Keep]
avgRadius = allRadii[ind2Keep]
avgEast = allEast[ind2Keep]
avgNorth = allNorth[ind2Keep]

sortOrder = np.argsort(avgAmp)
avgAmp = avgAmp[sortOrder]
avgTheta = avgTheta[sortOrder]
avgRadius = avgRadius[sortOrder]
avgDepth = avgDepth[sortOrder]
avgEast = avgEast[sortOrder]
avgNorth = avgNorth[sortOrder]

fig = plt.figure(constrained_layout=True,figsize=[6,6])
ax1 = fig.add_subplot(111,polar=True)
ax1.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray',alpha=0.5)

alphaVals = (avgAmp/20)
alphaVals[alphaVals>1] = 1
alphaVals = alphaVals**2.7
#randSample = np.random.random_integers(0,len(avgTheta),int(np.floor((len(avgTheta))*fract))-3)    
#cbar = ax.scatter(avgTheta[randSample]*np.pi/180,avgRadius[randSample],s=1,c=avgDepth[randSample]*100,cmap='turbo_r',vmin=0,vmax=60,alpha=alphaVals[randSample])
cbar = ax1.scatter(avgTheta*np.pi/180,avgRadius,s=1,c=avgAmp,cmap='cubehelix_r',vmin=vMin,vmax=vMax)
ax1.plot([HIGHLIGHTED_ANGLES[0],HIGHLIGHTED_ANGLES[0]],[0,14],c='tab:red',lw=2,ls='--')
ax1.plot([HIGHLIGHTED_ANGLES[1],HIGHLIGHTED_ANGLES[1]],[0,14],c='tab:gray',lw=2,ls='--')
ax1.plot([HIGHLIGHTED_ANGLES[2],HIGHLIGHTED_ANGLES[2]],[0,14],c='tab:cyan',lw=2,ls='--')

plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = 25  # pad is in points...
ax1.set_ylim([0, 14])
ax1.set_yticks(np.arange(0, 15, 1))
ax1.set_yticklabels([])
ax1.set_xticks(np.arange(0, 2 * np.pi, 20 * np.pi / 180));
titleStr = str(np.round(d0,2)) + ' cm to ' + str(np.round(df,2)) + ' cm'
ax1.set_title(titleStr)
fig.savefig(fileName,dpi=300,transparent=True) 

#%%  Depth Section 2 Figure 8b
d0 = 0.25
df = 0.45
fileName = 'Fig08b_DepthSection_' + str(d0) + 'to' + str(df) + '_.png'    
ind2Keep = np.where(np.logical_and(allDepths>d0,allDepths<=df))[0]

avgAmp = allAmps[ind2Keep]
avgDepth = allDepths[ind2Keep]
avgTheta = allThetas[ind2Keep]
avgRadius = allRadii[ind2Keep]
avgEast = allEast[ind2Keep]
avgNorth = allNorth[ind2Keep]

sortOrder = np.argsort(avgAmp)
avgAmp = avgAmp[sortOrder]
avgTheta = avgTheta[sortOrder]
avgRadius = avgRadius[sortOrder]
avgDepth = avgDepth[sortOrder]
avgEast = avgEast[sortOrder]
avgNorth = avgNorth[sortOrder]

fig = plt.figure(constrained_layout=True,figsize=[6,6])
ax1 = fig.add_subplot(111,polar=True)
ax1.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray',alpha=0.5)

alphaVals = (avgAmp/20)
alphaVals[alphaVals>1] = 1
alphaVals = alphaVals**2.7
#randSample = np.random.random_integers(0,len(avgTheta),int(np.floor((len(avgTheta))*fract))-3)    
#cbar = ax.scatter(avgTheta[randSample]*np.pi/180,avgRadius[randSample],s=1,c=avgDepth[randSample]*100,cmap='turbo_r',vmin=0,vmax=60,alpha=alphaVals[randSample])
cbar = ax1.scatter(avgTheta*np.pi/180,avgRadius,s=1,c=avgAmp,cmap='cubehelix_r',vmin=vMin,vmax=vMax)
ax1.plot([HIGHLIGHTED_ANGLES[0],HIGHLIGHTED_ANGLES[0]],[0,14],c='tab:red',lw=2,ls='--')
ax1.plot([HIGHLIGHTED_ANGLES[1],HIGHLIGHTED_ANGLES[1]],[0,14],c='tab:gray',lw=2,ls='--')
ax1.plot([HIGHLIGHTED_ANGLES[2],HIGHLIGHTED_ANGLES[2]],[0,14],c='tab:cyan',lw=2,ls='--')

plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = 25  # pad is in points...
ax1.set_ylim([0, 14])
ax1.set_yticks(np.arange(0, 15, 1))
ax1.set_yticklabels([])
ax1.set_xticks(np.arange(0, 2 * np.pi, 20 * np.pi / 180));
titleStr = str(np.round(d0,2)) + ' cm to ' + str(np.round(df,2)) + ' cm'
ax1.set_title(titleStr)
fig.savefig(fileName,dpi=300,transparent=True) 

#%%  Depth Section 2 Figure 8c
d0 = 0.45
df = 0.65
fileName = 'Fig08c_DepthSection_' + str(d0) + 'to' + str(df) + '_.png'    
ind2Keep = np.where(np.logical_and(allDepths>d0,allDepths<=df))[0]

avgAmp = allAmps[ind2Keep]
avgDepth = allDepths[ind2Keep]
avgTheta = allThetas[ind2Keep]
avgRadius = allRadii[ind2Keep]
avgEast = allEast[ind2Keep]
avgNorth = allNorth[ind2Keep]

sortOrder = np.argsort(avgAmp)
avgAmp = avgAmp[sortOrder]
avgTheta = avgTheta[sortOrder]
avgRadius = avgRadius[sortOrder]
avgDepth = avgDepth[sortOrder]
avgEast = avgEast[sortOrder]
avgNorth = avgNorth[sortOrder]

fig = plt.figure(constrained_layout=True,figsize=[6,6])
ax1 = fig.add_subplot(111,polar=True)
ax1.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray',alpha=0.5)

alphaVals = (avgAmp/20)
alphaVals[alphaVals>1] = 1
alphaVals = alphaVals**2.7
#randSample = np.random.random_integers(0,len(avgTheta),int(np.floor((len(avgTheta))*fract))-3)    
#cbar = ax.scatter(avgTheta[randSample]*np.pi/180,avgRadius[randSample],s=1,c=avgDepth[randSample]*100,cmap='turbo_r',vmin=0,vmax=60,alpha=alphaVals[randSample])
cbar = ax1.scatter(avgTheta*np.pi/180,avgRadius,s=1,c=avgAmp,cmap='cubehelix_r',vmin=vMin,vmax=vMax)
ax1.plot([HIGHLIGHTED_ANGLES[0],HIGHLIGHTED_ANGLES[0]],[0,14],c='tab:red',lw=2,ls='--')
ax1.plot([HIGHLIGHTED_ANGLES[1],HIGHLIGHTED_ANGLES[1]],[0,14],c='tab:gray',lw=2,ls='--')
ax1.plot([HIGHLIGHTED_ANGLES[2],HIGHLIGHTED_ANGLES[2]],[0,14],c='tab:cyan',lw=2,ls='--')

plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = 25  # pad is in points...
ax1.set_ylim([0, 14])
ax1.set_yticks(np.arange(0, 15, 1))
ax1.set_yticklabels([])
ax1.set_xticks(np.arange(0, 2 * np.pi, 20 * np.pi / 180));
titleStr = str(np.round(d0,2)) + ' cm to ' + str(np.round(df,2)) + ' cm'
ax1.set_title(titleStr)
fig.savefig(fileName,dpi=300,transparent=True) 

#%%  Depth Section 2 Figure 8d
d0 = 0.65
df = 0.85
fileName = 'Fig08d_DepthSection_' + str(d0) + 'to' + str(df) + '_.png'    
ind2Keep = np.where(np.logical_and(allDepths>d0,allDepths<=df))[0]

avgAmp = allAmps[ind2Keep]
avgDepth = allDepths[ind2Keep]
avgTheta = allThetas[ind2Keep]
avgRadius = allRadii[ind2Keep]
avgEast = allEast[ind2Keep]
avgNorth = allNorth[ind2Keep]

sortOrder = np.argsort(avgAmp)
avgAmp = avgAmp[sortOrder]
avgTheta = avgTheta[sortOrder]
avgRadius = avgRadius[sortOrder]
avgDepth = avgDepth[sortOrder]
avgEast = avgEast[sortOrder]
avgNorth = avgNorth[sortOrder]

fig = plt.figure(constrained_layout=True,figsize=[6,6])
ax1 = fig.add_subplot(111,polar=True)
ax1.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray',alpha=0.5)

alphaVals = (avgAmp/20)
alphaVals[alphaVals>1] = 1
alphaVals = alphaVals**2.7
#randSample = np.random.random_integers(0,len(avgTheta),int(np.floor((len(avgTheta))*fract))-3)    
#cbar = ax.scatter(avgTheta[randSample]*np.pi/180,avgRadius[randSample],s=1,c=avgDepth[randSample]*100,cmap='turbo_r',vmin=0,vmax=60,alpha=alphaVals[randSample])
cbar = ax1.scatter(avgTheta*np.pi/180,avgRadius,s=1,c=avgAmp,cmap='cubehelix_r',vmin=vMin,vmax=vMax)
ax1.plot([HIGHLIGHTED_ANGLES[0],HIGHLIGHTED_ANGLES[0]],[0,14],c='tab:red',lw=2,ls='--')
ax1.plot([HIGHLIGHTED_ANGLES[1],HIGHLIGHTED_ANGLES[1]],[0,14],c='tab:gray',lw=2,ls='--')
ax1.plot([HIGHLIGHTED_ANGLES[2],HIGHLIGHTED_ANGLES[2]],[0,14],c='tab:cyan',lw=2,ls='--')

plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = 25  # pad is in points...
ax1.set_ylim([0, 14])
ax1.set_yticks(np.arange(0, 15, 1))
ax1.set_yticklabels([])
ax1.set_xticks(np.arange(0, 2 * np.pi, 20 * np.pi / 180));
titleStr = str(np.round(d0,2)) + ' cm to ' + str(np.round(df,2)) + ' cm'
ax1.set_title(titleStr)
fig.savefig(fileName,dpi=300,transparent=True) 

#%% VIDEO OF DEPTH SECTIONS
depths4Vid = np.arange(0.02,1.32,0.02)
path = './DepthSections/'
makeSections = False

if makeSections:
    
    for i in range(1,len(depths4Vid)):
        d0 = depths4Vid[i-1]
        df = depths4Vid[i]
        print(d0,df)
        fileName = path + 'DepthSection_' + str(np.round(d0,2)) + 'to' + str(np.round(df,2)) + '_.png'    
        ind2Keep = np.where(np.logical_and(allDepths>d0,allDepths<=df))[0]
        
        avgAmp = allAmps[ind2Keep]
        avgDepth = allDepths[ind2Keep]
        avgTheta = allThetas[ind2Keep]
        avgRadius = allRadii[ind2Keep]
        avgEast = allEast[ind2Keep]
        avgNorth = allNorth[ind2Keep]
        
        sortOrder = np.argsort(avgAmp)
        avgAmp = avgAmp[sortOrder]
        avgTheta = avgTheta[sortOrder]
        avgRadius = avgRadius[sortOrder]
        avgDepth = avgDepth[sortOrder]
        avgEast = avgEast[sortOrder]
        avgNorth = avgNorth[sortOrder]
        
        fig = plt.figure(constrained_layout=True,figsize=[6,6])
        ax1 = fig.add_subplot(111,polar=True)
        ax1.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray',alpha=0.5)
        
        #randSample = np.random.random_integers(0,len(avgTheta),int(np.floor((len(avgTheta))*fract))-3)    
        #cbar = ax.scatter(avgTheta[randSample]*np.pi/180,avgRadius[randSample],s=1,c=avgDepth[randSample]*100,cmap='turbo_r',vmin=0,vmax=60,alpha=alphaVals[randSample])
        cbar = ax1.scatter(avgTheta*np.pi/180,avgRadius,s=1,c=avgAmp,cmap='cubehelix_r',vmin=vMin,vmax=vMax)
        #ax1.plot([HIGHLIGHTED_ANGLES[0],HIGHLIGHTED_ANGLES[0]],[0,14],c='tab:red',lw=2,ls='--')
        #ax1.plot([HIGHLIGHTED_ANGLES[1],HIGHLIGHTED_ANGLES[1]],[0,14],c='tab:gray',lw=2,ls='--')
        #ax1.plot([HIGHLIGHTED_ANGLES[2],HIGHLIGHTED_ANGLES[2]],[0,14],c='tab:cyan',lw=2,ls='--')
        
        plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
        plt.rcParams['axes.titlepad'] = 25  # pad is in points...
        ax1.set_ylim([0, 14])
        ax1.set_yticks(np.arange(0, 15, 1))
        ax1.set_yticklabels([])
        ax1.set_xticks(np.arange(0, 2 * np.pi, 20 * np.pi / 180));
        ax1.set_title(str(np.round(d0,2)) + ' m to ' + str(np.round(df,2)) + ' m ' )
        fig.savefig(fileName,dpi=300,transparent=True) 
        
#%% SMALL ADJUSTMENTS FOR CROSS SECTION Figure 9
  
outFile = 'Fig09_Gray_root.png'
N=1000
tol = 0.005
d0 = 0.05
df = 0.45
depth = (d0+df)/2
VE = 2
rootPickFile = 'picks_gray.txt'
outfile = 'Gray_root.png'
ind2Keep = np.where(np.logical_and(allDepths>d0,allDepths<=df))[0]

avgAmp = allAmps[ind2Keep]
avgDepth = allDepths[ind2Keep]
avgTheta = allThetas[ind2Keep]
avgRadius = allRadii[ind2Keep]
avgEast = allEast[ind2Keep]
avgNorth = allNorth[ind2Keep]

sortOrder = np.argsort(avgAmp)
avgAmp = avgAmp[sortOrder]
avgTheta = avgTheta[sortOrder]
avgRadius = avgRadius[sortOrder]
avgDepth = avgDepth[sortOrder]
avgEast = avgEast[sortOrder]
avgNorth = avgNorth[sortOrder]

picks_rad = np.loadtxt(rootPickFile)
XX,DD,TH,ENV,MIG = allGPRData.getRadialProfile(picks_rad,N,tol,powerVal)


xi = XX[0,:]*np.cos(TH[0,:]) + treeCenter[0]
yi = XX[0,:]*np.sin(TH[0,:]) + treeCenter[1]
XXi = XX*np.cos(TH) + treeCenter[0]
YYi = XX*np.sin(TH) + treeCenter[1]
DIST_PLOT = np.sqrt((xi[-1]-XXi)**2 + (yi[-1]-YYi)**2)
ZZ = np.zeros(XX.shape)
zElev = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (xi,yi),method='nearest')
for i in range(0,DD.shape[1]):
    ZZ[:,i] = zElev[i] - DD[:,i]     
    
fig = plt.figure(figsize=[13,5],constrained_layout=True)
gs = fig.add_gridspec(1, 4)
ax1 = fig.add_subplot(gs[0,0:2],aspect=VE)
#ax1.xaxis.tick_top()
#ax1.xaxis.set_label_position("top")
ax1.set_xlabel('Distance Along Profile (m)')
ax1.set_ylabel('Elevation (m)')

ax2 = fig.add_subplot(gs[0,2:4],polar=True)

ax1.pcolormesh(DIST_PLOT,ZZ,ENV,cmap='cubehelix_r',vmin=vMin,vmax=vMax)#YlGnBu_r
ax1.plot(DIST_PLOT[0,:],ZZ[0,:],c='k',lw=1)
#ax1.plot(DIST_PLOT[0,:],ZZ[0,:]-0.45,c='r',lw=1,ls='--')

#ax1.plot(XX[0,:],ZZ[0,:]-depth,c='tab:red',lw=1,ls='--')
#ax1.fill_between(XX[0,:],ZZ[0,:]-d0,ZZ[0,:]-df,color='tab:red',alpha=0.15)
#ax1.grid()
#ax1.set_ylim([-0.5,2.25])
#ax1.set_xlim([2,10.6])
ax1.set_ylim([-1.75,0.25])


tr = np.arctan2(NN,EE)
rr = (EE**2 + NN**2 )**0.5
ax2.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray',alpha=0.5)

cbar = ax2.scatter(avgTheta*np.pi/180,avgRadius,s=1,c=avgAmp,cmap='cubehelix_r',vmin=vMin,vmax=vMax)
#ax2.plot(picks_rad[:,0],picks_rad[:,1],c='tab:red',ls='--')

cbar = ax2.scatter(TH[0,:],XX[0,:],s=3,c=DIST_PLOT[0,:],cmap='rainbow',alpha=0.5)
ax2.plot([HIGHLIGHTED_ANGLES[1],HIGHLIGHTED_ANGLES[1]],[XX[0,0],XX[0,-1]],c='k',lw=2,ls='--')
plt.colorbar(cbar,ax=ax2,orientation='vertical',shrink=0.8,label='Distance Along Profile (m)')


# Panel labels
ax1.text(0.01, 0.02, '(a)', transform=ax1.transAxes,
         ha='left', va='bottom', fontsize=14, fontweight='regular', zorder=5)

# Place (b) just below the polar plot (slightly outside the axes)
ax2.text(0.5, -0.08, '(b)', transform=ax2.transAxes,
         ha='center', va='top', fontsize=14, fontweight='regular',
         clip_on=False, zorder=5)


ax2.set_ylim([0,13])
ax2.set_yticks(np.arange(0,13,1));
ax2.set_yticklabels([]);
ax2.grid()
ax2.set_xticklabels([]);
fig.savefig(outFile,dpi=600,transparent=True)

 #%% Cross seciton (VALIDATION)  
N=1000
tol = 0.005
d0 = 0.05
df = 0.45
depth = (d0+df)/2
VE = 2

ind2Keep = np.where(np.logical_and(allDepths>d0,allDepths<=df))[0]

avgAmp = allAmps[ind2Keep]
avgDepth = allDepths[ind2Keep]
avgTheta = allThetas[ind2Keep]
avgRadius = allRadii[ind2Keep]
avgEast = allEast[ind2Keep]
avgNorth = allNorth[ind2Keep]

sortOrder = np.argsort(avgAmp)
avgAmp = avgAmp[sortOrder]
avgTheta = avgTheta[sortOrder]
avgRadius = avgRadius[sortOrder]
avgDepth = avgDepth[sortOrder]
avgEast = avgEast[sortOrder]
avgNorth = avgNorth[sortOrder]

picks_xy = np.loadtxt('picks_validation.txt')
tmp_angle = np.arctan2(picks_xy[:,1]-treeCenter[1],picks_xy[:,0]-treeCenter[0]) 
tmp_angle = np.insert(tmp_angle,0,1.996*np.pi)
temp_r = np.sqrt((picks_xy[:,0]-treeCenter[0])**2 + (picks_xy[:,1]-treeCenter[1])**2)
temp_r = np.insert(temp_r,0,11.6)
picks_rad = np.column_stack([tmp_angle,temp_r])
picks_rad = np.flipud(picks_rad)
XX,DD,TH,ENV,MIG = allGPRData.getRadialProfile(picks_rad,N,tol,powerVal)


xi = XX[0,:]*np.cos(TH[0,:]) + treeCenter[0]
yi = XX[0,:]*np.sin(TH[0,:]) + treeCenter[1]
XXi = XX*np.cos(TH) + treeCenter[0]
YYi = XX*np.sin(TH) + treeCenter[1]
DIST_PLOT = np.sqrt((xi[-1]-XXi)**2 + (yi[-1]-YYi)**2)
ZZ = np.zeros(XX.shape)
zElev = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (xi,yi),method='nearest')
for i in range(0,DD.shape[1]):
    ZZ[:,i] = zElev[i] - DD[:,i]     
    
fig = plt.figure(figsize=[13,5],constrained_layout=True)
gs = fig.add_gridspec(1, 4)
ax1 = fig.add_subplot(gs[0,0:2],aspect=VE)
#ax1.xaxis.tick_top()
#ax1.xaxis.set_label_position("top")
ax1.set_xlabel('Distance Along Profile (m)')
ax1.set_ylabel('Elevation (m)')

ax2 = fig.add_subplot(gs[0,2:4],polar=True)

ax1.pcolormesh(DIST_PLOT,ZZ,ENV,cmap='cubehelix_r',vmin=vMin,vmax=vMax)#YlGnBu_r
ax1.plot(DIST_PLOT[0,:],ZZ[0,:],c='k',lw=1)
#ax1.plot(DIST_PLOT[0,:],ZZ[0,:]-0.45,c='r',lw=1,ls='--')

ind1 = np.argmin((XX[0,:]-(1.2+0.85))**2)
ax1.plot([DIST_PLOT[0,ind1],DIST_PLOT[0,ind1]],[0+elev_shfit,2.5],c='tab:blue',lw=1,ls='--')
ax1.plot([DIST_PLOT[0,ind1],DIST_PLOT[0,ind1]],[1.214+elev_shfit,1.246+elev_shfit],c='tab:blue',lw=5)

# ax1.plot([DIST_PLOT[0,ind1],DIST_PLOT[0,ind1]],[0,2.5],c='tab:blue',lw=1,ls='--')

ind2 = np.argmin((XX[0,:]-(3.6+0.85))**2)
ax1.plot([DIST_PLOT[0,ind2],DIST_PLOT[0,ind2]],[0+elev_shfit,2.5],c='tab:orange',lw=1,ls='--')
ax1.plot([DIST_PLOT[0,ind2],DIST_PLOT[0,ind2]],[1.224+elev_shfit,1.232+elev_shfit],c='tab:orange',lw=5)

# ax1.plot([DIST_PLOT[0,ind2],DIST_PLOT[0,ind2]],[0,2.5],c='tab:orange',lw=1,ls='--')

ind3 = np.argmin((XX[0,:]-(6.8+0.85))**2) 
ax1.plot([DIST_PLOT[0,ind3],DIST_PLOT[0,ind3]],[0+elev_shfit,2.5],c='tab:red',lw=1,ls='--')
ax1.plot([DIST_PLOT[0,ind3],DIST_PLOT[0,ind3]],[1.651+elev_shfit,1.665+elev_shfit],c='tab:red',lw=5)

# ax1.plot([DIST_PLOT[0,ind3],DIST_PLOT[0,ind3]],[0,2.5],c='tab:purple',lw=1,ls='--')


#ax1.plot(XX[0,:],ZZ[0,:]-depth,c='tab:red',lw=1,ls='--')
#ax1.fill_between(XX[0,:],ZZ[0,:]-d0,ZZ[0,:]-df,color='tab:red',alpha=0.15)
#ax1.grid()
#ax1.set_ylim([-0.5,2.25])
#ax1.set_xlim([2,10.6])
ax1.set_ylim([-2,0.5])

   
tr = np.arctan2(NN,EE)
rr = (EE**2 + NN**2 )**0.5
ax2.pcolormesh(TT,RR,HS_resamp_polar,cmap='gray',alpha=0.5)

cbar = ax2.scatter(avgTheta*np.pi/180,avgRadius,s=1,c=avgAmp,cmap='cubehelix_r',vmin=vMin,vmax=vMax)
ax2.scatter(TH[0,ind1],XX[0,ind1],s=75,c='tab:blue',ec='k')
ax2.scatter(TH[0,ind2],XX[0,ind2],s=75,c='tab:orange',ec='k')
ax2.scatter(TH[0,ind3],XX[0,ind3],s=75,c='tab:red',ec='k')

#cbar = ax2.scatter(TH[0,:],XX[0,:],s=3,c=DIST_PLOT[0,:],cmap='rainbow',alpha=0.5)
#plt.colorbar(cbar,ax=ax2,orientation='vertical',shrink=0.8,label='Distance Along Profile (m)')



ax2.set_ylim([0,13])
ax2.set_yticks(np.arange(0,13,1));
ax2.set_yticklabels([]);
ax2.set_xticklabels([]);
fig.savefig('Validation_root.png',dpi=600,transparent=True)


#%% PYVISTA PLOT SCATTER
vdf = pd.read_csv('SCBG_Validation.csv')
points = np.column_stack([vdf['x'].to_numpy(),vdf['y'].to_numpy()])
newz = griddata(np.column_stack([ee.ravel(),nn.ravel()]),elev.ravel(),points,method='nearest')
vdf['z'] = newz
validate = np.column_stack([vdf['x'].to_numpy(),vdf['y'].to_numpy(),vdf['z'].to_numpy()])
def my_cpos_callback():
    #p.add_text(str(p.camera.position)+'\n'+str(p.camera.focal_point)+'\n'+str(p.camera.view), name="cpos",color='k')
    p.add_text(str(p.camera_position), name="cpos",color='k')
    return


angle1 = 0   
angle2 = 25

ind2Keep = np.where(np.logical_and(allThetas>=angle1,allThetas<=angle2))[0]
avgAmp = allAmps[ind2Keep]
avgDepth = allDepths[ind2Keep]
avgTheta = allThetas[ind2Keep]
avgRadius = allRadii[ind2Keep]
avgEast = allEast[ind2Keep]
avgNorth = allNorth[ind2Keep]

sortOrder = np.argsort(avgAmp)
avgAmp = avgAmp[sortOrder]
avgTheta = avgTheta[sortOrder]
avgRadius = avgRadius[sortOrder]
avgDepth = avgDepth[sortOrder]
avgEast = avgEast[sortOrder]
avgNorth = avgNorth[sortOrder]


angle1 = 350    
angle2 = 360
ind2Keep = np.where(np.logical_and(allThetas>=angle1,allThetas<=angle2))[0]
avgAmp2 = allAmps[ind2Keep]
avgDepth2 = allDepths[ind2Keep]
avgTheta2 = allThetas[ind2Keep]
avgRadius2 = allRadii[ind2Keep]
avgEast2 = allEast[ind2Keep]
avgNorth2 = allNorth[ind2Keep]

sortOrder = np.argsort(avgAmp2)
avgAmp2 = avgAmp2[sortOrder]
avgTheta2 = avgTheta2[sortOrder]
avgRadius2 = avgRadius2[sortOrder]
avgDepth2 = avgDepth2[sortOrder]
avgEast2 = avgEast2[sortOrder]
avgNorth2 = avgNorth2[sortOrder]


avgElev = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (avgEast,avgNorth),method='nearest')
avgElev2 = griddata(np.column_stack([EE.ravel(),NN.ravel()]), ELV_resamp.ravel(), (avgEast2,avgNorth2),method='nearest')

xyzPoints = np.column_stack([avgEast,avgNorth,avgElev-avgDepth])
xyzPoints2 = np.column_stack([avgEast2,avgNorth2,avgElev2-avgDepth2])
xyzPointsElev = np.column_stack([avgEast,avgNorth,avgElev])


xrng = np.arange(-1,13,0.05)#e_resamp 
yrng = np.arange(-5.5,4,0.05) #n_resamp   
zrng = depths
x, y, z = np.meshgrid(xrng, yrng, zrng, indexing='ij')
ELV4Grid = griddata(np.column_stack([ee.ravel(),nn.ravel()]),elev.ravel(),(x[:,:,0],y[:,:,0]),method='nearest')
 
elvGrid = pv.StructuredGrid(x[:,:,0], y[:,:,0], ELV4Grid)
elvGrid['Data'] = elvGrid.points[:, 2]

p = pv.Plotter()        
p.set_background('white')
p.add_mesh(elvGrid,opacity=0.45,cmap='gray',clim=[0,2],
           show_scalar_bar=False)
p.add_points(xyzPoints,scalars=avgAmp,style='points_gaussian',
       point_size=2.5,show_scalar_bar=False,clim=[vMin,vMax],cmap='cubehelix_r',
       opacity='sigmoid',lighting=False)
p.add_points(xyzPoints2,scalars=avgAmp2,style='points_gaussian',
       point_size=2.5,show_scalar_bar=False,clim=[vMin,vMax],cmap='cubehelix_r',
       opacity='sigmoid',lighting=False)
p.add_points(validate,color='red',point_size=10,render_points_as_spheres=True)

p.camera_position = [(12.48,-20.19,18.02),
                     (6.04,-0.73,4.25),
                     (-0.21,0.52,0.83)]

# p.camera_position = [(32.82,3.06,16.95),
#                      (6.04,-0.73,4.25),
#                      (-0.43,0.00,0.90)]

p.set_scale(zscale=VE)
p.add_key_event("p", my_cpos_callback)
p.save_graphic("SCBG_volume_validation_V2a.pdf")
p.show()


#%% PYVISTA PLOT SCATTER
import pygimli.meshtools as mt
import pygimli as pg
from scipy.interpolate import RegularGridInterpolator
import pyvista as pv



depths_2_make = np.unique(allDepths)
depths_2_make = np.array([0.1,0.2,0.3,0.4])
depths_2_make = np.arange(0.05,1.0,0.02)

dz_pyvista = 0.005
d0 = 0.305
ind = np.where(allDepths==d0)
inner_center = treeCenter
inner_r = 1
inner_r_nSegments = 10
triSize = 0.05
model_r = 14
model_r_nSegments = 100

# inner = mt.createCircle(
#     pos=inner_center,
#     radius=inner_r,
#     marker=1,
#     boundaryMarker=1,
#     nSegments=inner_r_nSegments,
#     area=triSize * 30.0,
# )
# modArea = mt.createCircle(
#     pos=inner_center,
#     radius=model_r,
#     marker=2,
#     boundaryMarker=2,
#     nSegments=model_r_nSegments,
#     area=triSize)
rect = mt.createRectangle(start=[-5, -9.7], end=[-0.6, -1.5],
                          nSegments=inner_r_nSegments,
                          area=triSize)  
geom = rect #inner + modArea 
mesh_2d = mt.createMesh(geom)
pg.show(mesh_2d)
#%%
cc = mesh_2d.cellCenters()

print("***** Extruding 2D Mesh *****")
mesh_3d = pg.meshtools.extrudeMesh(mesh_2d, a=-depths_2_make)
print(mesh_3d)
print("***** Finished Extruding 2D Mesh *****")
mesh_3d.exportVTK('3dMesh.vtk')
#%%
cc_3d = mesh_3d.cellCenters()
depths_2_make_mids = np.sort(-np.unique(cc_3d[:,2]))
amps_3d = np.zeros(cc_3d.shape[0])  

dx_dy = 0.3
bounds = [-14,-14,14,14]
bin_x = np.arange(bounds[0], bounds[2], dx_dy)
bin_y = np.arange(bounds[1], bounds[3], dx_dy)
bin_x_mid = (bin_x[1:] + bin_x[:-1]) / 2.0
bin_y_mid = (bin_y[1:] + bin_y[:-1]) / 2.0

for i in range(1,len(depths_2_make)):
    d0 = depths_2_make[i]
    e,n,th,r,a = allGPRData.getDepthSection(d0, avgWindow, powerVal, 0)
    n += 1.2
    ret = stats.binned_statistic_2d(e, n, a, statistic="max", bins=[bin_x, bin_y])
    tmp = ret[0]
    # fill gaps with global median
    tmp[np.isnan(tmp)] = 0 #np.median(a)
    print(tmp.shape,bin_x_mid.shape,bin_y_mid.shape)
    u = RegularGridInterpolator(
        (bin_x_mid, bin_y_mid),
        tmp,
        bounds_error=False,
        fill_value=np.median(tmp.flatten()),
        method='cubic'
    )
    vals = u(cc[:,:2])
    ind_replace = np.where(np.abs(cc_3d[:,2]+depths_2_make_mids[i-1])<0.001)[0]
    amps_3d[ind_replace] =  u(cc[:,:2])
    #pg.show(mesh_2d,vals,cMin=vMin, cMax=vMax,cmap='cubehelix_r',colorBar=True)
    print(i,'of',len(depths_2_make))
    
amp_nodes = pg.meshtools.cellDataToNodeData(mesh_3d, amps_3d)

#%%
grid = pv.read('3dMesh.vtk')
grid['Amplitude'] = amp_nodes

x_picks_gray = np.cos(picks_rad[:,0])*picks_rad[:,1]
y_picks_gray = np.sin(picks_rad[:,0])*picks_rad[:,1]
z_picks_gray = np.zeros(len(x_picks_gray))-0.05
points = np.column_stack([x_picks_gray,y_picks_gray,z_picks_gray])
spline = pv.Spline(points, n_points=15)

contours = grid.contour([8], scalars='Amplitude')
contours2 = grid.contour([4], scalars='Amplitude')
single_slice = grid.slice(normal=[0, 1, 0])


splinePath = grid.slice_along_line(spline)
p = pv.Plotter()

p.add_mesh(contours, scalars='Amplitude', cmap='cubehelix_r', clim=[vMin,vMax],
         opacity=0.8, show_scalar_bar=False)
p.add_mesh(contours2, scalars='Amplitude', cmap='cubehelix_r', clim=[vMin,vMax],
         opacity=0.1, show_scalar_bar=False)
p.add_mesh(splinePath, scalars='Amplitude', cmap='cubehelix_r', clim=[vMin,vMax], 
           show_scalar_bar=True,lighting=False)
# p.show_grid(xlabel='X (m)', 
#             ylabel='Y (m)',
#             n_xlabels=10)
p.set_scale(zscale=3)
p.show()

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # pg.show(mesh_2d,vals,ax=ax,cMap='cubehelix_r',clim=[0,8])
    

    # d0 = depths4Vid[i-1]
    # df = depths4Vid[i]
    # print(d0,df)
    # fileName = path + 'DepthSection_' + str(np.round(d0,2)) + 'to' + str(np.round(df,2)) + '_.png'    
    # ind2Keep = np.where(np.logical_and(allDepths>d0,allDepths<=df))[0]
    
    # avgAmp = allAmps[ind2Keep]
    # avgDepth = allDepths[ind2Keep]
    # avgTheta = allThetas[ind2Keep]
    # avgRadius = allRadii[ind2Keep]
    # avgEast = allEast[ind2Keep]
    # avgNorth = allNorth[ind2Keep]
    


#ax.scatter(east,north,c=amp,s=1,cmap='cubehelix_r',vmin=0,vmax=10)









    
        