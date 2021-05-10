from getData import *

Data = makeDict(['Data'])
DataP = Data['Parameters']
DataP['D3'] = DataP['D1'] + DataP['D2']
DataP['dD3'] = DataP['dD1'] + DataP['dD2']
# Data adjustment might vary depending on data collection
Data['x'] = Data['x'] * 0.001 * 0.01
Data['dx'] = Data['dx'] * 0.001 * 0.01
### Adding uncertainty in radius of beam in quadrature
Data['dx'] = quadrature(Data['dx'], 0.000025)
Data['fr'] = Data['fr'] * 2 * np.pi
Data['dfr'] = Data['dfr'] * 2 * np.pi

B.pl.figure('Speed of Light')
B.plot_exp(Data['fr'], Data['x'], Data['dx'], xerr=Data['dfr'])
fit = B.linefit(Data['fr'], Data['x'], Data['dx'])
B.plot_line(fit.xpl, fit.ypl)

labels('$\omega\ Angular\ Frequency\ (rads/sec)$', '$\Delta x\ (meters)$', '$\Delta x\ vs\ \omega$',
       '$\Delta x = 4f_2D_3 \\frac{\omega}{c} $',
       fit=fit,sig=.3)

# Uncertainties and partials yay!
slope_partials = partials('4*f2*D3/S', 'f2 D3 S', f2=DataP['f2'], D3=DataP['D3'], S=fit.slope)
eq_partials = partials('f2*4*f*D3/x', 'f2 f D3 x', f2=DataP['f2'], f=Data['fr'], D3=DataP['D3'], x=Data['x'])

c_exp1 = DataP['f2'] * 4 * Data['fr'] * DataP['D3'] / Data['x']
# Adding partials in quadrature
partx = (eq_partials['x']['Evaluated'] * Data['dx'])
partD3 = (eq_partials['D3']['Evaluated'] * DataP['dD3'])
partf = (eq_partials['f']['Evaluated'] * Data['dfr'])
partf2 = (eq_partials['f2']['Evaluated'] * DataP['df2'])

sigmatotal = quadrature(partx, partD3, partf, partf2)

# Getting weighted mean of data
results = wmean(c_exp1, sigmatotal)
print('\n\n############# WEIGHTED MEAN C VALUE #################\n' + str(
    np.format_float_scientific(results[0])) + ' +/- ' + str(np.format_float_scientific(results[1])))

# Calculating C value from graph
c_exp2 = (4 * DataP['f2'] * (DataP['D3'])) / fit.slope
### Uncertainty for slope method
part1 = slope_partials['f2']['Evaluated'] * DataP['df2']
part2 = slope_partials['D3']['Evaluated'] * DataP['dD3']
part3 = slope_partials['S']['Evaluated'] * fit.sigma_s

c_exp2_uncertainty = quadrature(part1, part2, part3)
print('########### GRAPH C VALUE #############\n' + str(np.format_float_scientific(c_exp2)) + ' +/- ' + str(
    np.format_float_scientific(c_exp2_uncertainty)) + '\n\n')

B.pl.show()
