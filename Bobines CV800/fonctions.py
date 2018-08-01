# -*- coding: utf-8 -*-
"""
Module comprenant les fonctions de fit de base (sur l'axe) et sur le plan issu de la symmetrie axisymmétrique.
@author: Antoine Luboz
"""

import numpy as np 
import pandas as pd
from uncertainties import ufloat
#%% Fonctions de fit
def bobfit_axe(z,I = [1,1,1,1]):
    "Retourne la valeur du champ magnétique en Tesla induit par la superposition des bobines au point de profondeur dans le cryostat z avec les valeurs de courant contenuent dans le vecteur I où I[n] est respectivement le courant total dans la bobine n. Chaque bobine fait 30 tours."
    #import des cartes de champ
    bob1_1A_path = pd.read_csv('Data/bob1_1A_path.csv',skiprows=0, error_bad_lines=False)
    bob2_1A_path = pd.read_csv('Data/bob2_1A_path.csv',skiprows=0, error_bad_lines=False)
    bob3_1A_path = pd.read_csv('Data/bob3_1A_path.csv',skiprows=0, error_bad_lines=False)
    bob4_1A_path = pd.read_csv('Data/bob4_1A_path.csv',skiprows=0, error_bad_lines=False)
    
    result = []
    
    for Z in z:
        if Z >= bob1_1A_path.iloc[0,0] + 7e-1 and Z <= bob1_1A_path.iloc[len(bob1_1A_path['S (m)'])-1,0] + 7e-1:#regarde si le point Z est compris dans les bornes de la carte de champ sur l'axe
            #i = (np.abs(bob1_1A_path['S (m)']+7e-1 - Z)).argmin()#cherche l'indice de la valeur la plus proche
            i = (np.abs((bob1_1A_path['S (m)']+7e-1) - Z)).idxmin()#cherche l'indice de la valeur la plus proche
            result.append(I[0]*bob1_1A_path.iloc[i,4] + I[1]*bob2_1A_path.iloc[i,4] + I[2]*bob3_1A_path.iloc[i,4] + I[3]*bob4_1A_path.iloc[i,4])
        else:
                result.append(np.nan)
    return(result)

#%% Fonction de calcul de l'erreur  
def erreur_Bmes(errMagn,theta,phi):
    """
    Calcule l'erreur de mesure sur le champ magnétique en fonction de l'erreur intrinsèque au magnétomètre, et des erreurs de mesure liées à l'inclinaison et à la rotation de la perche de mesure.
    Prend en entrée la valeur de l'erreur intrinsèque du magnétomètre (nombre) et les erreurs d'orientation à chaque point de mesure : Le vecteur <theta> correspond à l'erreur sur l'inclinaison de la perche par rapport à la position verticale de référence (angle theta des coordonnées sphériques) et le vecteur phi représente l'erreur de rotation de la perche à chaque point de mesure par rapport à une position x de référence donnée (angle phi des coordonnées sphériques). Voir le modèle ANSYS pour le repère de référence dans la simulation.
    Retourne un array 3D présentant l'erreur sur les mesures du flux magnétique en B_x, B_y et B_z.
    """
    
    errBx = np.array()
    
#%% Fonction de calcul de l'erreur et de la valeur moyenne d'une incertitude de type A
def typeAUncertainty(a):
    """
    Retourne la valeur moyenne et l'écart-type expérimental d'une série de mesures.
    a un array 1D contenant les différentes valeurs mesurées.
    """
    n = len(a)
    mean = np.sum(a)/n
    s2 = 0
    for a_i in a:
        s2 = s2 + (a_i - mean)**2
    s2 = s2/(n-1)
    std = np.sqrt(s2/n)
    
    return(ufloat(mean,std))