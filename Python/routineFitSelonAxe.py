# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 17:46:05 2018

@author: Antoine Luboz
Liens utiles:
    https://www.science-emergence.com/Articles/Find-nearest-value-and-the-index-in-array-with-python-and-numpy/
"""
# Se placer dans ce directory
#cd C:\Users\luboz.IPN\Documents\Projets\CV800\Python\
#%% Import des packages
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from fonctions import * #C:\Users\luboz.IPN\Documents\Projets\CV800\Python\fonctions.py
#from FonctionsPython.extractionCsv import extractionCsv

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

#%% Parmètres de taille et constantes
largeurPlot = 6.68; #largeur en inch
ratioPlot = 1.5;
hauteurPlot = largeurPlot/ratioPlot;
print('Le point origine O est situé au niveau de la platine du cryostat. Voici ci-après les positions verticales des 4 bobines (30 tours)')
pos_bob_1 = 451e-3
pos_bob_2 = 990e-3
pos_bob_3 = 1565e-3
pos_bob_4 = 2114e-3
print(f'Les bobines sont situées aux positions selon z: {pos_bob_1}, {pos_bob_2}, {pos_bob_3}, {pos_bob_4}\n elles consistent en 30 tours de fil de cuivre dnas une goudole de 2cm de large environ.')
    
#%% Import des données:
""" 
format des données : Fichier CSV (séparateur virgule) avec pour colonnes

<profondeur dans le cryostat (m) >,<flux magnétique X (T)>,<flux magnétique Y (T)>,<flux magnétique Z (T)>,<erreur sur la profondeur dans le cryostat (m) >,<erreur sur l'inclinaison de la perche (°)>,<erreur sur la rotation de la perche (°)>

"""

expData_path = pd.read_csv('Data/exp.csv',skiprows=0, error_bad_lines=False)

#%% Plots - Champ sans correction
plt.plot(expData_path.iloc[:,0],expData_path.iloc[:,3],'r.', label= '$B_{z}$ sans correction')
plt.legend()
plt.errorbar(
        expData_path.iloc[:,0],expData_path.iloc[:,3],
        xerr = expData_path.iloc[:,4],yerr = expData_path.iloc[:,7],
        fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= 'erreur champ $B_{z}$ sans correction')#à commenter si l'erreur est nulle

plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood, ou 'log', nonposy = 'mask'
plt.xlabel('Profondeur dans le cryostat depuis la platine (m)')
plt.yscale('linear')
plt.ylabel('Champ magnétique (T)')
plt.minorticks_on()
plt.grid(b = True, which = 'major', axis = 'both')
plt.title(r"Champ magnétique vertical résiduel $B_z$ sur l'axe du cryostat en fonction de la profondeur depuis la platine")

