from getData import *
import LT_Fit.parameters as P
import LT_Fit.gen_fit as G

files = ['data1','data2']
Data = makeDict(files)
maximum = max(Data['data1']['Counts'])
currentData = Data['data1']
x = currentData['Angle']
y = currentData['Counts']
dy = np.sqrt(y)/maximum
y = y/maximum
B.plot_exp(x,y,dy)

A = P.Parameter(250., 'A')
Bs = P.Parameter(1., 'B')
C = P.Parameter(1., 'C')
D = P.Parameter(1., 'D')


def cosf(x):
    return -1*A() * np.cos(Bs() * x + C()) ** 2 + D()


fit = G.genfit(cosf, [A, Bs, C, D], x=x*np.pi/180, y=y)

B.plot_line(fit.xpl*180/np.pi,fit.ypl,color='red',label='$cos^2$ fit')
labels('Angle (Degrees)','Normalized Counts','Experimental Cosmic Rays',fit=fit,xy=(0.5,0.5))
B.pl.legend()

B.pl.figure('Second')

B.plot_exp(x,y,dy)
B.plot_line(fit.xpl*180/np.pi,fit.ypl,color='red',label='Coincidence Orientation 1')
fit_old = fit
currentData = Data['data2']
x = currentData['Angle']
y = currentData['Counts']
dy = np.sqrt(y)/maximum
y = y/maximum
B.plot_exp(x,y,dy,color='red')
fit = G.genfit(cosf, [A, Bs, C, D], x=x*np.pi/180, y=y)
B.plot_line(fit.xpl*180/np.pi,fit.ypl,color='blue',label='Coincidence Orientation 2')
B.pl.legend()
labels('Angle (Degrees)','Normalized Counts','Coincidence Module Orientation Bias',fit=[fit_old,fit],fit_names=['Orientation 1:','Orientation 2'],xy=(0.5,0.4))