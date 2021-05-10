from getData import *

files = ['data_1','data_2']
names = ['PMT A','PMT B']
Data = makeDict(files)

fornum = lambda x: range(len(x))


for k in fornum(files):

    currentData = Data[files[k]]
    V = currentData['V']
    C = currentData['counts']
    dC = np.sqrt(C)
    r1 = B.in_window(1200.0, 2000, V)


    B.plot_exp(V[r1], C[r1],dC[r1],label=names[k])

B.pl.title("Plateau PMTs (Counts vs Voltage)")
B.pl.xlabel("Volts")
B.pl.ylabel("Counts")
B.pl.legend()
B.pl.show()