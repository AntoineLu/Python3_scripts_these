# -*- coding: utf-8 -*-
"""
Script permettant de tracer les graphiques pour la mesure d'antenne des cavités  (couplage vs. longueur d'antenne)

Created on Tue Jul 17 16:53:25 2018

@author: luboz
se placer dans cd C:\Users\luboz.IPN\Documents\Projets\Test multi-mode\Python
"""
#%% Import des packages
import numpy as np 
import pandas as pd
from uncertainties import ufloat
from fonctions import * #C:\Users\luboz.IPN\Documents\Projets\Test multi-mode\Python\fonctions.py
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
    
#%% Définitions des constantes
largeurPlot = 6.68; #largeur en inch
ratioPlot = 1.5;
hauteurPlot = largeurPlot/ratioPlot;

#%% Type A uncertainty sur un set de données.
set = [-35.371,-35.427,-35.435]
meas = typeAUncertainty(set)
#meas.std_dev = np.sqrt(meas.s**2+0.005**2) #ajout d'autres sources d'incertitudes pour les fréquences (5e-4 pour le Delta f)
meas.std_dev = np.sqrt(meas.s**2+0.018**2) #ajout d'autres sources d'incertitudes pour les atténuations. Bruit de 0.008 dB (10 MHz à 3 GHz) et 0.018 dB (3 GHz à 6 GHz).
#meas.std_dev = np.sqrt(meas.s**2+0.03**2) #ajout d'autres sources d'incertitudes pour les longueurs mesurées au pied à coulisse de précision 3/100
print('{:.2uS}'.format(meas))
print('{:.2u}'.format(meas))

#%% Import des datas
# À 352 MHz
C2_352_dF = pd.read_csv('Data/C2_352.csv',skiprows=0, error_bad_lines=False)
F2_352_dF = pd.read_csv('Data/F2_352.csv',skiprows=0, error_bad_lines=False)
surcouplage_352 = True #si sur-couplage ou sous couplage de l'antenne incidente.
Li_mm_352 = ufloat(40.06,0.05) + ufloat(24.96,0.05) + ufloat(99.9,0.05) #longueur de l'antenne incidente utilisée.
diam_mm_352 = typeAUncertainty([7.83,7.77,7.84,7.85,7.85]) #diamètre de l'antenne incidente utilisée.

#%% Modification en ufloat
# À 352 MHz
C2_352_dF = conv_pdToUfloat(C2_352_dF)
F2_352_dF = conv_pdToUfloat(F2_352_dF)

#%% Calcul de Q
# À 352 MHz
C2_352_dF['QL'] = C2_352_dF['f (MHz)']/C2_352_dF['Delta f (MHz)']
F2_352_dF['QL'] = F2_352_dF['f (MHz)']/F2_352_dF['Delta f (MHz)']
if surcouplage_352:
    C2_352_dF['Qi'] = 2*C2_352_dF['QL']/(1+10**(C2_352_dF['S11 (dB)']/20))
    C2_352_dF['Qt'] = 2*C2_352_dF['QL']*10**(-C2_352_dF['S21 (dB)']/10)*(1+10**(C2_352_dF['S11 (dB)']/20))
    F2_352_dF['Qi'] = 2*F2_352_dF['QL']/(1+10**(F2_352_dF['S11 (dB)']/20))
    F2_352_dF['Qt'] = 2*F2_352_dF['QL']*10**(-F2_352_dF['S21 (dB)']/10)*(1+10**(F2_352_dF['S11 (dB)']/20))
else:
    C2_352_dF['Qi'] = 2*C2_352_dF['QL']/(1-10**(C2_352_dF['S11 (dB)']/20))
    C2_352_dF['Qt'] = 2*C2_352_dF['QL']*10**(-C2_352_dF['S21 (dB)']/10)*(1-10**(C2_352_dF['S11 (dB)']/20))
    F2_352_dF['Qi'] = 2*F2_352_dF['QL']/(1-10**(F2_352_dF['S11 (dB)']/20))
    F2_352_dF['Qt'] = 2*F2_352_dF['QL']*10**(-F2_352_dF['S21 (dB)']/10)*(1-10**(F2_352_dF['S11 (dB)']/20))
    
#%% Plot
#%% À 352 MHz
popt_C2_352, pcov_C2_352 = curve_fit(expfit, xdata = unumpy.nominal_values(C2_352_dF['Lt (mm)']), ydata = unumpy.nominal_values(C2_352_dF['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(C2_352_dF['Qt']))
popt_F2_352, pcov_F2_352 = curve_fit(expfit, xdata = unumpy.nominal_values(F2_352_dF['Lt (mm)']), ydata = unumpy.nominal_values(F2_352_dF['Qt']), p0 = [1e17,0.1], sigma = unumpy.std_devs(F2_352_dF['Qt']))

plt.figure(num='Qt vs. Lt @ 352 MHz', figsize = (largeurPlot, hauteurPlot))
plt.plot(unumpy.nominal_values(F2_352_dF['Lt (mm)']),unumpy.nominal_values(F2_352_dF['Qt']),'b.', label= 'F2 @ 352 MHz')
plt.plot(unumpy.nominal_values(C2_352_dF['Lt (mm)']),unumpy.nominal_values(C2_352_dF['Qt']),'r.', label= 'C2 @ 352 MHz')

x_th = np.linspace(50,130,50)
plt.plot(x_th, expfit(x_th, *popt_F2_352),'b--',label= fr'${ufloat(popt_F2_352[0],np.sqrt(np.diag(pcov_F2_352))[0]):.2uSL}\times \exp({ufloat(popt_F2_352[1],np.sqrt(np.diag(pcov_F2_352))[1]):.2uSL} \times l)$')
plt.plot(x_th, expfit(x_th, *popt_C2_352),'r--',label= fr'${ufloat(popt_C2_352[0],np.sqrt(np.diag(pcov_C2_352))[0]):.2uSL}\times \exp({ufloat(popt_C2_352[1],np.sqrt(np.diag(pcov_C2_352))[1]):.2uSL} \times l)$')

plt.legend()

plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(unumpy.nominal_values(C2_352_dF['Lt (mm)']),unumpy.nominal_values(C2_352_dF['Qt']), xerr = unumpy.std_devs(C2_352_dF['Lt (mm)']) , yerr = unumpy.std_devs(C2_352_dF['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'C2err')
plt.errorbar(unumpy.nominal_values(F2_352_dF['Lt (mm)']),unumpy.nominal_values(F2_352_dF['Qt']), xerr = unumpy.std_devs(F2_352_dF['Lt (mm)']) , yerr = unumpy.std_devs(F2_352_dF['Qt']), fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'F2err')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.yscale('log', nonposy = 'mask')
plt.minorticks_on()
#plt.yscale('linear')
plt.ylabel(r'Couplage')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel("Longueur d'antenne (mm)")
#plt.xlim(); plt.ylim()
    
plt.minorticks_on()
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Caract\'{e}risation des brides C2 et F2 en transmission \`{a} 352 MHz")
plt.tight_layout()#pour séparer un peu les plots
    
name = "QtVsLt_352MHz"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% MWE
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
