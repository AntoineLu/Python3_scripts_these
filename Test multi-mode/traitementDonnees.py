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

#%% Type A uncertainty sur un set de données. MANUEL
if False:
    vecteur = [] #freq en MHz, longueurs en mm, atténuations en dB
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

F1_352_david = couplingCalculator('david_F1_352.csv', 'sur')
C1_352_david = couplingCalculator('david_C1_352.csv', 'sous')

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
popt_C2_352, pcov_C2_352 = curve_fit(expfit, xdata = unumpy.nominal_values(C2_352['Lt (mm)']), ydata = unumpy.nominal_values(C2_352['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_352['Qt']))
popt_F2_352, pcov_F2_352 = curve_fit(expfit, xdata = unumpy.nominal_values(F2_352['Lt (mm)']), ydata = unumpy.nominal_values(F2_352['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_352['Qt']))
popt_F1_352_david, pcov_F1_352_david = curve_fit(expfit, xdata = unumpy.nominal_values(F1_352_david['Lt (mm)']), ydata = unumpy.nominal_values(F1_352_david['Qt']), p0 = [6.7915e17,0.183818])
popt_C1_352_david, pcov_C1_352_david = curve_fit(expfit, xdata = unumpy.nominal_values(C1_352_david['Lt (mm)']), ydata = unumpy.nominal_values(C1_352_david['Qt']), p0 = [3.4e13,0.172588])

# 721 MHz
popt_C2_721, pcov_C2_721 = curve_fit(expfit, xdata = unumpy.nominal_values(C2_721['Lt (mm)']), ydata = unumpy.nominal_values(C2_721['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_721['Qt']))
popt_F2_721, pcov_F2_721 = curve_fit(expfit, xdata = unumpy.nominal_values(F2_721['Lt (mm)']), ydata = unumpy.nominal_values(F2_721['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_721['Qt']))

# 1314 MHz mode 7C
popt_C2_1314_7C, pcov_C2_1314_7C = curve_fit(expfit, xdata = unumpy.nominal_values(C2_1314_7C['Lt (mm)']), ydata = unumpy.nominal_values(C2_1314_7C['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_1314_7C['Qt']))
popt_F2_1314_7C, pcov_F2_1314_7C = curve_fit(expfit, xdata = unumpy.nominal_values(F2_1314_7C['Lt (mm)']), ydata = unumpy.nominal_values(F2_1314_7C['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_1314_7C['Qt']))

# 1314 MHz mode 7D
popt_C2_1314_7D, pcov_C2_1314_7D = curve_fit(expfit, xdata = unumpy.nominal_values(C2_1314_7D['Lt (mm)']), ydata = unumpy.nominal_values(C2_1314_7D['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_1314_7D['Qt']))
popt_F2_1314_7D, pcov_F2_1314_7D = curve_fit(expfit, xdata = unumpy.nominal_values(F2_1314_7D['Lt (mm)']), ydata = unumpy.nominal_values(F2_1314_7D['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_1314_7D['Qt']))

#%% Plots
#%% À 352 MHz
plt.figure(num='Qt vs. Lt @ 352 MHz', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(C2_352['Lt (mm)']),unumpy.nominal_values(C2_352['Qt']),'r.', label= 'C2 @ 352 MHz')
plt.plot(unumpy.nominal_values(F2_352['Lt (mm)']),unumpy.nominal_values(F2_352['Qt']),'b.', label= 'F2 @ 352 MHz')

plt.plot(np.linspace(50,130,10), expfit(np.linspace(50,130,10), *popt_C2_352),'r--',label= fr'${ufloat(popt_C2_352[0],np.sqrt(np.diag(pcov_C2_352))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_352[1],np.sqrt(np.diag(pcov_C2_352))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(50,130,10), expfit(np.linspace(50,130,10), *popt_F2_352),'b--',label= fr'${ufloat(popt_F2_352[0],np.sqrt(np.diag(pcov_F2_352))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_352[1],np.sqrt(np.diag(pcov_F2_352))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(unumpy.nominal_values(C2_352['Lt (mm)']),unumpy.nominal_values(C2_352['Qt']), xerr = unumpy.std_devs(C2_352['Lt (mm)']) , yerr = unumpy.std_devs(C2_352['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_352['Lt (mm)']),unumpy.nominal_values(F2_352['Qt']), xerr = unumpy.std_devs(F2_352['Lt (mm)']) , yerr = unumpy.std_devs(F2_352['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()

plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation des ports C2 et F2 en transmission \`{a} 352 MHz")
plt.tight_layout()#pour séparer un peu les plots
plt.minorticks_on()
    
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

plt.plot(np.linspace(50,130,10), expfit(np.linspace(50,130,10), *popt_C1_352_david),'r--',label= fr'${ufloat(popt_C1_352_david[0],np.sqrt(np.diag(pcov_C1_352_david))[0]):.2uSL}\times \exp(-{ufloat(popt_C1_352_david[1],np.sqrt(np.diag(pcov_C1_352_david))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(50,130,10), expfit(np.linspace(50,130,10), *popt_F1_352_david),'b--',label= fr'${ufloat(popt_F1_352_david[0],np.sqrt(np.diag(pcov_F1_352_david))[0]):.2uSL}\times \exp(-{ufloat(popt_F1_352_david[1],np.sqrt(np.diag(pcov_F1_352_david))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')
    

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()

plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Mesures de David \`{a} 352 MHz")
plt.tight_layout()#pour séparer un peu les plots
plt.minorticks_on()
    
name = "QtVsLt_352MHz_david"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.show()

#%% À 721 MHz
plt.figure(num='Qt vs. Lt @ 721 MHz', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(C2_721['Lt (mm)']),unumpy.nominal_values(C2_721['Qt']),'r.', label= 'C2 @ 721 MHz')
plt.plot(unumpy.nominal_values(F2_721['Lt (mm)']),unumpy.nominal_values(F2_721['Qt']),'b.', label= 'F2 @ 721 MHz')

plt.plot(np.linspace(20,90,10), expfit(np.linspace(20,90,10), *popt_C2_721),'r--', label= fr'${ufloat(popt_C2_721[0],np.sqrt(np.diag(pcov_C2_721))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_721[1],np.sqrt(np.diag(pcov_C2_721))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(40,150,10), expfit(np.linspace(40,150,10), *popt_F2_721),'b--', label= fr'${ufloat(popt_F2_721[0],np.sqrt(np.diag(pcov_F2_721))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_721[1],np.sqrt(np.diag(pcov_F2_721))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(unumpy.nominal_values(C2_721['Lt (mm)']),unumpy.nominal_values(C2_721['Qt']), xerr = unumpy.std_devs(C2_721['Lt (mm)']) , yerr = unumpy.std_devs(C2_721['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_721['Lt (mm)']),unumpy.nominal_values(F2_721['Qt']), xerr = unumpy.std_devs(F2_721['Lt (mm)']) , yerr = unumpy.std_devs(F2_721['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation des ports C2 et F2 en transmission \`{a} 721 MHz")
plt.tight_layout()#pour séparer un peu les plots
plt.minorticks_on()
    
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

plt.plot(np.linspace(0,70,10), expfit(np.linspace(0,70,10), *popt_C2_1314_7C),'r--', label= fr'${ufloat(popt_C2_1314_7C[0],np.sqrt(np.diag(pcov_C2_1314_7C))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_1314_7C[1],np.sqrt(np.diag(pcov_C2_1314_7C))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(40,150,10), expfit(np.linspace(40,150,10), *popt_F2_1314_7C),'b--', label= fr'${ufloat(popt_F2_1314_7C[0],np.sqrt(np.diag(pcov_F2_1314_7C))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_1314_7C[1],np.sqrt(np.diag(pcov_F2_1314_7C))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(unumpy.nominal_values(C2_1314_7C['Lt (mm)']),unumpy.nominal_values(C2_1314_7C['Qt']), xerr = unumpy.std_devs(C2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7C['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_1314_7C['Lt (mm)']),unumpy.nominal_values(F2_1314_7C['Qt']), xerr = unumpy.std_devs(F2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7C['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation des ports C2 et F2 en transmission \`{a} 1314 MHz (mode 7C)")
plt.tight_layout()#pour séparer un peu les plots
plt.minorticks_on()
    
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

plt.plot(np.linspace(0,80,10), expfit(np.linspace(0,80,10), *popt_C2_1314_7D),'r--', label= fr'${ufloat(popt_C2_1314_7D[0],np.sqrt(np.diag(pcov_C2_1314_7D))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_1314_7D[1],np.sqrt(np.diag(pcov_C2_1314_7D))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(30,150,10), expfit(np.linspace(30,150,10), *popt_F2_1314_7D),'b--', label= fr'${ufloat(popt_F2_1314_7D[0],np.sqrt(np.diag(pcov_F2_1314_7D))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_1314_7D[1],np.sqrt(np.diag(pcov_F2_1314_7D))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend(loc = 'lower right')

plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(unumpy.nominal_values(C2_1314_7D['Lt (mm)']),unumpy.nominal_values(C2_1314_7D['Qt']), xerr = unumpy.std_devs(C2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7D['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_1314_7D['Lt (mm)']),unumpy.nominal_values(F2_1314_7D['Qt']), xerr = unumpy.std_devs(F2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7D['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")

#plt.yticks([1e3,1e4,1e5,1e6,1e7,1e8,1e9,1e10,1e11,1e12,1e13])
#plt.xlim(); plt.ylim()

plt.minorticks_on()
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

plt.plot(np.linspace(0,130,10), expfit(np.linspace(0,130,10), *popt_C2_352),'r-',label= fr'${ufloat(popt_C2_352[0],np.sqrt(np.diag(pcov_C2_352))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_352[1],np.sqrt(np.diag(pcov_C2_352))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(20,90,10), expfit(np.linspace(20,90,10), *popt_C2_721),'r--', label= fr'${ufloat(popt_C2_721[0],np.sqrt(np.diag(pcov_C2_721))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_721[1],np.sqrt(np.diag(pcov_C2_721))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(0,70,10), expfit(np.linspace(0,70,10), *popt_C2_1314_7C),'r-.', label= fr'${ufloat(popt_C2_1314_7C[0],np.sqrt(np.diag(pcov_C2_1314_7C))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_1314_7C[1],np.sqrt(np.diag(pcov_C2_1314_7C))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(0,80,10), expfit(np.linspace(0,80,10), *popt_C2_1314_7D),'r:', label= fr'${ufloat(popt_C2_1314_7D[0],np.sqrt(np.diag(pcov_C2_1314_7D))[0]):.2uSL}\times \exp(-{ufloat(popt_C2_1314_7D[1],np.sqrt(np.diag(pcov_C2_1314_7D))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.errorbar(unumpy.nominal_values(C2_352['Lt (mm)']),unumpy.nominal_values(C2_352['Qt']), xerr = unumpy.std_devs(C2_352['Lt (mm)']) , yerr = unumpy.std_devs(C2_352['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(C2_721['Lt (mm)']),unumpy.nominal_values(C2_721['Qt']), xerr = unumpy.std_devs(C2_721['Lt (mm)']) , yerr = unumpy.std_devs(C2_721['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(C2_1314_7C['Lt (mm)']),unumpy.nominal_values(C2_1314_7C['Qt']), xerr = unumpy.std_devs(C2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7C['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(C2_1314_7D['Lt (mm)']),unumpy.nominal_values(C2_1314_7D['Qt']), xerr = unumpy.std_devs(C2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(C2_1314_7D['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation du ports C2 en transmission pour les quatre modes")
plt.tight_layout()#pour séparer un peu les plots
plt.minorticks_on()
    
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

plt.plot(np.linspace(50,130,10), expfit(np.linspace(50,130,10), *popt_F2_352),'b-',label= fr'${ufloat(popt_F2_352[0],np.sqrt(np.diag(pcov_F2_352))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_352[1],np.sqrt(np.diag(pcov_F2_352))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(40,150,10), expfit(np.linspace(40,150,10), *popt_F2_721),'b--', label= fr'${ufloat(popt_F2_721[0],np.sqrt(np.diag(pcov_F2_721))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_721[1],np.sqrt(np.diag(pcov_F2_721))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(40,150,10), expfit(np.linspace(40,150,10), *popt_F2_1314_7C),'b-.', label= fr'${ufloat(popt_F2_1314_7C[0],np.sqrt(np.diag(pcov_F2_1314_7C))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_1314_7C[1],np.sqrt(np.diag(pcov_F2_1314_7C))[1]):.2uSL} \times l)$', linewidth = 1)
plt.plot(np.linspace(30,150,10), expfit(np.linspace(30,150,10), *popt_F2_1314_7D),'b:', label= fr'${ufloat(popt_F2_1314_7D[0],np.sqrt(np.diag(pcov_F2_1314_7D))[0]):.2uSL}\times \exp(-{ufloat(popt_F2_1314_7D[1],np.sqrt(np.diag(pcov_F2_1314_7D))[1]):.2uSL} \times l)$', linewidth = 1)

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.errorbar(unumpy.nominal_values(F2_352['Lt (mm)']),unumpy.nominal_values(F2_352['Qt']), xerr = unumpy.std_devs(F2_352['Lt (mm)']) , yerr = unumpy.std_devs(F2_352['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')
plt.errorbar(unumpy.nominal_values(F2_721['Lt (mm)']),unumpy.nominal_values(F2_721['Qt']), xerr = unumpy.std_devs(F2_721['Lt (mm)']) , yerr = unumpy.std_devs(F2_721['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')
plt.errorbar(unumpy.nominal_values(F2_1314_7C['Lt (mm)']),unumpy.nominal_values(F2_1314_7C['Qt']), xerr = unumpy.std_devs(F2_1314_7C['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7C['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')
plt.errorbar(unumpy.nominal_values(F2_1314_7D['Lt (mm)']),unumpy.nominal_values(F2_1314_7D['Qt']), xerr = unumpy.std_devs(F2_1314_7D['Lt (mm)']) , yerr = unumpy.std_devs(F2_1314_7D['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation du ports F2 en transmission pour les quatre modes")
plt.tight_layout()#pour séparer un peu les plots
plt.minorticks_on()
    
name = "QtVsLt_F2"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% Sur port C2 juste les lignes
plt.figure(num='Port C2', figsize = (largeurPlot, hauteurPlot))
plt.plot(np.linspace(0,130,10), expfit(np.linspace(0,130,10), *popt_C2_352),'r-',label= 'C2 @ 352 MHz')
plt.plot(np.linspace(20,90,10), expfit(np.linspace(20,90,10), *popt_C2_721),'r--', label= 'C2 @ 721 MHz')
plt.plot(np.linspace(0,70,10), expfit(np.linspace(0,70,10), *popt_C2_1314_7C),'r-.', label= 'C2 @ 1314 MHz (7C)')
plt.plot(np.linspace(0,80,10), expfit(np.linspace(0,80,10), *popt_C2_1314_7D),'r:', label= 'C2 @ 1314 MHz (7D)')

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation du ports C2 en transmission pour les quatre modes")
plt.tight_layout()#pour séparer un peu les plots
plt.minorticks_on()
    
name = "QtVsLt_C2_lines"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% Sur port F2 juste les lignes
plt.figure(num='Port F2', figsize = (largeurPlot, hauteurPlot))
plt.plot(np.linspace(50,130,10), expfit(np.linspace(50,130,10), *popt_F2_352),'b-',label= 'F2 @ 352 MHz')
plt.plot(np.linspace(40,150,10), expfit(np.linspace(40,150,10), *popt_F2_721),'b--', label= 'F2 @ 721 MHz')
plt.plot(np.linspace(40,150,10), expfit(np.linspace(40,150,10), *popt_F2_1314_7C),'b-.', label= 'F2 @ 1314 MHz (7C)')
plt.plot(np.linspace(30,150,10), expfit(np.linspace(30,150,10), *popt_F2_1314_7D),'b:', label= 'F2 @ 1314 MHz (7D)')

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()
    
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation du ports F2 en transmission pour les quatre modes")
plt.tight_layout()#pour séparer un peu les plots
plt.minorticks_on()
    
name = "QtVsLt_F2_lines"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 200)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()
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
