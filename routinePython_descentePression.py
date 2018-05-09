# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 09:55:38 2018

@author: Antoine Luboz

Liens utiles :
    https://pythonhosted.org/spyder/editor.html?highlight=cell#how-to-define-a-code-cell
    http://www.chicoree.fr/w/Fichiers_CSV_en_Python
"""
# Se placer dans ce directory
#cd C:\Users\luboz.IPN\Documents\Projets\QualificationFour\ExperienceCapots
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

#classe des choix de graphes à tracer
class Plots_descentePression:
    """"Classe permettant de choisir quel graphes tracer.
    - P_cav, logique, defaut = True
    - P_LV, logique, defaut = True
    - P_HV, logique, defaut = True
    - Subplots, logique, defaut = True"""
    
    def __init__(self,P_cav,P_LV,P_HV,Subplots):
        self.P_cav = True
        self.P_LV = True
        self.P_HV = True
        self.Subplots = True
        
from matplotlib.ticker import Locator


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

#%% Parmètres de taille
largeurPlot = 6.68; #largeur en inch
ratioPlot = 1.5;
hauteurPlot = largeurPlot/ratioPlot;
#%% Choix des graphes à générer (je crée cette classe pour m'entrainer aux classes)        
choix = Plots_descentePression(True,True,True,True)

#%% Extraction des datas
descentePression_sansCapots = pd.read_csv('Data/descentePression_sansCapots.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)
descentePression_10mm = pd.read_csv('Data/descentePression_10mm.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)
descentePression_1mm = pd.read_csv('Data/descentePression_1mm.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)

#%% Suppression des colonnes inutiles et renommage

del descentePression_sansCapots["Date et heure"] ; del descentePression_sansCapots["Commentaires"]
del descentePression_10mm["Date et heure"] ; del descentePression_10mm["Commentaires"]
del descentePression_1mm["Date et heure"] ; del descentePression_1mm["Commentaires"]

#%% Ajout de l'erreur de chaque jauge

descentePression_sansCapots["erreur P_cav (mbar)"] = 0.4*descentePression_sansCapots["P_cav (mbar)"] ; descentePression_sansCapots["erreur P_LV "] = 0.15*descentePression_sansCapots["P_LV (mbar)"] ; descentePression_sansCapots["erreur P_HV"] = 0.15*descentePression_sansCapots["P_HV (mbar)"]
descentePression_10mm["erreur P_cav (mbar)"] = 0.4*descentePression_10mm["P_cav (mbar)"] ; descentePression_10mm["erreur P_LV "] = 0.15*descentePression_10mm["P_LV (mbar)"] ; descentePression_10mm["erreur P_HV"] = 0.15*descentePression_10mm["P_HV (mbar)"]
descentePression_1mm["erreur P_cav (mbar)"] = 0.4*descentePression_1mm["P_cav (mbar)"] ; descentePression_1mm["erreur P_LV "] = 0.15*descentePression_1mm["P_LV (mbar)"] ; descentePression_1mm["erreur P_HV"] = 0.15*descentePression_1mm["P_HV (mbar)"]

# Tracé des courbes
#%% P_cav en fonction du temps lors du pompage
if choix.P_cav:
    plt.figure(num='pCav', figsize = (largeurPlot, hauteurPlot))
    plt.plot(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_cav (mbar)'],'r.', label= 'sans capots')
    plt.plot(descentePression_10mm['Temps (min)'],descentePression_10mm['P_cav (mbar)'],'b.', label= '10 mm')
    plt.plot(descentePression_1mm['Temps (min)'],descentePression_1mm['P_cav (mbar)'],'k.', label= '1 mm')
    plt.legend()
    
    plt.errorbar(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_cav (mbar)'], yerr = descentePression_sansCapots['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'sans capots')
    plt.errorbar(descentePression_10mm['Temps (min)'],descentePression_10mm['P_cav (mbar)'], yerr = descentePression_10mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '10 mm')
    plt.errorbar(descentePression_1mm['Temps (min)'],descentePression_1mm['P_cav (mbar)'], yerr = descentePression_1mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '1 mm')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log')
    #plt.ylim((1e-7,1e3))
    #yaxis = plt.gca().yaxis
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    plt.ylabel(r'$P_{cav}$ (mbar)')
    plt.xscale('symlog', linthreshy=1e-1)#symlog displays a linear interval at 0 neighborhood
    xaxis = plt.gca().xaxis
    xaxis.set_minor_locator(MinorSymLogLocator(1e-1))
    plt.xlabel('Temps (min)')
    
    #plt.xlim()
    #plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    plt.tight_layout()
    #export en png et pgf pour latex.
    name = "pompage_pCav"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 460)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()

#%% P_HV et en fonction du temps lors du pompage
if choix.P_HV:
    plt.figure(num='pHv', figsize = (largeurPlot, hauteurPlot))
    plt.plot(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_HV (mbar)'],'r.', label= 'sans capots')
    plt.plot(descentePression_10mm['Temps (min)'],descentePression_10mm['P_HV (mbar)'],'b.', label= '10 mm')
    plt.plot(descentePression_1mm['Temps (min)'],descentePression_1mm['P_HV (mbar)'],'k.', label= '1 mm')
    plt.legend()

    plt.errorbar(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_HV (mbar)'], yerr = descentePression_sansCapots['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'sans capots')
    plt.errorbar(descentePression_10mm['Temps (min)'],descentePression_10mm['P_HV (mbar)'], yerr = descentePression_10mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '10 mm')
    plt.errorbar(descentePression_1mm['Temps (min)'],descentePression_1mm['P_HV (mbar)'], yerr = descentePression_1mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '1 mm')
    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log')
    plt.ylabel(r'$P_{HV}$ (mbar)')
    plt.xscale('log')
    plt.xlabel('Temps (min)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    #plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')

    #export en png et pgf pour latex.
    name = "pompage_pHv"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()

#%% P_LV et en fonction du temps lors du pompage
if choix.P_LV:
    plt.figure(num='pLv', figsize = (largeurPlot, hauteurPlot))
    plt.plot(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_LV (mbar)'],'r.', label= 'sans capots')
    plt.plot(descentePression_10mm['Temps (min)'],descentePression_10mm['P_LV (mbar)'],'b.', label= '10 mm')
    plt.plot(descentePression_1mm['Temps (min)'],descentePression_1mm['P_LV (mbar)'],'k.', label= '1 mm')
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.grid(b = True, which = 'major', axis = 'both')

    plt.errorbar(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_LV (mbar)'], yerr = descentePression_sansCapots['erreur P_LV '], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'sans capots')
    plt.errorbar(descentePression_10mm['Temps (min)'],descentePression_10mm['P_LV (mbar)'], yerr = descentePression_10mm['erreur P_LV '], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '10 mm')
    plt.errorbar(descentePression_1mm['Temps (min)'],descentePression_1mm['P_LV (mbar)'], yerr = descentePression_1mm['erreur P_LV '], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '1 mm')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    
    plt.yscale('log')
    plt.ylabel(r'$P_{LV}$ (mbar)')
    plt.xlim((0,1e2))
    plt.xscale('symlog', linthreshy=1e-1)#symlog displays a linear interval at 0 neighborhood
    xaxis = plt.gca().xaxis
    xaxis.set_minor_locator(MinorSymLogLocator(1e-1))
    plt.xlabel('Temps (min)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.ylim()
    #plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    #export en png et pgf pour latex.
    name = "pompage_pLv"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
#%% P_four et en fonction du temps lors du pompage
#Les deux figures précédentes en haut et en bas
if choix.Subplots:
    plt.figure(num='pFour', figsize = (largeurPlot, hauteurPlot))
    plt.subplot(2,1,1)
    plt.plot(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_LV (mbar)'],'r.', label= 'sans capots')
    plt.plot(descentePression_10mm['Temps (min)'],descentePression_10mm['P_LV (mbar)'],'b.', label= '10 mm')
    plt.plot(descentePression_1mm['Temps (min)'],descentePression_1mm['P_LV (mbar)'],'k.', label= '1 mm')
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    #plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')

    plt.errorbar(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_LV (mbar)'], yerr = descentePression_sansCapots['erreur P_LV '], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'sans capots')
    plt.errorbar(descentePression_10mm['Temps (min)'],descentePression_10mm['P_LV (mbar)'], yerr = descentePression_10mm['erreur P_LV '], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '10 mm')
    plt.errorbar(descentePression_1mm['Temps (min)'],descentePression_1mm['P_LV (mbar)'], yerr = descentePression_1mm['erreur P_LV '], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '1 mm')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log')
    plt.ylabel('$P_{LV}$ (mbar)')
    plt.xlim((0,1e2))
    plt.xscale('symlog', linthreshy=1e-1)#symlog displays a linear interval at 0 neighborhood
    xaxis = plt.gca().xaxis
    xaxis.set_minor_locator(MinorSymLogLocator(1e-1))
    plt.title('Pompage primaire')
    plt.grid(b = True, which = 'major', axis = 'both')

    plt.subplot(2,1,2)
    plt.plot(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_HV (mbar)'],'r.', label= 'sans capots')
    plt.plot(descentePression_10mm['Temps (min)'],descentePression_10mm['P_HV (mbar)'],'b.', label= '10 mm')
    plt.plot(descentePression_1mm['Temps (min)'],descentePression_1mm['P_HV (mbar)'],'k.', label= '1 mm')
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.grid(b = True, which = 'major', axis = 'both')

    plt.errorbar(descentePression_sansCapots['Temps (min)'],descentePression_sansCapots['P_HV (mbar)'], yerr = descentePression_sansCapots['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'sans capots')
    plt.errorbar(descentePression_10mm['Temps (min)'],descentePression_10mm['P_HV (mbar)'], yerr = descentePression_10mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '10 mm')
    plt.errorbar(descentePression_1mm['Temps (min)'],descentePression_1mm['P_HV (mbar)'], yerr = descentePression_1mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '1 mm')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log')
    plt.ylabel(r'$P_{HV}$ (mbar)')
    plt.xscale('symlog', linthreshy=1e-1)#symlog displays a linear interval at 0 neighborhood
    xaxis = plt.gca().xaxis#minor ticks on symlog
    xaxis.set_minor_locator(MinorSymLogLocator(1e-1))
    plt.xlabel('Temps (min)')
    plt.title('Pompage secondaire')
    plt.grid(b = True, which = 'major', axis = 'both')
    plt.tight_layout()#pour séparer un peu les plots

    #export en png et pgf pour latex.
    name = "pompage_pFour"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    #plt.savefig(('Graphes/'+name+'.ps'), format = 'ps', transparent=True)
    plt.show()
#%% Des tests
#import numpy as np
#import matplotlib.pyplot as plt 
#plt.figure(figsize = (6.69, 5.1461538461538465))

# do some plotting here
#x = np.linspace(-2, 2, 100)
#plt.plot(x, x)

# save to file
#plt.savefig('test.pgf')