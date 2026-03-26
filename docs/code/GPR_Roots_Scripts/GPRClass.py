#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:23:08 2024

@author: bflinch
"""
import pandas as pd
import numpy as np
from scipy import signal
import gprpy.gprpy as gp
import pickle
from osgeo import gdal


def getDataFromGeoTiff(fileName):
    """
    DEPENDINCIES: 
        GDAL: from osgeo import gdal
        NUMPY: import numpy as np
    Parameters
    ----------
    fileName : String
        This is the name of the geoTiff file. It requries the file path
        unless the geoTiff is in the current working directory.

    Returns
    -------
    easting : nx1 Array
        An array containing the easting values for the geoTiff file
        it could also be the longitude if the geotiff was in lat long.
    northing : mx1
        An array containing the northing values for the geoTiff file
        it could also be the lattitude if the geotiff was in lat long.
    elev : mxn Array
        This is a matrix that contains all of the elevations (or info) from
        band 1 in the geotiff file.
    """
    #1. Read the geotiff file
    gtif = gdal.Open(fileName) #gtif = gdal object with properties and methods
    band = gtif.GetRasterBand(1) #band = gdal object with properties and methods
    elev = band.ReadAsArray() #Extract the elev values (or values in band 1) this is an mxn array
    nrows,ncols = elev.shape #Get the number of rows and columns from elev
    
    #Get key coordinates from geotiff-- specifically the lower left corner
    #x0 = easting/longitude of lower left corner
    #dx = grid spacing in x-direction
    #dxdy = 0 not used but required by the method--probably a relationship beteween band 1 and band 2
    #y0 = northing/lattitude of lower left corner
    #dydx = 0 not used
    #dy = grid spacing in y-direction
    x0, dx, dxdy, y0, dydx, dy = gtif.GetGeoTransform()
    
    #Calculate the coordinates of the upper left (UL) corner using the dx and number of grid points in geotiff
    easting_UL = x0 + dx * ncols
    northing_UL = y0 + dy * nrows


    #Create the easting/longitude and norhting/lattitude vectors to return
    easting = np.linspace(x0,easting_UL,num=ncols)
    northing = np.linspace(y0,northing_UL,num=nrows)
    
    return easting,northing,elev

class treeGPRStructure:    
    def __init__(self):
        self.nLines = 0
        self.fileNames = []
        self.fileNumbers = []
        self.SoLs = []
        self.EoLs = []
        self.sectionNumbers = []
        self.saveDir = ''
        self.hilbertNormAmps = []
        self.locationDataFrame = None

        
        
        self.envelope = []
        self.gpr_xPos = []
        self.processedData_preMig = []
        self.processedData_postMig = []
        self.gpr_eastings = []
        self.gpr_northings = []
        self.gpr_twtts = []
        self.gpr_lineNumbers = []
        self.gpr_depths = []
        self.gpr_E =[]
        self.gpr_N = []
        self.gpr_theta_deg = []
        self.gpr_r = []

    def initalizeData(self,file,tree_loc):
        data = pd.read_csv(file)
        self.locationDataFrame = data
        self.nLines = data.shape[0]
        for i in range(0,data.shape[0]):   
            self.addData(self.sectionNumbers,data.loc[i,'Section']) 
            self.addData(self.gpr_lineNumbers,data.loc[i,'Line'])
            self.addData(self.fileNumbers,i) 
            self.addData(self.fileNames,data.loc[i,'File Name']) 
            EoL = [data.loc[i,'end_x'],data.loc[i,'end_y']]
            SoL = [data.loc[i,'start_x'],data.loc[i,'start_y']]
            self.addData(self.SoLs,SoL)
            self.addData(self.EoLs,EoL)
            self.tree_loc = tree_loc
            
    def setProcessingParms(self,saveDir,deWowVal,meanTraceVal,hpVal,lpVal,filtOrder,gprVel):
        self.deWowVal = deWowVal
        self.meanTraceVal = meanTraceVal
        self.hpVal = hpVal
        self.lpVal = lpVal
        self.filtOrder = filtOrder
        self.gprVel = gprVel
        self.saveDir = saveDir
    
    def addData(self,prop,array):
        prop = prop.append(array)
    
    def hilbertTransformData(self,data):
        env = 0*data
        data = np.nan_to_num(data)
        for i in range(0,data.shape[1]):
            analytic_signal = signal.hilbert(data[:,i])
            env[:,i] = np.abs(analytic_signal)
        return env   
    
    def projectCoordinates(self,SoL,EoL,x):
        dx = EoL[0]-SoL[0]
        dy = EoL[1]-SoL[1]
        mag = np.sqrt(dx**2+dy**2)
        ux = dx/mag
        uy = dy/mag
        
        rot_x = x*ux + SoL[0]
        rot_y = x*uy + SoL[1]
        return rot_x, rot_y
        
    def bpData(self,data, lf, hf, nq, order):
        """
        Applies a band-pass filter to each trace (column in 2d array)
        Inputs
        data = a numpy array that is nt x ns (nt = time samples, ns = number of recievers)
        lf = lower corner frequency (Hz)
        hf = upper corner frequency (Hz)
        nq = nyquist frequency (1/2*dt)
        order = order of the bp filter (required for sp.signal.butter)
        
        Outputs: 
        fData = a filtered (along columns) numpy array that is nt x ns (nt = time samples, ns = number of recievers)
        """
        wl = lf / nq
        wh = hf / nq
        b, a = signal.butter(order, [wl, wh], btype="bandpass")
        print(b,a)
        fData = data * 0
        for i in range(0, data.shape[1]):
            fData[:, i] = signal.filtfilt(b, a, data[:, i],axis=0)

        return fData
    
    def read_gprPy_ProcessedData(self,fileNumber):
        fileName = self.saveDir + self.fileNames[fileNumber].split('/')[-2]+'_'+self.fileNames[fileNumber].split('/')[-1] + '.processed'

        f = open(fileName, 'rb')
        tmpData = pickle.load(f)
        f.close()
        #saveData = [xPos,twtt,depths,preMigData,migData,env]
        self.addData(self.gpr_xPos,tmpData[0])
        self.addData(self.gpr_twtts,tmpData[1])
        self.addData(self.gpr_depths, tmpData[2])
        self.addData(self.processedData_preMig,tmpData[3])
        self.addData(self.processedData_postMig,tmpData[4])
        self.addData(self.envelope,tmpData[5])
        
        
    def gprPyProcess(self,fileNumber,z0,zf,dz):
        
        deWowVal = self.deWowVal
        meanTraceVal = self.meanTraceVal
        hpVal = self.hpVal
        lpVal = self.lpVal
        filtOrder = self.filtOrder
        gprVel = self.gprVel
     
        mygpr = gp.gprpyProfile()
        mygpr.importdata(self.fileNames[fileNumber])
        mygpr.dewow(deWowVal)
        mygpr.remMeanTrace(meanTraceVal)
        dt = mygpr.twtt[1] - mygpr.twtt[0]
        mygpr.data = self.bpData(mygpr.data, lpVal*1e6, hpVal*1e6, 1/(2*dt*1e-9), filtOrder)      
        mygpr.setVelocity(gprVel)
        preMigData = np.copy(mygpr.data)
        mygpr.fkMigration()
        migData = np.copy(mygpr.data)
        env = self.hilbertTransformData(migData)
        xPos = mygpr.profilePos
        twtt = mygpr.twtt
        
        depths = mygpr.depth 
        
        
        
        #INTERPOLATE TO THE SAME DEPTHS
        newDepths = np.arange(z0,zf,dz)
        interpMigData = np.zeros([len(newDepths),migData.shape[1]])
        interpPreMigData = np.zeros([len(newDepths),migData.shape[1]])
        interpENV = np.zeros([len(newDepths),migData.shape[1]])
        for i in range(0,migData.shape[1]):
            interpMigData[:,i] = np.interp(newDepths,depths,migData[:,i])
            interpPreMigData[:,i] = np.interp(newDepths,depths,preMigData[:,i])
            interpENV[:,i] = np.interp(newDepths,depths,env[:,i])
            
        
        #ADD DATA TO STRUCTURE
        self.addData(self.gpr_depths, newDepths)
        self.addData(self.gpr_xPos,xPos)
        self.addData(self.processedData_preMig,interpPreMigData)
        self.addData(self.processedData_postMig,interpMigData)
        self.addData(self.envelope,interpENV)
        self.addData(self.gpr_twtts,twtt)
        print(interpENV.shape,env.shape)
        saveData = [xPos,twtt,newDepths,interpPreMigData,interpMigData,interpENV]
        saveFileName = self.saveDir + self.fileNames[fileNumber].split('/')[-2]+'_'+self.fileNames[fileNumber].split('/')[-1] + '.processed'
        f = open(saveFileName, 'wb')
        pickle.dump(saveData, f)
        f.close()
        

    
    def spatiallyLocateProfiles(self):
        for i in range(0,self.nLines):
            x = self.gpr_xPos[i]
            SoL = self.SoLs[i]
            EoL = self.EoLs[i]
            theoreticalDist = ((EoL[0]-SoL[0])**2+(EoL[1]-SoL[1])**2)**0.5
            measuredDist = np.max(x)
            diff = theoreticalDist - measuredDist
            #print(diff)
            x = x + diff/2
            rot_x,rot_y = self.projectCoordinates(SoL,EoL,x)
            self.addData(self.gpr_E,rot_x)
            self.addData(self.gpr_N,rot_y)

    def processGPR_all(self,z0,zf,dz):
        for i in range(0,self.nLines):
            self.gprPyProcess(i,z0,zf,dz)
            
    def readProcessedGPR_all(self,):
        for i in range(0,self.nLines):                
            self.read_gprPy_ProcessedData(i)
   
    def getNormalizngEnvAmplitudes(self,indexValues,envFunction):
        """
        envFunction = 1 for mean
        envFunction = 2 for max
        envFunction = 3 for median

        """
        print(len(indexValues))
        index = indexValues[0]
        allEnv = self.envelope[index]
        for i in range(1,len(indexValues)):
            index = indexValues[i]
            allEnv = np.concatenate((allEnv,self.envelope[index]),1)
                
        if envFunction == 2:
            envAmps = np.max(allEnv,axis=1)
        elif envFunction == 3:
            envAmps = np.median(allEnv,axis=1)
        else:
            envAmps = np.mean(allEnv,axis=1)
        return envAmps
    
    def readEnvNormVals(self):
        fileName = self.saveDir + 'hilbert_amplitudes.pckl'
        f = open(fileName, 'rb')
        tmpData = pickle.load(f)
        f.close()
        self.hilbertNormAmps = tmpData
        
    def getEnvNormVals(self,envFunction):
        print('Section 1 (Hard Coded)')
        sectionNumbers = np.array(self.sectionNumbers)
        indexValues = np.where(sectionNumbers<=4)[0]
        normVals_sec1 = self.getNormalizngEnvAmplitudes(indexValues,envFunction)
        self.addData(self.hilbertNormAmps,normVals_sec1)
        
        print('Section 2 (Hard Coded)')
        indexValues = np.where(np.logical_and(sectionNumbers>4,sectionNumbers<=8))[0]
        normVals_sec2 = self.getNormalizngEnvAmplitudes(indexValues,envFunction)
        self.addData(self.hilbertNormAmps,normVals_sec2)
        
        print('Section 3 (Hard Coded)')
        indexValues = np.where(np.logical_and(sectionNumbers>8,sectionNumbers<=12))[0]
        normVals_sec3 = self.getNormalizngEnvAmplitudes(indexValues,envFunction)
        self.addData(self.hilbertNormAmps,normVals_sec3)
        
        print('Section 4 (Hard Coded)')
        indexValues = np.where(sectionNumbers>12)[0]
        normVals_sec4 = self.getNormalizngEnvAmplitudes(indexValues,envFunction)
        self.addData(self.hilbertNormAmps,normVals_sec4)
        
        saveFileName = self.saveDir + 'hilbert_amplitudes.pckl'
        f = open(saveFileName, 'wb')
        pickle.dump(self.hilbertNormAmps, f)
        f.close()
        
    def calcRadialCoordinates(self):
        for i in range(0,self.nLines):
            eastings =  self.gpr_E[i] - self.tree_loc[0] 
            northings = self.gpr_N[i] - self.tree_loc[1]
            r = (eastings**2 + northings**2)**0.5
            theta = np.arctan2(northings,eastings)*180/np.pi
            theta[theta<0] = 360 + theta[theta<0]
            self.addData(self.gpr_r,r)
            self.addData(self.gpr_theta_deg,theta)

            

    def getDepthSection(self,depth,avgWindow,powerVal,thresh):
        #normVals = (self.hilbertNormAmps[0]+self.hilbertNormAmps[1])/2
        ePoints = np.array([])
        nPoints = np.array([])
        amplitudes = np.array([])
        thetaPoints = np.array([])
        rPoints = np.array([])
        depth_index = np.argmin((self.gpr_depths[0]-depth)**2)
        
        for i in range(0,self.nLines):
            if self.sectionNumbers[i] <=4:
                normVals = self.hilbertNormAmps[0]
            elif self.sectionNumbers[i] >4 and self.sectionNumbers[i] <= 8:
                normVals = self.hilbertNormAmps[1]
            elif self.sectionNumbers[i] >8 and self.sectionNumbers[i] <= 12:
                normVals = self.hilbertNormAmps[2]
            else:
                normVals = self.hilbertNormAmps[3]
             
            #AVERGE EVERYTHING
            #normVals = (self.hilbertNormAmps[0]+self.hilbertNormAmps[1]+self.hilbertNormAmps[2]+self.hilbertNormAmps[3])/4
            
            #Get data Trace normalized!
            #tmpData = (self.envelope[i]/np.expand_dims(normVals, 1))**powerVal
            col_vec = normVals[:,None]
            tmpData = ((self.envelope[i]-col_vec)/np.expand_dims(normVals, 1))**powerVal
            #print(i,'of',nFiles)
      
            #DO VERTICAL AVERAGING
            startInd = depth_index - avgWindow//2
            endInd = depth_index + avgWindow//2
            tmpData = np.mean(tmpData[startInd:endInd,:],axis=0) 

            
            ePoints = np.append(ePoints,self.gpr_E[i])
            nPoints = np.append(nPoints,self.gpr_N[i])
            thetaPoints = np.append(thetaPoints,self.gpr_theta_deg[i])
            rPoints = np.append(rPoints,self.gpr_r[i])
            amplitudes = np.append(amplitudes,tmpData)
            
        #Filter out lower thresholds for less points
        ampFiltInd = np.where(amplitudes>thresh)[0]
        amplitudes = amplitudes[ampFiltInd]
        ePoints = ePoints[ampFiltInd]
        nPoints = nPoints[ampFiltInd]
        thetaPoints = thetaPoints[ampFiltInd]
        rPoints = rPoints[ampFiltInd]
        
        #sort so scatter plots the highest amplitudes on top
        newSortOrder = np.argsort(amplitudes)
        amplitudes = amplitudes[newSortOrder]
        ePoints = ePoints[newSortOrder]
        nPoints = nPoints[newSortOrder]
        thetaPoints = thetaPoints[newSortOrder]
        rPoints = rPoints[newSortOrder]

            
        return ePoints,nPoints,thetaPoints,rPoints,amplitudes
        


    def getRadialProfile_byLine(self,lineNumber,powerVal):
        df = self.locationDataFrame
        lines2Plot = df.loc[(df['Line'] == lineNumber)] 

        circum_noMig = np.array([])
        circum_mig = np.array([])
        circum_ENV = np.array([])

        full_dist = np.array([])
        full_theta = np.array([])
        full_r = np.array([])

        for i in range(0,lines2Plot.shape[0]):
            index = lines2Plot.index[i]
            section = lines2Plot['Section'].iloc[i]
            
            if section <=4:
                normVals = self.hilbertNormAmps[0]
            elif section >4 and section <= 8:
                normVals = self.hilbertNormAmps[1]
            elif section >8 and section <= 12:
                normVals = self.hilbertNormAmps[2]
            else:
                normVals = self.hilbertNormAmps[3]
                
            col_vec = normVals[:,None]
            
            if i > 0:
                full_dist = np.append(full_dist,self.gpr_xPos[index]+full_dist[-1])
                full_theta = np.append(full_theta,self.gpr_theta_deg[index])
                full_r = np.append(full_r,self.gpr_r[index])

                circum_noMig = np.column_stack((circum_noMig,self.processedData_preMig[index]/np.expand_dims(normVals, 1)))
                circum_mig = np.column_stack((circum_mig,self.processedData_postMig[index]/np.expand_dims(normVals, 1)))
                circum_ENV = np.column_stack((circum_ENV,(self.envelope[index]-col_vec)/np.expand_dims(normVals, 1)))

            else:
                full_dist = self.gpr_xPos[index]
                full_r = self.gpr_r[index]
                full_theta = self.gpr_theta_deg[index]
                circum_noMig = self.processedData_preMig[index]/np.expand_dims(normVals, 1)
                circum_mig = self.processedData_postMig[index]/np.expand_dims(normVals, 1)
                circum_ENV = (self.envelope[index]-col_vec)/np.expand_dims(normVals, 1)

     
        full_dist = np.linspace(0,np.max(full_dist),len(full_dist))
        print(full_r.shape,full_dist.shape,full_theta.shape,circum_noMig.shape)
        sortInd = np.argsort(full_theta)
        full_theta = full_theta[sortInd]
        full_r = full_r[sortInd]

        circum_mig = circum_mig[:,sortInd]
        circum_noMig = circum_noMig[:,sortInd]
        circum_ENV = circum_ENV[:,sortInd]**powerVal

        return full_dist,full_theta,full_r,circum_noMig,circum_mig,circum_ENV
    
    
   
    def calculate_smoothed_spline(self,x, y,nSamples):
        from scipy.interpolate import splev, splrep
        path_t = np.linspace(0,1,x.size)
        r = np.vstack((x.reshape((1,x.size)),y.reshape((1,y.size))))
        t = np.linspace(np.min(path_t),np.max(path_t),nSamples)
        spline = splrep(path_t, r[0,:],k=3)
        spline2 = splrep(path_t, r[1,:],k=3)
        x1 = splev(t,spline)
        x2 = splev(t,spline2)
        return x1,x2
    
    def getAllLocs(self):
        e = np.array([])
        n = np.array([])
        ln = np.array([])
        tr = np.array([])
        r = np.array([])
        theta = np.array([])
        for i in range(0,len(self.gpr_E)):
            e = np.append(e,self.gpr_E[i])
            n = np.append(n,self.gpr_N[i])
            r = np.append(r,self.gpr_r[i])
            theta = np.append(theta,self.gpr_theta_deg[i])

            ln = np.append(ln,self.fileNumbers[i]*np.ones(len(self.gpr_E[i])))
            tr = np.append(tr,np.arange(0,len(self.gpr_E[i]),1))
        
        self.all_lines = ln
        self.all_traces = tr
        self.all_e = e
        self.all_n = n
        self.all_r = r
        self.all_theta = theta
        
    def getRadialProfile(self,picks_rad,N,tol,powerVal):
        
        thetaPicks = np.zeros(len(picks_rad))
        rPicks = np.zeros(len(picks_rad))
        xPicks = np.zeros(len(picks_rad))
        yPicks = np.zeros(len(picks_rad))
        for i in range(0,len(picks_rad)):
            thetaPicks[i] = picks_rad[i][0]
            rPicks[i] = picks_rad[i][1]
            xPicks[i] = rPicks[i]*np.cos(thetaPicks[i])# + tree_center[0]
            yPicks[i] = rPicks[i]*np.sin(thetaPicks[i])# + tree_center[1]
        xPicks = np.flip(xPicks)
        yPicks = np.flip(yPicks)
        
        xInt,yInt = self.calculate_smoothed_spline(xPicks,yPicks,N)
        rInt = np.sqrt(xInt**2+yInt**2)
        thetaInt = np.arctan2(yInt,xInt)
    
        
        XX = np.array([])
        DD = np.array([])
        ENV = np.array([])
        MIG = np.array([])
        TH = np.array([])
        index = 0
        for i in range(0,len(thetaInt)):
            tmp = self.getNearestProfile_polar(rInt[i],thetaInt[i],tol,powerVal)
            #print(rInt[i],thetaInt[i],len(tmp))
            if len(tmp)>2:
                
                #ax.scatter(thetaInt[i],rInt[i],s=20,c='k')
                
                if index == 0:
                    XX = rInt[i]*np.ones(self.gpr_depths[0].shape[0])
                    DD = self.gpr_depths[0]
                    ENV = tmp[2]
                    MIG = tmp[3]
                    TH = thetaInt[i]*np.ones(self.gpr_depths[0].shape[0])
    
                    index +=1
                else:
                    XX = np.column_stack([XX,rInt[i]*np.ones(self.gpr_depths[0].shape[0])])
                    TH = np.column_stack([TH,thetaInt[i]*np.ones(self.gpr_depths[0].shape[0])])

                    DD = np.column_stack([DD,self.gpr_depths[0]])
                    ENV = np.column_stack([ENV,tmp[2]])
                    MIG = np.column_stack([MIG,tmp[3]])
    
                    index +=1
                    # positiveFill = np.copy(filteredValues[i][4])               
        return XX,DD,TH,ENV,MIG
    
    
    def getNearestProfile_polar(self,r,theta,tol,powerVal):
        if theta < 0:
            theta = 2*np.pi+theta
        ln = self.all_lines
        tr = self.all_traces
        ind = np.argmin(((self.all_theta*np.pi/180-theta)**2+(self.all_r-r)**2)**0.5)
        residual = np.min(((self.all_theta*np.pi/180-theta)**2+(self.all_r-r)**2)**0.5)
        if residual <= tol:
            lineNumber = ln[ind].astype(int)
            traceNumber = tr[ind].astype(int)
            radius = self.all_r[ind] #self.gpr_r[lineNumber][traceNumber]
            angle_rad = self.all_theta[ind]*np.pi/180 #self.gpr_theta_deg[lineNumber]
            
            section = self.sectionNumbers[lineNumber]
            #print(section)
            if section <=4:
                normVals = self.hilbertNormAmps[0]
            elif section >4 and section <= 8:
                normVals = self.hilbertNormAmps[1]
            elif section >8 and section <= 12:
                normVals = self.hilbertNormAmps[2]
            else:
                normVals = self.hilbertNormAmps[3]
                
            profile_env = (self.envelope[lineNumber][:,traceNumber]/normVals)**powerVal
            #self.envelope[lineNumber][:,traceNumber]/normVals
            profile_postMig = (self.processedData_postMig[lineNumber][:,traceNumber]/normVals)
            return radius,angle_rad,profile_env,profile_postMig,residual
        else:
            'Nothing in Tolerance'
            return 0,0
            
    
    
    
    
    
    
    
    
    
    
    
        
        
        
