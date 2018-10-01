# -*- coding: utf-8 -*-
r"""
Script permettant de tracer les graphiques pour la mesure d'antenne des cavités  (couplage vs. longueur d'antenne)

Created on Tue Jul 17 16:53:25 2018

@author: luboz
se placer dans cd C:/Users/luboz.IPN/Documents/Projets/Test multi-mode/Python
"""
#%% Import des packages
import numpy as np 
import pandas as pd
from uncertainties import ufloat
from fonctions import * #C:/Users/luboz.IPN/Documents/Projets/Test multi-mode/Python/fonctions.py
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import rc
import matplotlib as mpl
import uncertainties
from uncertainties import unumpy
import matplotlib.ticker

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         #r"\usepackage{cmbright}",
         ]
}
mpl.rcParams.update(pgf_with_pdflatex)
del(pgf_with_pdflatex)
    
#%% Définitions des constantes
largeurPlot = 16.9672 * 0.393701; #largeur en inch
ratioPlot = 4/3;
hauteurPlot = largeurPlot/ratioPlot;
(xmin, xmax) = (-10, 150)
(ymin, ymax) = (1e3, 1e15)

#%% Type A uncertainty sur un set de données. MANUEL
if False:#True or False pour l'utiliser
    vecteur = np.array([]) #freq en MHz, longueurs en mm, atténuations en dB
    # ajout d'autres sources d'incertitudes pour les atténuations.
    #err = [0.008] # (10 MHz à 3 GHz)
    #err = [0.018] # (3 GHz à 6 GHz)
    
    # ajout d'autres sources d'incertitudes pour les fréquences (5e-4 MHz pour le Delta f)
    #stepsize = 0.00125 #stepsize (MHz) désigné par l'appareil en fonction du span et du nombre de points
    #err = [5e-4,stepsize]
    #err = [0.0007071067811865475,stepsize] # err pour le delta f (différence de deux fréquences)
    
    # ajout d'autres sources d'incertitudes pour les longueurs mesurées au pied à coulisse de précision 3/100
    #err = [0.03]
    
    meas = typeAUncertainty(vecteur,err, verbose = True, save = True, path = "output_m.txt", wtw = 'mean')
    meas = typeAUncertainty(vecteur,err, verbose = True, save = True, path = "output_s.txt", wtw = 'std')

#%% Import des datas
# À 352 MHz
C2_352 = couplingCalculator('Data/C2@352.csv', 'sur')
F2_352 = couplingCalculator('Data/F2@352.csv', 'sur')

F1_352_david = couplingCalculator('Data/david_F1_352.csv', 'sur')
C1_352_david = couplingCalculator('Data/david_C1_352.csv', 'sous')

# À 721 MHz
C2_721 = couplingCalculator('Data/C2@721MHz.csv', 'sous')
F2_721 = couplingCalculator('Data/F2@721MHz.csv', 'sous')

# À 1314 MHz
C2_1314_7C = couplingCalculator('Data/C2@1314MHz_7C.csv', 'sous')
F2_1314_7C = couplingCalculator('Data/F2@1314MHz_7C.csv', 'sous')
C2_1314_7D = couplingCalculator('Data/C2@1314MHz_7D.csv', 'sous')
F2_1314_7D = couplingCalculator('Data/F2@1314MHz_7D.csv', 'sous')

#%% Fits
# 352 MHz
(popt_C2_352, pcov_C2_352) = curve_fit(expfit, xdata = unumpy.nominal_values(C2_352.iloc[0:3,0]), ydata = unumpy.nominal_values(C2_352.iloc[0:3,7]), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_352.iloc[0:3,7]))
x_th_C2_352 = np.linspace(10,90,5)
popt_F2_352, pcov_F2_352 = curve_fit(expfit, xdata = unumpy.nominal_values(F2_352['Lt (mm)']), ydata = unumpy.nominal_values(F2_352['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_352['Qt']))
x_th_F2_352 = np.linspace(10,140,5)

popt_C1_352_david, pcov_C1_352_david = curve_fit(expfit, xdata = unumpy.nominal_values(C1_352_david.iloc[0:3,0]), ydata = unumpy.nominal_values(C1_352_david.iloc[0:3,7]), p0 = [6.7915e17,0.183818])
x_th_C1_352_david = np.linspace(10,90,5)
popt_F1_352_david, pcov_F1_352_david = curve_fit(expfit, xdata = unumpy.nominal_values(F1_352_david['Lt (mm)']), ydata = unumpy.nominal_values(F1_352_david['Qt']), p0 = [3.4e13,0.172588])
x_th_F1_352_david = np.linspace(10,140,5)

# 721 MHz
popt_C2_721, pcov_C2_721 = curve_fit(expfit, xdata = unumpy.nominal_values(C2_721['Lt (mm)']), ydata = unumpy.nominal_values(C2_721['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_721['Qt']))
x_th_C2_721 = np.linspace(10,90,5)
popt_F2_721, pcov_F2_721 = curve_fit(expfit, xdata = unumpy.nominal_values(F2_721['Lt (mm)']), ydata = unumpy.nominal_values(F2_721['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_721['Qt']))
x_th_F2_721 = np.linspace(10,140,5)

# 1314 MHz mode 7C
popt_C2_1314_7C, pcov_C2_1314_7C = curve_fit(expfit, xdata = unumpy.nominal_values(C2_1314_7C.iloc[0:4,0]), ydata = unumpy.nominal_values(C2_1314_7C.iloc[0:4,7]), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_1314_7C.iloc[0:4,7]))
x_th_C2_1314_7C = np.linspace(0,35,5)
popt_F2_1314_7C, pcov_F2_1314_7C = curve_fit(expfit, xdata = unumpy.nominal_values(F2_1314_7C['Lt (mm)']), ydata = unumpy.nominal_values(F2_1314_7C['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_1314_7C['Qt']))
x_th_F2_1314_7C = np.linspace(10,120,5)

# 1314 MHz mode 7D
popt_C2_1314_7D, pcov_C2_1314_7D = curve_fit(expfit, xdata = unumpy.nominal_values(C2_1314_7D.iloc[0:4,0]), ydata = unumpy.nominal_values(C2_1314_7D.iloc[0:4,7]), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_1314_7D.iloc[0:4,7]))
x_th_C2_1314_7D = np.linspace(0,32,5)
popt_F2_1314_7D, pcov_F2_1314_7D = curve_fit(expfit, xdata = unumpy.nominal_values(F2_1314_7D['Lt (mm)']), ydata = unumpy.nominal_values(F2_1314_7D['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_1314_7D['Qt']))
x_th_F2_1314_7D = np.linspace(30,110,5)

#%% Plots
#%% À 352 MHz
plt.figure(num='Qt vs. Lt @ 352 MHz', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(C2_352['Lt (mm)']),unumpy.nominal_values(C2_352['Qt']),'r.', label= 'C2 @ 352 MHz')
plt.plot(unumpy.nominal_values(F2_352['Lt (mm)']),unumpy.nominal_values(F2_352['Qt']),'b.', label= 'F2 @ 352 MHz')

plt.plot(x_th_C2_352, expfit(x_th_C2_352, *popt_C2_352),'r--',label= fr'${ufloat(popt_C2_352[0],np.sqrt(np.diag(pcov_C2_352))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_352[1],np.sqrt(np.diag(pcov_C2_352))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_F2_352, expfit(x_th_F2_352, *popt_F2_352),'b--',label= fr'${ufloat(popt_F2_352[0],np.sqrt(np.diag(pcov_F2_352))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_352[1],np.sqrt(np.diag(pcov_F2_352))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.errorbar(unumpy.nominal_values(C2_352['Lt (mm)']),unumpy.nominal_values(C2_352['Qt']), xerr = unumpy.std_devs(C2_352['Lt (mm)']) , yerr = unumpy.std_devs(C2_352['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_352['Lt (mm)']),unumpy.nominal_values(F2_352['Qt']), xerr = unumpy.std_devs(F2_352['Lt (mm)']) , yerr = unumpy.std_devs(F2_352['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
#plt.yticks(np.logspace(np.log10(ymin),np.log10(ymax),num=np.log10(ymax)-np.log10(ymin)+1, endpoint=True))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))

plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation des ports C2 et F2 en transmission \`{a} 352 MHz")
plt.tight_layout()#pour séparer un peu les plots
    
name = "QtVsLt_352MHz"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% À 352 MHz David
plt.figure(num='Qt vs. Lt @ 352 MHz david', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(C1_352_david['Lt (mm)']),unumpy.nominal_values(C1_352_david['Qt']),'r.', label= 'C1 @ 352 MHz')
plt.plot(unumpy.nominal_values(F1_352_david['Lt (mm)']),unumpy.nominal_values(F1_352_david['Qt']),'b.', label= 'F1 @ 352 MHz')

plt.plot(x_th_C1_352_david, expfit(x_th_C1_352_david, *popt_C1_352_david),'r--',label= fr'${ufloat(popt_C1_352_david[0],np.sqrt(np.diag(pcov_C1_352_david))[0]):.2uSL}\times \exp(-{ufloat(popt_C1_352_david[1],np.sqrt(np.diag(pcov_C1_352_david))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_F1_352_david, expfit(x_th_F1_352_david, *popt_F1_352_david),'b--',label= fr'${ufloat(popt_F1_352_david[0],np.sqrt(np.diag(pcov_F1_352_david))[0]):.2uSL}\times \exp(-{ufloat(popt_F1_352_david[1],np.sqrt(np.diag(pcov_F1_352_david))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')
    

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))

plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Mesures de David \`{a} 352 MHz")
plt.tight_layout()#pour séparer un peu les plots
    
name = "QtVsLt_352MHz_david"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% À 721 MHz
plt.figure(num='Qt vs. Lt @ 721 MHz', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(C2_721['Lt (mm)']),unumpy.nominal_values(C2_721['Qt']),'r.', label= 'C2 @ 721 MHz')
plt.plot(unumpy.nominal_values(F2_721['Lt (mm)']),unumpy.nominal_values(F2_721['Qt']),'b.', label= 'F2 @ 721 MHz')

plt.plot(x_th_C2_721, expfit(x_th_C2_721, *popt_C2_721),'r--', label= fr'${ufloat(popt_C2_721[0],np.sqrt(np.diag(pcov_C2_721))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_721[1],np.sqrt(np.diag(pcov_C2_721))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_F2_721, expfit(x_th_F2_721, *popt_F2_721),'b--', label= fr'${ufloat(popt_F2_721[0],np.sqrt(np.diag(pcov_F2_721))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_721[1],np.sqrt(np.diag(pcov_F2_721))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(unumpy.nominal_values(C2_721['Lt (mm)']),unumpy.nominal_values(C2_721['Qt']), xerr = unumpy.std_devs(C2_721['Lt (mm)']) , yerr = unumpy.std_devs(C2_721['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_721['Lt (mm)']),unumpy.nominal_values(F2_721['Qt']), xerr = unumpy.std_devs(F2_721['Lt (mm)']) , yerr = unumpy.std_devs(F2_721['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation des ports C2 et F2 en transmission \`{a} 721 MHz")
plt.tight_layout()#pour séparer un peu les plots
    
name = "QtVsLt_721MHz"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% À 1314 MHz mode 7C
plt.figure(num='Qt vs. Lt @ 1314 MHz mode 7C', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(C2_1314_7C['Lt (mm)']),unumpy.nominal_values(C2_1314_7C['Qt']),'r.', label= 'C2 @ 1314 MHz (7C)')
plt.plot(unumpy.nominal_values(F2_1314_7C['Lt (mm)']),unumpy.nominal_values(F2_1314_7C['Qt']),'b.', label= 'F2 @ 1314 MHz (7C)')

plt.plot(x_th_C2_1314_7C, expfit(x_th_C2_1314_7C, *popt_C2_1314_7C),'r--', label= fr'${ufloat(popt_C2_1314_7C[0],np.sqrt(np.diag(pcov_C2_1314_7C))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_1314_7C[1],np.sqrt(np.diag(pcov_C2_1314_7C))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_F2_1314_7C, expfit(x_th_F2_1314_7C, *popt_F2_1314_7C),'b--', label= fr'${ufloat(popt_F2_1314_7C[0],np.sqrt(np.diag(pcov_F2_1314_7C))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_1314_7C[1],np.sqrt(np.diag(pcov_F2_1314_7C))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(unumpy.nominal_values(C2_1314_7C['Lt (mm)']),unumpy.nominal_values(C2_1314_7C['Qt']), xerr = unumpy.std_devs(C2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7C['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_1314_7C['Lt (mm)']),unumpy.nominal_values(F2_1314_7C['Qt']), xerr = unumpy.std_devs(F2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7C['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation des ports C2 et F2 en transmission \`{a} 1314 MHz (mode 7C)")
plt.tight_layout()#pour séparer un peu les plots
    
name = "QtVsLt_1314MHz_7C"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% À 1314 MHz mode 7D
plt.figure(num='Qt vs. Lt @ 1314 MHz mode 7D', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(C2_1314_7D['Lt (mm)']),unumpy.nominal_values(C2_1314_7D['Qt']),'r.', label= 'C2 @ 1314 MHz (7D)')
plt.plot(unumpy.nominal_values(F2_1314_7D['Lt (mm)']),unumpy.nominal_values(F2_1314_7D['Qt']),'b.', label= 'F2 @ 1314 MHz (7D)')

plt.plot(x_th_C2_1314_7D, expfit(x_th_C2_1314_7D, *popt_C2_1314_7D),'r--', label= fr'${ufloat(popt_C2_1314_7D[0],np.sqrt(np.diag(pcov_C2_1314_7D))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_1314_7D[1],np.sqrt(np.diag(pcov_C2_1314_7D))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_F2_1314_7D, expfit(x_th_F2_1314_7D, *popt_F2_1314_7D),'b--', label= fr'${ufloat(popt_F2_1314_7D[0],np.sqrt(np.diag(pcov_F2_1314_7D))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_1314_7D[1],np.sqrt(np.diag(pcov_F2_1314_7D))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend(loc = 'lower right')

plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(unumpy.nominal_values(C2_1314_7D['Lt (mm)']),unumpy.nominal_values(C2_1314_7D['Qt']), xerr = unumpy.std_devs(C2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7D['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_1314_7D['Lt (mm)']),unumpy.nominal_values(F2_1314_7D['Qt']), xerr = unumpy.std_devs(F2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7D['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation des ports C2 et F2 en transmission \`{a} 1314 MHz (mode 7D)")
plt.tight_layout()#pour séparer un peu les plots

    
name = "QtVsLt_1314MHz_7D"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% Sur port C2
plt.figure(num='Port C2', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(C2_352['Lt (mm)']),unumpy.nominal_values(C2_352['Qt']),'r*', label= 'C2 @ 352 MHz')
plt.plot(unumpy.nominal_values(C2_721['Lt (mm)']),unumpy.nominal_values(C2_721['Qt']),'ro', label= 'C2 @ 721 MHz')
plt.plot(unumpy.nominal_values(C2_1314_7C['Lt (mm)']),unumpy.nominal_values(C2_1314_7C['Qt']),'r^', label= 'C2 @ 1314 MHz (7C)')
plt.plot(unumpy.nominal_values(C2_1314_7D['Lt (mm)']),unumpy.nominal_values(C2_1314_7D['Qt']),'rv', label= 'C2 @ 1314 MHz (7D)')

plt.plot(x_th_C2_352, expfit(x_th_C2_352, *popt_C2_352),'r-',label= fr'${ufloat(popt_C2_352[0],np.sqrt(np.diag(pcov_C2_352))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_352[1],np.sqrt(np.diag(pcov_C2_352))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_C2_721, expfit(x_th_C2_721, *popt_C2_721),'r--', label= fr'${ufloat(popt_C2_721[0],np.sqrt(np.diag(pcov_C2_721))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_721[1],np.sqrt(np.diag(pcov_C2_721))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_C2_1314_7C, expfit(x_th_C2_1314_7C, *popt_C2_1314_7C),'r-.', label= fr'${ufloat(popt_C2_1314_7C[0],np.sqrt(np.diag(pcov_C2_1314_7C))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_1314_7C[1],np.sqrt(np.diag(pcov_C2_1314_7C))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_C2_1314_7D, expfit(x_th_C2_1314_7D, *popt_C2_1314_7D),'r:', label= fr'${ufloat(popt_C2_1314_7D[0],np.sqrt(np.diag(pcov_C2_1314_7D))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_1314_7D[1],np.sqrt(np.diag(pcov_C2_1314_7D))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.errorbar(unumpy.nominal_values(C2_352['Lt (mm)']),unumpy.nominal_values(C2_352['Qt']), xerr = unumpy.std_devs(C2_352['Lt (mm)']) , yerr = unumpy.std_devs(C2_352['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(C2_721['Lt (mm)']),unumpy.nominal_values(C2_721['Qt']), xerr = unumpy.std_devs(C2_721['Lt (mm)']) , yerr = unumpy.std_devs(C2_721['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(C2_1314_7C['Lt (mm)']),unumpy.nominal_values(C2_1314_7C['Qt']), xerr = unumpy.std_devs(C2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7C['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(C2_1314_7D['Lt (mm)']),unumpy.nominal_values(C2_1314_7D['Qt']), xerr = unumpy.std_devs(C2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7D['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation du ports C2 en transmission pour les quatre modes")
plt.tight_layout()#pour séparer un peu les plots
    
name = "QtVsLt_C2"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% Sur port F2
plt.figure(num='Port F2', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(F2_352['Lt (mm)']),unumpy.nominal_values(F2_352['Qt']),'b*', label= 'F2 @ 352 MHz')
plt.plot(unumpy.nominal_values(F2_721['Lt (mm)']),unumpy.nominal_values(F2_721['Qt']),'bo', label= 'F2 @ 721 MHz')
plt.plot(unumpy.nominal_values(F2_1314_7C['Lt (mm)']),unumpy.nominal_values(F2_1314_7C['Qt']),'b^', label= 'F2 @ 1314 MHz (7C)')
plt.plot(unumpy.nominal_values(F2_1314_7D['Lt (mm)']),unumpy.nominal_values(F2_1314_7D['Qt']),'bv', label= 'F2 @ 1314 MHz (7D)')

plt.plot(x_th_F2_352, expfit(x_th_F2_352, *popt_F2_352),'b-',label= fr'${ufloat(popt_F2_352[0],np.sqrt(np.diag(pcov_F2_352))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_352[1],np.sqrt(np.diag(pcov_F2_352))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_F2_721, expfit(x_th_F2_721, *popt_F2_721),'b--', label= fr'${ufloat(popt_F2_721[0],np.sqrt(np.diag(pcov_F2_721))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_721[1],np.sqrt(np.diag(pcov_F2_721))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_F2_1314_7C, expfit(x_th_F2_1314_7C, *popt_F2_1314_7C),'b-.', label= fr'${ufloat(popt_F2_1314_7C[0],np.sqrt(np.diag(pcov_F2_1314_7C))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_1314_7C[1],np.sqrt(np.diag(pcov_F2_1314_7C))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(x_th_F2_1314_7D, expfit(x_th_F2_1314_7D, *popt_F2_1314_7D),'b:', label= fr'${ufloat(popt_F2_1314_7D[0],np.sqrt(np.diag(pcov_F2_1314_7D))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_1314_7D[1],np.sqrt(np.diag(pcov_F2_1314_7D))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.errorbar(unumpy.nominal_values(F2_352['Lt (mm)']),unumpy.nominal_values(F2_352['Qt']), xerr = unumpy.std_devs(F2_352['Lt (mm)']) , yerr = unumpy.std_devs(F2_352['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')
plt.errorbar(unumpy.nominal_values(F2_721['Lt (mm)']),unumpy.nominal_values(F2_721['Qt']), xerr = unumpy.std_devs(F2_721['Lt (mm)']) , yerr = unumpy.std_devs(F2_721['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')
plt.errorbar(unumpy.nominal_values(F2_1314_7C['Lt (mm)']),unumpy.nominal_values(F2_1314_7C['Qt']), xerr = unumpy.std_devs(F2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7C['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')
plt.errorbar(unumpy.nominal_values(F2_1314_7D['Lt (mm)']),unumpy.nominal_values(F2_1314_7D['Qt']), xerr = unumpy.std_devs(F2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7D['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation du ports F2 en transmission pour les quatre modes")
plt.tight_layout()#pour séparer un peu les plots
    
name = "QtVsLt_F2"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% Sur port C2 juste les lignes
plt.figure(num='Port C2', figsize = (largeurPlot, hauteurPlot))
plt.plot(x_th_C2_352, expfit(x_th_C2_352, *popt_C2_352),'r-',label= 'C2 @ 352 MHz')
plt.plot(x_th_C2_721, expfit(x_th_C2_721, *popt_C2_721),'r--', label= 'C2 @ 721 MHz')
plt.plot(x_th_C2_1314_7C, expfit(x_th_C2_1314_7C, *popt_C2_1314_7C),'r-.', label= 'C2 @ 1314 MHz (7C)')
plt.plot(x_th_C2_1314_7D, expfit(x_th_C2_1314_7D, *popt_C2_1314_7D),'r:', label= 'C2 @ 1314 MHz (7D)')

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation du ports C2 en transmission pour les quatre modes")
plt.tight_layout()#pour séparer un peu les plots
    
name = "QtVsLt_C2_lines"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% Sur port F2 juste les lignes
plt.figure(num='Port F2', figsize = (largeurPlot, hauteurPlot))
plt.plot(x_th_F2_352, expfit(x_th_F2_352, *popt_F2_352),'b-',label= 'F2 @ 352 MHz')
plt.plot(x_th_F2_721, expfit(x_th_F2_721, *popt_F2_721),'b--', label= 'F2 @ 721 MHz')
plt.plot(x_th_F2_1314_7C, expfit(x_th_F2_1314_7C, *popt_F2_1314_7C),'b-.', label= 'F2 @ 1314 MHz (7C)')
plt.plot(x_th_F2_1314_7D, expfit(x_th_F2_1314_7D, *popt_F2_1314_7D),'b:', label= 'F2 @ 1314 MHz (7D)')

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation du ports F2 en transmission pour les quatre modes")
plt.tight_layout()#pour séparer un peu les plots

name = "QtVsLt_F2_lines"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% Import du fichier facteurs Q et ajout des colonnes comportant les coefficients de fit.
facteursQ = pd.read_csv('Data/facteursQ.csv', skiprows=0, error_bad_lines=False)
#facteursQ.drop(facteursQ.index[4]) #je supprime la ligne 4 correspondant au mode 7B inexploité pour l'instant.
#les coefficients du mode 7B tels que égaux à ceux de 7C
popt_C2_1314_7B = popt_C2_1314_7C
popt_F2_1314_7B = popt_F2_1314_7C
# import des colonnes a et b
facteursQ['a C2'] = [popt_C2_352[0], popt_C2_721[0], popt_C2_1314_7C[0], popt_C2_1314_7D[0], popt_C2_1314_7B[0]]
facteursQ['b C2'] = [popt_C2_352[1], popt_C2_721[1], popt_C2_1314_7C[1], popt_C2_1314_7D[1], popt_C2_1314_7B[1]]
facteursQ['a F2'] = [popt_F2_352[0], popt_F2_721[0], popt_F2_1314_7C[0], popt_F2_1314_7D[0], popt_F2_1314_7B[0]]
facteursQ['b F2'] = [popt_F2_352[1], popt_F2_721[1], popt_F2_1314_7C[1], popt_F2_1314_7D[1], popt_F2_1314_7B[1]]
facteursQ.to_csv('Data/facteursQ.csv',index = False)


#%% Sur port C2 FINAL
xmax = 170
xendlines = 110
liBool = False
ltBool = True

plt.figure(num='Port C final', figsize = (largeurPlot, hauteurPlot))
plt.plot(x_th_C2_352, expfit(x_th_C2_352, *popt_C2_352),'r-',label = 'C2 @ 352 MHz', linewidth = 1)
plt.plot(x_th_C2_721, expfit(x_th_C2_721, *popt_C2_721),'r--', label = 'C2 @ 721 MHz', linewidth = 1)
plt.plot(x_th_C2_1314_7C, expfit(x_th_C2_1314_7C, *popt_C2_1314_7C),'r-.', label = 'C2 @ 1314 MHz (7C)', linewidth = 1)
plt.plot(x_th_C2_1314_7D, expfit(x_th_C2_1314_7D, *popt_C2_1314_7D),'r:', label = 'C2 @ 1314 MHz (7D)', linewidth = 1)
#plt.plot(x_th_C2_1314_7C, expfit(x_th_C2_1314_7C, *popt_C2_1314_7B),'r:', label = 'C2 @ 1314 MHz (7B)', linewidth = 1)

plt.errorbar(unumpy.nominal_values(C2_352['Lt (mm)']),unumpy.nominal_values(C2_352['Qt']), xerr = unumpy.std_devs(C2_352['Lt (mm)']) , yerr = unumpy.std_devs(C2_352['Qt']), fmt='r*', ecolor = 'k', elinewidth = 1, capsize = 1)
plt.errorbar(unumpy.nominal_values(C2_721['Lt (mm)']),unumpy.nominal_values(C2_721['Qt']), xerr = unumpy.std_devs(C2_721['Lt (mm)']) , yerr = unumpy.std_devs(C2_721['Qt']), fmt='ro', ecolor = 'k', elinewidth = 1, capsize = 1)
plt.errorbar(unumpy.nominal_values(C2_1314_7C['Lt (mm)']),unumpy.nominal_values(C2_1314_7C['Qt']), xerr = unumpy.std_devs(C2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7C['Qt']), fmt='r^', ecolor = 'k', elinewidth = 1, capsize = 1)
plt.errorbar(unumpy.nominal_values(C2_1314_7D['Lt (mm)']),unumpy.nominal_values(C2_1314_7D['Qt']), xerr = unumpy.std_devs(C2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7D['Qt']), fmt='rv', ecolor = 'k', elinewidth = 1, capsize = 1)

# tracé des lignes - lignes horizontales Q_0 (4.2K) - noir
if liBool:
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['Q_0 (4.2K)'][0] / facteursQ['a C2'][0]) / facteursQ['b C2'][0]], [facteursQ['Q_0 (4.2K)'][0], facteursQ['Q_0 (4.2K)'][0]], linestyle='-', color='k', label = '$Q_0$(4.2 K)')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['Q_0 (4.2K)'][0] / facteursQ['a C2'][0]) / facteursQ['b C2'][0], xendlines], [facteursQ['Q_0 (4.2K)'][0], facteursQ['Q_0 (4.2K)'][0]], linestyle='--', color='k')) #ligne à Q_0(4K) 352 MHz
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['Q_0 (4.2K)'][1] / facteursQ['a C2'][1]) / facteursQ['b C2'][1]], [facteursQ['Q_0 (4.2K)'][1], facteursQ['Q_0 (4.2K)'][1]], linestyle='-', color='k')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['Q_0 (4.2K)'][1] / facteursQ['a C2'][1]) / facteursQ['b C2'][1], xendlines], [facteursQ['Q_0 (4.2K)'][1], facteursQ['Q_0 (4.2K)'][1]], linestyle='--', color='k')) #ligne à Q_0(4K) 721 MHz
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['Q_0 (4.2K)'][2] / facteursQ['a C2'][2]) / facteursQ['b C2'][2]], [facteursQ['Q_0 (4.2K)'][2], facteursQ['Q_0 (4.2K)'][2]], linestyle='-', color='k')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['Q_0 (4.2K)'][2] / facteursQ['a C2'][2]) / facteursQ['b C2'][2], xendlines], [facteursQ['Q_0 (4.2K)'][2], facteursQ['Q_0 (4.2K)'][2]], linestyle='--', color='k')) #ligne à Q_0(4K) 7C
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['Q_0 (4.2K)'][3] / facteursQ['a C2'][3]) / facteursQ['b C2'][3]], [facteursQ['Q_0 (4.2K)'][3], facteursQ['Q_0 (4.2K)'][3]], linestyle='-', color='k')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['Q_0 (4.2K)'][3] / facteursQ['a C2'][3]) / facteursQ['b C2'][3], xendlines], [facteursQ['Q_0 (4.2K)'][3], facteursQ['Q_0 (4.2K)'][3]], linestyle='--', color='k')) #ligne à Q_0(4K) 7D
#    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['Q_0 (4.2K)'][4] / facteursQ['a C2'][4]) / facteursQ['b C2'][4]], [facteursQ['Q_0 (4.2K)'][4], facteursQ['Q_0 (4.2K)'][4]], linestyle='-', color='k')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['Q_0 (4.2K)'][4] / facteursQ['a C2'][4]) / facteursQ['b C2'][4], xendlines], [facteursQ['Q_0 (4.2K)'][4], facteursQ['Q_0 (4.2K)'][4]], linestyle='--', color='k')) #ligne à Q_0(4K) 7B
    plt.plot(-np.log(facteursQ['Q_0 (4.2K)'] / facteursQ['a C2']) / facteursQ['b C2'], facteursQ['Q_0 (4.2K)'],color='k',marker='s', linestyle='', label = 'intersection rouge/noir')
    
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][0]/10 / facteursQ['a C2'][0]) / facteursQ['b C2'][0]], [facteursQ['10Q_0(2K)'][0]/10, facteursQ['10Q_0(2K)'][0]/10], linestyle='-', color='c', label = r'$Q_0$(2 K)')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][0]/10 / facteursQ['a C2'][0]) / facteursQ['b C2'][0], xendlines], [facteursQ['10Q_0(2K)'][0]/10, facteursQ['10Q_0(2K)'][0]/10], linestyle='--', color='c')) #ligne à Q_0(4K) 352 MHz
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][1]/10 / facteursQ['a C2'][1]) / facteursQ['b C2'][1]], [facteursQ['10Q_0(2K)'][1]/10, facteursQ['10Q_0(2K)'][1]/10], linestyle='-', color='c')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][1]/10 / facteursQ['a C2'][1]) / facteursQ['b C2'][1], xendlines + 30], [facteursQ['10Q_0(2K)'][1]/10, facteursQ['10Q_0(2K)'][1]/10], linestyle='--', color='c')) #ligne à Q_0(4K) 721 MHz
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][2]/10 / facteursQ['a C2'][2]) / facteursQ['b C2'][2]], [facteursQ['10Q_0(2K)'][2]/10, facteursQ['10Q_0(2K)'][2]/10], linestyle='-', color='c')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][2]/10 / facteursQ['a C2'][2]) / facteursQ['b C2'][2], xendlines], [facteursQ['10Q_0(2K)'][2]/10, facteursQ['10Q_0(2K)'][2]/10], linestyle='--', color='c')) #ligne à Q_0(4K) 7C
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][3]/10 / facteursQ['a C2'][3]) / facteursQ['b C2'][3]], [facteursQ['10Q_0(2K)'][3]/10, facteursQ['10Q_0(2K)'][3]/10], linestyle='-', color='c')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][3]/10 / facteursQ['a C2'][3]) / facteursQ['b C2'][3], xendlines], [facteursQ['10Q_0(2K)'][3]/10, facteursQ['10Q_0(2K)'][3]/10], linestyle='--', color='c')) #ligne à Q_0(4K) 7D
#    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][4]/10 / facteursQ['a C2'][4]) / facteursQ['b C2'][4]], [facteursQ['10Q_0(2K)'][4]/10, facteursQ['10Q_0(2K)'][4]/10], linestyle='-', color='c')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][4]/10 / facteursQ['a C2'][4]) / facteursQ['b C2'][4], xendlines], [facteursQ['10Q_0(2K)'][4]/10, facteursQ['10Q_0(2K)'][4]/10], linestyle='--', color='c')) #ligne à Q_0(4K) 7B
    plt.plot(-np.log(facteursQ['10Q_0(2K)']/10 / facteursQ['a C2']) / facteursQ['b C2'], facteursQ['10Q_0(2K)']/10,color='c',marker='s', linestyle='', label = 'intersection rouge/cyan')

    
# - lignes horizontales 10Q_0 (2K) - magenta
if ltBool:
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][0] / facteursQ['a C2'][0]) / facteursQ['b C2'][0]], [facteursQ['10Q_0(2K)'][0], facteursQ['10Q_0(2K)'][0]], linestyle='-', color='m', label = r'$10\times Q_0$(2 K)')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][0] / facteursQ['a C2'][0]) / facteursQ['b C2'][0], xendlines], [facteursQ['10Q_0(2K)'][0], facteursQ['10Q_0(2K)'][0]], linestyle='--', color='m')) #ligne à 10Q_0(2K) 352 MHz
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][1] / facteursQ['a C2'][1]) / facteursQ['b C2'][1]], [facteursQ['10Q_0(2K)'][1], facteursQ['10Q_0(2K)'][1]], linestyle='-', color='m')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][1] / facteursQ['a C2'][1]) / facteursQ['b C2'][1], xendlines + 30], [facteursQ['10Q_0(2K)'][1], facteursQ['10Q_0(2K)'][1]], linestyle='--', color='m')) #ligne à 10Q_0(2K) 721 MHz
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][2] / facteursQ['a C2'][2]) / facteursQ['b C2'][2]], [facteursQ['10Q_0(2K)'][2], facteursQ['10Q_0(2K)'][2]], linestyle='-', color='m')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][2] / facteursQ['a C2'][2]) / facteursQ['b C2'][2], xendlines], [facteursQ['10Q_0(2K)'][2], facteursQ['10Q_0(2K)'][2]], linestyle='--', color='m')) #ligne à 10Q_0(2K) 7C
    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][3] / facteursQ['a C2'][3]) / facteursQ['b C2'][3]], [facteursQ['10Q_0(2K)'][3], facteursQ['10Q_0(2K)'][3]], linestyle='-', color='m')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][3] / facteursQ['a C2'][3]) / facteursQ['b C2'][3], xendlines], [facteursQ['10Q_0(2K)'][3], facteursQ['10Q_0(2K)'][3]], linestyle='--', color='m')) #ligne à 10Q_0(2K) 7D
#    plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][4] / facteursQ['a C2'][4]) / facteursQ['b C2'][4]], [facteursQ['10Q_0(2K)'][4], facteursQ['10Q_0(2K)'][4]], linestyle='-', color='m')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][4] / facteursQ['a C2'][4]) / facteursQ['b C2'][4], xendlines], [facteursQ['10Q_0(2K)'][4], facteursQ['10Q_0(2K)'][4]], linestyle='--', color='m')) #ligne à 10Q_0(2K) 7B
    plt.plot(-np.log(facteursQ['10Q_0(2K)'] / facteursQ['a C2']) / facteursQ['b C2'], facteursQ['10Q_0(2K)'],color='m',marker='s', linestyle='', label = 'intersection rouge/magenta')

# - annotations -- noir
if liBool:
    plt.text(x = xendlines + 1, y = facteursQ['Q_0 (4.2K)'][0], s = f"352 MHz: {facteursQ['Q_0 (4.2K)'][0]:.1e}", color = 'k', fontsize = 9, verticalalignment='bottom')#ajout possible : bbox=dict(facecolor='white', alpha=0.5, edgecolor = 'None')
    plt.text(x = xendlines + 1, y = facteursQ['Q_0 (4.2K)'][1], s = f"721 MHz: {facteursQ['Q_0 (4.2K)'][1]:.1e}", color = 'k', fontsize = 9, verticalalignment='center')
    plt.text(x = xendlines + 1, y = facteursQ['Q_0 (4.2K)'][2]*(1-0.4), s = f"7C: {facteursQ['Q_0 (4.2K)'][2]:.1e}", color = 'k', fontsize = 9, verticalalignment='center')
    plt.text(x = xendlines + 1, y = facteursQ['Q_0 (4.2K)'][3], s = f"7D: {facteursQ['Q_0 (4.2K)'][3]:.1e}", color = 'k', fontsize = 9, verticalalignment='center')
#    plt.text(x = xendlines + 1, y = facteursQ['Q_0 (4.2K)'][4], s = f"7B: {facteursQ['Q_0 (4.2K)'][4]:.1e}", color = 'k', fontsize = 9, verticalalignment='center')

    plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][0]/10*(1+0.1), s = f"352 MHz: {facteursQ['10Q_0(2K)'][0]/10:.1e}", color = 'c', fontsize = 9, verticalalignment='bottom')
    plt.text(x = xendlines + 1 + 30, y = facteursQ['10Q_0(2K)'][1]/10, s = f"721 MHz: {facteursQ['10Q_0(2K)'][1]/10:.1e}", color = 'c', fontsize = 9, verticalalignment='center')
    plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][2]/10*(1-0.5), s = f"7C: {facteursQ['10Q_0(2K)'][2]/10:.1e}", color = 'c', fontsize = 9, verticalalignment='center')
    plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][3]/10, s = f"7D: {facteursQ['10Q_0(2K)'][3]/10:.1e}", color = 'c', fontsize = 9, verticalalignment='center')
#      plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][4]/10, s = f"7B: {facteursQ['10Q_0(2K)'][4]/10:.1e}", color = 'c', fontsize = 9, verticalalignment='center')

# -- magenta
if ltBool:
    plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][0]*(1+0.1), s = f"352 MHz: {facteursQ['10Q_0(2K)'][0]:.1e}", color = 'm', fontsize = 9, verticalalignment='bottom')
    plt.text(x = xendlines + 1 + 30, y = facteursQ['10Q_0(2K)'][1], s = f"721 MHz: {facteursQ['10Q_0(2K)'][1]:.1e}", color = 'm', fontsize = 9, verticalalignment='center')
    plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][2]*(1-0.5), s = f"7C: {facteursQ['10Q_0(2K)'][2]:.1e}", color = 'm', fontsize = 9, verticalalignment='center')
    plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][3], s = f"7D: {facteursQ['10Q_0(2K)'][3]:.1e}", color = 'm', fontsize = 9, verticalalignment='center')
#    plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][4], s = f"7B: {facteursQ['10Q_0(2K)'][4]:.1e}", color = 'm', fontsize = 9, verticalalignment='center')

# zones colorées - Qi -- noir (débatement de 50 mm)
if liBool:
    spanLi = 50 #50mm
    centreLi = 40-10 #longueur Li centrale
    plt.axes().axvspan(xmin = centreLi-spanLi/2, xmax = centreLi+spanLi/2, ymin = np.log10(1e4/1e3)/np.log10(1e15/1e3), alpha=0.2, color='k')
#    plt.text(x = centreLi, y = 3e3, s = r"$L_i = [${centreLi-spanLi/2:.1};{centreLi+spanLi/2:.1}$]\; \vert \; Q_i = Q_0$(4.2 K)", color = 'k', fontsize = 'large', fontweight = 'heavy', verticalalignment='center', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor = 'None'))
    plt.text(x = centreLi, y = 3e3, s = rf"$L_i = [${centreLi-spanLi/2};{centreLi+spanLi/2}$]$ mm", color = 'k', fontsize = 'large', fontweight = 'heavy', verticalalignment='center', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor = 'None'))

# - Qt -- magenta (longueur fixe)
if ltBool:
    longLt = 20 # longueur Lt
    plt.axes().axvline(x = longLt, ymin = np.log10(1e4/1e3)/np.log10(1e15/1e3), alpha=0.2, color='m', linewidth = 3)
#    plt.text(x = longLt, y = 3e3, s = rf"$L_t = ${longLt}$\; \vert \; Q_t > 10\,Q_0$(2 K)", color = 'm', fontsize = 'large', fontweight = 'heavy', verticalalignment='center', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor = 'None'))
#    plt.text(x = longLt, y = 3e3, s = rf"$L_t =$ {longLt} mm", color = 'm', fontsize = 'large', fontweight = 'heavy', verticalalignment='center', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor = 'None'))
    plt.text(x = longLt, y = 3e3, s = r"$L_t =$ ?? mm", color = 'm', fontsize = 'large', fontweight = 'heavy', verticalalignment='center', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor = 'None'))

# Ajouter un gros point à l'intersection des deux courbes horizontales et courbes de Q_t/i

#plt.legend(loc = 'best', ncol = 2)
plt.legend(loc = 'upper right', ncol = 2)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax + 10)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"D\'{e}termination des longeurs d'antenne sur C2")
plt.tight_layout()#pour séparer un peu les plots

if liBool == True and ltBool == False:
    name = "QtVsLt_C2_final_Li"
elif ltBool== True and liBool == False:
    name = "QtVsLt_C2_final_Lt"
else:
    name = "QtVsLt_C2_final"
    
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()
print('GRAPHES IMPRIMÉS')

#%% Sur port F2 FINAL
xmax = 200
xendlines = 170

plt.figure(num='Port F final', figsize = (largeurPlot, hauteurPlot))
plt.plot(x_th_F2_352, expfit(x_th_F2_352, *popt_F2_352),'r-',label = 'F2 @ 352 MHz', linewidth = 1)
plt.plot(x_th_F2_721, expfit(x_th_F2_721, *popt_F2_721),'r--', label = 'F2 @ 721 MHz', linewidth = 1)
plt.plot(x_th_F2_1314_7C, expfit(x_th_F2_1314_7C, *popt_F2_1314_7C),'r-.', label = 'F2 @ 1314 MHz (7C)', linewidth = 1)
plt.plot(x_th_F2_1314_7D, expfit(x_th_F2_1314_7D, *popt_F2_1314_7D),'r:', label = 'F2 @ 1314 MHz (7D)', linewidth = 1)
#plt.plot(x_th_F2_1314_7C, expfit(x_th_F2_1314_7B, *popt_F2_1314_7B),'r-.', label = 'F2 @ 1314 MHz (7B)', linewidth = 1)


plt.errorbar(unumpy.nominal_values(F2_352['Lt (mm)']),unumpy.nominal_values(F2_352['Qt']), xerr = unumpy.std_devs(F2_352['Lt (mm)']) , yerr = unumpy.std_devs(F2_352['Qt']), fmt='r*', ecolor = 'k', elinewidth = 1, capsize = 1)
plt.errorbar(unumpy.nominal_values(F2_721['Lt (mm)']),unumpy.nominal_values(F2_721['Qt']), xerr = unumpy.std_devs(F2_721['Lt (mm)']) , yerr = unumpy.std_devs(F2_721['Qt']), fmt='ro', ecolor = 'k', elinewidth = 1, capsize = 1)
plt.errorbar(unumpy.nominal_values(F2_1314_7C['Lt (mm)']),unumpy.nominal_values(F2_1314_7C['Qt']), xerr = unumpy.std_devs(F2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7C['Qt']), fmt='r^', ecolor = 'k', elinewidth = 1, capsize = 1)
plt.errorbar(unumpy.nominal_values(F2_1314_7D['Lt (mm)']),unumpy.nominal_values(F2_1314_7D['Qt']), xerr = unumpy.std_devs(F2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7D['Qt']), fmt='rv', ecolor = 'k', elinewidth = 1, capsize = 1)

# - lignes horizontales 10Q_0 (2K) - magenta
plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][0] / facteursQ['a F2'][0]) / facteursQ['b F2'][0]], [facteursQ['10Q_0(2K)'][0], facteursQ['10Q_0(2K)'][0]], linestyle='-', color='m', label = r'$10\times Q_0$(2 K)')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][0] / facteursQ['a F2'][0]) / facteursQ['b F2'][0], xendlines], [facteursQ['10Q_0(2K)'][0], facteursQ['10Q_0(2K)'][0]], linestyle='--', color='m')) #ligne à Q_0(4K) 352 MHz
plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][1] / facteursQ['a F2'][1]) / facteursQ['b F2'][1]], [facteursQ['10Q_0(2K)'][1], facteursQ['10Q_0(2K)'][1]], linestyle='-', color='m')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][1] / facteursQ['a F2'][1]) / facteursQ['b F2'][1] + 5, xendlines], [facteursQ['10Q_0(2K)'][1], facteursQ['10Q_0(2K)'][1]], linestyle='--', color='m')) #ligne à Q_0(4K) 721 MHz
plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][2] / facteursQ['a F2'][2]) / facteursQ['b F2'][2]], [facteursQ['10Q_0(2K)'][2], facteursQ['10Q_0(2K)'][2]], linestyle='-', color='m')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][2] / facteursQ['a F2'][2]) / facteursQ['b F2'][2], xendlines], [facteursQ['10Q_0(2K)'][2], facteursQ['10Q_0(2K)'][2]], linestyle='--', color='m')) #ligne à Q_0(4K) 7C
plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][3] / facteursQ['a F2'][3]) / facteursQ['b F2'][3]], [facteursQ['10Q_0(2K)'][3], facteursQ['10Q_0(2K)'][3]], linestyle='-', color='m')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][3] / facteursQ['a F2'][3]) / facteursQ['b F2'][3], xendlines], [facteursQ['10Q_0(2K)'][3], facteursQ['10Q_0(2K)'][3]], linestyle='--', color='m')) #ligne à Q_0(4K) 7D
#plt.axes().add_line(mpl.lines.Line2D([xmin, -np.log(facteursQ['10Q_0(2K)'][4] / facteursQ['a F2'][3]) / facteursQ['b F2'][4]], [facteursQ['10Q_0(2K)'][4], facteursQ['10Q_0(2K)'][4]], linestyle='-', color='m')) ; plt.axes().add_line(mpl.lines.Line2D([-np.log(facteursQ['10Q_0(2K)'][4] / facteursQ['a F2'][4]) / facteursQ['b F2'][4], xendlines], [facteursQ['10Q_0(2K)'][4], facteursQ['10Q_0(2K)'][4]], linestyle='--', color='m')) #ligne à Q_0(4K) 7B
plt.plot(-np.log(facteursQ['10Q_0(2K)'] / facteursQ['a F2']) / facteursQ['b F2'],facteursQ['10Q_0(2K)'],color='m',marker='s', linestyle='', label = 'intersection rouge/magenta')

# - annotations -- magenta
plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][0]*(1+0.3), s = f"352 MHz: {facteursQ['10Q_0(2K)'][0]:.1e}", color = 'm', fontsize = 9, verticalalignment='bottom')
plt.text(x = xendlines + 1 + 5, y = facteursQ['10Q_0(2K)'][1], s = f"721 MHz: {facteursQ['10Q_0(2K)'][1]:.1e}", color = 'm', fontsize = 9, verticalalignment='center')
plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][2], s = f"7C: {facteursQ['10Q_0(2K)'][2]:.1e}", color = 'm', fontsize = 9, verticalalignment='center')
plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][3]*(1-0.35), s = f"7D: {facteursQ['10Q_0(2K)'][3]:.1e}", color = 'm', fontsize = 9, verticalalignment='top')
#plt.text(x = xendlines + 1, y = facteursQ['10Q_0(2K)'][4], s = f"7B: {facteursQ['10Q_0(2K)'][4]:.1e}", color = 'm', fontsize = 9, verticalalignment='center')

# - Qt -- magenta (longueur fixe)
longLt = 75 # longueur Lt
plt.axes().axvline(x = longLt, ymin = np.log10(1e4/1e3)/np.log10(1e15/1e3), alpha=0.2, color='m', linewidth = 3)
plt.text(x = longLt, y = 3e3, s = rf"$L_t =$ {longLt} mm", color = 'm', fontsize = 'large', fontweight = 'heavy', verticalalignment='center', horizontalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor = 'None'))


plt.legend(loc = 'lower right')
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage $Q$')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
plt.xlim((xmin, xmax + 10)); plt.ylim((ymin, ymax))
plt.xticks(np.arange(0,xmax,20))
plt.axes().yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100))
plt.axes().xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
plt.axes().yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100))
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"D\'{e}termination de la longueur d'antenne transmise ($L_t$) sur F2")
plt.tight_layout()#pour séparer un peu les plots

name = "QtVsLt_F2_final"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()
print('GRAPHES IMPRIMÉS')

#%% MWE
if False:
    import pandas as pd
    from uncertainties import ufloat
    import uncertainties
    import matplotlib.pyplot as plt
    from uncertainties import unumpy
    
    # building of a dataframe filled with ufloats
    d = {'value1': [ufloat(1,.1),ufloat(3,.2),ufloat(5,.6),ufloat(8,.2)], 'value2': [ufloat(10,5),ufloat(50,2),ufloat(30,3),ufloat(5,1)]}
    df = pd.DataFrame(data = d)
    
    # plot of value2 vs. value1 with errobars.
    #plt.plot(x = unumpy.nominal_values(df['value1']), y = unumpy.nominal_values(df['value2']))
    plt.errorbar(x = unumpy.nominal_values(df['value1']), y = unumpy.nominal_values(df['value2']), xerr = unumpy.std_devs(df['value1']), yerr = unumpy.std_devs(df['value2']))
    # obviously .n and .s won't work.
