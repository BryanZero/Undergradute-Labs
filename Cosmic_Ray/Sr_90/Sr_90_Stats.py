from getData import *

import LT_Fit.parameters as P
import LT_Fit.gen_fit as G

import scipy.special as ms;

from scipy.stats import poisson

# It is consider a good practice instead of put directly in the the function get_file
files = ['data_1','data_2','data_3']
Data = makeDict(files)

nBins = 5

fornum = lambda x: range(len(x))

for k in fornum(files):
    currentData = Data[files[k]]
    counts = currentData['counts']
    max_count = max(counts)
    min_count = min(counts)

    if max_count < 10:
        #Poisson so bin width should be 1
        nBins=5
        B.pl.figure('mu = 1')
    elif max_count <100:
        nBins = 10
        B.pl.figure('mu = 10')
    else:
        nBins = 10
        B.pl.figure('mu = 100')

    h0 = B.histo(counts, range=(min_count-.5, max_count+.5), bins=nBins);

    hx = h0.bin_center
    hy = h0.bin_content
    dy = np.sqrt(hy);

    mu = P.Parameter(np.average(counts), '$\mu$');
    norm = P.Parameter(10., 'A');

    # Poisson function
    def myfun1(x):
        value = norm() * mu() ** (x) * np.exp(-mu()) / ms.gamma(x + 1.0)
        return value


    # Fitting as we did in example 2
    fit10 = G.genfit(myfun1, [mu, norm], x=hx, y=hy);
    if max_count < 60:
        B.plot_line(fit10.xpl, fit10.ypl, color="red",label='Poisson Fit');

    # Other Parameters
    myheight = P.Parameter(30., 'A');

    mymean = P.Parameter(np.average(counts), '$\mu$');

    mysigma = P.Parameter(10, '$\sigma$');


    # Now the Fuction

    # Second Order Polinomial + Gaussian

    def myfun(x):
        value = myheight() * np.exp(-0.5 * ((x - mymean()) / mysigma()) ** 2) / mysigma()
        return value



    # Then we can fit the function fit above
    fit5 = G.genfit(myfun, [myheight, mymean, mysigma], x=hx, y=hy)
    B.plot_line(fit5.xpl, fit5.ypl, color='orange',label='Gaussian Fit');
    B.pl.legend()
    h0.plot();
    if max_count < 10:
        labels('Counts','Frequency',f'Histogram Fit $\mu = {np.average(counts)}$',fit=[fit10,fit5],fit_names=['Poisson Fit:','Gaussian Fit'],xy=(0.7,0.34))
    elif max_count <100:
        labels('Counts','Frequency',f'Histogram Fit $\mu = {round(np.average(counts),2)}$',fit=[fit10,fit5],fit_names=['Poisson Fit:','Gaussian Fit'],xy=(0.82,0.45))
    else:
        labels('Counts','Frequency',f'Histogram Fit $\mu = {round(np.average(counts),2)}$',fit=fit10,fit_names=['Gaussian Fit'],xy=(0.8,0.3))
    B.pl.show();

