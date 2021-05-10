import numpy as np
import LT.box as Box
import LT_Fit.parameters as P
import LT_Fit.gen_fit as G
import scipy.special as ms

#Get data
file = 'examples.data'
f = Box.get_file(file)
A = Box.get_data(f,'A')
b = Box.get_data(f,'b')
db= Box.get_data(f,'db')
C = Box.get_data(f,'C')
D = Box.get_data(f,'D')

#definitions
c1 = P.Parameter(1.,'pol0')
c2 = P.Parameter(1., 'pol1')
c3 = P.Parameter(1., 'pol2')
height = P.Parameter(8., 'height')
mean = P.Parameter(6., 'mean')
sigma = P.Parameter(1., 'sigma')

def myfun(x):
    #Please for the love of god use clearer parenthesis when writing out a formula in python
    value = c1()+c2()*x+c3()*x**2+height()*np.exp(-((x-mean())/(2*sigma()))**2)
    return value
fit5 = G.genfit(myfun,[c1,c2,c3,height,mean,sigma],x=C,y=D,y_err=db)
Box.plot_line(fit5.xpl,fit5.ypl,color='blue')

#definitions, vectorization and fitting
R3 = Box.in_window(2.0,12.0,C)
fit6 = G.genfit(myfun,[c1,c2,c3,height,mean,sigma],x=C[R3],y=D[R3],y_err=db[R3])
Box.plot_line(fit6.xpl,fit6.ypl,color='magenta')
mu = P.Parameter(6.,'mu')
norm = P.Parameter(10.,'norm')

def myfun1(x):
    value = norm()*mu()**(x)*np.exp(-mu())/ms.gamma(x+1.0)
    return value

#more fitting lines
fit7 = G.genfit(myfun1,[mu,norm],x=C[R3],y=D[R3],y_err=db[R3])
Box.plot_line(fit7.xpl,fit7.ypl,color='red')
#redefinition
mu = P.Parameter(7.,'mu')
norm = P.Parameter(20.,'norm')

def myfun2(x):
    pol2 = c1()+c2()*x+c3()*x**2
    value = pol2 + norm()*mu()**(x)*np.exp(-mu())/ms.gamma(x+1.0)
    return value
#more vectorization and fitting
R4 = Box.in_window(4.0,16.0,C)

fit8 = G.genfit(myfun2,[c1,c2,c3,mu,norm],x=C[R4],y=D[R4],y_err=db[R4])
Box.plot_line(fit8.xpl,fit8.ypl,color='brown')
c2.set(0.)

fit9 = G.genfit(myfun2, [c1,c3,mu,norm],x=C[R4],y=D[R4],y_err=db[R4])
Box.plot_line(fit9.xpl,fit9.ypl,color='green')
#definitions for printing which isn't needed but..
muvalue = mu.value
muerr = mu.err
print("mu has the value of %.3f +- %.3f\n" % (muvalue,muerr))

Box.plot_exp(C,D,db)
Box.pl.show()