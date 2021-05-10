from getData import *
import LT_Fit.parameters as P
import LT_Fit.gen_fit as G

Verr = 0.2

files = ['T1','T2']

Data = makeDict(files)

T1x = Data['T1']['T']
T2x = Data['T2']['T']

T1y = Data['T1']['V']
T1y[34:] = -1*T1y[34:]
T2y = Data['T2']['V']


M0 = P.Parameter(-12.6,r'$M_0$')
Mi = P.Parameter(-12.6,r'$M_i$')
T1 = P.Parameter(1.,r'$T_1$')
OFF = P.Parameter(12.,'OFF')
def T1fit(x):
    return M0()-(M0()-Mi())*np.exp(-x/T1())

fit = B.linefit(T1x[-30:],T1y[-30:],Verr)

fit = G.genfit(T1fit,[M0,Mi,T1],T1x,T1y,Verr)
test = B.linefit(T1x[-30:],T1y[-30:])
B.pl.figure('T1')
B.plot_line(fit.xpl,fit.ypl,label='Exponential Fit',color='red')
B.plot_exp(T1x,T1y,Verr,label='Experimental')
labels("Delay time (s)","Voltage (V)","Voltage vs Delay Time","Fit: $M_0-(M_0-M_i)e^{-t/T_1}$ \n\n",fit=fit)
B.pl.legend()


M0 = P.Parameter(-12.6,r'$M_0$')
T2 = P.Parameter(1.,r'$T_2$')
b = P.Parameter(13.4,'b')
def T2fit(x):
    #return M0()-(M0()-Mi())*np.exp(-x/T2())
    return M0()*(1-np.exp(-x/T2())) + b()

B.pl.figure('T2')
fit2 = G.genfit(T2fit,[T2,M0],T2x,T2y,Verr)
B.plot_line(fit2.xpl,fit2.ypl,label='Exponential Fit')
B.plot_exp(T2x,T2y,Verr,label='Experimental')
labels("Delay time (s)","Voltage (V)","Voltage vs Delay Time","Fit: $M_0(1-e^{-t/T_2})+b$\n",fit=fit2,xy=(0.6,0.5))
B.pl.legend()
