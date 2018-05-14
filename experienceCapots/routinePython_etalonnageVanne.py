#!/usr/bin/env python
# coding: utf-8
"""
Created on Wed May  9 16:59:12 2018

@author: luboz
"""

#%% Import des packages
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
#from FonctionsPython.extractionCsv import extractionCsv

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#from matplotlib2tikz import save as tikz_save
import matplotlib as mpl
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
        
from matplotlib.ticker import Locator
from scipy.optimize import curve_fit

class MinorSymLogLocator(Locator):
    """
    Dynamically find minor tick positions based on the positions of
    major ticks for a symlog scaling.
    """
    def __init__(self, linthresh):
        """
        Ticks will be placed between the major ticks.
        The placement is linear for x between -linthresh and linthresh,
        otherwise its logarithmically
        """
        self.linthresh = linthresh

    def __call__(self):
        'Return the locations of the ticks'
        majorlocs = self.axis.get_majorticklocs()

        # iterate through minor locs
        minorlocs = []

        # handle the lowest part
        for i in range(1, len(majorlocs)):
            majorstep = majorlocs[i] - majorlocs[i-1]
            if abs(majorlocs[i-1] + majorstep/2) < self.linthresh:
                ndivs = 10
            else:
                ndivs = 9
            minorstep = majorstep / ndivs
            locs = np.arange(majorlocs[i-1], majorlocs[i], minorstep)[1:]
            minorlocs.extend(locs)

        return self.raise_if_exceeds(np.array(minorlocs))

    def tick_values(self, vmin, vmax):
        raise NotImplementedError('Cannot get tick locations for a '
                                  '%s type.' % type(self))
from uncertainties import ufloat#incertitudes

#%% Parmètres de taille et constantes
largeurPlot = 6.68; #largeur en inch
ratioPlot = 1.5;
hauteurPlot = largeurPlot/ratioPlot;

#%% Import des données
etalonnage_vanne = pd.read_csv('Data/calibrationVanne.csv',skiprows=0, infer_datetime_format = True, error_bad_lines=False)
del etalonnage_vanne['Taux de fuite He (mbar*L/s)']
#%% Définition des sources d'erreurs
erreur_vanne = 1/np.sqrt(6)*0.25/2#0.25 tour d'erreur en distribution triangulaire, tour.
volume = 3.8
erreur_volume = 0.1/2/np.sqrt(6)#erreur du volume du setup triangulaire, L (3.8 litres au total)
erreur_temps = 1.5#erreur prise du temps, exponnentielle +1.5s de la valeur courante
erreur_jauge = 0.4#40% d'erreur
erreur_mano = 0.5#50% d'erreur, choisi au pif

#%% Ajout des colonnes d'erreurs
etalonnage_vanne['erreur pression mano']  = erreur_mano*etalonnage_vanne['Delta P mano (mbar)']
etalonnage_vanne['erreur pression jauge 1']  = erreur_jauge*etalonnage_vanne['Delta P jauge (mbar)']
etalonnage_vanne['erreur pression jauge 2']  = erreur_jauge*etalonnage_vanne['Delta P jauge (mbar)']

etalonnage_vanne['erreur fuite mano+'] = np.sqrt( ((-etalonnage_vanne['Delta P mano (mbar)']*volume/etalonnage_vanne['Delta t mano (s)']**2)*erreur_temps)**2 + (etalonnage_vanne['Delta P mano (mbar)']/etalonnage_vanne['Delta t mano (s)']*erreur_volume)**2 + (volume/etalonnage_vanne['Delta t mano (s)']*etalonnage_vanne['erreur pression mano'])**2 )
etalonnage_vanne['erreur fuite mano-'] = np.sqrt( (etalonnage_vanne['Delta P mano (mbar)']/etalonnage_vanne['Delta t mano (s)']*erreur_volume)**2 + (volume/etalonnage_vanne['Delta t mano (s)']*etalonnage_vanne['erreur pression mano'])**2 )

etalonnage_vanne['erreur fuite jauge1+'] = np.sqrt( ((-etalonnage_vanne['Delta P jauge (mbar)']*volume/etalonnage_vanne['Delta t jauge (s)']**2)*erreur_temps)**2 + (etalonnage_vanne['Delta P jauge (mbar)']/etalonnage_vanne['Delta t jauge (s)']*erreur_volume)**2 + (volume/etalonnage_vanne['Delta t jauge (s)']*etalonnage_vanne['erreur pression jauge 1'])**2 )
etalonnage_vanne['erreur fuite jauge1-'] = np.sqrt( (etalonnage_vanne['Delta P jauge (mbar)']/etalonnage_vanne['Delta t jauge (s)']*erreur_volume)**2 + (volume/etalonnage_vanne['Delta t jauge (s)']*etalonnage_vanne['erreur pression jauge 1'])**2 )

etalonnage_vanne['erreur fuite jauge2+'] = np.sqrt( ((-etalonnage_vanne['Delta P jauge2 (mbar)']*volume/etalonnage_vanne['Delta t jauge2 (s)']**2)*erreur_temps)**2 + (etalonnage_vanne['Delta P jauge2 (mbar)']/etalonnage_vanne['Delta t jauge2 (s)']*erreur_volume)**2 + (volume/etalonnage_vanne['Delta t jauge2 (s)']*etalonnage_vanne['erreur pression jauge 2'])**2 )
etalonnage_vanne['erreur fuite jauge2-'] = np.sqrt( (etalonnage_vanne['Delta P jauge2 (mbar)']/etalonnage_vanne['Delta t jauge2 (s)']*erreur_volume)**2 + (volume/etalonnage_vanne['Delta t jauge2 (s)']*etalonnage_vanne['erreur pression jauge 2'])**2 )

#%% Tracé
plt.figure(num='etalonnage_vanne', figsize = (largeurPlot, hauteurPlot))
plt.plot(etalonnage_vanne['nombre tour'], etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Manometre'], 'r.', label= r'Manom\`{e}tre')
plt.plot(etalonnage_vanne['nombre tour'], etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Jauge'], 'b.', label= 'Jauge')
        
plt.legend()

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.grid(b = True, which = 'major', axis = 'both')
    
plt.errorbar(etalonnage_vanne['nombre tour'], etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Manometre'], xerr = erreur_vanne, yerr = [etalonnage_vanne['erreur fuite mano-'], etalonnage_vanne['erreur fuite mano+']], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= r'Manom\`{e}tre')
plt.errorbar(etalonnage_vanne['nombre tour'], etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Jauge'], xerr = erreur_vanne, yerr = [etalonnage_vanne['erreur fuite jauge1-'], etalonnage_vanne['erreur fuite jauge1+']], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'Jauge')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#plt.yscale('linear')
plt.yscale('log', nonposy = 'mask')
plt.ylabel(r'Taux de fuite (mbar$\times$L/s)')
plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
plt.xlabel('Ouverture de la vanne (tour)')
#plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
#plt.tick_params(axis='y', which='minor')
#plt.xlim(); plt.ylim()
plt.annotate(r'$Q = 1\times 10^{-1}$ mbar$\times$L/s $\Rightarrow$ 12,75 tours', xy=(12.75, 1e-1), xytext=(14, 2e-1),
            arrowprops=dict(facecolor='black', shrink = 0, width = 1, headwidth = 4, headlength = 3),
            verticalalignment='center',
            horizontalalignment='left')

plt.minorticks_on()
plt.grid(b = True, which = 'major', axis = 'both')
#plt.title("Sans capots")
plt.tight_layout()#pour séparer un peu les plots
    
#export en png et pgf pour latex.
name = "etalonnageVanne"
plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
plt.show()

#%% relatif au fit polynomial
"""
Je définit un array unique contenant toutes les valeurs que l'on va fitter, tout dispositifs de mesure confondus, je sélectionne les "plus beaux datas.
et on fit ensuite avec une polynomial, exponnentiel?
"""
x_tour = etalonnage_vanne['nombre tour']
y_mano = etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Manometre']
y_jauge = etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Jauge']
#on supprime tous les NaN


#%% Essais à garder.
essais = False
if essais:
    from numpy.polynomial import Polynomial
    def linfunc(x,a,b):
        return(a*x+b)
    
    def expfunc(x,a,b):
        return(a*np.exp(x*b))
        
        x = etalonnage_vanne['nombre tour'] ; y = etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Jauge']
        #j'ai besoin de nettoyer les NaN.
        clean_index = np.isfinite(etalonnage_vanne['nombre tour']) & np.isfinite(etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Jauge'])
        clean_index[0] = False;
        polyfit_param = np.polyfit(x[clean_index], y[clean_index], deg = 8, cov = True)
        popt_jauge, pcov_jauge = curve_fit(expfunc, x[clean_index], y[clean_index])

#%% Avec le fit
if essais:
    plt.figure(num='etalonnage_vanne_fit', figsize = (largeurPlot, hauteurPlot))
    #plt.plot(etalonnage_vanne['nombre tour'], etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Manometre'], 'r.', label= r'Manom\`{e}tre')
    plt.plot(etalonnage_vanne['nombre tour'], etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Jauge'], 'b.', label= 'Jauge')
    x_func = np.linspace(x[10],x[22],100)
    plt.plot(x_func, expfunc(x_func,popt_jauge[0],popt_jauge[1]), 'b--', label= r"%.1E$\cdot\exp(%.2f\cdot x)$" %(popt_jauge[0],popt_jauge[1]))##{{}} pour afficher des brackets dans les strings avec variables "{}".format(variable)
    p = np.poly1d(polyfit_param[0])
    #plt.plot(x_func, p(x_func), 'b--', label = f"Poly({len(polyfit_param[0])-1})")
    
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.grid(b = True, which = 'major', axis = 'both')
        
    #plt.errorbar(etalonnage_vanne['nombre tour'], etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Manometre'], xerr = erreur_vanne, yerr = [etalonnage_vanne['erreur fuite mano-'], etalonnage_vanne['erreur fuite mano+']], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= r'Manom\`{e}tre')
    plt.errorbar(etalonnage_vanne['nombre tour'], etalonnage_vanne['Taux de fuite N2 (mbar*L/s) Jauge'], xerr = erreur_vanne, yerr = [etalonnage_vanne['erreur fuite jauge1-'], etalonnage_vanne['erreur fuite jauge1+']], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'Jauge')
    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    #plt.yscale('linear')
    #plt.yscale('log', nonposy = 'mask')
    plt.ylabel(r'$Q$ (mbar$\times$L/s)')
    plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
    plt.xlabel('Ouverture de la vanne (tour)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    #plt.title("Sans capots")
    plt.tight_layout()#pour séparer un peu les plots
        
    #export en png et pgf pour latex.
    name = "etalonnageVanne_test"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
