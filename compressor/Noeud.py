# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 10:59:50 2021

@author: kasumi
"""



class Noeud:
    def __init__(self, x, y, w, h, r, g, b, parent, hg, hd, bg, bd):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.red = r
        self.green = g
        self.blue = b
        
        #partie 2
        self.parent=parent
        self.kid1 = hg # haut-gauche
        self.kid2 = hd # haut-droite
        self.kid3 = bg # bas-gauche
        self.kid4 = bd # bas-droite
        
      
    #getter/setter
    def getParent(self):
        return self.parent
    
    def getKids(self):
        return [self.kid1,self.kid2,self.kid3,self.kid4]
    
    def getRect(self):
        return [self.x,self.y,self.w,self.h]
    
    def setKid(self,kid1,kid2,kid3,kid4):
        self.kid1=kid1
        self.kid2=kid2
        self.kid3=kid3
        self.kid4=kid4
    