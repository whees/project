# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:50:40 2022

@author: lcuev
"""
import numpy as np
from string import ascii_lowercase as alphabet
import time
from math import exp,log
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


np.random.seed(int(time.time()))
alpha = alphabet  + ' '
length = len(alpha)

dicts = {}
revdicts = {}

for index,letter in enumerate(alpha):
    dicts[letter] = index
    
for index,letter in enumerate(alpha):
    revdicts[index] = letter



alpha_freqs = np.load('alphabet_wiki.npy',allow_pickle = 'True').item()

def get_freq_dict(string):
    ret = {}
    for a in alpha:
        for b in alpha:
            for c in alpha:
                key = a + b + c
                ret[key] = 0
    for i in range(1,len(string) - 1):
        key = string[i-1] + string[i] + string[i+1]
        if key in ret:
            ret[key] +=1
    
    norm = 0
    for a in alpha:
        for b in alpha:
            for c in alpha:
                key = a + b + c
                norm += ret[key]
    for a in alpha:
        for b in alpha:
            for c in alpha:
                key = a + b + c
                ret[key] /= norm     
    return ret
        
def freq_score(ph):
    ret = {}
    for i in range(1,len(ph)-1):
        key = ph[i-1] + ph[i] +  ph[i + 1]
        if key in alpha_freqs:
            if key in ret:
                ret[key] += log(alpha_freqs[key]) 
            else:
                ret[key] = log(alpha_freqs[key])
    return ret
                
def resum(log_dict):
    ret = 0
    for key in log_dict:
        ret += exp(log_dict[key])
    return ret

def get_score(ph):
    ret = 0
    for i in range(1,len(ph)-1):
        if ph[i-1] in alpha and ph[i] in alpha and ph[i+1] in alpha:
            key = ph[i-1] + ph[i] + ph[i + 1]
            k = alpha_freqs[key]
            if  k > 0:
                ret += log(k)
            else:
                ret -= 10
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

    

def get_rand_cipher():
    ordr = np.random.choice(26,26,replace = False)
    ret = {}
    for index,letter in enumerate(alphabet):
        ret[letter] = alphabet[ordr[index]]
    ret[' '] = ' '
    return ret

def should_swap(proposed_score, current_score,rate):
    diff = proposed_score - current_score
    if diff > 0:
        comp = 1.1
    else:
        comp = exp(diff*rate)
    
    return comp > np.random.random()


def should_swap_v2(proposed_score, current_score,rate):
    #diff = proposed_score - current_score
    diff =  proposed_score - current_score
    ret = False
    if diff > 0 or exp(diff) > np.random.random():
        print(exp(diff))
        ret = True
    
    return ret

cipher = get_rand_cipher()
    
unscrambled = ' jack and jill went up the hill to fetch a pail of water '
scrambled = apply_cipher(cipher,unscrambled)

print('\n')
print('encrypted phrase: ', scrambled)

print('\n') 
repeat = True
while repeat:
    max_swaps = 3000
    decipher = get_rand_cipher()
    max_futures = 30
    present_futures = 0
    futures = []
    phrases = [] 
    
    deciphered = apply_cipher(decipher, scrambled)
    #phrase_freqs = get_freq_dict(deciphered)
    best_score = get_score(deciphered)
    times = []
    bests = []
    rate = 0.8
    
    
    for swap in range(max_swaps):
        proposed_decipher = propose_decipher(decipher)
        phrase = apply_cipher(proposed_decipher,scrambled)
        #phrase_freqs = get_freq_dict(phrase)
        temp_score = get_score(phrase)
        do_swap = should_swap(temp_score, best_score,rate)
        if do_swap:
            if temp_score < best_score and present_futures < max_futures:
                futures += [decipher]
                present_futures += 1
    
            decipher = proposed_decipher
            best_score = temp_score
            bests += [best_score]
            times += [swap]
    if best_score > -440:
        repeat = False
            
phrases += [phrase]
        
plt.plot(times,np.multiply(-1,bests))
plt.show()
best_best = best_score
future_scores = []
times = range(max_swaps)
ts = []

print('planting seeds...')
seeds = '['
for i in futures:
    seeds += ' '
seeds +=']'
    
_last_print_len = 0 
def reprint(msg, finish=False): 
    global _last_print_len 
     
    print(' '*_last_print_len, end='\r') 
     
    if finish: 
        end = '\n' 
        _last_print_len = 0 
    else: 
        end = '\r' 
        _last_print_len = len(msg) 
     
    print(msg, end=end) 


for n,future in enumerate(futures):
    reprint(seeds)
    seeds =  '[' +'.' + '.' * n + ' ' * (len(futures)-2 - n) + ']'
    t = [0]
    deciphered = apply_cipher(future,scrambled)
    #phrase_freqs = get_freq_dict(deciphered)
    best_score = get_score(deciphered)
    rate = 0.7
    scores = [best_score]


    for swap in range(max_swaps):
        proposed_decipher = propose_decipher(decipher)
        phrase = apply_cipher(proposed_decipher,scrambled)
        #phrase_freqs = get_freq_dict(phrase)
        temp_score = get_score(phrase)
        do_swap = should_swap(temp_score, best_score,rate)
        if do_swap:
            decipher = proposed_decipher
            best_score = temp_score
            if best_score > best_best:
                best_best = best_score
                best_phrase = phrase
            scores += [best_score]
            t += [swap]
    ts += [t]
    phrases += [phrase]
    future_scores += [scores]

min_min = min(np.multiply(-1,future_scores[0]))
for j in future_scores:
    if min(np.multiply(-1,j)) < min_min:
        min_min = min(np.multiply(-1,j))
    
color_list = list(mcolors.TABLEAU_COLORS)
for i,j in enumerate(future_scores):
    plt.plot(ts[i],np.multiply(-1,j),color = color_list[i % len(color_list)])
    plt.fill_between(ts[i], min_min, np.multiply(-1,j), color = color_list[i % len(color_list)], alpha=1)

print('\n')


for phrase in phrases:
    print(phrase,'\n')





    
