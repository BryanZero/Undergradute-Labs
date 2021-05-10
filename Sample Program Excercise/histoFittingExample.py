import numpy as np
import LT.box as Box
import LT_Fit.parameters as P
import LT_Fit.gen_fit as G
import scipy.special as ms
#get data
file = 'histoFitting.data'
f = Box.get_file(file)
A = Box.get_data(f,'A')

#definining parameters for histogram usage
h2 = Box.histo(A,(.5,10.5),10)

hx = h2.bin_center
hy = h2.bin_content
dy = np.sqrt(hy)
print("hy is:\n",hy)
print("dy is:\n",dy)
mu = P.Parameter(2.,'mu')
norm = P.Parameter(10.,'norm')

#calculation
def myfun(x):
    value = norm()*mu()**(x)*np.exp(-mu())/ms.gamma(x+1.0)
    return value
#fitting and plotting
fit10 = G.genfit(myfun, [mu,norm],x=hx,y=hy)
Box.plot_line(fit10.xpl,fit10.ypl,color='red')
h2.plot()
Box.pl.show()

