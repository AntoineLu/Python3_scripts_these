# -*- coding: utf-8 -*-
"""
Created on Fri May  4 16:59:31 2018

@author: luboz
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
class Plots_videStatiqueVanneOuverte:
    """"Classe permettant de choisir quel graphes tracer.
    - sans_capots, logique, defaut = True
    - P_LV, logique, defaut = True
    - P_HV, logique, defaut = True
    - Subplots, logique, defaut = True"""
    
    def __init__(self,sans_capots, capots_10mm, capots_1mm, deltaP):
        self.sans_capots = True
        self.capots_10mm = True
        self.capots_1mm = True
        self.deltaP = True

from uncertainties import ufloat#incertitudes
        
with open('Graphes/resultats_statiqueVanneOuverte.txt','w') as file:
    file.write('---------------------------------------\nPARAMÈTRES DE FIT LORS DU VIDE STATIQUE VANNE OUVERTE')

#%% Parmètres de taille et constantes
largeurPlot = 6.68; #largeur en inch
ratioPlot = 1.5;
hauteurPlot = largeurPlot/ratioPlot;
volumeFour = np.array([4500,20])#en litre
print(f'V_f = {ufloat(volumeFour[0],volumeFour[1]):+.2uS} L')

#on défnit d'abord la fonction linéaire et exp
def linfunc(x,a,b):
    return(a*x+b)
    
def cstfunc(x,a):
    return(a + 0*x)

#%% Choix des graphes à générer (je crée cette classe pour m'entrainer aux classes)        
choix = Plots_videStatiqueVanneOuverte(False,False,True,True)

#%% Extraction des datas
videStatiqueVanneOuverte_sansCapots = pd.read_csv('Data/videStatiqueVanneOuverte_sansCapots.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)
videStatiqueVanneOuverte_10mm = pd.read_csv('Data/videStatiqueVanneOuverte_10mm.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)
videStatiqueVanneOuverte_1mm = pd.read_csv('Data/videStatiqueVanneOuverte_1mm.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)

#%% Suppression des colonnes inutiles et renommage
del videStatiqueVanneOuverte_sansCapots["Date et heure"] ; del videStatiqueVanneOuverte_sansCapots["Commentaires"] ; del videStatiqueVanneOuverte_sansCapots['Unnamed: 6']
del videStatiqueVanneOuverte_10mm["Date et heure"] ; del videStatiqueVanneOuverte_10mm["Commentaires"] ; del videStatiqueVanneOuverte_10mm['Unnamed: 6']
del videStatiqueVanneOuverte_1mm["Date et heure"] ; del videStatiqueVanneOuverte_1mm["Commentaires"] ; del videStatiqueVanneOuverte_1mm['Unnamed: 6']
#videStatiqueVanneOuverte_1mm.drop(videStatiqueVanneOuverte_1mm.index[1],inplace=True) ; #videStatiqueVanneOuverte_1mm.drop(videStatiqueVanneOuverte_1mm.index[7], inplace=True)#pour supprimer des lignes

#%% Ajout de l'erreur de chaque jauge
videStatiqueVanneOuverte_sansCapots["erreur P_cav (mbar)"] = 0.4*videStatiqueVanneOuverte_sansCapots["P_cav (mbar)"] ; videStatiqueVanneOuverte_sansCapots["erreur P_HV"] = 0.15*videStatiqueVanneOuverte_sansCapots["P_HV (mbar)"]
videStatiqueVanneOuverte_10mm["erreur P_cav (mbar)"] = 0.4*videStatiqueVanneOuverte_10mm["P_cav (mbar)"] ; videStatiqueVanneOuverte_10mm["erreur P_HV"] = 0.15*videStatiqueVanneOuverte_10mm["P_HV (mbar)"]
videStatiqueVanneOuverte_1mm["erreur P_cav (mbar)"] = 0.4*videStatiqueVanneOuverte_1mm["P_cav (mbar)"] ; videStatiqueVanneOuverte_1mm["erreur P_HV"] = 0.15*videStatiqueVanneOuverte_1mm["P_HV (mbar)"]

# Tracé des courbes
#%% P sans capots en fonction du temps en vide statique
if choix.sans_capots:
    func_x = np.linspace(1,6.4,22)

    popt_sansCapots_pCav, pcov_sansCapots_pCav = curve_fit(linfunc, videStatiqueVanneOuverte_sansCapots.iloc[1:6,0], videStatiqueVanneOuverte_sansCapots.iloc[1:6,1], sigma = videStatiqueVanneOuverte_sansCapots.iloc[1:6,4])#.iloc[range ou num row, range ou num colonnes], range: #:#, selection: [#, #, #] ici, les 6 premières valeurs de la colonne 0
    popt_sansCapots_pHv, pcov_sansCapots_pHv = curve_fit(linfunc, videStatiqueVanneOuverte_sansCapots.iloc[1:6,0], videStatiqueVanneOuverte_sansCapots.iloc[1:6,2], sigma = videStatiqueVanneOuverte_sansCapots.iloc[1:6,5])

    plt.figure(num='videStatiqueVanneOuverte_sansCapots_fit', figsize = (largeurPlot, hauteurPlot))
    plt.plot(videStatiqueVanneOuverte_sansCapots['Temps (min)'],videStatiqueVanneOuverte_sansCapots['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    plt.plot(videStatiqueVanneOuverte_sansCapots['Temps (min)'],videStatiqueVanneOuverte_sansCapots['P_HV (mbar)'],'b*', label= '$P_{HV}$')
    
    plt.plot(func_x,linfunc(func_x, *popt_sansCapots_pCav),'r--', label = 'lin(1:5)' )
    plt.plot(func_x,linfunc(func_x, *popt_sansCapots_pHv),'b--', label = 'lin(1:5)' )
        
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.grid(b = True, which = 'major', axis = 'both')
    
    plt.errorbar(videStatiqueVanneOuverte_sansCapots['Temps (min)'],videStatiqueVanneOuverte_sansCapots['P_cav (mbar)'], yerr = videStatiqueVanneOuverte_sansCapots['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    plt.errorbar(videStatiqueVanneOuverte_sansCapots['Temps (min)'],videStatiqueVanneOuverte_sansCapots['P_HV (mbar)'], yerr = videStatiqueVanneOuverte_sansCapots['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log', nonposy = 'mask')
    plt.ylabel(r'$P$ (mbar)')
    plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
    plt.xlabel('Temps (min)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    plt.title(r"Sans capots")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "videStatiqueVanneOuverte_sansCapots_fit"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
    print(f'Équation de la courbe P_cav :\n y = ax + b avec a = {ufloat(popt_sansCapots_pCav[0],np.sqrt(np.diag(pcov_sansCapots_pCav))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pCav[1],np.sqrt(np.diag(pcov_sansCapots_pCav))[1]):+.2uS}')
    print(f'Équation de la courbe P_HV :\n y = ax + b avec a = {ufloat(popt_sansCapots_pHv[0],np.sqrt(np.diag(pcov_sansCapots_pHv))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pHv[1],np.sqrt(np.diag(pcov_sansCapots_pHv))[1]):+.2uS}')
    #Dire dans le CR, on néglige le premier point car il y a une forte augmentation de la pression dues aux fuites d'Ar lors de l'opération des vannes.
    print(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA : \n {ufloat(popt_sansCapots_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pCav))[0]*volumeFour[0])**2 + (popt_sansCapots_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_sansCapots_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pHv))[0]*volumeFour[0])**2 + (popt_sansCapots_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}')#^2 s'écrit **2 en python
    
    with open('Graphes/resultats_statiqueVanneOuverte.txt','a') as file:
        file.write(f'\n\n{name}:')
        file.write(f'\n Équation de la courbe P_cav :\n y = ax + b avec a = {ufloat(popt_sansCapots_pCav[0],np.sqrt(np.diag(pcov_sansCapots_pCav))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pCav[1],np.sqrt(np.diag(pcov_sansCapots_pCav))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_HV :\n y = ax + b avec a = {ufloat(popt_sansCapots_pHv[0],np.sqrt(np.diag(pcov_sansCapots_pHv))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pHv[1],np.sqrt(np.diag(pcov_sansCapots_pHv))[1]):+.2uS}')
        file.write(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA : \n {ufloat(popt_sansCapots_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pCav))[0]*volumeFour[0])**2 + (popt_sansCapots_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_sansCapots_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pHv))[0]*volumeFour[0])**2 + (popt_sansCapots_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}')
        file.write('\nMatrice de covariance de la courbe P_cav:')
        file.write(f'\n{pcov_sansCapots_pCav}')
        file.write('\n Matrice de covariance de la courbe P_HV:')
        file.write(f'\n{pcov_sansCapots_pHv}')
#%% P capots 10mm en fonction du temps en vide statique
if choix.capots_10mm:
    func_x = np.linspace(.4,3.2,22)

    popt_10mm_pCav, pcov_10mm_pCav = curve_fit(linfunc, videStatiqueVanneOuverte_10mm.iloc[1:7,0], videStatiqueVanneOuverte_10mm.iloc[1:7,1], sigma = videStatiqueVanneOuverte_10mm.iloc[1:7,4])#.iloc[range ou num row, range ou num colonnes], range: #:#, selection: [#, #, #] ici, les 6 premières valeurs de la colonne 0
    popt_10mm_pHv, pcov_10mm_pHv = curve_fit(linfunc, videStatiqueVanneOuverte_10mm.iloc[2:7,0], videStatiqueVanneOuverte_10mm.iloc[2:7,2], sigma = videStatiqueVanneOuverte_10mm.iloc[2:7,5])

    plt.figure(num='videStatiqueVanneOuverte_10mm_fit', figsize = (largeurPlot, hauteurPlot))
    plt.plot(videStatiqueVanneOuverte_10mm['Temps (min)'],videStatiqueVanneOuverte_10mm['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    plt.plot(videStatiqueVanneOuverte_10mm['Temps (min)'],videStatiqueVanneOuverte_10mm['P_HV (mbar)'],'b*', label= '$P_{HV}$')
    
    plt.plot(func_x,linfunc(func_x, *popt_10mm_pCav),'r--', label = 'lin(1:6)' )
    plt.plot(func_x,linfunc(func_x, *popt_10mm_pHv),'b--', label = 'lin(1:5)' )
        
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.grid(b = True, which = 'major', axis = 'both')
    
    plt.errorbar(videStatiqueVanneOuverte_10mm['Temps (min)'],videStatiqueVanneOuverte_10mm['P_cav (mbar)'], yerr = videStatiqueVanneOuverte_10mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    plt.errorbar(videStatiqueVanneOuverte_10mm['Temps (min)'],videStatiqueVanneOuverte_10mm['P_HV (mbar)'], yerr = videStatiqueVanneOuverte_10mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log', nonposy = 'mask')
    plt.ylabel(r'$P$ (mbar)')
    plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
    plt.xlabel('Temps (min)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    plt.title(r"Capots \`{a} 10 mm")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "videStatiqueVanneOuverte_10mm_fit"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
    print(f'Équation de la courbe P_cav :\n y = ax + b avec a = {ufloat(popt_10mm_pCav[0],np.sqrt(np.diag(pcov_10mm_pCav))[0]):+.2uS} et b = {ufloat(popt_10mm_pCav[1],np.sqrt(np.diag(pcov_10mm_pCav))[1]):+.2uS}')
    print(f'Équation de la courbe P_HV :\n y = ax + b avec a = {ufloat(popt_10mm_pHv[0],np.sqrt(np.diag(pcov_10mm_pHv))[0]):+.2uS} et b = {ufloat(popt_10mm_pHv[1],np.sqrt(np.diag(pcov_10mm_pHv))[1]):+.2uS}')
    #Dire dans le CR, on néglige le premier point car il y a une forte augmentation de la pression dues aux fuites d'Ar lors de l'opération des vannes.
    print(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité et HV: \n {ufloat(popt_10mm_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pCav))[0]*volumeFour[0])**2 + (popt_10mm_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_10mm_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pHv))[0]*volumeFour[0])**2 + (popt_10mm_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}')#^2 s'écrit **2 en python
    
    with open('Graphes/resultats_statiqueVanneOuverte.txt','a') as file:
        file.write(f'\n\n{name}:')
        file.write(f'\n Équation de la courbe P_cav :\n y = ax + b avec a = {ufloat(popt_10mm_pCav[0],np.sqrt(np.diag(pcov_10mm_pCav))[0]):+.2uS} et b = {ufloat(popt_10mm_pCav[1],np.sqrt(np.diag(pcov_10mm_pCav))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_HV :\n y = ax + b avec a = {ufloat(popt_10mm_pHv[0],np.sqrt(np.diag(pcov_10mm_pHv))[0]):+.2uS} et b = {ufloat(popt_10mm_pHv[1],np.sqrt(np.diag(pcov_10mm_pHv))[1]):+.2uS}')
        file.write(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA : \n {ufloat(popt_10mm_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pCav))[0]*volumeFour[0])**2 + (popt_10mm_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_10mm_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pHv))[0]*volumeFour[0])**2 + (popt_10mm_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}')
        file.write('\nMatrice de covariance de la courbe P_cav:')
        file.write(f'\n{pcov_10mm_pCav}')
        file.write('\n Matrice de covariance de la courbe P_HV:')
        file.write(f'\n{pcov_10mm_pHv}')
#%% P capots 1mm en fonction du temps en vide statique
if choix.capots_1mm:
    func_x = np.linspace(0,1.6,22)

    popt_1mm_pCav, pcov_1mm_pCav = curve_fit(linfunc, videStatiqueVanneOuverte_1mm.iloc[1:4,0], videStatiqueVanneOuverte_1mm.iloc[1:4,1], sigma = videStatiqueVanneOuverte_1mm.iloc[1:4,4], absolute_sigma = False)#.iloc[range ou num row, range ou num colonnes], range: #:# (attention, n'inclu pas le dernier point), selection: [#, #, #] ici, les 6 premières valeurs de la colonne 0
    popt_1mm_pHv, pcov_1mm_pHv = curve_fit(linfunc, videStatiqueVanneOuverte_1mm.iloc[1:4,0], videStatiqueVanneOuverte_1mm.iloc[1:4,2], sigma = videStatiqueVanneOuverte_1mm.iloc[1:4,5], absolute_sigma = False)

    plt.figure(num='videStatiqueVanneOuverte_1mm_fit', figsize = (largeurPlot, hauteurPlot))
    plt.plot(videStatiqueVanneOuverte_1mm['Temps (min)'],videStatiqueVanneOuverte_1mm['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    plt.plot(videStatiqueVanneOuverte_1mm['Temps (min)'],videStatiqueVanneOuverte_1mm['P_HV (mbar)'],'b*', label= '$P_{HV}$')
    
    plt.plot(func_x,linfunc(func_x, *popt_1mm_pCav),'r--', label = 'lin(1:3)' )
    plt.plot(func_x,linfunc(func_x, *popt_1mm_pHv),'b--', label = 'lin(1:3)' )
        
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.grid(b = True, which = 'major', axis = 'both')
    
    plt.errorbar(videStatiqueVanneOuverte_1mm['Temps (min)'],videStatiqueVanneOuverte_1mm['P_cav (mbar)'], yerr = videStatiqueVanneOuverte_1mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    plt.errorbar(videStatiqueVanneOuverte_1mm['Temps (min)'],videStatiqueVanneOuverte_1mm['P_HV (mbar)'], yerr = videStatiqueVanneOuverte_1mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')
    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log', nonposy = 'mask')
    plt.ylabel(r'$P$ (mbar)')
    plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
    plt.xlabel('Temps (min)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    plt.title(r"Capots \`{a} 1 mm")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "videStatiqueVanneOuverte_1mm_fit"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
    print(f'Équation de la courbe P_cav :\n y = ax + b avec a = {ufloat(popt_1mm_pCav[0],np.sqrt(np.diag(pcov_1mm_pCav))[0]):+.2uS} et b = {ufloat(popt_1mm_pCav[1],np.sqrt(np.diag(pcov_1mm_pCav))[1]):+.2uS}')
    print(f'Équation de la courbe P_HV :\n y = ax + b avec a = {ufloat(popt_1mm_pHv[0],np.sqrt(np.diag(pcov_1mm_pHv))[0]):+.2uS} et b = {ufloat(popt_1mm_pHv[1],np.sqrt(np.diag(pcov_1mm_pHv))[1]):+.2uS}')
    #Dire dans le CR, on néglige le premier point car il y a une forte augmentation de la pression dues aux fuites d'Ar lors de l'opération des vannes.
    print(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité et HV: \n {ufloat(popt_1mm_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pCav))[0]*volumeFour[0])**2 + (popt_1mm_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_1mm_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pHv))[0]*volumeFour[0])**2 + (popt_1mm_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}')#^2 s'écrit **2 en python
    
    with open('Graphes/resultats_statiqueVanneOuverte.txt','a') as file:
        file.write(f'\n\n{name}:')
        file.write(f'\n Équation de la courbe P_cav :\n y = ax + b avec a = {ufloat(popt_1mm_pCav[0],np.sqrt(np.diag(pcov_1mm_pCav))[0]):+.2uS} et b = {ufloat(popt_1mm_pCav[1],np.sqrt(np.diag(pcov_1mm_pCav))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_HV :\n y = ax + b avec a = {ufloat(popt_1mm_pHv[0],np.sqrt(np.diag(pcov_1mm_pHv))[0]):+.2uS} et b = {ufloat(popt_1mm_pHv[1],np.sqrt(np.diag(pcov_1mm_pHv))[1]):+.2uS}')
        file.write(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité et HV: \n {ufloat(popt_1mm_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pCav))[0]*volumeFour[0])**2 + (popt_1mm_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_1mm_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pHv))[0]*volumeFour[0])**2 + (popt_1mm_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}')
        file.write('\nMatrice de covariance de la courbe P_cav:')
        file.write(f'\n{pcov_1mm_pCav}')
        file.write('\n Matrice de covariance de la courbe P_HV:')
        file.write(f'\n{pcov_1mm_pHv}')
        
#%% \Delta P en fonction de l'ouverture de la vanne et du taux de fuite pour les 3 positions de capots différentes.
if choix.deltaP:
    
    func_x = np.linspace(0,6,10)
    
    deltaP_sansCapots = videStatiqueVanneOuverte_sansCapots['P_cav (mbar)'] - videStatiqueVanneOuverte_sansCapots['P_HV (mbar)']
    deltaP_10mm = videStatiqueVanneOuverte_10mm['P_cav (mbar)'] - videStatiqueVanneOuverte_10mm['P_HV (mbar)']
    deltaP_1mm = videStatiqueVanneOuverte_1mm['P_cav (mbar)'] - videStatiqueVanneOuverte_1mm['P_HV (mbar)']
    
    deltaP_erreur_sansCapots = videStatiqueVanneOuverte_sansCapots['erreur P_cav (mbar)'] + videStatiqueVanneOuverte_sansCapots['erreur P_HV']
    deltaP_erreur_10mm = videStatiqueVanneOuverte_10mm['erreur P_cav (mbar)'] + videStatiqueVanneOuverte_10mm['erreur P_HV']
    deltaP_erreur_1mm = videStatiqueVanneOuverte_1mm['erreur P_cav (mbar)'] + videStatiqueVanneOuverte_1mm['erreur P_HV']
    
    popt_sansCapots_deltaP, pcov_sansCapots_deltaP = curve_fit(cstfunc, videStatiqueVanneOuverte_sansCapots.iloc[1:6,0], deltaP_sansCapots[1:6], sigma = deltaP_erreur_sansCapots[1:6])
    popt_10mm_deltaP, pcov_10mm_deltaP = curve_fit(cstfunc, videStatiqueVanneOuverte_10mm.iloc[2:7,0], deltaP_10mm[2:7], sigma = deltaP_erreur_10mm[2:7])
    popt_1mm_deltaP, pcov_1mm_deltaP = curve_fit(cstfunc, videStatiqueVanneOuverte_1mm.iloc[1:4,0], deltaP_1mm[1:4], sigma = deltaP_erreur_1mm[1:4], absolute_sigma = False)
    
    fig = plt.figure(num='DeltaP', figsize = (largeurPlot, hauteurPlot))
    
    plt.plot(videStatiqueVanneOuverte_sansCapots['Temps (min)'],deltaP_sansCapots,'r.', label= 'sans capots')
    plt.plot(videStatiqueVanneOuverte_10mm['Temps (min)'],deltaP_10mm,'b*', label= '10 mm')
    plt.plot(videStatiqueVanneOuverte_1mm['Temps (min)'],deltaP_1mm,'k^', label= '1 mm')
    
    plt.plot(func_x,cstfunc(func_x, *popt_sansCapots_deltaP),'r--', label = f'$y = {ufloat(popt_sansCapots_deltaP,np.sqrt(np.diag(pcov_sansCapots_deltaP))):.2eSL}$ mbar' )
    plt.plot(func_x,cstfunc(func_x, *popt_10mm_deltaP),'b--', label = f'$y = {ufloat(popt_10mm_deltaP,np.sqrt(np.diag(pcov_10mm_deltaP))):.2eSL}$ mbar' )
    plt.plot(func_x,cstfunc(func_x, *popt_1mm_deltaP),'k--', label = f'$y = {ufloat(popt_1mm_deltaP,np.sqrt(np.diag(pcov_1mm_deltaP))):.2eSL}$ mbar' )
        
    plt.legend(loc = 'upper right')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.grid(b = True, which = 'major', axis = 'both')
    
    plt.errorbar(videStatiqueVanneOuverte_sansCapots['Temps (min)'],deltaP_sansCapots, yerr = deltaP_erreur_sansCapots, fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'sans capots')
    plt.errorbar(videStatiqueVanneOuverte_10mm['Temps (min)'],deltaP_10mm, yerr = deltaP_erreur_10mm, fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '10 mm')
    plt.errorbar(videStatiqueVanneOuverte_1mm['Temps (min)'],deltaP_1mm, yerr = deltaP_erreur_1mm, fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '1 mm')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    #plt.yscale('log', nonposy = 'mask')
    plt.yscale('linear') 
    plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0)) # (m, n), pair of integers; if style is ‘sci’, scientific notation will be used for numbers outside the range 10`m`:sup: to 10`n`:sup:. Use (0,0) to include all numbers.
    plt.ylabel(r'$\Delta P$ (mbar)')
    plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
    plt.xlabel('Temps (min)') 
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    plt.title(r"$\Delta P = P_{cav} - P_{HV}$ en fonction du temps")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "videStatiqueVanneOuverte_deltaP"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    #plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
    tauxInjection = ufloat(0.0000167,0.000003)
    print(f"Conductance sans capots: {tauxInjection/ufloat(popt_sansCapots_deltaP,np.sqrt(np.diag(pcov_sansCapots_deltaP))):.2eSL}")
    print(f"Conductance capots à 10 mm: {tauxInjection/ufloat(popt_10mm_deltaP,np.sqrt(np.diag(pcov_10mm_deltaP))):.2eSL}")
    print(f"Conductance capots à 1 mm: {tauxInjection/ufloat(popt_1mm_deltaP,np.sqrt(np.diag(pcov_1mm_deltaP))):.2eSL}")