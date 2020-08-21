# -*- coding: utf-8 -*-
"""
Isolating Events Visualization Algorithm

red = P wave
yellow = S wave
blue = rest of the wave
The end of each color is the point of the wave
"""

from obspy import read
import numpy as np
import matplotlib.pyplot as plt
import math
from obspy.signal.trigger import pk_baer
from obspy.signal.trigger import ar_pick

import os
import fnmatch



# Call AMD Data
stationname = [] #empty list to get all the AMD station names

 #os filter finding all AMD files
listOfFiles = os.listdir('your_file_name')
pattern = '*.AMD.EHZ*' #EHZ channel is the vertical movement of the seismogram
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern):
        stationname = stationname + [entry]
    stationname.sort() #this sort function starts with the May 1st


PermanentRoot = 'D:/your/path'  #Change this to your root

# Read file and create stream object
st = read(PermanentRoot+stationname[0])

# Define first trace as new variable
tr = st[0] #Trace gives the plotting data

# Set trace data as new variable
trdata = tr.data  # Using this as trdata(xx:xx) will give corresponding Y-Values
tr.plot() # plots given data
print('\n')

Yarray = [] 
Xarray = []

# this finds all points that go above 200 
for i in range (trdata.size):
    if trdata[i] > 200:
        Yarray = Yarray + [trdata[i]]
        Xarray = Xarray + [i]        
        
#============================================================================
#this collects all the data points into seperate lists 
figNumber = 0

for i in range (len(Xarray)):
    isox = [] # isox stands for isolated x-values 
    figNumber += 1 #used for figure numbers   
    n = 0  
        
    while Xarray[n+1] - Xarray[n] < 4000:     

        isox = isox + [Xarray[n]]
        n = n+1
        
        if n+1 >= len(Xarray):
             break
         
            
    if len(isox) > 0:
#==========================================================================================================================       
    #Finding maxes from each event waveform to distinguish P and S
          startwave = isox[0] - 10000 #start of graph
          endwave = isox[len(isox)-1] + 20000  #end of graph
          
          waveform = trdata[startwave:endwave]
          diff = endwave - startwave
          graphSection = math.floor(diff/500) #break down the wave graph into different sections
          allmax = []
          maxloc = []
          for i in range (graphSection):
                  startIteration = (startwave+(i*500))
                  endIteration = startIteration+500
                  if startIteration > 8640000:
                      continue
                  elif endIteration > 8640000:
                      continue
                  waveIteration = np.max(trdata[startIteration:endIteration]) 
                  iterationLoc = np.argmax(trdata[startIteration:endIteration])
                  allmax = allmax + [waveIteration] # finding the maxes of each section
                  maxloc = maxloc + [startIteration+iterationLoc]
          
          # finding the maxes of the section maxes from "allmax" 
          realmax = []
          realmaxloc = []
          for i in range (len(allmax)):
              leftmax = allmax[0+i]
              midmax = allmax[i+1]
              rightmax = allmax[i+2]
              if (midmax > leftmax and midmax > rightmax):  
                   realmax = realmax + [midmax] 
                   realmaxloc = realmaxloc + [maxloc[i+1]]
              if i+4 > len(allmax):
                    break      
          
          #Finding S-wave Amplitude  
          pswaves = []
          pstimes = []
          for i in range (2):
             max1 = np.max(realmax)
             maxtimeloc = np.argmax(realmax)
             for i in range (len(realmax)-1):
                 if max1 == realmax[i]:
                     if len(pswaves) == 2:
                         break
                     pswaves = pswaves + [max1]
                     pstimes = pstimes + [realmaxloc[maxtimeloc]]
                     del realmax[i]
                     del realmaxloc[i]      
          
          for i in range (2):
              if len(pstimes) <= 1:
                  continue
              if pstimes[1] - pstimes[0] > 0:
                  Samp = pswaves[0]

              else :
                  Samp = pswaves[1]
  
                  
# ------------------------------------------------------------------------------------------------------------------------                 
          df = tr.stats.sampling_rate
          BAp_pick, phase_info = pk_baer(tr.data[startwave:endwave], df,
                               20, 60, 7.0, 12.0, 100, 100)

          df = tr.stats.sampling_rate
          ARp_pick, S_pick = ar_pick(tr.data[startwave:endwave], tr.data[startwave:endwave], tr.data[startwave:endwave],df,
                             1.0, 20.0, 1.0, 0.1, 4.0, 1.0, 2, 8, 0.1, 0.2, s_pick=True )
          
          Bap = int((startwave + BAp_pick))
          Arp = int((startwave) + (ARp_pick*100))
          Pwave = round((Bap+Arp)/2)
          Swave = int((startwave) + (S_pick*100))
          # P-wave Amplitude
          Pamp = abs(trdata[Arp]) 

      
          plt.figure(figNumber)
          plt.plot(trdata[startwave:endwave],'b',trdata[startwave:Swave],'y',trdata[startwave:Pwave],'r')

          plt.xlabel('Centiseconds of Event ')
          plt.ylabel('Count')
          EventName = "Event " + str(figNumber)
          plt.title(EventName)  
          
          print('\t\t'+ EventName)
          print('----------------------------------------------------------')
          print('P-Wave Amp \t S-Wave Amp')
          print('  {0:.1f} \t\t {1:.1f}\n'.format(Pamp,Samp))
    
    del Xarray[0:n+1]
    if len(Xarray) == 0:
        break         
    
