from getData import *

Data = makeDict(['data'])

try:
    Data['T'] = np.vectorize(eval)(Data['T'])
except:
    pass

Data['T'] = Data['T']/2
offset = -.1822
Data['T'] += offset
B.pl.figure('Counts')
B.plot_exp(Data['T'],Data['C']/Data['Parameters']['Time'],np.sqrt(Data['C']/Data['Parameters']['Time']))
labels('$\\theta$','Count Rate','Uncertainty = $\\sigma_{R}$')

Peak1 = [(Data['T']>=14.0+offset) & (Data['T'] <=14.5+offset)]
Peak2 = [(Data['T']>=15.6+offset) & (Data['T'] <=16.2+offset)]
Peak3 = [(Data['T']>=29.4+offset) & (Data['T'] <=30+offset)]
Peak4 = [(Data['T']>=32.9+offset) & (Data['T'] <=33.6+offset)]
Peak5 = [(Data['T']>=54.9+offset) & (Data['T'] <=55.4+offset)]

peaks = [Peak1,Peak2,Peak3,Peak4,Peak5]

for k in peaks:
    fit = B.polyfit(Data['T'][k],Data['C'][k]/Data['Parameters']['Time'],np.sqrt(Data['C'][k]/Data['Parameters']['Time']))
    B.plot_line(fit.xpl,fit.ypl)

B.pl.figure('first')
x1 = np.sin(np.pi/180*np.array([Data['T'][Peak2][5],Data['T'][Peak4][6],Data['T'][Peak5][4]]))
sx1 = np.cos(np.pi/180*np.array([Data['T'][Peak2][5],Data['T'][Peak4][6],Data['T'][Peak5][4]]))*0.0833/2
x2 = np.sin(np.pi/180*np.array([Data['T'][Peak1][6],Data['T'][Peak3][5]]))
sx2 = np.cos(np.pi/180*np.array([Data['T'][Peak1][6],Data['T'][Peak3][5]]))*0.0833/2
B.plot_exp(np.array([1,2,3])*1.542,x1,sx1,label='$K\\alpha$')
B.plot_exp(np.array([1,2])*1.392,x2,sx2,label='$K\\beta$')

fit2 = B.linefit(np.array([1*1.542,2*1.542,3*1.542,1*1.392,2*1.392]),np.append(x1,x2),np.append(sx1,sx2))
B.plot_line(fit2.xpl,fit2.ypl,color='r')
B.pl.legend()
labels('n (Order)','$sin(\\theta)$','$K\\alpha\ and\ K\\beta$ Uncertainty = $\sigma_{sin(\\theta)}$','Slope= $\\frac{\\lambda}{2D}$\n',fit=fit2)

