from getData import *

colors = ['yellow', 'green', 'blue', 'violet', 'ultraviolet']
## Windows ranges is just the domain for the 3 individual line fits, its in order according to color and line.
windowRanges = [[0.46, 0.6, .56, .7, .7, 1.1], [0.35, 0.7, 0.54, 0.9, 0.74, 2.2], [0.69, 1.22, 1.0, 1.9, 1.27, 3],
                [0.68, 1.3, 1.0, 1.55, 1.24, 3.5],
                [0.5, 1.0, 0.9, 2.0, 1.5, 3.5]]

Data = makeDict(colors)

# Graphing data for each color
for k in range(len(colors)):
    dataV = Data[colors[k]]['V']
    dataI = Data[colors[k]]['I'] - Data[colors[k]]['Parameters']['ZeroAdjust']
    datadI = Data[colors[k]]['dI'] + Data[colors[k]]['Parameters']['ZeroAdjustSig']

    B.pl.figure(colors[k] + ' Graph')
    B.plot_exp(dataV, dataI, datadI)
    B.pl.xlabel('Voltage (V)')
    B.pl.ylabel('Current (mA)')
    B.pl.title(f'Photo-Current vs Voltage [{colors[k]}]')

    # Getting the ranges and graphing lines for them
    print('#####################################################################')
    print(colors[k])
    tV = B.in_window(windowRanges[k][0], windowRanges[k][1], dataV)
    tV2 = B.linefit(dataV[tV], dataI[tV], datadI[tV])
    B.plot_line(tV2.xpl, tV2.ypl, zorder=3)

    tV3 = B.in_window(windowRanges[k][2], windowRanges[k][3], dataV)
    tV4 = B.linefit(dataV[tV3], dataI[tV3], datadI[tV3])
    B.plot_line(tV4.xpl, tV4.ypl, color='red', zorder=4)

    tV5 = B.in_window(windowRanges[k][4], windowRanges[k][5], dataV)
    tV6 = B.linefit(dataV[tV5], dataI[tV5], datadI[tV5])
    B.plot_line(tV6.xpl, tV6.ypl, color='purple', zorder=5)

    # Finding the x and y intercept by using basic y=mx+b manipulation, storing and then plotting them.
    xintercept = (tV6.offset - tV2.offset) / (tV2.slope - tV6.slope)
    yintercept = (tV2.slope * xintercept + tV2.offset)

    xintercept2 = (tV6.offset - tV4.offset) / (tV4.slope - tV6.slope)
    yintercept2 = (tV4.slope * xintercept2 + tV4.offset)

    B.pl.plot(xintercept, yintercept, 'bo', zorder=6)
    B.pl.plot(xintercept2, yintercept2, 'bo', zorder=6)
    B.pl.plot([xintercept,xintercept2],[yintercept,yintercept2],'r--')

    ### Storing data into dictionary
    Data[colors[k]]['xint1'] = xintercept
    Data[colors[k]]['yint1'] = yintercept
    Data[colors[k]]['xint2'] = xintercept2
    Data[colors[k]]['yint2'] = yintercept2
    Data[colors[k]]['x_mean'] = ((xintercept2-xintercept)/2) + xintercept

    ##Adding uncertainties of slopes in quadrature
    sigmaint1 = quadrature(tV2.sigma_s,tV4.sigma_s,tV4.sigma_o,tV6.sigma_o)
    sigmaint2 = quadrature(tV4.sigma_s,tV6.sigma_s,tV4.sigma_o,tV6.sigma_o)

    sigmatotal = quadrature((xintercept2-xintercept)/2)
    B.pl.annotate('Intercept of lines: (%.2f,%.2f)  +/- %.3f\nIntercept of lines: (%.2f,%.2f)  +/- %.3f' % (
        xintercept, yintercept, sigmaint1, xintercept2, yintercept2, sigmaint2), xy=(.38, .9),
                  xycoords='axes fraction')
    Data[colors[k]]['sigmatotal'] = sigmatotal

###################################  END OF FOR LOOP   ##############################
print('########################################################')
B.pl.figure('Energy vs Frequency')
wavelengths = np.array([578, 546, 436, 405, 365]) * (1e-9)
sigmawavelength = np.cbrt(wavelengths)
frequency = 3e8 / (wavelengths)
frequencysigma = 3e8 / (sigmawavelength)
## A little bit of list comprehension, you could've done the same thing in a regular for loop.
B.plot_exp(frequency, [Data[x]['x_mean'] for x in colors], [Data[x]['sigmatotal'] for x in colors],xerr=frequencysigma)
fit = B.linefit(frequency, np.asarray([Data[x]['x_mean'] for x in colors]),
                np.asarray([Data[x]['sigmatotal'] for x in colors]))
B.plot_line(fit.xpl, fit.ypl, label='Experimental Values')


################################ PLOTTING ACCEPTED VALUE LINE ###########################
x = np.linspace(5e14, 9e14)
y = 4.135667696e-15 * x - 1.53
B.pl.plot(x, y, 'r--', label='Accepted Slope Value (Offset is experimental @-1.53)')
##########################################################################################

B.pl.legend(loc='best', prop={'size': 8})
labels('Frequency (Hz)','Stopping Voltage ($eV$)','Energy vs Frequency','$hf-\phi = eV_s$',fit,xy=(0.5,0.07),sig=.3)
