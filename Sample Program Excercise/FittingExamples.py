import numpy as np
import LT.box as Box

file = 'examples.data'
#Getting data from file and assigning it
f = Box.get_file(file)
A = Box.get_data(f, 'A')
b = Box.get_data(f, 'b')
db = Box.get_data(f,'db')
C = Box.get_data(f,'C')
D = Box.get_data(f,'D')

#Labels
Box.pl.xlabel("x (unit)")
Box.pl.ylabel("y (unit)")
Box.pl.title("y vs x graph")
#fitting
fit1 = Box.linefit(A,C,db)
Box.plot_line(fit1.xpl,fit1.ypl)

#vectorize inbetween given values to select start position and end position
R1 = Box.in_window(4.0,10.0,C)
R2 = Box.in_window(2.0,12.0,C)
#fit lines
fit3 = Box.linefit(A[R1], C[R1], db[R1])
Box.plot_line(fit3.xpl,fit3.ypl)
#############################################
fit4 = Box.polyfit(A[R1],C[R1],db[R1],1)
Box.plot_line(fit4.xpl,fit4.ypl)
speed = fit4.par[1]
d_speed = fit4.parameters[1].err

print("\nspeed is %.3E +/- %.3E m/s\n" % (speed, d_speed))
#showing labels on graph
Box.pl.figtext(.3,.8, "speed = %.3E +/- %.3E m/s"%(speed,d_speed))
Box.pl.figtext(.15,.6,"v=(%.3E)$\pm$(%.3E)m/s"%(speed,d_speed))

#more fit lines
fit5 = Box.polyfit(A[R2],C[R2],db[R2],2)
Box.plot_line(fit5.xpl,fit5.ypl)
####
Box.plot_exp(A,C,db)
Box.pl.show()
