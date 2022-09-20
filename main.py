# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

#Created on Wed May 11 00:16:49 2022



#Application Indicateur de risque
#Auteur Titouan Cocheril, Ivan Salle
#Date 04.05.2022


#--------------------------------------------------------------------------------------------


#Importation interface
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font as tkfont 

#Importation carte et navigateur
import folium 
from folium import plugins
from folium.plugins import HeatMapWithTime
from folium.plugins import HeatMap
import geopy as geo
import webbrowser
from pyproj import Proj, transform

#Importation base de données
import pyodbc
import pandas as pd
import random



#Connexion avec la base de donnée
conn=pyodbc.connect('DSN=BD_ACCIDENT')
cursor = conn.cursor()

#Fonctions :

def to_lonlatdf(df):
    inProj = Proj(init='epsg:27561')
    outProj = Proj(init='epsg:4326')
    df['x'], df['y'] = transform(inProj, outProj, df['x'].tolist(), df['y'].tolist())
    return df
#Fonction de convertion en latitude longitude
def to_lonlat(x,y):
    inProj = Proj(init='epsg:27561')
    outProj = Proj(init='epsg:4326')
    lon,lat = transform(inProj, outProj, x, y)
    return lat,lon

#Fonction qui lance une carte après avoir récupérer dans la base de données les informations
#En fonction des paramêtres fournis par l'utilisateur
def lancerCarte(luminosite,meteo,mois):
    
    #Reqête sur la base de données
    sql3="SELECT MLieu.x,MLieu.y,nb_morts*10+nb_blesses_graves*5+nb_blesses_legers AS indice_gravite FROM MAccident JOIN MLieu ON MLieu.lieu_id=MAccident.lieu_id JOIN MLuminosite ON MAccident.lum_id=MLuminosite.code JOIN MIntemperie ON MIntemperie.code=MAccident.intemp_id JOIN MDate ON MDate.date_id=MAccident.date_id WHERE MLuminosite.libelle_luminosite=? AND MIntemperie.libelle=? AND MONTH(MDate.DateFormatStandard)=?;"
    param = (f'{luminosite}',f'{meteo}',mois)
    #Insertion des données dans le DataFrame
    df2=pd.read_sql(sql3,conn,params=param)
    
    #Parcour du DataFrame pour remplir liste_coord des accidents remplissant les critères
    liste_coord = []
    to_lonlatdf(df2)
    for i in range(len(df2)):
        for gravite in range(df2.iloc[i,2]):
            liste_coord.append([df2.iloc[i,1],df2.iloc[i,0]])
    
    #Place la carte sur la ville de Lille
    m = folium.Map(location=[50.632661,3.064955], zoom_start=12,min_opacity=0.1) 
    #Superposition des points d'accidents à la carte
    HeatMap(liste_coord,radius=25).add_to(m)
    m.save("map.html") 
    #Lance le navigateur
    webbrowser.open("map.html")



def lancerCarte2(luminosite,meteo):

    #Reqête sur la base de données
    sql3="SELECT MLieu.x,MLieu.y,nb_morts*1.2+nb_blesses_graves*0.8+nb_blesses_legers*0.4 AS indice_gravite,MONTH(MDate.DateFormatStandard) AS mois FROM MAccident JOIN MLieu ON MLieu.lieu_id=MAccident.lieu_id JOIN MLuminosite ON MAccident.lum_id=MLuminosite.code JOIN MIntemperie ON MIntemperie.code=MAccident.intemp_id JOIN MDate ON MDate.date_id=MAccident.date_id WHERE MLuminosite.libelle_luminosite=? AND MIntemperie.libelle=?;"
    param = (f'{luminosite}',f'{meteo}')
    #Insertion des données dans le DataFrame
    
    df2=pd.read_sql(sql3,conn,params=param)

    liste_coord = [[] for i in range(12)]    
    #Parcour du DataFrame pour remplir liste_coord des accidents remplissant les critères
    to_lonlatdf(df2)
    for i in range(len(df2)):
        #point=to_lonlat(df2.iloc[i,0],df2.iloc[i,1])
       #liste_coord[df2.iloc[i,3]-1].append([point[0],point[1],df2.iloc[i,2]])   #df2.iloc[i,2]
       liste_coord[df2.iloc[i,3]-1].append([df2.iloc[i,1],df2.iloc[i,0],df2.iloc[i,2]])
       print([df2.iloc[i,1],df2.iloc[i,0],df2.iloc[i,2]])
    #Liste des mois
    index_mois=['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
    
    #Place la position de la carte sur la ville de Lille
    m = folium.Map(location=[50.632661,3.064955], zoom_start=12,min_opacity=0.1) 
    #Superposition des points d'accidents à la carte
    auto=choixCheckBtn.get()
    if(auto==0):
        HeatMapWithTime(liste_coord,position='bottomright',radius=25,index=index_mois).add_to(m)
    else:
        HeatMapWithTime(liste_coord,auto_play=True,position='bottomright',radius=25,index=index_mois).add_to(m)
    m.save("map.html") 
    #Lance le navigateur
    webbrowser.open("map.html")
    


#Création de fen^tre type
class IndicateurDeRisque(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #Design des titres de fenêtre
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        
        #Le conteneur est l'endroit où nous allons empiler un tas de cadres
        #les uns sur les autres, puis celui que nous voulons visible
        #sera élevé au-dessus des autres
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            #Toutes les pages au même endroit ;
            #celui en haut de l'ordre d'empilement
            #sera celui qui est visible.
            frame.grid(row=0, column=0, sticky="nsew")

        #Initialise la fenêtre sur la page StartPage
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        #Afficher un cadre pour le nom de page donné
        frame = self.frames[page_name]
        frame.tkraise()


#Fenêtre de menu
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Titre
        label_titre=  tk.Label (self,text="Indicateur de risque",font=controller.title_font,fg='#0080ff')
        label_titre.pack(side="top", fill="x", pady=5)
        
        #Textes présentation programme
        label_texte=tk.Label (self,text="--------------------------")
        label_texte.pack()   
        label_texte=tk.Label (self,text="Les deux programmes ci-dessous \n renvoient une Heatmap indiquant les \n zones les plus à  risques en fonction \n des conditions saisient  ")
        label_texte.pack()
        label_texte=tk.Label (self,text="--------------------------")
        label_texte.pack()   
        
        #Premier programme
        label_texte2=tk.Label (self,text="Sans évolution chronologique :")
        label_texte2.pack()
        bouton_Page1 = tk.Button(self,text="N°1",command=lambda: controller.show_frame("PageOne"),font=("Calibri", 12),fg="#0080ff")
        bouton_Page1.pack(padx=5)
        
        #Deuxième programme
        label_texte3=tk.Label (self,text="Avec évolution chronologique :")
        label_texte3.pack()
        bouton_Page2 = tk.Button(self,text="N°2",command=lambda: controller.show_frame("PageTwo"),font=("Calibri", 12),fg="#0080ff")
        bouton_Page2.pack(padx=10,pady=5)       
        
            

#Fenêtre premier programme sans évolution chronologique
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Titre
        label_titre=  tk.Label (self,text="Indicateur de risque",font=controller.title_font,fg="#0080ff")
        label_titre.pack(side="top", fill="x",padx=10, pady=5)
        
        #Liste de choix luminosité
        list_luminosite = ["Jour", "Nuit"]
        Combo1 = ttk.Combobox(self, values=list_luminosite)
        Combo1.set("Choisi une luminosité")
        Combo1.pack(padx=5, pady=5)
        
        
        #Liste de choix intempéries
        list_intemperie = ["Brouillard","Pluie legere", "Pluie forte", "Vent fort tempete","Grele", "Neige"]
        Combo2 = ttk.Combobox(self, values=list_intemperie)
        Combo2.set("Choisi une intempérie")
        Combo2.pack(padx=5)
        
        
        #Scroll bar de choix du mois de l'années
        label=  tk.Label (self,text="Choisi le mois de l'année")
        label.pack(side="top", fill="x")
        scrol_bar = Scale(self, from_=1, to=12, orient=HORIZONTAL)
        scrol_bar.pack(padx=5)
        
        
        #Bouton valider qui lance le programme
        bouton_V = tk.Button(self,text="Valider",command=lambda: lancerCarte(Combo1.get(),Combo2.get(),scrol_bar.get()),font=("Calibri", 12),fg="#008000")
        bouton_V.pack(padx=5, pady=10)
        
        #Bouton précédent qui revient à la page de menu PageStart
        bouton_P = tk.Button(self,text="Précédent",command=lambda: controller.show_frame("StartPage"),font=("Calibri", 12),fg="#FF0000")
        bouton_P.pack(padx=5, pady=5,side=BOTTOM)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Titre
        label_titre=  tk.Label (self,text="Indicateur de risque",font=controller.title_font,fg="#0080ff")
        label_titre.pack(side="top", fill="x",padx=10, pady=5)
        
        #Liste de choix de luminosité
        list_luminosite = ["Jour", "Nuit"]
        Combo1 = ttk.Combobox(self, values=list_luminosite)
        Combo1.set("Choisi une luminosité")
        Combo1.pack(padx=5, pady=5)  
        
        #Liste de choix intempéries
        list_intemperie = ["Brouillard","Pluie legere", "Pluie forte", "Vent fort tempete","Grele", "Neige"]
        Combo2 = ttk.Combobox(self, values=list_intemperie)
        Combo2.set("Choisi une intempérie")
        Combo2.pack(padx=5, pady=5)
        
        #Check bouton qui demamnde à l'utilisateur si il veut ou non un lancement automatique de l'évolution de la carte
        global choixCheckBtn
        choixCheckBtn =IntVar()
        ChkBttn = Checkbutton(self, text = "Lancement automatique",width = 30, variable = choixCheckBtn)
        ChkBttn.pack(padx = 5, pady = 10)
        
        
        #Bouton valider qui lance le programme
        bouton_V = tk.Button(self,text="Valider",command=lambda: lancerCarte2(Combo1.get(),Combo2.get()),font=("Calibri", 12),fg="#008000")
        bouton_V.pack(padx=5, pady=10)
    
        #Bouton précédent qui revient à la page de menu PageStart
        bouton_P = tk.Button(self,text="Précédent",command=lambda: controller.show_frame("StartPage"),font=("Calibri", 12),fg="#FF0000")
        bouton_P.pack(padx=5, pady=5,side=BOTTOM)


#Boucle d'affichage et d'intération de la fenêtre
if __name__ == "__main__":
    app = IndicateurDeRisque()
    app.mainloop()
