# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:56:56 2020

@author: meyne
"""
import cherrypy
import csv
import json
import urllib.parse
import urllib.request
import requests
from cherrypy.lib import auth_basic
import webbrowser

conf ={
   '/protected/area': {
       'tools.auth_basic.on': True,
       'tools.auth_basic.accept_charset': 'UTF-8',
     }
    }

   
def check(identifiant,mdp):

        names = open("bdd_id.csv",'r')
        lire_names = names.read()
        #print(lire_names)
        lire=lire_names.split('\n')
        val=[]
        for x in lire:
            print(x)
            val.append(x.split(','))
        print(val)
        for i in range(len(val)):
            if(identifiant==val[i][9] and mdp==val[i][10]):
                with open('connexion.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(val[i])
                return(True)
        return(False)

def add(nom,prenom,numero,adresse,codepostal,ville,mail,tel,genre,identifiant,mdp):
    ligne=[nom,prenom,numero,adresse,codepostal,ville,mail,tel,genre,identifiant,mdp]
    with open('bdd_id.csv', 'a', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(ligne)
 
           
def add_commande(liste):
    idclient=recupe()[4]
    liste=','+idclient
    with open('bdd_commande.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(liste)            
 
    

def modif_bdd_stock(liste):     
    names = open("bdd_stock.csv",'r')
    lire_names = names.read()
    lire=lire_names.split('\n')
    val=[]
    for x in lire:
        val.append(x.split(','))
        
    for i in range(len(liste)):
        val[i][1]=int(val[i][1])-int(liste[i])  
        
    with open('bdd_stock.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(val)
        

def ecrire_dans_fichier(liste):
    with open('test.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(liste[1])
        
           
def commande_possible(liste):
    stock = open("bdd_stock.csv",'r')
    lire_stock = stock.read()
    lire=lire_stock.split('\n')
    for i in range(len(liste)):
        ingre=lire[i].split(',')
        if(int(liste[i])>int(ingre[1])):
            return(False)
    return(True)       

def recupe():
    with open('connexion.csv','r',newline='') as f:
        reader = csv.reader(f)
        for row in reader:
                return(row[2],row[3],row[4],row[5],row[9])
    


class Site(object):
    
    
   
    @cherrypy.expose
    def index(self):
        return open('acceuil.html')
    
    @cherrypy.expose
    def creation(self):
        return open('creation.html')
    
    @cherrypy.expose
    def connexion(self,pseudo,mdp):
        if(check(pseudo,mdp)):
            return open('commande.html')
        else:
            return open('incorrect.html')
    
    @cherrypy.expose
    def retour_apres_creation(self,nom,prenom,numero,adresse,codepostal,ville,mail,tel,genre,identifiant,mdp):
        print(genre)
        add(nom,prenom,numero,adresse,codepostal,ville,mail,tel,genre,identifiant,mdp)
        return(open('acceuil.html'))
        
    @cherrypy.expose
    def  validation_commande(self,v_commande,eau,pate,riz,fruit,conserve_fruit,conserve_viande,conserve_poisson,pain,farine,oeuf,lait,huile,sucre,cereale,savon,dentifrice,masque,papier_toilette,sac_poubelle,lingette):
        liste=[eau,pate,riz,fruit,conserve_fruit,conserve_viande,conserve_poisson,pain,farine,oeuf,lait,huile,sucre,cereale,savon,dentifrice,masque,papier_toilette,sac_poubelle,lingette]
        if(commande_possible(liste)):
            modif_bdd_stock(liste)
            add_commande(liste)
            return(open('validation.html'))




    @cherrypy.expose
    def maping(self):
        num,adresse,codepostal,ville,idclient=recupe()
        encode= num +', '+adresse+', ' + codepostal +' '+ ville 
        
        addre=urllib.parse.urlencode({'address': encode})
        url='https://maps.googleapis.com/maps/api/geocode/json?address='+addre+'&key=AIzaSyAU5hqMhmRqN7pRKGnFJRIAyz_UjrUkSsk'
        r = requests.get(url)
        jsonObj=json.loads(r.text)
        lat,long=jsonObj['results'][0]['geometry']['location']['lat'],jsonObj['results'][0]['geometry']['location']['lng']
        
        new_url='https://www.google.com/maps?q='+str(lat)+','+str(long)
        return(webbrowser.open(new_url))  #On arrivais pas a l'ouvrir normalement avec open donc on ouvre une autre page internet
         

if __name__ == '__main__': 

    cherrypy.quickstart(Site(), '/', conf)







        