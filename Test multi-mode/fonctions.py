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
from uncertainties import unumpy

#%% Définition des différentes fonctions
def couplingCalculator(file, couplage = '', write = ''):
    """
    Calcule les coefficients de couplage en prenant en entrée un fichier CSV contenant les en-têtes "Lt (mm),err Lt (mm),S11 (dB),err S11 (dB),S21 (dB),err S21 (dB),f (MHz),err f (MHz),Delta f (MHz),err Delta f (MHz),Remarques".
    Attention aux noms des en-têtes qui doivent correspondre.
    La fonction retourne un pandas dataFrame avec les colonnes concaténées au CSV.
    
    file
        chaine. Chemin d'accès vers le fichier CSV.
    couplage
        chaine valant soit 'sur' ou 'sous' en cas de sur-couplage ou sous-complage de l'antenne d'excitation.
    write
        chaine. Chemin d'accès au fichier CSV à écrire
    """
    try:
        dataFrame = pd.read_csv(file, skiprows=0, error_bad_lines=False)
        dataFrame = conv_pdToUfloat(dataFrame)
        
        dataFrame['QL'] = dataFrame['f (MHz)']/dataFrame['Delta f (MHz)']
        
#        if couplage == '':
#            couplage = dataFrame['couplage']
        
        if couplage == 'sur':
            dataFrame['Qi'] = 2*dataFrame['QL']/(1+10**(dataFrame['S11 (dB)']/20))
            dataFrame['Qt'] = 2*dataFrame['QL']*10**(-dataFrame['S21 (dB)']/10)*(1+10**(dataFrame['S11 (dB)']/20))
        elif couplage == 'sous':
            dataFrame['Qi'] = 2*dataFrame['QL']/(1-10**(dataFrame['S11 (dB)']/20))
            dataFrame['Qt'] = 2*dataFrame['QL']*10**(-dataFrame['S21 (dB)']/10)*(1-10**(dataFrame['S11 (dB)']/20))
        else:
            print("ERREUR. couplage prend la valeur 'sous' ou 'sur'")
            
        if write != '':
            with open(write, 'w') as f:
                dataFrame2 = unumpy.nominal_values(dataFrame)
                dataFrame2.to_csv(f,index = False)
            
        return(dataFrame)
        
    except:
        print("Les noms des en-têtes du fichier CSV sont probablement mal définis. Consultez la documentation help(couplingCalculator)")

def conv_pdToUfloat(dataFrame):
    """
    Transforme les pandas.dataframe avec pour en-tête <Lt (mm)>,<err Lt (mm)>,<S11 (dB)>,<err S11 (dB)>,<S21 (dB)>,<err S21 (dB)>,<f (MHz)>,<err f (MHz)>,<Delta f (MHz)>,<err Delta f (MHz)
    en data frame contenant <Lt (mm)>,<S11 (dB)>,<S21 (dB)>,<f (MHz)>,<Delta f (MHz)> en ufloat plus simple pour éffectuer la propagation des incertitudes par la suite.
    """
#    try: #À voir pour la prochaine fois, faire cette fonction en moins bricollée.
#        if 'err Lt (mm)'
    
    try:
        if dataFrame.shape[1] >= 10:
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
        
        else:
            print("Pas de colonnes d'erreur.")
            Lt_mm = []
            S11_dB = []
            S21_dB =[]
            f_Mhz = []
            Deltaf_MHz = []
        
            for i in range(0,dataFrame.shape[0]):
                Lt_mm.append(ufloat(dataFrame.iloc[i,0],0))
                S11_dB.append(ufloat(dataFrame.iloc[i,1],0))
                S21_dB.append(ufloat(dataFrame.iloc[i,2],0))
                f_Mhz.append(ufloat(dataFrame.iloc[i,3],0))
                Deltaf_MHz.append(ufloat(dataFrame.iloc[i,4],0))
                
            data = {'Lt (mm)': Lt_mm, 'S11 (dB)': S11_dB, 'S21 (dB)': S21_dB, 'f (MHz)': f_Mhz, 'Delta f (MHz)': Deltaf_MHz}
            dataFrame_ufloat = pd.DataFrame(data, columns = data.keys())
            return(dataFrame_ufloat)
        
    except:
        print("Erreur. Lire la documentation de la fonction.")

def typeAUncertainty(meas, otherUncertaintySources = [0], verbose = False, language = '', save = False, path = '', wtw = ''):
    """
    Retourne la valeur moyenne et l'écart-type expérimental d'une série de mesures. Pour des erreurs indépendantes.
    
    meas
        un array 1D contenant les différentes valeurs mesurées.
    otherUncertaintySources
        un array 1D repérant les valeurs des std_dev des autres formes d'incertitudes. Elles sont ensuites combinées à la somme de l'incertitude de type A. Par défaut, pas d'incertitude supplémentaire.
    verbose
        booléen pour afficher la valeur retournée. Par défaut faux.
    save
        booléen, sauvegarde la quantité wtw dans le fichier path
    wtw
        une chaine, soit mean soit std pour imprimer dans le fichier. Prend la valeur 'mean' ou 'std'.
    path
        chaine, lien vers le fichier où imprimer.
    """
    try:
        n = len(meas)
        mean = np.sum(meas)/n
        std = np.sqrt(sum((i - mean)**2 for i in meas)/(n*(n-1))) #écart-type expérimental
        std = np.sqrt(std**2 + sum(i**2 for i in otherUncertaintySources)) # Ajout des autres formes d'incertitudes par la méthode classique de propagation

        output = ufloat(mean,std)
        if verbose:
            print('{:.2uS}'.format(output))
            print('\n')
            print('{:.2u}'.format(output))
            if language == 'fr':
                print('Excel:','=MOYENNE(',';'.join([str(i).replace('.', ',') for i in meas]),')') # si séparateur est un point-virgule (fichier Excel français).
            else:
                print('Excel:','=MOYENNE(',','.join([str(i) for i in meas]),')')
        
        if save:
            try:
                if wtw == 'mean' or wtw == 'std':
                    print('Impression dans',path,'de',wtw)
                    if wtw == 'mean':
                        string = '=MOYENNE('
                        if language == 'fr':
                            string = string + ';'.join([str(i).replace('.', ',') for i in meas]) # si séparateur est un point-virgule (fichier Excel français).
                        else:
                            string = string + ','.join([str(i) for i in meas])
                        string = string + ')'
                    elif wtw == 'std':
                        string = f'{std}'
                        
                    with open(path,'a') as file:
                        file.write(string)
                        file.write('\n')
            except:
                print("Vous devez définir un chemin d'accès vers le fichier à écrire.")
        
        return(output)
        
    except:
        print('Erreur. meas doit être une liste de nombres.')

def linfit(x,a,b):
    """
    Retourne la valeur de a × x + b
    """
    return(a*x+b)
   
def expfit(x,a,b):
    """
    Retourne la valeur de a × exp(b × x)
    """
    return(a*np.exp(-b*x))
