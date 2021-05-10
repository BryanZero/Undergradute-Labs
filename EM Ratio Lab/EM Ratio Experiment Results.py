import numpy as np
import LT.box as B

def wmean(x, sig):
    w = 1. / sig ** 2
    # weighted mean
    wm = np.sum(x * w) / np.sum(w)
    sig_wm = np.sqrt(1. / np.sum(w))
    return wm, sig_wm


def showResult(x):
    dfile = x
    #Get data from file and make an array
    #I = current D = diameter of electron beam dD = deviation in measurement of diameter
    f = B.get_file(dfile)
    I = B.get_data(f,'I')
    D = B.get_data(f,'D')
    dD = B.get_data(f,'dD')
    V = f.par.get_value('V')
    #Physical Constant
    munot = np.pi*4e-7
    #Measured radius of coils
    R = (30.5/2) * 0.01
    #Published value of the em Ratio
    Rem_Pub = 1.6e-19/9.11e-31
    #Calculating the BField magnitude
    bField = (munot * 132 * I * ((4/5)**(3/2)) ) / R
    #D*0.1/2 converts the cm to meters and the diameter to the radius.
    r = (D*.01)/2
    Rem = (2*V) / ((bField**2)*(r**2))

    #Error Analysis
    #defining sigmas obtained
    sigmaN = 0.0
    sigmaR = 0.00025
    sigmaI = 0.01
    sigmaV = 1.00
    sigmar = dD/2

    #Defining the partial Derivatives
    partialBN = (I/R)
    partialBR = (I*132/(R**2))
    partialBI = (132/R)
    #Defining sigmaB by the error equation
    sigmaB = (4/5)**(3/2) * munot * np.sqrt( (partialBN**2 * sigmaN**2) + (partialBR**2 * sigmaR**2) + (partialBI**2 * sigmaI**2))
    #Defining partial derivatives
    partialRemV = 2/((bField**2)*(r**2))
    partialRemB = -4*V/((bField**3)*(r**2))
    partialRemr = -4*V/((bField**2)*(r**3))
    #defining sigmaRem by the error equation
    sigmaRem = np.sqrt( (partialRemV**2 * sigmaV**2) + (partialRemB**2 * sigmaB**2) + (partialRemr**2 * sigmar**2) )

    #Printing out stats
    print("############ Results for V" + str(V) + " #################")
    print("Actual Value of Rem: " + np.format_float_scientific(Rem_Pub))
    ARem,ErRem = wmean(Rem,sigmaRem)
    print("Average Value for Rem (Weighted): " + np.format_float_scientific(ARem))
    print("Weighted Uncertainty: " + np.format_float_scientific(ErRem))
    print("Percent Error: " + str((Rem_Pub - ARem)/(Rem_Pub)*100) + "%")
    print("Actual - Experimental/Uncertainty: " + str((Rem_Pub - ARem)/(ErRem)))

    #Making the plot
    B.pl.figure('EM Experiment')
    B.plot_exp(I,Rem,sigmaRem)
    B.plot_line(I,np.ones_like(I)*Rem_Pub)
    B.pl.xlabel('Current (A)')
    B.pl.ylabel('e/m ratio C/kg')
    B.pl.title('Accelerating Voltage = {%.0f} (V)' %(V))
    #Uncomment to show graphs
    B.pl.show()
    return ARem, ErRem

list = ['V150.data','V200.data','V300.data','V400.data']
aa = []
nn = []
for k in list:
    n,a = showResult(k)
    nn.append(n)
    aa.append(a)
print("#################################################")
overallAV, overallAD = wmean(np.asarray(nn),np.asarray(aa))
print("Average weighted value for all trials: " + str(np.format_float_scientific(overallAV)))
print("Average weighted uncertainty for all trials: " + str(np.format_float_scientific(overallAD)))
print("Error percentage for all trails is: " + str((( (1.6e-19/9.11e-31) - overallAV)/(1.6e-19/9.11e-31))*100) + "%")
print("Actual - Experimental/Uncertainty: " + str(((1.6e-19/9.11e-31) - overallAV)/(overallAD)))