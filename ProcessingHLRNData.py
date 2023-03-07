import numpy as np
import os
import toml

import ScheduleConfigs as Schedule
import CreateToml as Create
import PlottingResults as Plot
import ReadAndSaveResults as Save


#the values yoe want to iterate over
P = [1]
L = [3]
Beta = [30.0]
U = [1.0]                           
KSteps = [100, 121]
Ns = [5, 7]
Symm = [False, True]

resolutionPointsHybridPlot = 100                                                            #zooming parameter, high means large intervall of i\nu, 0 means only the largest i\nu


calculate = True
plotDoubleOccupancy = False 
plotAsymptotic = False


#all paths needed
blueprintConfigPath = "/home/hhpnhytt/configFiles/blueprintConfig.toml"                     #blueprint config, from which you only change that stuff below
configTargetDirectory = "/home/hhpnhytt/configFiles/testConfigsKStepsFullMatrix"                                       #where to put the config files
configSourceDirectory = "/home/hhpnhytt/configFiles/testConfigsKStepsFullMatrix"                                        #where we had our config files

wrapperDirectory = "/home/hhpnhytt/lDGAPythonWrapper"

directoryRawDataSource = "/scratch/usr/hhpnhytt/tests/toCompareKStepsFullMatrix"                            #Raw Data always lies in SCRATCH, change for different types of calculations
directoryRefined = "/home/hhpnhytt/refined/toCompareKStepsFullMatrix"



if __name__ == "__main__":

    #if True, the config.toml will be created and scheduled on the HLRN to calculate DMFT
    if calculate:
        Create.CreateConfigs(Beta, P, L, U, KSteps, Ns, Symm, blueprintConfigPath, configTargetDirectory)
        Schedule.ScheduleCalculations(P, L, Beta, U, KSteps, Ns, Symm, configSourceDirectory, wrapperDirectory)

    #if True, the double occupancy will be read from the DMFT reults, saved in a DataFrame and plotted
    if plotDoubleOccupancy:
        Save.saveDoubleOccupancyToUse(Beta, U, P, L, KSteps, Ns, Symm, directoryRawDataSource, directoryRefined)
        Plot.plotOccupancy(directoryRefined, Beta, P, L, KSteps, Ns, Symm)

    if plotAsymptotic:
        Plot.plotHybridFunc(Beta, P, L, U, KSteps, Ns, Symm, resolutionPointsHybridPlot, directoryRawDataSource, directoryRefined)
        Plot.plotGreens(Beta, P, L, U, KSteps, Ns, Symm, directoryRawDataSource, directoryRefined)





