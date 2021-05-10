#Import the numpy package
import numpy as np
#import scipy for curve fitting
from scipy.optimize import curve_fit
from scipy.stats import poisson as poisson
from scipy.special import factorial
from scipy.special import gamma
#import graphing tool
import matplotlib.pyplot as plt

def nSphere(n,iter=27000):
    inside = 0
    total = 0
    for k in range(iter):
        #Basically saying if x_1^2 + x_2^2 + ... x_n^2 < 1 where x_n is a random float from [-1,1] then count it into the "inside" variable
        if np.sum(np.random.uniform(-1,1,n)**2) < 1:
            inside += 1
        total += 1
        #Ratio of inside to outside
        result = inside/total

        #Define uncertainty through the use of the binomial uncertainty
    N = iter
    p= result
    std = np.sqrt(p*(1-p)/N)*(2**n)
    result = result*(2**n)
    print(f'For a sphere of {n} dimensions, we get a volume of {result} with a standard deviation of {std}')
    return result, std


def calculatePi(iterations=2700):
    #Save a single trial into memory
    trial = nSphere(2,iterations)
    #Account for the area of the square compared to the area of the circle using r=1
    pi,uncertainty = trial[0],trial[1]
    print("#########################################")
    print(f"π = {pi} +/- {uncertainty}")
    print("#########################################")
    #return pi,uncertainty

def poissonDist(iter=10000):
    #Define desired mu values and desired binwidth
    mu = [1.0,10.3,102.1] #[1.0,10.3]
    binwidth = 1

    #define poisson function
    def poissonf(x,mu):
        if mu < 100 and x.any() < 153:
            return mu ** x * np.exp(-1. * mu) / factorial(x)
        else:
            x = x.astype(int)
            return poisson.pmf(x,mu=mu)

    #Creating the r function
    r = lambda mu,x: sum( mu**k * np.exp(-mu)/np.math.gamma(k+1) for k in range(x+1))
    results = [[],[],[]] #Too lazy to use a dictionary
    #Run this process for every element in the mu list
    for j in range(len(mu)):
        #Use the acceptance Rejection method to get poisson deviates http://pdg.lbl.gov/2011/reviews/rpp2011-rev-monte-carlo-techniques.pdf
        for k in range(iter):
            x = 0
            random = np.random.rand()
            while r(mu[j],x) < random:
                x += 1
            results[j].append(x)

        #Make graph pretty
        plt.figure('mu = {}'.format(mu[j]))
        # Store bin information to convert histogram to curve later on
        bin_heights,bin_borders,*p = plt.hist(results[j],bins=np.arange(min(results[j]), max(results[j]) + binwidth, binwidth),density=True,label='Histogram')

        # find bin centers (plt.hist stores edge information) https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.hist.html
        bin_centers = bin_borders[:-1] + bin_borders[1:] / 2

        # Define x interval for poisson curve (10000 is arbitrary, just need it high enough for a nice continous curve)
        x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)

        # plot curve
        plt.plot(x_interval_for_fit, poissonf(x_interval_for_fit, mu[j]), 'r--', label=f'Poisson Distribution')

        # Use the definition of chisq https://en.wikipedia.org/wiki/Chi-squared_test & http://www.physics.utah.edu/~detar/lessons/python/curve_fit/node1.html
        print(bin_centers)
        Nexp = poissonf(bin_centers, mu[j])
        r_1 = bin_heights - Nexp
        chisq = np.sum((r_1**2/ Nexp))
        redchisq = chisq/(r_1.size-1)
        print("##################")
        print(f'{chisq}')
        print(f"Reduced Chisq = {redchisq}")
        print("##################")
        plt.xlabel('Deviant')
        plt.ylabel('Counts')
        plt.title(r'Acceptance-Rejection Method $\mu = {}$'.format(mu[j]))
        plt.legend()
        plt.annotate(f'$Reduced \chi^2 = %{.7}g $' % (redchisq),xy=(0.70,0.72),xycoords='axes fraction')
    #return np.array([np.array(xi) for xi in results])



def gaussDist(iter=100000):

    #Define the gaussian function for the fitting module https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    def gaussian(x, mean, standard_deviation,A):
        return A/(standard_deviation*np.sqrt(2*np.pi)) * np.exp(- ((x - mean) / standard_deviation) ** 2)

    results = []
    #Box-Muller 2D method, https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform
    for k in range(iter):
        r1,r2 = np.random.rand(2)
        z1 = np.sqrt(-2*np.log(r1))*np.cos(2*np.pi*r2)
        results.append(z1)
    results = np.asarray(results)

    #Initializing the canvas we will be working on
    plt.figure('Gaussian transformation')

    #Store bin information to convert histogram to curve later on
    bin_heights,bin_borders,*p =plt.hist(results,bins=40,range=(-4,4),density=False,label='Histogram')

    #find bin centers (plt.hist stores edge information) https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.hist.html
    bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2

    #Use scipy optimize.curve_fit function to store the fit parameters (in this case the mean and standard_deviation
    #defined in gaussian() ) and then the covariance matrix associated with those parameters)
    pfit, pcov = curve_fit(gaussian, bin_centers, bin_heights, p0=[0, 1.,1.],absolute_sigma=True)

    #Define x interval for fit curve (10000 is arbitrary, just need it high enough for a nice continous curve)
    x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)

    #plot curve
    plt.plot(x_interval_for_fit, gaussian(x_interval_for_fit, *pfit),'r--', label='Gaussian Fit')

    #Use the definition of chisq https://en.wikipedia.org/wiki/Chi-squared_test & http://www.physics.utah.edu/~detar/lessons/python/curve_fit/node1.html
    Nexp=gaussian(bin_centers, *pfit)
    r = bin_heights-Nexp
    chisq = np.sum(r**2/Nexp)
    from scipy.stats import chisquare
    print(chisquare(bin_heights,Nexp))
    redchisq = chisq/(r.size-1)

    #Get diagnal elements of covariance matrix and sqrt them to find the std of the parameters. (The diagnols are the variance of each parameter)
    error = []
    for i in range(len(pfit)):
        error.append(np.absolute(pcov[i][i])**0.5)

    #Start prettying up the graph with labels and annotations
    plt.legend()
    plt.title('Box-Muller 2D Gaussian Transformation')
    plt.xlabel('X')
    plt.ylabel('Y')
    red = '{red}'
    plt.annotate(f'Fit Information\n $\chi^2_{red} = %{.7}g $' % (redchisq),xy=(0.70,0.72),xycoords='axes fraction')
    plt.annotate(f'$\mu = %{.3}g \pm %{.3}g$' % (pfit[0],error[0]),xy=(0.63,0.67),xycoords='axes fraction')
    plt.annotate(f'$\sigma = %{.2}g \pm %{.2}g$' % (pfit[1],error[1]),xy=(0.71,0.62),xycoords='axes fraction')
    plt.annotate(f'$A = %{.2}g \pm %{.2}g$' % (pfit[2],error[2]),xy=(0.71,0.57),xycoords='axes fraction')

    print("##############################################")
    print("Chisq = ", chisq)
    print("Red. Chisq = ",redchisq)
    print(f"Mean = {pfit[0]} +/- {error[0]}, Standard Deviation = {pfit[1]} +/- {error[1]}")
    print('      Covariance Matrix')
    print(*(f'{row}' for row in pcov), sep='\n')
    print("##############################################")
    return r,pcov