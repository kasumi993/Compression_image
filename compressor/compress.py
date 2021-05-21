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
from Noeud import *


# im = Image.new('RGB', (200,200),(255,0,0))
# im.save("MonImage.png", "PNG")

class Compress:

    def __init__(self,imageName):

        self.im = Image.open(imageName) #charge l'image

        self.__px = self.im.load() # Importation des pixels de l'image

        self.W,self.H = self.im.size #dimensions de l'image

        self.arbre=[] #initialisation : arbre de la quadripartition sous forme de liste


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
    
    
    racine = Noeud(0, 0, 4, 4, 128, 128, 128,None,
                    Noeud(0, 0, 2, 2, 255, 255, 255,None,None,None,None,None), 
                    Noeud(2, 0, 2, 2, 128, 128, 128,None,
                          Noeud(2, 0, 1, 1, 128, 128, 128, None,None, None, None, None),
                          Noeud(2+1, 0, 1, 1, 128, 128, 128,None,None, None, None, None), 
                          Noeud(2, 2+1, 1, 1, 255, 255, 255, None,None, None, None, None), 
                          Noeud(2+1, 2+1, 1, 1, 255, 255, 255,None, None, None, None, None),
                          ),
                    Noeud(2, 2, 2, 2, 128, 128, 128,None,
                          Noeud(2, 0, 1, 1, 128, 128, 128,None, None, None, None, None),
                          Noeud(2+1, 0, 1, 1, 128, 128, 128,None,None, None, None, None), 
                          Noeud(2, 2+1, 1, 1, 0, 0, 0, None,None, None, None, None), 
                          Noeud(2+1, 2+1, 1, 1, 0, 0, 0, None, None,None, None, None),
                          ),
                    Noeud(0, 2, 2, 2, 0, 0, 0, None,None, None, None, None)
                    )
    
    #Cree un noeud à partir d'un rectangle et retourne le noeud correspondant à l'arbre de descendance
    def createNoeud(self,rect,parent):
        try:
            if parent==None:
                #creation du noeud en fonction du rectangle
                parent=Noeud(rect[0], rect[1], rect[2], rect[3], 128, 128, 128,None,None,None,None,None)
                
            #quadripartition du rectangle
            kids=self.div_rect(rect)
           
            #la liste de noeuds fils
            kid=[]
            
            #creation des noeud pour les enfants
            if kids!=[]:
                kid.append(Noeud(kids[0][0],kids[0][1],kids[0][2],kids[0][3],128, 128, 128,parent,None,None,None,None))
                kid.append(Noeud(kids[1][0],kids[1][1],kids[1][2],kids[1][3],128, 128, 128,parent,None,None,None,None))
                kid.append(Noeud(kids[2][0],kids[2][1],kids[2][2],kids[2][3],128, 128, 128,parent,None,None,None,None))
                kid.append(Noeud(kids[3][0],kids[3][1],kids[3][2],kids[3][3],128, 128, 128,parent,None,None,None,None))
                
                #affectation des noeud enfant au noeud parent
                parent.setKid(kid[0], kid[1], kid[2], kid[3])
                
                #appel recursif de la fonction sur les enfants
                self.createNoeud(kids[0],kid[0])
                self.createNoeud(kids[1],kid[1])
                self.createNoeud(kids[2],kid[2])
                self.createNoeud(kids[3],kid[3])
                   
            return parent
        
        except: 
            return "erreur"
    
    
    #verifie si le rectangle est homogene et affecte une couleur correspondant à la moyenne
    def terminalCheck(self,rect,seuil):
        #determination de la moyenne des pixels du rectangle racine
        moyenne=self.moyenne_pixel(rect)
        
        #verification de l'homogénéité du rectangle racine
        if self.homogene(rect,seuil):
            #création du noeud parent
            color=moyenne
            self.paint_rect(rect, color)
            return True
        else: 
            
            #si le rectangle n'est pas homogène, division en 4 fils
            kids=self.div_rect(rect)
            #gestion de cas enfant inexistant
            if kids==[]:
                return 1
         
            #appel recursif de la fonction sur les fils
            self.terminalCheck(kids[0], seuil)
            self.terminalCheck(kids[1], seuil)
            self.terminalCheck(kids[2], seuil)
            self.terminalCheck(kids[3], seuil)
            return 0
     
        
    #donne le nombre de fils d'un noeud
    def nombreFils(self,Noeud,cpt):
        #recupération des enfants du noeud donné en paramètre
        kids=Noeud.getKids()
        if kids!=[None,None,None,None]:
            cpt+=4
            for i in range(4):
                cpt=self.nombreFils(kids[i],cpt)
        return cpt
    
    
    #peint les noeud en fonction de leur profondeur dans l'arbre
    def degrade(self,Noeud):
        
        #recupère les fils du noeud s'ils existent
        kids=Noeud.getKids()
        
        if kids!=[None,None,None,None]:
            #recupère le nombre de fils du noeud, ce sera la hauteur max de l'arbre
            hauteur_max=(self.nombreFils(Noeud, 1)-1)/4
            h=hauteur_max-1
            #on parcourt la hauteur de l'arbre
            while h>1:
                color=[h/hauteur_max*255,0,0]
                #on parcourt les 4 fils de chaque niveau de l'arbre
                for i in range(4):
                    #verifie si le noeud est terminal
                    if kids[i].getKids()==[None,None,None,None]:
                        rect=kids[i].getRect()
                        self.paint_rect(rect,color)
                #on passe au niveau suivant de l'arbre  
                h-=1
        else:
            #recupère les coordonnées du rectangle du noeud
            rect=Noeud.getRect()
            self.paint_rect(rect,[255,0,0])
            
            
    def PSNR(self,noeud):
        sommex=0
        color=noeud.getColor()
        r=color[0]
        g=color[1]
        b=color[2]
        
        rect=noeud.getRect()
        x=rect[0]
        y=rect[1]
        w=rect[2]
        h=rect[3]
    
        #calcul de l'erreur quadratique "EQ"
        for x in range(x,x+w): 
            for y in range(y,y+h):
                self.__EQ=self.__EQ+(r-self.__px[x,y][0])**2 + (g-self.__px[x,y][1])**2 + (b-self.__px[x,y][2])**2
        
        #retourne le PNSR
        return 20*log10(255)-10*log10(self.__EQ/(3*self.__w*self.__h))
   
    

            
            
    
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
    
   
    
    #image.paint_rect(rect_test,couleur)
    #moyenne=image.moyenne_pixel(rect_test)
    #print(moyenne)
    # ecart=image.ecart_pixel(rect_test)
    # print(ecart)
    # result=image.homogene(rect_test,1)
    # print(result)
    #kids=image.div_rect(rect_test)
    
    #result=image.terminalCheck(rect_test,20)
    #print(result)
    
    # nbrFils=image.nombreFils(image.racine,1)
    # print(nbrFils)
    #noeud=image.createNoeud(rect_test, None)
    #noeud=image.nombreFils(noeud,1)
    #print(noeud)
    
    for i in range(3):
        start_time = time.time()
        noeud=image.createNoeud(rect_test, None)
        temps.append(time.time() - start_time)
    
    print("--- %s seconds ---" % (temps))
    
    

    l = range(3) #nombre essais

    plt.plot(l, temps, 'o') #create scatter plot 
    
    m, b = np.polyfit(l, temps, 1) #m = slope, b=intercept
    
    
    plt.plot(l, m*l+b)
    print(m)
    print(b)
    
    nbrFils=image.nombreFils(noeud,1)
    print(sys.getsizeof(noeud)*nbrFils)
    
    plt.show()
    
    #degrade=image.degrade(noeud)
    #print(degrade)
    
    # result=image.div_rect(rect_test)
    # image.paint_rect(result[0],couleur)
    # image.paint_rect(result[1],couleur2)
    # image.paint_rect(result[2],couleur3)
    # image.paint_rect(result[3],couleur4)
    
  
    #image.im.show() #on affiche l'image
    
    
    
