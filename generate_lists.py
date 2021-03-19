#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:50:07 2021

@author: micaelavieira
"""

import numpy as np
import random

def latin_square(n: int) -> np.ndarray:
    """
    Purpose
    -------
    Return a n x n balanced latin square.

    Parameters
    ----------
    n : int
        Order of the latin square.

    Returns
    -------
    square : np.ndarray
        Latin square.
    """
    square = np.empty((n,n))*np.nan
    square[:,0] = np.arange(1, n+1, dtype=int)
    
    shift = (.5-np.mod(np.array(np.arange(1,n)),2))/.5*np.ceil(np.array(np.arange(1,n))/2)
    shift = shift.astype(int)
  
    for col in np.arange(1, n):
        square[:, col] = np.roll(square[:,0], shift[col-1])
    return square

def save_filename_with_lists_according_to_latin_square(filename: str):
    """
    Purpose
    -------
    Take input from a file and split them into different lists according to a
    latin square.

    Parameters
    ----------
    filename : str
        Name of the file containing the input data in the form 
        'sentence \t version \t text'.

    Returns
    -------
    None.
    """
    #insert filler and experimental stimuli in lists of dictionaries
    filler_triples = []
    stimuli_triples = []
    with open(filename) as f:
        line_triples = [line.strip('\n') for line in f if line != '\n']
        for line_triple in line_triples:
            line_triple_split = line_triple.split('\t')
            if int(line_triple_split[0]) == 0:
                filler_dictionary = {'text': line_triple_split[2], 'sentence': line_triple_split[0], 'version': line_triple_split[1]}
                filler_triples.append(filler_dictionary)
            else:
                stimulus_dictionary = {'text': line_triple_split[2], 'sentence': line_triple_split[0], 'version': line_triple_split[1]}
                stimuli_triples.append(stimulus_dictionary)
    
    #get values for amount of sentences and versions
    amount_sentences = len(set([i.get('sentence') for i in stimuli_triples]))
    amount_versions = len([i.get('version') for i in stimuli_triples if i.get('sentence')=='1'])
    
    #save the experimental stimuli in lists according to a latin square
    final_list_of_stimuli_for_list = []
    latin_square_amount_versions = latin_square(amount_versions)
    for i in np.arange(amount_versions):
        single_list_of_stimuli_for_list = []
        order = [int(i) for i in latin_square_amount_versions[i]]
        counter = 0
        for j in np.arange(1, amount_sentences+1):
            stimulus = [i for i in stimuli_triples if i.get('sentence')==str(j) and i.get('version')==str(order[counter])][0]
            single_list_of_stimuli_for_list.append(stimulus)
            counter += 1
            if counter > len(order)-1:
                counter = 0
        final_list_of_stimuli_for_list.append(single_list_of_stimuli_for_list)
    
    #create a random order to distribute stimuli and filler
    order_stimuli_filler = ['f' for i in np.arange(len(filler_triples))] + ['s' for i in np.arange(amount_sentences)]
    random.shuffle(order_stimuli_filler)
    
    #save stimuli to files (one for each list)
    counter_list = 1
    counter_stimuli = 0
    counter_filler = 0
    for i in final_list_of_stimuli_for_list:
        with open('Data/list_of_stimuli_'+str(counter_list)+'.txt', 'w') as f:
            for j in order_stimuli_filler:
                if j == 's':
                    f.write(i[counter_stimuli].get('sentence')+'\t'+i[counter_stimuli].get('version')+'\t'+i[counter_stimuli].get('text')+'\n')
                    counter_stimuli += 1
                elif j == 'f':
                    f.write(filler_triples[counter_filler].get('sentence')+'\t'+filler_triples[counter_filler].get('version')+'\t'+filler_triples[counter_filler].get('text')+'\n')
                    counter_filler += 1
            counter_stimuli = 0
            counter_filler = 0
        counter_list += 1
    return


def main():
    save_filename_with_lists_according_to_latin_square('Data/input_data.txt')
    
if __name__ == "__main__":
    main()