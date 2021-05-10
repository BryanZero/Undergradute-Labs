import LT.box as B
import numpy as np
from sympy import *
#from sympy.parsing.latex import parse_latex


def makeDict(names, dataType='.data'):
    Data = {}
    for k in names:
        try:
            if dataType == '.data':
                Data[k] = dict(dataFile=B.get_file(k + dataType))
                Data[k]['Parameters'] = {}
                try:
                    for x in Data[k]['dataFile'].par.get_variable_names():
                        Data[k]['Parameters'][x] = Data[k]['dataFile'].par.get_value(x)
                except:
                    print(k + '.data has no parameters.')
                for j in range(len(Data[k]['dataFile'].get_keys()) - 1):
                    Data[k][Data[k]['dataFile'].get_keys()[j]] = \
                        B.get_data(Data[k]['dataFile'], Data[k]['dataFile'].get_keys()[j])
            elif dataType == '.Spe':
                Data[k] = dict(dataFile=B.get_spectrum(k + dataType))
        except:
            print(k + dataType + ' not found')
    if len(names) == 1: Data = Data[names[0]];
    return Data


def wmean(x, sig):
    w = 1. / sig ** 2
    # weighted mean
    wm = np.sum(x * w) / np.sum(w)
    sig_wm = np.sqrt(1. / np.sum(w))
    return wm, sig_wm


def labels(xlabel='', ylabel='', title='', annotate='', fit=None, xy=(0.5, 0.1), xycoords='axes fraction', sig=.4,
           fontsize=10,parext=None ):
    if xlabel: B.pl.xlabel(xlabel);
    if ylabel: B.pl.ylabel(ylabel);
    if title: B.pl.title(title);
    if annotate:
        # noinspection PyStringFormat
        B.pl.annotate(f'{annotate}\n\n\n', xy=xy, xycoords=xycoords, fontsize=fontsize)
    if fit:
        # noinspection PyStringFormat
        try:
            B.pl.annotate(f'Slope: %{sig}g +/- %{sig}g \nOffset: %{sig}g +/- %{sig}g\n $\chi^2/dof: $ %{sig}g' % (
                fit.slope, fit.sigma_s, fit.offset, fit.sigma_o, fit.chi_red), xy=xy, xycoords=xycoords, fontsize=fontsize)
        except:
            if fit.parameters:
                temp = []
                num=0
                for k in fit.parameters:
                    if not num:
                        B.pl.annotate(f'$\chi^2_r$: %{sig}g' % fit.chi2_red, xy=xy,xycoords=xycoords,fontsize=fontsize)
                    num += 1
                    test = '\n'*num
                    if parext:
                        B.pl.annotate(f'{k.name}: %{sig}g $\pm$ %{sig}g {parext[num]} {test}' % (k.value,k.err),xy=xy,xycoords=xycoords,fontsize=fontsize)
                    else:
                        B.pl.annotate(f'{k.name}: %{sig}g $\pm$ %{sig}g {test}' % (k.value,k.err),xy=xy,xycoords=xycoords,fontsize=fontsize)
def quadrature(*args):
    args2 = (0, 0,
             0) + args  # bug fix, if you don't add a tuple of zeros the next statement adds all the numbers together and doesn't create seperate arrays
    args = np.asarray(args2)
    return np.sqrt(np.sum(args ** 2))

def partials(expression, variables, **values):
    partials = {}
    for k in variables.split():
        locals()[k] = Symbol(k)  # Assign the Symbol as a local variable
    expression = eval(expression)
    partials['Equation'] = latex(expression)
    for k in expression.free_symbols:  # For all the variables in the expression
        partials[str(k)] = {}
        partials[str(k)]['Partial'] = diff(expression,
                                           k)  # Calculate the partial derivative and store it into a dictionary
    if values:
        tmpList = [x for x in expression.free_symbols]
        lambdifyFunction = lambdify(tmpList, expression)
        templist = [i for i, j in zip([str(x) for x in expression.free_symbols], values)]
        results = [values[x] for x in templist]
        partials['OriginalEvaluated'] = lambdifyFunction(*results)

    for k in partials:  # For all the variables in the dictionary
        if not k == 'Equation' and not k == 'OriginalEvaluated':
            if values:
                llist = [x for x in
                         partials[str(k)]['Partial'].free_symbols]  # Get a list of remaining variables in each partial
                tmplambdify = lambdify(llist, partials[str(k)][
                    'Partial'])  # Lambdify the partial which means create a callable function which accepts the variables in llist
                templist = [i for i, j in zip([str(x) for x in partials[str(k)]['Partial'].free_symbols],
                                              values)]  # This was one way to maintain the order, for every symbol in each partial get it's corresponding value.
                results = [values[x] for x in templist]
                partials[str(k)]['Evaluated'] = tmplambdify(*results)
            partials[str(k)]['Partial'] = latex(partials[str(k)]['Partial'])

    return partials
