# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:10:46 2018

@author: Antoine Luboz

"""
# Se placer dans ce directory
#cd C:\Users\luboz.IPN\Documents\Projets\QualificationFour\ExperienceCapots
#%% Import des packages
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.ticker
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
        
#classe des choix de graphes à tracer
class Plots_ouvertureVanne:
    """"Classe permettant de choisir quel graphes tracer.
    - sans_capots, logique, defaut = True
    - P_LV, logique, defaut = True
    - P_HV, logique, defaut = True
    - Subplots, logique, defaut = True"""
    
    def __init__(self,sans_capots, capots_10mm, capots_1mm):
        self.sans_capots = True
        self.capots_10mm = True
        self.capots_1mm = True

from uncertainties import ufloat#incertitudes
        
with open('Graphes/resultats_vanne.txt','w') as file:
    file.write("---------------------------------------\nOUTPUT LORS DE L'OUVERTURE DE LA VANNE")
    
#%% Parmètres de taille et constantes
largeurPlot = 6.68; #largeur en inch
ratioPlot = 1.5;
hauteurPlot = largeurPlot/ratioPlot;
volumeFour = 4500#en litre

#on défnit d'abord la fonction linéaire
def linfunc(x,a,b):
    return(a*x+b)

#%% Choix des graphes à générer (je crée cette classe pour m'entrainer aux classes)        
choix = Plots_ouvertureVanne(True,True,True)

#%% Extraction des datas
ouvertureVanne_sansCapots = pd.read_csv('Data/ouvertureVanne_sansCapots.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)
ouvertureVanne_10mm = pd.read_csv('Data/ouvertureVanne_10mm.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)
ouvertureVanne_1mm = pd.read_csv('Data/ouvertureVanne_1mm.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)

#%% Suppression des colonnes inutiles et renommage
del ouvertureVanne_sansCapots["Remarques"]
del ouvertureVanne_10mm["Remarques"]
del ouvertureVanne_1mm["Remarques"]

#%% Ajout de l'erreur de chaque jauge
ouvertureVanne_sansCapots["erreur P_cav (mbar)"] = 0.4*ouvertureVanne_sansCapots["P_cav (mbar)"] ; ouvertureVanne_sansCapots["erreur P_HV"] = 0.15*ouvertureVanne_sansCapots["P_HV (mbar)"]
ouvertureVanne_10mm["erreur P_cav (mbar)"] = 0.4*ouvertureVanne_10mm["P_cav (mbar)"] ; ouvertureVanne_10mm["erreur P_HV"] = 0.15*ouvertureVanne_10mm["P_HV (mbar)"]
ouvertureVanne_1mm["erreur P_cav (mbar)"] = 0.4*ouvertureVanne_1mm["P_cav (mbar)"] ; ouvertureVanne_1mm["erreur P_HV"] = 0.15*ouvertureVanne_1mm["P_HV (mbar)"]

# Tracé des courbes
#%% P sans capots en fonction de l'ouverture de la vanne et du taux de fuite
if choix.sans_capots:

    fig = plt.figure(num='ouvertureVanne_sansCapots', figsize = (largeurPlot, hauteurPlot))
    fig, ax1 = plt.subplots()
    ax1.plot(ouvertureVanne_sansCapots["ouverture vanne (tours)"],ouvertureVanne_sansCapots['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    ax1.plot(ouvertureVanne_sansCapots["ouverture vanne (tours)"],ouvertureVanne_sansCapots['P_HV (mbar)'],'b.', label= '$P_{HV}$')
    ax1.plot(ouvertureVanne_sansCapots["ouverture vanne (tours)"],ouvertureVanne_sansCapots['P_RGA (mbar)'],'k.', label= '$P_{RGA}$')
        
    plt.legend()

    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    ax1.errorbar(ouvertureVanne_sansCapots['ouverture vanne (tours)'],ouvertureVanne_sansCapots['P_cav (mbar)'], yerr = ouvertureVanne_sansCapots['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    ax1.errorbar(ouvertureVanne_sansCapots['ouverture vanne (tours)'],ouvertureVanne_sansCapots['P_HV (mbar)'], yerr = ouvertureVanne_sansCapots['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')
    #plt.errorbar(ouvertureVanne_sansCapots['Temps (min)'],ouvertureVanne_sansCapots['P_RGA (mbar)'], yerr = ouvertureVanne_sansCapots['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{RGA}$')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    ax1.set_yscale('log', nonposy = 'mask')
    ax1.set_ylabel(r'$P$ (mbar)')
    ax1.set_xscale('linear')#symlog displays a linear interval at 0 vicinity
    ax1.set_xlabel('Ouverture de la vanne (tour)')
    #ax1.set_xlim(10.75,12.75);
    plt.minorticks_on()
    
    #ajout d'un second axe donnant le taux de fuite
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    new_tick_locations = np.array(ouvertureVanne_sansCapots["ouverture vanne (tours)"])
    new_tick_label = ['{:.2e}'.format(x) for x in ouvertureVanne_sansCapots["Taux de fuite (mbar × L/s)"]]
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(new_tick_label, rotation=20)
    ax2.set_xlabel(r'Taux de fuite (mbar$\times$L/s)')
    
    #plt.title("Sans capots")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "ouvertureVanne_sansCapots"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
#%% P 10mm en fonction de l'ouverture de la vanne et du taux de fuite
if choix.capots_10mm:

    fig = plt.figure(num='ouvertureVanne_10mm', figsize = (largeurPlot, hauteurPlot))
    fig, ax1 = plt.subplots()
    ax1.plot(ouvertureVanne_10mm["ouverture vanne (tours)"],ouvertureVanne_10mm['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    ax1.plot(ouvertureVanne_10mm["ouverture vanne (tours)"],ouvertureVanne_10mm['P_HV (mbar)'],'b.', label= '$P_{HV}$')
    ax1.plot(ouvertureVanne_10mm["ouverture vanne (tours)"],ouvertureVanne_10mm['P_RGA (mbar)'],'k.', label= '$P_{RGA}$')
        
    plt.legend()

    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    ax1.errorbar(ouvertureVanne_10mm['ouverture vanne (tours)'],ouvertureVanne_10mm['P_cav (mbar)'], yerr = ouvertureVanne_10mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    ax1.errorbar(ouvertureVanne_10mm['ouverture vanne (tours)'],ouvertureVanne_10mm['P_HV (mbar)'], yerr = ouvertureVanne_10mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')
    #plt.errorbar(ouvertureVanne_10mm['Temps (min)'],ouvertureVanne_10mm['P_RGA (mbar)'], yerr = ouvertureVanne_10mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{RGA}$')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    ax1.set_yscale('log', nonposy = 'mask')
    ax1.set_ylabel(r'$P$ (mbar)')
    ax1.set_xscale('linear')#symlog displays a linear interval at 0 vicinity
    ax1.set_xlabel('Ouverture de la vanne (tour)')
    #ax1.set_xlim(10.75,12.75);
    plt.minorticks_on()
    
    #ajout d'un second axe donnant le taux de fuite
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    new_tick_locations = np.array(ouvertureVanne_10mm["ouverture vanne (tours)"])
    new_tick_label = ['{:.2e}'.format(x) for x in ouvertureVanne_10mm["Taux de fuite (mbar × L/s)"]]
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(new_tick_label, rotation=17)
    ax2.set_xlabel(r'Taux de fuite (mbar$\times$L/s)')
    
    #plt.title("Sans capots")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "ouvertureVanne_10mm"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
#%% P 1mm en fonction de l'ouverture de la vanne et du taux de fuite
if choix.capots_1mm:

    fig = plt.figure(num='ouvertureVanne_1mm', figsize = (largeurPlot, hauteurPlot))
    fig, ax1 = plt.subplots()
    ax1.plot(ouvertureVanne_1mm["ouverture vanne (tours)"],ouvertureVanne_1mm['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    ax1.plot(ouvertureVanne_1mm["ouverture vanne (tours)"],ouvertureVanne_1mm['P_HV (mbar)'],'b.', label= '$P_{HV}$')
    ax1.plot(ouvertureVanne_1mm["ouverture vanne (tours)"],ouvertureVanne_1mm['P_RGA (mbar)'],'k.', label= '$P_{RGA}$')
        
    plt.legend()

    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    ax1.errorbar(ouvertureVanne_1mm['ouverture vanne (tours)'],ouvertureVanne_1mm['P_cav (mbar)'], yerr = ouvertureVanne_1mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    ax1.errorbar(ouvertureVanne_1mm['ouverture vanne (tours)'],ouvertureVanne_1mm['P_HV (mbar)'], yerr = ouvertureVanne_1mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')
    #plt.errorbar(ouvertureVanne_1mm['Temps (min)'],ouvertureVanne_1mm['P_RGA (mbar)'], yerr = ouvertureVanne_1mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{RGA}$')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    ax1.set_yscale('log', nonposy = 'mask')
    ax1.set_ylabel(r'$P$ (mbar)')
    ax1.set_xscale('linear')#symlog displays a linear interval at 0 vicinity
    ax1.set_xlabel('Ouverture de la vanne (tour)')
    #ax1.set_xlim(10.75,12.75);
    plt.minorticks_on()
    
    #ajout d'un second axe donnant le taux de fuite
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    new_tick_locations = np.array(ouvertureVanne_1mm["ouverture vanne (tours)"])
    new_tick_label = ['{:.2e}'.format(x) for x in ouvertureVanne_1mm["Taux de fuite (mbar × L/s)"]]
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(new_tick_label, rotation=17)
    ax2.set_xlabel(r'Taux de fuite (mbar$\times$L/s)')
    
    #plt.title("Sans capots")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "ouvertureVanne_1mm"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
#%% Working example
workingExample = False
if workingExample:
    #HEADERS
    import numpy as np 
    import pandas as pd 
    import matplotlib.pyplot as plt 
    
    from matplotlib import rc
    rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    rc('text', usetex=True)
    
    from matplotlib.ticker import Locator	
	
    #/HEADERS
    	
    turns = np.array([11.000, 11.500, 11.750, 12.000, 12.250, 12.375])
    leak = np.array([3.89e-05, 4.63e-05, 1.67e-04, 1.45000000e-03, 8.61e-03, 1.71e-02])
    pressure1 = np.array([7.9e-07, 3.0e-06, 3.5e-05, 6.1e-04, 5.1e-03, 1.8e-02])
    pressure2 = np.array([8.22e-07, 8.22e-07, 8.71e-07, 1.8e-06, 1.150e-05, 7.24e-05])
    pressure3 = np.array([2e-06, 2e-06, 2e-06, 1.2e-05, 1.2e-04, 6e-04])
    
    fig = plt.figure(num='test', figsize = (6.68, 6.68*1.3))
    fig, ax1 = plt.subplots()
    ax1.plot(turns, pressure1, 'r.', label= '$P_1$')
    ax1.plot(turns, pressure2, 'b.', label= '$P_2$')
    ax1.plot(turns, pressure3,'k.', label= '$P_3$')
         
    plt.legend()
    
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    ax1.errorbar(turns, pressure1, yerr = .4*pressure1, fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{1err}$')
    ax1.errorbar(turns, pressure2, yerr = .15*pressure2, fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{2err}$')
    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    
    ax1.set_yscale('log', nonposy = 'mask')
    ax1.set_ylabel(r'$P$')
    ax1.set_xscale('linear')
    ax1.set_xlabel('Opening (turns)')
    #ax1.set_xlim(10.75,12.75);
    plt.minorticks_on()
    #plt.grid(b = True, which = 'major', axis = 'both')
        
    #adding a secondary x-axis above
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    new_tick_locations = turns
    new_tick_label = ['{:.2e}'.format(x) for x in leak] #dtype?
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(new_tick_label, rotation=17)
    #ax2.xaxis.set_scientific(True)
    #ax2.get_xaxis().set_major_formatter((matplotlib.ticker.Formatter(set_scientific(True)))
    #ax2.get_xaxis().set_major_formatter().set_scientific(True)
    ax2.set_xlabel(r'Leak rate (mbar$\times$L/s)')
    
    plt.tight_layout()
    
    #export png
    plt.savefig(('export.png'), format = 'png', transparent=False, dpi = 300)
    plt.show()
