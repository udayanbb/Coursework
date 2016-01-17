from classify import *
import math

### Data sets for the lab
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')



### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)




def euclidean_distance(list1, list2):
    val = 0
    for i in range(len((list1))):
        val += pow((list1[i] - list2[i]), 2)
    return pow(val, 0.5)


my_classifier = nearest_neighbors(euclidean_distance, 3)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

def information_disorder(yes, no):



    list1 = yes[:]
    list2 = no[:]

    len1= len(list1)
    len2 = len(list2)
    len_total = len1+len2

    len1 *= 1.0
    len2 *= 1.0

    list_1_uniques = []
    for element in list1:
        if  list_1_uniques.count(element) == 0:
            list_1_uniques.append(element)



    list_2_uniques = []
    for element in list2:
        if  list_2_uniques.count(element) == 0:
            list_2_uniques.append(element)


    list_1_intermediate_sum = 0
    for element in list_1_uniques:
        list_1_intermediate_sum += -(list1.count(element)/len1)* math.log((list1.count(element)/len1),2)

    list_1_sum = (len1/len_total) * list_1_intermediate_sum

    list_2_intermediate_sum = 0
    for element in list_2_uniques:
        list_2_intermediate_sum += -(list2.count(element)/len2)* math.log((list2.count(element)/len2),2)

    list_2_sum = (len2/len_total) * list_2_intermediate_sum

    total_sum = list_1_sum + list_2_sum

    return total_sum


#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)


def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)


