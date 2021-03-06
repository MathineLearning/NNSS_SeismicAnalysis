# SeismicAnalysis_NeuralNetwork_NNSS
***DISCLAIMER: This was a student lead project attempting to solve a research problem provided by the Nevada National Security Site (NNSS). This does not provide a full proof analysis and should only be used to demonstrate the coding ability of the team. 

*** the data used was to big to upload. 

# Objective
Provide a method of differentiating natural seismic events from non-natural seismic events. Natural seismic events would be any kind of earthquake. A non-natural seismic event could be anything from mining demolitions to nuclear weapons tests. The purpose of the project would be to identify if big/nuclear weapons testing is occuring around the world and if possible to identify the location of these tests. However, this project attempts to just identify if the events are natural or non-natural. The main toolbox used was Obspy

# What is Included
- Isolating Events Visualization Algorithm
    - A visual algorithm isolating the events of one day and analyzing each anomaly for P and S waves. P waves, primary waves, that arrive first and S waves, secondary waves, arrive second

- Writing Isolated Events to Spreadsheet Algorithm
    - An algorithm, very similar to the Isolating Events Visualization Algorithm, that takes each anomaly and writes it to an excel spreadsheet instead of visualizing it.

- A script that takes each spreadsheet and combines the anomalies into one spreadsheet

- Neural Network code in R


# Isolating Events Visualization Algorithm
This script allows you to view the plots of the whole day and any anomalies that the  algorithm detects. This was developed using Anaconda and Spyder, therefore using this in other editors could produce different results as the graphs appear in the Spyder command window. This algorithm works by:
1. Searching to see if any amplitude values are above 200 and collects these points in a list
2. Starting from the first point it checks if the next point is greater than 4000 centiseconds in time (using this terminology because it is "written" this way in the code) and inputs these values into a list called "isox" (Isolated X-values)
3. The graph starts 10,000 points before the anomaly and 20,000 after (This allows the graph to display the buildup and the aftermath of each anomaly)
4. The graph section is then divided into different sections
5. From these sections the max amplitudes of each section are calculated (variable = allmax)
6. Using the section max amplitudes data, the location of the max was found
7. For this project this max was assumed to be the potential S-wave max amplitude
8. Two pickers were used from obspy.signal.trigger to find the locations of the P and S waves on each anomaly, pk_baer and ar_pick
9. pk_baer find only p-wave and ar_pick finds both P and S waves
10. The two P waves were averaged together and rounded to get that point and the S wave point was used from ar_pick

The output graphs start with the whole day. The text shows the amplitudes of each wave. Then the graphs of each anomaly with the colors of the waves, red=P-wave, yellow=S-wave and blue= the rest of the wave.
