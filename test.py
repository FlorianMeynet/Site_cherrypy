# -*- coding: utf-8 -*-
"""
Created on Sun May 10 14:52:15 2020

@author: meyne
"""

import csv
import json
import urllib.parse
import urllib.request
import requests

L=[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]

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
            if(identifiant==val[i][8] and mdp==val[i][9]):
                return(True)
        return(False)
        
        
def add(nom,prenom,adresse,ville,pays,mail,tel,genre,identifiant,mdp):

    ligne=[nom,prenom,adresse,ville,pays,mail,tel,genre,identifiant,mdp]
    with open('bdd_id.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(ligne)
            print('Suces')
            
            
def modif_bdd_stock(liste):
     
    names = open("bdd_stock.csv",'r')
    lire_names = names.read()
    lire=lire_names.split('\n')
    val=[]
    for x in lire:
        val.append(x.split(','))
        
    for i in range(len(liste)):
        val[i][1]=int(val[i][1])-liste[i]

    with open('bdd_stock.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(val)

    
"""   
adre=urllib.parse.urlencode({'address':'49, rue de la gurnaz, 74550 Perrignier'})
#print(adre)

url='https://maps.googleapis.com/maps/api/geocode/json?address=address=49%2C+rue+de+la+gurnaz%2C+74550+Perrignier&key=AIzaSyAU5hqMhmRqN7pRKGnFJRIAyz_UjrUkSsk'
r = requests.get(url)
jsonObj=json.loads(r.text)
lat,long=jsonObj['results'][0]['geometry']['location']['lat'],jsonObj['results'][0]['geometry']['location']['lng']

print(lat,long)

new_url='http://maps.google.com/?q='+str(lat)+','+str(long)
print(new_url)

open(new_url)

"""

def recupe():
    with open('connexion.csv','r',newline='') as f:
        reader = csv.reader(f)
        for row in reader:
                return(row[2],row[3],row[4],row[5],row[9])
                
                
                
                
def ouverture(liste):
    stock = open("bdd_stock.csv",'r')
    lire_stock = stock.read()
    lire=lire_stock.split('\n')
    print(lire)
    for i in range(len(liste)):
        ingre=lire[i].split(',')
        print(i)
        print(lire[i])
        print(liste[i],ingre[1])
        if(liste[i]>int(ingre[1])):
            return(False)
        print(i)    
    return(True)
    
