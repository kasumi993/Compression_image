# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 08:20:29 2021

@author: kasumi
"""
from functools import reduce

import numpy as np

from PIL import Image # importation de la librairie d'image PILLOW

from math import sqrt, log10 # fonctions essentielles de la librairie math

import matplotlib.pyplot as plt

import time

import sys

#importation fonctions locales
from Noeud_partie3 import *


# im = Image.new('RGB', (200,200),(255,0,0))
# im.save("MonImage.png", "PNG")

class Compress:

    def __init__(self,imageName):

        self.im = Image.open(imageName) #charge l'image

        self.__px = self.im.load() # Importation des pixels de l'image

        self.W,self.H = self.im.size #dimensions de l'image

        self.arbre={} #initialisation : arbre de la quadripartition sous forme de liste


    def paint_rect(self,rect,color):
        try:
            r,g,b=int(color[0]),int(color[1]),int(color[2])
            x=rect[0]
            y=rect[1]
            w=rect[2]
            h=rect[3]
            for i in range(int(h)):
                for j in range(int(w)):
                    self.__px[x+j,y+i] = r, g, b
            return "success"
        except: 
            return "erreur"


    def moyenne_pixel(self,rect):
        try:
            x=rect[0]
            y=rect[1]
            w=rect[2]
            h=rect[3]
            r,g,b=[],[],[]
            for i in range(h):
                for j in range(w):
                     red,green,blue = self.__px[x+j,y+i]
                     r.append(red)
                     g.append(green)
                     b.append(blue)
                     
            moyenne=[sum(r)/len(r),sum(g)/len(g),sum(b)/len(b)]
            return moyenne
            
        except: 
            return "erreur"
    
    
    
    def ecart_pixel(self,rect):
        try:
            x=rect[0]
            y=rect[1]
            w=rect[2]
            h=rect[3]
            r,g,b=[],[],[]
            for i in range(h):
                for j in range(w):
                     red,green,blue = self.__px[x+j,y+i]
                     r.append(red**2)
                     g.append(green**2)
                     b.append(blue**2)
                     
            moyenne=self.moyenne_pixel(rect)
            ecartR=sqrt((sum(r)/len(r))-moyenne[0]**2)
            ecartG=sqrt((sum(g)/len(g))-moyenne[1]**2)
            ecartB=sqrt((sum(b)/len(b))-moyenne[2]**2)
            
            ecart=[ecartR,ecartG,ecartB]
            
            return ecart
        except: 
            return "erreur"
    
    
    def homogene(self,rect,seuil):
        try:
            ecart=self.ecart_pixel(rect)
            if sum(ecart)/3<seuil:
                return True
            return False
        except: 
            return "erreur"   
    
    
    #quadripartition d'un rectangle
    def div_rect(self,rect):
        try:
            x=rect[0]
            y=rect[1]
            w=rect[2]
            h=rect[3]
            
            #gestion du cas w ou h=0 et du cas: w<4 et h<4
            if w<=0 or h<=0 or (w<4 and h<4):
                return []
    
            #gestion des cas impairs
               
            new_rect1=[x,y,w//2,h//2]
            new_rect2=[x+w//2,y,w-w//2,h-h//2]
            new_rect3=[x,y+h//2,w//2,h//2]
            new_rect4=[x+w//2,y+h//2,w-w//2,h-h//2]
            
            return [new_rect1,new_rect2,new_rect3,new_rect4]
          
        except: 
            return "erreur"
    
    

    
    #Cree un noeud à partir d'un rectangle et retourne le noeud correspondant à l'arbre de descendance
    def createNoeud(self,rect,indice_parent):
      #  try:
        #creation du noeud racine de l'arbre en fonction du rectangle
        self.arbre[indice_parent]=Noeud(rect[0], rect[1], rect[2], rect[3], 128, 128, 128)
        
        #quadripartition du rectangle
        kids=self.div_rect(rect)
       
        #la liste de noeuds fils
        kid=[]
        
        #creation des noeuds pour les enfants
        if kids!=[]:
            kid.append(Noeud(kids[0][0],kids[0][1],kids[0][2],kids[0][3],128, 128, 128))
            kid.append(Noeud(kids[1][0],kids[1][1],kids[1][2],kids[1][3],128, 128, 128))
            kid.append(Noeud(kids[2][0],kids[2][1],kids[2][2],kids[2][3],128, 128, 128))
            kid.append(Noeud(kids[3][0],kids[3][1],kids[3][2],kids[3][3],128, 128, 128))
            
                   
            #affectation des premieres branches de l'arbre
            self.arbre[indice_parent+"1"]=Noeud(kids[0][0],kids[0][1],kids[0][2],kids[0][3],128, 128, 128)
            self.arbre[indice_parent+"2"]=Noeud(kids[1][0],kids[1][1],kids[1][2],kids[1][3],128, 128, 128)
            self.arbre[indice_parent+"3"]=Noeud(kids[2][0],kids[2][1],kids[2][2],kids[2][3],128, 128, 128)
            self.arbre[indice_parent+"4"]=Noeud(kids[3][0],kids[3][1],kids[3][2],kids[3][3],128, 128, 128)
            
            #appel recursif de la fonction sur les enfants
            self.createNoeud(kids[0],indice_parent+"1")
            self.createNoeud(kids[1],indice_parent+"2")
            self.createNoeud(kids[2],indice_parent+"3")
            self.createNoeud(kids[3],indice_parent+"4")
            
        return self.arbre
        
        # except: 
        #     return "erreur ici"
    
   
     
   
            
   
            
            
    
if __name__=="__main__":
    
    #tests fonctions
    
    
    #instanciation de la classe compress
    image=Compress("image.jpg")
    
    w=image.W
    h=image.H
    x=0
    y=0
    rect_test=[x,y,10,10]
    couleur=[0,0,0]
    couleur2=[255,255,255]
    couleur3=[255,255,0]
    couleur4=[0,255,255]
    temps=[]
    
   
    for i in range(3):
        start_time = time.time()
        noeud=image.createNoeud(rect_test, "0")
        temps.append(time.time() - start_time)
    
    print("--- %s seconds ---" % (temps))
     

    l = range(3) #nombre essais

    plt.plot(l, temps, 'o') #create scatter plot 
    
    m, b = np.polyfit(l, temps, 1) #m = slope, b=intercept
    
    
    plt.plot(l, m*l+b)
    print(m)
    print(b)
    
    print(sys.getsizeof(noeud))
  
    plt.show()

    #image.im.show() #on affiche l'image
    
    
    
