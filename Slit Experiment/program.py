from getData import *

Data = makeDict(['single1','single2','double'])

background = 0.007

for k in Data:
    Data[k]['V'] = Data[k]['V'] - background
    Data[k]['mm'] = Data[k]['mm'] * 1e-3

#Constants:
DS = 0.505 #m
DC = 5.05 * 1e-3 # meters
D1 = Data['single1']
D2 = Data['single2']
D3 = Data['double']
D2['mm']=D2['mm'][10:-5]
D2['V']=D2['V'][10:-5]
D2['dV']=D2['dV'][10:-5]

#Theta:
thetaC = (np.arctan(DC/DS)) # radians

theta1 = (np.arctan(D3['mm']/DS)) - thetaC #rad
theta2 = (np.arctan(D3['mm']/DS)) - thetaC #rad
theta3 = (np.arctan(D3['mm']/DS)) - thetaC #rad

for k in Data:
    Data[k]['V'] = (Data[k]['V'] - Data[k]['V'].min()) / (Data[k]['V'].max() - Data[k]['V'].min())

#Define wavenumber - k:
Ix1 = theta1
Ix2 = theta2
Ix3 = theta3

Iy1 = D1['V']
Iy2 = D2['V']
Iy3 = D3['V']

lam = 670.e-9
k = 2.*np.pi/lam
#------------------------------------------------------------------------------------------------------------#
B.pl.figure('Single Slit 1')
#Define Intensity Function for single slit left:
I0 = B.Parameter(1.,'$I_0$') #maximum intensity
D = B.Parameter(0.15e-3,'D') #slit width
x0 = B.Parameter(DC,'$x_0$')

def I(x):
    th = ((x-x0())/DS) + 1.e-10
    A1 = k*D()*np.sin(th)/2.
    Atot = np.sin(A1)/A1
    intensity = I0()*Atot**2.
    return intensity
fit = B.genfit(I, [D,I0,x0], D1['mm'], y=D1['V'])
B.plot_exp(D1['mm'], D1['V'],(1/0.805)*0.0005)
th = np.linspace(0,0.01, 1000)
B.plot_line(th,I(th))
labels('Viewing Angle (Radians)','Intensity','Normalized Intensity vs Viewing Angle (Left Slit)',fit=fit,xy=(0.7,0.8),parext=('','m','m','rad'))
#------------------------------------------------------------------------------------------------------------#
B.pl.figure('Single Slit 2')
#Define Intensity Function for single slit left:
I0 = B.Parameter(1.,'$I_0$') #maximum intensity
D = B.Parameter(0.15e-3,'D') #slit width
x0 = B.Parameter(DC,'$x_0$')

def I(x):
    th = ((x-x0())/DS) + 1.e-10
    A1 = k*D()*np.sin(th)/2.
    Atot = np.sin(A1)/A1
    intensity = I0()*Atot**2.
    return intensity
fit = B.genfit(I, [D,I0,x0], D2['mm'], y=D2['V'])
B.plot_exp(D2['mm'], D2['V'],(1/0.805)*0.0005)
th = np.linspace(0,0.0115, 1000)
B.plot_line(th,I(th))
labels('Viewing Angle (Radians)','Intensity','Normalized Intensity vs Viewing Angle (Right Slit)',fit=fit,xy=(0.7,0.8),parext=('','m','m','rad'))

#------------------------------------------------------------------------------------------------------------#
B.pl.figure('Double Slit')
S = B.Parameter(0.4e-3,'S') #slit separation
I0 = B.Parameter(1.,'$I_0$') #maximum intensity
D = B.Parameter(0.6e-3,'D') #slit width
x0 = B.Parameter(DC,'$x_0$')

def I(x):
    th = ((x-x0())/DS) + 1.e-22
    A1 = k*D()*np.sin(th)/2.
    A2 = k*S()*np.sin(th)/2.
    Atot = (np.sin(A1)*np.cos(A2))/A1
    intensity = I0()*Atot**2.
    return intensity

fit = B.genfit(I, [D,S,I0,x0], D3['mm'], y=D3['V'])
B.plot_exp(D3['mm'],D3['V'], (1/1.836)*0.0005)
B.plot_line(fit.xpl,fit.ypl)

th = np.linspace(0,0.009, 1000)
B.plot_line(th[150:-75],I(th[150:-75]))

labels('Viewing Angle (Radians)','Intensity','Normalized Intensity vs Viewing Angle (Double Slit)',fit=fit,xy=(0.7,0.8),parext=('','m','m','','rad'))

B.pl.show()