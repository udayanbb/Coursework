'''
Problem statement:
find_occurrences(T, W): given a text string T and a target word W of length l,
returns an ascending list of indices i such that T[i : i + l] is a permutation
of W
ARGS:
  T - the string to search
  W - the string whose permutations you want to search for
RETURN:
  a list of indices in T such that T[i : i + l] is a permutation of W; if there
  are no such indices, the empty list should be returned
'''

import string

def find_occurrences(T, W):

    freq_dict = {}
    actual_dict = {}

    output_list = []


    for char in W:
        if char in actual_dict:
            actual_dict[char] += 1
        else:
            actual_dict[char] = 1

    for char in T[0:len(W)]:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1

    if freq_dict == actual_dict:
        output_list.append(0)

    for index in range(1, len(T) - len(W) + 1):
        freq_dict[T[index - 1]] -= 1
        if T[index + len(W) - 1] in freq_dict:
            freq_dict[T[index + len(W) - 1]] += 1
        else:
            freq_dict[T[index + len(W) - 1]] = 1
        if freq_dict == actual_dict:
            output_list.append(index)

    return output_list














