# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 17:11:04 2018

@author: 寻ME
"""
fr=open('lenses.txt')
lenses=[inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels=['age','prescript','astigmatic','tearRate']
lensesTree=createTree(lenses,lensesLabels)