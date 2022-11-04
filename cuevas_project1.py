# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:50:40 2022

@author: lcuev
"""
import numpy as np
from string import ascii_lowercase as alphabet
import time
import csv
from math import exp,log10

np.random.seed(int(time.time()))
alpha = alphabet  + ' '
length = len(alpha)

dicts = {}
revdicts = {}

for index,letter in enumerate(alpha):
    dicts[letter] = index
    
for index,letter in enumerate(alpha):
    revdicts[index] = letter

with open('freqs.csv', newline='') as csvfile:
    freqs = list(csv.reader(csvfile))

for i in range(length):
    for j in range(length):
        freqs[i][j] = float(freqs[i][j])
    
def get_score(sc):
    ret = 1
    for i in range(length):
        for j in range(length):
            ret *= (freqs[i][j] + 1) ** sc[i][j]
    return ret

def get_score_2(ph):
    ret = 0
    for i in range(1,len(ph)):
        if ph[i] in alpha and ph[i-1] in alpha:
            freq = freqs[dicts[ph[i-1]]][dicts[ph[i]]]
            if freq > 0:
                ret += log10(freq)
            else:
                ret += -10
    return ret

def apply_cipher(dec,ph):
    ret = ''

    for index,i in enumerate(ph):
        if i in alpha:
            ret += dec[i]
        else:
            ret += ph[index]
    return ret

def propose_decipher(ciph):
    first_letter = np.random.choice(26)
    second_letter = np.random.choice(26)

    while(first_letter == second_letter):
        second_letter = np.random.choice(26)

    new_cipher = {}
    for letter in alphabet:
        if (letter == alphabet[first_letter]):
            new_cipher[letter] = ciph[alphabet[second_letter]]
        elif (letter == alphabet[second_letter]):
            new_cipher[letter] = ciph[alphabet[first_letter]]
        else:
            new_cipher[letter] = ciph[letter]
    new_cipher[' '] = ' '
    return new_cipher

    
    
def get_freqs(ph):
    ret = [[0 for i in range(length)] for j in range(length)]
    
    for index in range(1,len(ph)):
        if ph[index] in alpha and ph[index - 1] in alpha:
            ret[dicts[ph[index-1]]][dicts[ph[index]]] += 1   
            
    return ret

def get_cipher(ordr):
    ret = {}
    for index,letter in enumerate(alphabet):
        ret[letter] = alphabet[ordr[index]]
    ret[' '] = ' '
    return ret

def should_swap(proposed_score, current_score):
    diff = proposed_score - current_score

    return exp(diff) > np.random.random()




order = np.random.choice(26,26,replace = False)
cipher = get_cipher(order)
    
unscrambled = input('input a phrase to encrypt (lowercase): ')
scrambled = apply_cipher(cipher,unscrambled)

print('\n')
print('encrypted phrase: ', scrambled)

print('\n') 

max_swaps = 10000
deorder = np.random.choice(26,26,replace = False)
decipher = get_cipher(deorder)
    
deciphered = apply_cipher(decipher, scrambled)
deciphered_freqs = get_freqs(deciphered)
best_score = get_score_2(deciphered)

for swap in range(max_swaps):
    proposed_decipher = propose_decipher(decipher)
    phrase = apply_cipher(proposed_decipher,scrambled)
    #phrase_freqs = get_freqs(phrase)
    temp_score = get_score_2(phrase)
    if should_swap(temp_score, best_score):
        decipher = proposed_decipher
        best_score = temp_score


final_phrase = apply_cipher(decipher,scrambled)
print('decrypted phrase: ',phrase)


    
