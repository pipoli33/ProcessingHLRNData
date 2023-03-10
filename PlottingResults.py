import numpy as np
import os
import math
import cmath
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D








'''
do the plotting of Double Occupancy with matplotlib reading from a DataFrame which was saved before with ReadAndSaveResults.py
'''
def plotOccupancy(directoryRefined, Beta, P, L, KSteps, Ns, Symm):
    DataFrame = pd.read_csv(directoryRefined + '/tests/DoubleOccupancies/occupancies_toCompareKsteps.csv')                         #load saved Dataframe
    for beta in Beta:
        for p in P:
            for l in L:
                for steps in KSteps:
                    for ns in Ns:
                        for symm in Symm:
                            smallDataFrame = DataFrame.loc[(DataFrame['L'] == l) & (DataFrame['Beta'] == beta)  & (DataFrame['P'] == p) & 
                                                            (DataFrame['Ksteps'] == steps) & (DataFrame['Ns'] == ns) & (DataFrame['Symmetry'] == symm)]            #select only the rows where the conditions of this iteration hold true, & is and
                            plt.plot(smallDataFrame.loc[:, 'U'], smallDataFrame.loc[:, 'Double Occupancies'], label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm), marker = '+')
                            plt.xlabel("U")
                            plt.ylabel(r'$<n_{i \uparrow} n_{i \downarrow}>$')
                            plt.legend()
                            plt.savefig(directoryRefined  + "/tests/DoubleOccupancies/occupanciesPlot_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                            plt.clf()



'''
Plot Hybridizationfunction Delta(iv) to look for asymptotic behaviour 
'''
def plotHybridFunc(Beta, P, L, U, KSteps, Ns, Symm, resolutionPoints, sourceDirectory, targetDirectory):
    for beta in Beta:
        for p in P:
            for l in L:
                for u in U:
                    for steps in KSteps:
                        for ns in Ns:
                            for symm in Symm:
                                #load files
                                input = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/g0mand'.format(beta, u, u/2, p, l, steps, ns, symm))
                                inputFort = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/fort.1002'.format(beta, u, u/2, p, l, steps, ns, symm))
                                inputBigFort = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/fort.2002'.format(beta, u, u/2, p, l, steps, ns, symm))
                                inputSigma = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/self-en_wim'.format(beta, u, u/2, p, l, steps, ns, symm))

                                



                                #Calculation of Delta and plotting zoomed in and full of g0mand, which has Gloc AFTER fitting
                                Delta = np.zeros(len(input))                                #to store the hybridization function in
                                x = np.zeros(len(input))
                                for i in range(len(input)):
                                    Delta[i] = input[i, 0] * (input[i, 0] - input[i, 2])           #calculate Delta by i\nu - 1/G_0(i\nu)
                                    x[i] = input[i, 0]

                                plt.plot(x[-resolutionPoints:], Delta[-resolutionPoints:], label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm), marker = '+')
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend("plot hybridization function after fitting to the Anderson parameters")
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotPartG0mand_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()

                                plt.plot(x, Delta, label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm), marker = '+')
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotFullG0mand_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()
                            




                                #Calculate Delta with the fort.2002 file, which has the frequencies of all processor, 
                                # but using self-en_wim instead of the theoretical value of Sigma
                                # we are only using the first iteration in fort.2002 since self-en_wim is only that long
                                DeltaBigFortSigma = np.zeros(len(inputSigma))
                                xBigFortSigma = np.zeros(len(inputSigma))
                                for i in range(len(inputSigma)):
                                    DeltaBigFortSigma[i] = - inputBigFort[i, 0] * (inputBigFort[i, 0] + inputBigFort[i, 2]/(inputBigFort[i, 1] * inputBigFort[i, 1] + inputBigFort[i, 2] * inputBigFort[i, 2]))         \
                                                      + inputBigFort[i, 0] * inputSigma[i, 2]                    #calculate Im(Delta) = i\nu - 1/G_loc(i\nu) - Sigma(i\nu)       n=1 in Sigma for half filling
                                    xBigFortSigma[i] = inputBigFort[i, 0]

                                plt.plot(xBigFortSigma[-resolutionPoints:], DeltaBigFortSigma[-resolutionPoints:], label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm),linewidth=0.5)
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotPartFort2002Sigma_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()

                                plt.plot(xBigFortSigma, DeltaBigFortSigma, label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm),linewidth=0.5)
                                plt.axhline(y=0.25, color='r', linestyle='-')
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotFullFort2002Sigma_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()





                                #Calculate Delta with the fort.1002 file, which only has the frequencies of the first processor
                                DeltaFort = np.zeros(len(inputFort))
                                xFort = np.zeros(len(inputFort))
                                for i in range(len(inputFort)):
                                    DeltaFort[i] = - inputFort[i, 0] * (inputFort[i, 0] + inputFort[i, 2]/(inputFort[i, 1] * inputFort[i, 1] + inputFort[i, 2] * inputFort[i, 2]))         \
                                                   - u*u * 1/2 * (1 - 1/2)                     #calculate Im(Delta) = i\nu - 1/G_loc(i\nu) - Sigma(i\nu)       n=1 in Sigma for half filling
                                    xFort[i] = inputFort[i, 0]

                                plt.plot(xFort[-resolutionPoints:], DeltaFort[-resolutionPoints:], label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm),linewidth=0.5)
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotPartFort1002_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()

                                plt.plot(xFort, DeltaFort, label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm),linewidth=0.5)
                                plt.axhline(y=0.25, color='r', linestyle='-')
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotFullFort1002_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()






                                #Calculate Delta with the fort.2002 file, which has the frequencies of all processors
                                DeltaBigFort = np.zeros(len(inputBigFort))
                                xBigFort = np.zeros(len(inputBigFort))
                                for i in range(len(inputBigFort)):
                                    DeltaBigFort[i] = - inputBigFort[i, 0] * (inputBigFort[i, 0] + inputBigFort[i, 2]/(inputBigFort[i, 1] * inputBigFort[i, 1] + inputBigFort[i, 2] * inputBigFort[i, 2]))         \
                                                      - u*u * 1/2 * (1 - 1/2)                     #calculate Im(Delta) = i\nu - 1/G_loc(i\nu) - Sigma(i\nu)       n=1 in Sigma for half filling
                                    xBigFort[i] = inputBigFort[i, 0]

                                plt.plot(xBigFort[-resolutionPoints:], DeltaBigFort[-resolutionPoints:], label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm),linewidth=0.5)
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotPartFort2002_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()

                                plt.plot(xBigFort, DeltaBigFort, label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm),linewidth=0.5)
                                plt.axhline(y=0.25, color='r', linestyle='-')
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotFullFort2002_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()





                                '''
                                if symm:                        #only have to do it once
                                    #Calculate Delta for True
                                    inputTrue = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/g0mand'.format(beta, u, u/2, p, l, steps, ns, True))
                                    DeltaTrue = np.zeros(len(inputTrue))                               
                                    x = np.zeros(len(inputTrue))
                                    for i in range(len(inputTrue)):
                                        DeltaTrue[i] = inputTrue[i, 0] * (inputTrue[i, 0] - inputTrue[i, 2])        
                                        x[i] = inputTrue[i, 0]
                                    #now calculate the same for False
                                    inputFalse = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/g0mand'.format(beta, u, u/2, p, l, steps, ns, False))
                                    DeltaFalse = np.zeros(len(inputFalse))                               
                                    for i in range(len(inputFalse)):
                                        DeltaFalse[i] = inputFalse[i, 0] * (inputFalse[i, 0] - inputFalse[i, 2])        
                                        x[i] = inputFalse[i, 0]
                                    #Therefore can plot the difference of the True and False plot
                                    plt.plot(x, DeltaTrue - DeltaFalse, label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = True - False$'.format(beta, p, l, steps, ns), marker = '+')
                                    plt.xlabel(r'$i\nu$')
                                    plt.ylabel(r'$\Delta(i\nu)$')
                                    plt.legend()
                                    plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/hybridPlotDiffG0mand_B{}_P{}_L{}_steps{}_Ns{}_symmTrue-False.png".format(beta, p, l, steps, ns))
                                    plt.clf()
                                '''



def plotGreens(Beta, P, L, U, KSteps, Ns, Symm, sourceDirectory, targetDirectory):
    for beta in Beta:
        for p in P:
            for l in L:
                for u in U:
                    for steps in KSteps:
                        for ns in Ns:
                            for symm in Symm:
                                input0mand = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/g0mand'.format(beta, u, u/2, p, l, steps, ns, symm))
                                inputw = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/g0m'.format(beta, u, u/2, p, l, steps, ns, symm))

                                #Just Plot some Greens function times i nu
                                G0mand = np.zeros(len(input0mand))                                
                                x0mand = np.zeros(len(input0mand))
                                for i in range(len(input0mand)):
                                    G0mand[i] = input0mand[i, 0] * (input0mand[i, 2])                         #just i\nu * Im(G)        
                                    x0mand[i] = input0mand[i, 0]


                                GW = np.zeros(len(inputw))                                
                                xW = np.zeros(len(inputw))
                                for i in range(len(inputw)):
                                    GW[i] = inputw[i, 0] * (inputw[i, 2])                         #just i\nu * Im(G)        
                                    xW[i] = inputw[i, 0]
 

                                plt.plot(x0mand, G0mand, label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm), marker = '+')
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/GPlotFrom0mand_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()

                                plt.plot(xW, GW, label = r'$\beta = {}, p = {}, L = {}, Ksteps = {}, Ns = {}, symmetry = {}$'.format(beta, p, l, steps, ns, symm), marker = '+')
                                plt.xlabel(r'$i\nu$')
                                plt.ylabel(r'$\Delta(i\nu)$')
                                plt.legend()
                                plt.savefig(targetDirectory  + "/tests/hybridizationFunctions/GPlotFromG0w_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()


 
'''
Read out and plot Sigma from our file
'''
def plotSigma(Beta, P, L, U, KSteps, Ns, Symm, sourceDirectory, targetDirectory):
    for beta in Beta:
        for p in P:
            for l in L:
                for u in U:
                    for steps in KSteps:
                        for ns in Ns:
                            for symm in Symm:
                                dataToRead = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/self-en_wim'.format(beta, u, u/2, p, l, steps, ns, symm))
                                MatsubaraFreq = dataToRead[:, 0]
                                RealPart = dataToRead[:, 1]
                                ImagPart = dataToRead[:, 2]
                                plt.plot(MatsubaraFreq[:20], ImagPart[:20])                             #only plot until Matsubara frequency is the 20s value to see more structure
                                plt.xlabel(r'$\omega$')
                                plt.ylabel(r'Im($\Sigma$)')
                                plt.savefig(targetDirectory  + "/tests/selfEnergies/SelfEnergies_B{}_P{}_L{}_steps{}_Ns{}_symm{}.png".format(beta, p, l, steps, ns, symm))
                                plt.clf()
                                if symm:
                                    dataToReadFalse = np.loadtxt(sourceDirectory + '/B{}_U{}_Mu{}_P{}_L{}_steps{}_Ns{}_symm{}/ed_dmft/self-en_wim'.format(beta, u, u/2, p, l, steps, ns, symm))
                                    MatsubaraFreqFalse = dataToReadFalse[:, 0]
                                    RealPartFalse = dataToReadFalse[:, 1]
                                    ImagPartFalse = dataToReadFalse[:, 2]
                                    plt.plot(MatsubaraFreq[:10], ImagPart[:10], label = r'symmetry = True')                         #plot both the values for True and False
                                    plt.plot(MatsubaraFreqFalse[:10], ImagPartFalse[:10], label = r'symmetry = False')                             
                                    plt.xlabel(r'$\omega$')
                                    plt.ylabel(r'Im($\Sigma$)')
                                    plt.legend()
                                    plt.savefig(targetDirectory  + "/tests/selfEnergies/SelfEnergiesComparisonTrueFalse_B{}_P{}_L{}_steps{}_Ns{}.png".format(beta, p, l, steps, ns))
                                    plt.clf()






'''
below not used yet
'''






'''
do the plotting of Sigma(small) values with matplotlib
'''
def PlotFirstSigma(U, Beta):
    FirstImags = np.zeros((len(U)))

    for beta in Beta: 
        for u in range((len(U))):
            Matsubara, Real, Imag = readSigma("/afs/physnet.uni-hamburg.de/users/th1_km/nhyttrek/Desktop/MA/MACode/dmft_code_not_parallel/BetterFewCalculations/SigmaValuesU{}Beta{}.txt".format(U[u], beta))
            FirstImags[u] = Imag[0]
        plt.plot(U, FirstImags, label = r'$\beta = {}$'.format(beta), linestyle = 'dashed', marker = '+')   
        for u in range((len(U))):
            Matsubara, Real, Imag = readSigma("/afs/physnet.uni-hamburg.de/users/th1_km/nhyttrek/Desktop/MA/MACode/dmft_code_not_parallel/BetterFewCalculations/SigmaValuesU{}Beta{}_Hysterese.txt".format(U[u], beta))
            FirstImags[u] = Imag[0]
        plt.plot(U, FirstImags, label = ' '.join(["Hysterese", r'$\beta = {}$'.format(beta)]), linestyle = 'dashed', marker = '+')                       
    plt.xlabel("U")
    plt.ylabel(r'Im($\Sigma(\omega_0)$)')
    plt.legend()
    plt.savefig("/afs/physnet.uni-hamburg.de/users/th1_km/nhyttrek/Desktop/MA/MACode/dmft_code_not_parallel/BetterFewCalculations/SmallImagValues.png")
    plt.clf()

    
'''
Now try to approximate Sigma(0) by Gradient of w_0 and w_1
'''    
def PlotZerosSigma(U, Beta):
    ZeroImags = np.zeros((len(U)))

    for beta in Beta: 
        for u in range((len(U))):
            Matsubara, Real, Imag = readSigma("/afs/physnet.uni-hamburg.de/users/th1_km/nhyttrek/Desktop/MA/MACode/dmft_code_not_parallel/BetterFewCalculations/SigmaValuesU{}Beta{}.txt".format(U[u], beta)) 
            Gradient = (Imag[1] - Imag[0])/(Matsubara[1] - Matsubara[0])
            ZeroImags[u] = Imag[0] - Gradient * Matsubara[0]
        plt.plot(U, ZeroImags, label = r'$\beta = {}$'.format(beta), linestyle = 'dashed', marker = '+')
                   
        for u in range((len(U))):
            Matsubara, Real, Imag = readSigma("/afs/physnet.uni-hamburg.de/users/th1_km/nhyttrek/Desktop/MA/MACode/dmft_code_not_parallel/BetterFewCalculations/SigmaValuesU{}Beta{}_Hysterese.txt".format(U[u], beta))
            Gradient = (Imag[1] - Imag[0])/(Matsubara[1] - Matsubara[0])
            ZeroImags[u] = Imag[0] - Gradient * Matsubara[0]
        plt.plot(U, ZeroImags, label = ' '.join(["Hysterese", r'$\beta = {}$'.format(beta)]), linestyle = 'dashed', marker = '+')                    
    plt.xlabel("U")
    plt.ylabel(r'Im($\Sigma(0)$)')
    plt.legend()
    plt.savefig("/afs/physnet.uni-hamburg.de/users/th1_km/nhyttrek/Desktop/MA/MACode/dmft_code_not_parallel/BetterFewCalculations/ZeroImagValues.png")
    plt.clf()







    










