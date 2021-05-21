# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 10:59:50 2021

@author: kasumi
"""



class Noeud:
    def __init__(self, x, y, w, h, r, g, b):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.red = r
        self.green = g
        self.blue = b

    
    def getRect(self):
        return [self.x,self.y,self.w,self.h]
    

    