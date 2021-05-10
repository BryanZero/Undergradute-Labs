from getData import *

list = ['-30_deg','-25_deg','-20_deg','-15_deg','-10_deg','-5_deg','0_deg','5_deg','10_deg','15_deg','20_deg']

Data = makeDict(list,'.Spe')

degList = []
Rates = []
dRates = []

def get_time(sp):
    tt = float(sp.title.split('=')[1].split('s')[0])
    return tt

for k in Data:
    Data[k]['Time'] = get_time(Data[k]['dataFile'])
    if k == 'no_foil':
        Data[k]['Sum&Err'] = Data[k]['dataFile'].sum(20, 80)
    else:
        Data[k]['Sum&Err'] = Data[k]['dataFile'].sum(28, 58)
    Data[k]['Rate'] = Data[k]['Sum&Err'][0]/Data[k]['Time']
    Data[k]['dRate'] = Data[k]['Sum&Err'][1]/Data[k]['Time']

    Data[k]['dataFile'].plot()
    B.pl.title('All Spectrums Together')
    degList.append(int(k.split('_')[0]))
    if k != 'foil_0deg' or 'no_foil':
        Rates.append(Data[k]['Rate'])
        dRates.append(Data[k]['dRate'])



#Check power law
#%%
B.pl.figure('Separate Graphs')
theta_0 = -3.2992992992992995
degList = np.asarray(degList)
Rates = np.asarray(Rates)
dRates = np.asarray(dRates)
pos = degList > 0
neg = ~pos

'''
oldfit = 100000
for theta_0 in np.linspace(-4,-2,1000):
    if fit.chi_red < oldfit:
        oldfit = fit.chi_red
        oldmax = theta_0
'''

Xpos = np.log(np.sin(np.pi/180*np.abs(degList[pos]-theta_0))/2)
Xneg = np.log(np.sin(np.pi/180*np.abs(degList[neg]-theta_0))/2)
Ypos = np.log(Rates[pos])
dYpos= dRates[pos]/Rates[pos]
Yneg = np.log(Rates[neg])
dYneg = dRates[neg]/Rates[neg]

Xtot = np.append(Xneg,Xpos)
Ytot = np.append(Yneg,Ypos)
dYtot = np.append(dYneg,dYpos)

sel = Xtot>-2.2
fit = B.linefit(Xtot[sel],Ytot[sel],dYtot[sel])
#B.plot_exp(Xtot,Ytot,dYtot)
B.plot_line(fit.xpl,fit.ypl)

B.plot_exp(Xpos,Ypos,dYpos,color='r',label='Positive Angles')
B.plot_exp(Xneg,Yneg,dYneg,color='b',label='Negative Angles')

B.pl.legend()
labels('Natural Logarithm of θ (rads)','Natural Logarithm of Rate (Counts/s)','Rutherford Scattering $\\theta_0 = -3.3$')
#%%
B.pl.figure('All')
B.plot_exp(degList,Rates,dRates,logy=True,color='b',label='Angles')
B.plot_exp(degList[sel],Rates[sel],dRates[sel],color='r',label='Rutherford Scattering Angles')


C = B.Parameter(10., 'C')       # define the parameter
t0 = B.Parameter(-3.3, 'theta_0') # define parameter for


def S(x): # define the function
    return C()/(np.sin(np.pi/180*0.5*(x - t0() ) )**4)


sfit = B.genfit( S, [C, t0], x = degList[sel], y = Rates[sel], y_err = dRates[sel])
B.plot_line(sfit.xpl,sfit.ypl,color='r')
B.pl.legend()
labels('$\\theta$ (deg)','Rates','Rutherford Scattering (Log scale)')

