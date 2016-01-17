from itertools import islice
from sets import Set


'''
Problem Statement:
make_sentence(s, L): given a string of letters s and a list of valid words L,
inserts spaces into s to form a valid sentence and returns the sentence as a
string. If there are multiple valid sentences, then the one with the highest
score will be returned, where score is defined as the sum of the cubes
of the lengths of the words in the sentence.
ARGS:
  s - the string of letters to transform into a sentence
  L - the list of valid words allowed in the sentence
RETURN:
  the sentence string resulting from inserting spaces into s
'''
def make_sentence(s, L):

    size = len(s)

    i = 0

    scores = [0] * (size + 1)
    spaces = [0] * (size + 1)

    words = {}

    if '' in L:
        L.remove('')

    max_len = 0
    for word in L:
        wsize = len(word)
        words[word] = pow(wsize, 3)
        max_len = max(max_len, wsize)

    while i <= size:
        if not scores[i] == 0 or i == 0:
            wsize = 1
            while wsize <= max_len and i + wsize <= size:
                word = s[i:i + wsize]
                if word in words:
                    new_score = words[word] + scores[i]
                    if new_score > scores[i + wsize]:
                        scores[i + wsize] = new_score
                        spaces[i + wsize] = i
                wsize += 1
        i += 1

    if scores[size] == 0:
        return None
    else:
        correct_spaces = []
        prev_space_loc = spaces[size]

        while not prev_space_loc == 0:
            correct_spaces.append(prev_space_loc)
            prev_space_loc = spaces[prev_space_loc]

        output = []
        prev_space_loc = 0

        for space in reversed(correct_spaces):
            output.append(str(s[prev_space_loc:space]))
            prev_space_loc = space
        output.append(str(s[prev_space_loc:]))
        space = " "
        return space.join(output)


'''

# Examples
s = 'abeareatspies'
L = ['a', 'abe', 'are', 'at', 'bear', 'eats', 'pies', 'spies']
print make_sentence(s, L)
# should print 'a bear eats pies'

L.remove('a')
L.remove('at')
print make_sentence(s, L)
# should return None

s = 'a' * 40000
L = []
for i in range(25):
    L.append('a' * (i * 2))


print make_sentence(s, L)
import time

t0 = time.time()

s = 'a' * 40001
L = []
for i in range(25):
    L.append('a' * (i * 2))
print make_sentence(s, L)

t1 = time.time()

print (t1-t0)

'''


