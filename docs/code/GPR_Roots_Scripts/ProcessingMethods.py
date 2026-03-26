#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:23:08 2024

@author: bflinch
"""

from osgeo import gdal
import numpy as np
from scipy import interpolate
import pandas as pd


def getDataFromGeoTiff(fileName):
    """
    Reads a GeoTIFF file and extracts coordinate data and elevation values.
    
    Dependencies:
        - GDAL: from osgeo import gdal
        - NumPy: import numpy as np
    
    Parameters
    ----------
    fileName : str
        Path to the GeoTIFF file.
    
    Returns
    -------
    easting : np.ndarray
        1D array of easting (or longitude) values.
    northing : np.ndarray
        1D array of northing (or latitude) values.
    elev : np.ndarray
        2D array (matrix) of elevation values from band 1 of the GeoTIFF.
    """
    # Open the GeoTIFF file
    gtif = gdal.Open(fileName)
    band = gtif.GetRasterBand(1)  # Extract the first band (elevation data)
    elev = band.ReadAsArray()  # Convert band data to a NumPy array
    nrows, ncols = elev.shape  # Get the dimensions of the elevation matrix
    
    # Extract geospatial transformation parameters
    x0, dx, _, y0, _, dy = gtif.GetGeoTransform()
    
    # Compute upper-left corner coordinates
    easting_UL = x0 + dx * ncols
    northing_UL = y0 + dy * nrows
    
    # Generate coordinate vectors for easting and northing
    easting = np.linspace(x0, easting_UL, num=ncols)
    northing = np.linspace(y0, northing_UL, num=nrows)
    
    return easting, northing, elev
            
def read_total_station_output(file):
    """
    Reads total station survey output and extracts grid point coordinates.
    
    Parameters
    ----------
    file : str
        Path to the CSV file containing total station data.
    
    Returns
    -------
    xGrid : np.ndarray
        X-coordinates of grid points.
    yGrid : np.ndarray
        Y-coordinates of grid points.
    zGrid : np.ndarray
        Z-coordinates (elevation) of grid points.
    """
    totalStation_df = pd.read_csv(file)  # Load CSV file into DataFrame
    ind = totalStation_df['name'].str.startswith('GRID')  # Filter rows containing 'GRID'
    
    # Extract coordinate data and convert to NumPy arrays
    xGrid = totalStation_df['x'][ind].to_numpy()
    yGrid = totalStation_df['y'][ind].to_numpy()
    zGrid = totalStation_df['z'][ind].to_numpy()
    
    return xGrid, yGrid, zGrid
    
    
def calcUnitVector(SoL, EoL):
    """
    Computes a unit vector and magnitude between two points.
    
    Parameters
    ----------
    SoL : list or tuple
        Coordinates [x, y] of the start location.
    EoL : list or tuple
        Coordinates [x, y] of the end location.
    
    Returns
    -------
    ux : float
        X-component of the unit vector.
    uy : float
        Y-component of the unit vector.
    mag : float
        Magnitude (distance) between the two points.
    """
    dx = EoL[0] - SoL[0]  # Difference in x-coordinates
    dy = EoL[1] - SoL[1]  # Difference in y-coordinates
    mag = (dx**2 + dy**2)**0.5  # Compute Euclidean distance
    ux = dx / mag  # Compute x-component of unit vector
    uy = dy / mag  # Compute y-component of unit vector
    return ux, uy, mag


def calcLoc(SoL, EoL, dist, tree_center):
    """
    Calculates a new location along a line segment and computes polar coordinates relative to a reference point.
    
    Parameters
    ----------
    SoL : list or tuple
        Start location [x, y].
    EoL : list or tuple
        End location [x, y].
    dist : float
        Distance along the line from the start location.
    tree_center : list or tuple
        Reference point [x, y] for computing polar coordinates.
    
    Returns
    -------
    r : float
        Radial distance from tree_center to the new location.
    theta : float
        Angle (in degrees) from the reference point to the new location.
    e : float
        X-coordinate of the new location.
    n : float
        Y-coordinate of the new location.
    """
    ux, uy, mag = calcUnitVector(SoL, EoL)  # Get unit vector and magnitude
    
    # Compute new location coordinates
    e = ux * dist + SoL[0]
    n = uy * dist + SoL[1]
    
    # Compute relative position to reference point
    tmpdx = e - tree_center[0]
    tmpdy = n - tree_center[1]
    
    # Compute angle in degrees
    theta = np.arctan2(tmpdy, tmpdx) * 180 / np.pi
    
    # Compute radial distance
    r = (tmpdx**2 + tmpdy**2) ** 0.5
    
    return r, theta, e, n
    
    
    
    
    
    
    
    
    
    
        
        
        
