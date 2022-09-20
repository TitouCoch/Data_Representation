# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 08:35:10 2022

@author: tcocheril001
"""

import pandas as pd


Accident=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MAccident.csv',
                            sep=",")
Accident.columns = ['accident_id', 'lieu_id', 'date_id', 'cause_id', 'lum_id', 'intemp_id', 'etat_surface_id', 'impliq_id', 'nb_blesses_graves', 'nb_blesses_legers', 'nb_indemns', 'gravite', 'nb_morts']


Cause=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MCause.csv',
                            sep=",")
Cause.columns =['cause_id', 'libelle']


Date=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MDate.csv',
                            sep=",")
Date.columns =['date_id', 'dateFormatStandart', 'Commentaire']


EtatSurface=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MEtatSurface.csv',
                            sep=",")
EtatSurface.columns=['etat_surface_id', 'libelle_etat_surface', 'type_code_etat_surface']


Implique=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MImplique.csv',
                            sep=",")
Implique.columns=['impliq_id', 'libelle', 'type_code_implique']


Intemperie=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MIntemperie.csv',
                            sep=",")
Intemperie.columns=['intemp_id','libelle']


Lieu=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MLieu.csv',
                            sep=",")
Lieu.columns=['lieu_id', 'commune', 'x', 'y']


Luminosite=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MLuminosite.csv',
                            sep=",")
Luminosite.columns=['lum_id', 'libelle', 'type_luminosite', 'libelle_luminosite']


TypeEtatSurface=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MTypeEtatSurface.csv',
                            sep=",")
TypeEtatSurface.columns=['id_etat_surface','libelle_type_code_etat_surface']


TypeImplication=pd.read_table('F:\\BUT\\Semestre2\\SAE-Stat-Bd\\MTypeImplication.csv',
                            sep=",")
TypeImplication.columns=['id', 'libelleType']


Accident = pd.merge(Accident,Cause, on=['cause_id'])
Accident = pd.merge(Accident,Date, on=['date_id'])
Accident = pd.merge(Accident,EtatSurface, on=['etat_surface_id'])
Accident = pd.merge(Accident,Implique, on=['impliq_id'])
Accident = pd.merge(Accident,Intemperie, on=['intemp_id'])
Accident = pd.merge(Accident,Lieu, on=['lieu_id'])
Accident = pd.merge(Accident,Luminosite, on=['lum_id'])


Accident = Accident.drop(['lieu_id','cause_id', 'date_id', 'lum_id', 'intemp_id', 'etat_surface_id', 'impliq_id'], axis = 1) 




