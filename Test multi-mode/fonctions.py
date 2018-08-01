# -*- coding: utf-8 -*-
"""
Module comprenant les fonctions permettant le traitement des données de la mesure d'antenne
Created on Wed Jul 25 15:34:59 2018

@author: luboz
"""
#%% Import des packages
import numpy as np 
import pandas as pd
from uncertainties import ufloat

#%% Définition des différentes fonctions
def typeAUncertainty(meas, otherUncertaintySources = [0], verbose = False):
    """
    Retourne la valeur moyenne et l'écart-type expérimental d'une série de mesures.
    
    meas
        un array 1D contenant les différentes valeurs mesurées.
    otherUncertaintySources
        un array 1D repérant les valeurs des std_dev des autres formes d'incertitudes. Elles sont ensuites combinées à la somme de l'incertitude de type A. Par défaut, pas d'incertitude supplémentaire.
    verbose
        booléen pour afficher la valeur retournée. Par défaut faux.
    """
    try:
        n = len(meas)
        mean = np.sum(meas)/n
        std = np.sqrt(sum((i - mean)**2 for i in meas)/(n*(n-1))) #écart-type expérimental
        std = np.sqrt(std**2 + sum(i**2 for i in otherUncertaintySources)) # Ajout des autres formes d'incertitudes par la méthode classique de propagation

        output = ufloat(mean,std)
        if verbose: print('{:.2uS}'.format(output),'\n{:.2u}'.format(output))
        return(output)
        
    except:
        print('Erreur. meas doit être une liste de nombres.')
    
def expfit(x,a,b):
    """
    Retourne la valeur de a × exp(b × x)
    """
    return(a*np.exp(-b*x))

def conv_pdToUfloat(dataFrame):
    """
    Transforme les pandas.dataframe avec pour en-tête <Lt (mm)>,<err Lt (mm)>,<S11 (dB)>,<err S11 (dB)>,<S21 (dB)>,<err S21 (dB)>,<f (MHz)>,<err f (MHz)>,<Delta f (MHz)>,<err Delta f (MHz)
    en data frame contenant <Lt (mm)>,<S11 (dB)>,<S21 (dB)>,<f (MHz)>,<Delta f (MHz)> en ufloat plus simple pour éffectuer la propagation des incertitudes par la suite.
    """
    try:
        Lt_mm = []
        S11_dB = []
        S21_dB =[]
        f_Mhz = []
        Deltaf_MHz = []
    
        for i in range(0,dataFrame.shape[0]):
            Lt_mm.append(ufloat(dataFrame.iloc[i,0],dataFrame.iloc[i,1]))
            S11_dB.append(ufloat(dataFrame.iloc[i,2],dataFrame.iloc[i,3]))
            S21_dB.append(ufloat(dataFrame.iloc[i,4],dataFrame.iloc[i,5]))
            f_Mhz.append(ufloat(dataFrame.iloc[i,6],dataFrame.iloc[i,7]))
            Deltaf_MHz.append(ufloat(dataFrame.iloc[i,8],dataFrame.iloc[i,9]))
            
        data = {'Lt (mm)': Lt_mm, 'S11 (dB)': S11_dB, 'S21 (dB)': S21_dB, 'f (MHz)': f_Mhz, 'Delta f (MHz)': Deltaf_MHz}
        dataFrame_ufloat = pd.DataFrame(data, columns = data.keys())
        return(dataFrame_ufloat)
    except:
        print("Erreur. Lire la documentation de la fonction.")