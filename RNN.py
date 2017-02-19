# -*- coding: utf-8 -*-
# Recurrent Neural Network

import copy
import os
import numpy as np
import json
import math
import random
import time

# Sigmond as activation function
def sigmond(x):
    return .5 *(1 + np.tanh(.5 * x))

# Parameters Preset
alpha = 0.01
lamda = 0
mask = 10
epoch = 0

# Behavior understanding
training_set = []
raw_data = open("user_cart.json",'r')
unum = raw_data.read().count('\n')
raw_data.seek(0)
unum = 0
inum = 0
lines = raw_data.readlines()
for li in lines:
    record = json.loads(li)
    if(True):
        thisline = []
        for i in range(len(record)):
            thisline.append(int(record[i]))
            if(int(record[i])>inum):
                inum = int(record[i])
        training_set.append(thisline[0:int(len(record)*0.8)])
        unum = unum + 1

# Represent -- 10D features
np.random.seed(0)
I = np.random.randn(inum+1, mask) * 0.5
H = np.zeros((unum+1, mask))
U = np.random.randn(mask, mask) * 0.5
R = np.random.randn(mask, mask) * 0.5

# The random J choose
opt_set = []
count = 0
for user in xrange(unum):
    new_rand = []
    for item in xrange(len(training_set[user])):
        j = random.randint(0,8532)
        while(j == training_set[user][item]):
            j = random.randint(0, 8532)
        new_rand.append(j)
    opt_set.append(new_rand)


# RNN Network
def train():
    global I, U, R, H
    for user in xrange(unum):
        isum = len(training_set[user])

        H3 = np.zeros((1, 10))
        H3 = H3[0]
        # The first item
        item = 0
        #feed-forward
        i = training_set[user][item] -1
        I2 = I[i]
        A2 = np.dot(H3, R) + np.dot(I2, U)
        H2 = np.zeros((1, mask))
        H2 = H2[0]
        for k in xrange(mask):
            H2[k] = sigmond(A2[k])

        # The second item
        item = 1
        #feed-forward
        i = training_set[user][item] -1
        j = opt_set[user][item] -1
        I1 = I[i]
        J1 = I[j]
        A1 = np.dot(H2, R) + np.dot(I1, U)
        H1 = np.zeros((1, 10))
        H1 = H1[0]
        for k in xrange(mask):
            H1[k] = sigmond(A1[k])
        X = np.dot(H2, I1.T) - np.dot(H2, J1.T)
        dI1 = H2
        dJ1 = -H2
        I[i] += alpha *((1 - sigmond(X))* dI1 - lamda * I1)
        I[j] += alpha *((1 - sigmond(X))* dJ1 - lamda * J1)
        I1 = I[i]
        J1 = I[j]
        # back-propagation for once
        dXH2 = I1 - J1
        dHA2 = np.zeros((1, 10))
        dHA2 = dHA2[0]
        for k in xrange(mask):
            dHA2[k] = H2[k] *(1 - H2[k])
        dU = np.zeros((10, 10))
        dR = np.zeros((10, 10))
        Ut = U
        Rt = R
        U += alpha *((1 - sigmond(X))* dU - lamda * Ut)
        R += alpha *((1 - sigmond(X))* dR - lamda * Rt)

        #the third item
        item = 2
        #feed-forward
        i = training_set[user][item]-1
        j = opt_set[user][item]-1
        Inow = I[i]
        Jnow = I[j]
        X = np.dot(H1, Inow.T) - np.dot(H1, Jnow.T)
        dXInow = H1
        dXJnow = -H1
        I[i] += alpha *((1 - sigmond(X))* dXInow - lamda * Inow)
        I[j] += alpha *((1 - sigmond(X))* dXJnow - lamda * Jnow)
        Inow = I[i]
        Jnow = I[j]
        #back-propagation --first
        dXH1 = Inow - Jnow
        dHA1 = np.zeros((1, 10))
        for k in xrange(mask):
            dHA1[0][k] = H1[k] *(1 - H1[k])
        dU = np.zeros((10, 10))
        dR = np.zeros((10, 10))
        dU1 = np.zeros((10, 10))
        for k in xrange(mask):
            dU[k] = I1[k] * dHA1 * dXH1
            dR[k] = H2[k] * dHA1 * dXH1
        Ut = U
        Rt = R
        U += alpha *((1 - sigmond(X))* dU - lamda * Ut)
        R += alpha *((1 - sigmond(X))* dR - lamda * Rt)
        #back-propagation --second
        dXH2 = np.dot(dHA1*dXH1, R.T)
        for k in xrange(mask):
            dU[k] = I2[k] * dHA2 * dXH2
            dR[k] = H3[k] * dHA2 * dXH2
        Ut = U
        Rt = R
        U += alpha *((1 - sigmond(X))* dU - lamda * Ut)
        R += alpha *((1 - sigmond(X))* dR - lamda * Rt)

        #    I2   I1 Inow Inext
        #    J2   J1 Jnow Jnext
        #  dHA2 dHA1
        #  dXH2 dXH1
        #H3  H2   H1 Hnow

        # the forth and other items
        item = 3
        Hnow = np.zeros((1, 10))
        Hnow = Hnow[0]
        while item < isum:
            #feed-forward
            i = training_set[user][item]-1
            j = opt_set[user][item]-1
            Inext = I[i]
            Jnext = I[j]
            Anow = np.dot(Inow, U) + np.dot(Jnow, R)
            for k in xrange(mask):
                Hnow[k] = sigmond(Anow[k])
            X = np.dot(Hnow, Inext.T) - np.dot(Hnow, Jnext.T)
            dXInext = Hnow
            dXJnext = -Hnow
            I[i] += alpha *((1 - sigmond(X))* dXInext - lamda * Inext)
            I[j] += alpha *((1 - sigmond(X))* dXJnext - lamda * Jnext)
            Inext = I[i]
            Jnext = I[j]
            #back-propagation --first
            dXHnow = Inext - Jnext
            dHAnow = np.zeros((1, 10))
            for k in xrange(mask):
                dHAnow[0][k] = Hnow[k] *(1 - Hnow[k])
            dU = np.zeros((10, 10))
            dR = np.zeros((10, 10))
            for k in xrange(mask):
                dU[k] = Inow[k] * dHAnow * dXHnow
                dR[k] = H1[k] * dHAnow * dXHnow
            Ut = U
            Rt = R
            U += alpha *((1 - sigmond(X))* dU - lamda * Ut)
            R += alpha *((1 - sigmond(X))* dR - lamda * Rt)

            #back-propagation --second
            dXH1 = np.dot(dHAnow*dXHnow, R.T)
            for k in xrange(mask):
                dU[k] = I1[k] * dHA1 * dXH1 ###TOHAVEWRONG!!!!!
                dR[k] = H2[k] * dHA1 * dXH1
            Ut = U
            Rt = R
            U += alpha *((1 - sigmond(X))* dU - lamda * Ut)
            R += alpha *((1 - sigmond(X))* dR - lamda * Rt)

            #back-propagation --third
            dXH2 = np.dot(dHA1*dXH1, R.T)
            for k in xrange(mask):
                dU[k] = I2[k] * dHA2 * dXH2
                dR[k] = H3[k] * dHA2 * dXH2
            Ut = U
            Rt = R
            U += alpha *((1 - sigmond(X))* dU - lamda * Ut)
            R += alpha *((1 - sigmond(X))* dR - lamda * Rt)

            #The next step
            H3 = H2
            H2 = H1
            H1 = Hnow
            #Hnow and Hnext will be calculate at first
            I2 = I1 ; J2 = J1
            I1 = Inow ; J1 = Jnow
            Inow = Inext ; Jnow = Jnext
            #I/Jnext will be found at first
            dHA2 = dHA1
            dHA1 = dHAnow
            item += 1
        H[user] = Hnow

# Load the parameter from param.json
def loadmodel(unum, inum):
    global I,U,R,H
    raw_param = open("param.json",'r')
    lines = raw_param.readlines()
    lnum = 0
    for li in lines:
        record = json.loads(li)
        if(lnum<10):
            for i in range(10):
                U[lnum][i] = record[i]
        elif(lnum<20):
            for i in range(10):
                R[lnum-10][i] = record[i]
        elif(lnum<21+unum):
            for i in range(10):
                H[lnum-20][i] = record[i]
        elif(lnum-21-unum<inum+1):
            for i in range(10):
                I[lnum-21-unum][i] = record[i]
        lnum = lnum + 1
    raw_param.close()

# Reset parameter of param.json
def savemodel(unum,inum):
    raw_param = open("param.json", 'w')
    for i in range(10):
        raw_param.write('[')
        for j in range(9):
            raw_param.write(str(U[i][j]) + ', ')
        raw_param.write(str(U[i][9]) + ']\n')

    for i in range(10):
        raw_param.write('[')
        for j in range(9):
            raw_param.write(str(R[i][j]) + ', ')
        raw_param.write(str(R[i][9]) + ']\n')

    for i in range(unum+1):
        raw_param.write('[')
        for j in range(9):
            raw_param.write(str(H[i][j]) + ', ')
        raw_param.write(str(H[i][9]) + ']\n')

    for i in range(inum+1):
        raw_param.write('[')
        for j in range(9):
            raw_param.write(str(I[i][j]) + ', ')
        raw_param.write(str(I[i][9]) + ']\n')
    raw_param.close()

# Offer new model for others
def savematrix(unum, inum):
    matrix = open("cataToTag.csv",'w')
    for i in range(unum+1):
        for j in range(9):
            matrix.write(str(H[i][j]) + ',')
        matrix.write(str(H[i][j])+'\n')
    matrix.close()

    matrix = open("tagToAd.csv",'w')
    for j in range(10):
        for i in range(inum):
            matrix.write(str(I[i][j]) + ',')
        matrix.write(str(I[inum][j])+'\n')
    matrix.close()

# The first epoch
"""
loadmatrix(unum, inum)
for i in xrange(30):
    train()
savematrix(unum, inum)
savemodel(unum, inum)
"""

# Other epoch
loadmodel(unum, inum)
for i in xrange(30):
    train()
savematrix(unum, inum)
savemodel(unum, inum)
