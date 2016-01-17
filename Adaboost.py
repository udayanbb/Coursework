# 6.034 Lab 7 2015: Boosting (Adaboost)

from collections import OrderedDict
from math import log as ln
INF = float('inf')

# Helper function for pick_best_classifier and adaboost
def fix_roundoff_error(inp, n=15):
    fix_val = lambda val: round(abs(val),n)*[-1,1][val>=0]
    if isinstance(inp, list): return map(fix_val, inp)
    if isinstance(inp, dict): return {key: fix_val(inp[key]) for key in inp}
    return fix_val(inp)


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""

    weights = {}

    for point in training_points:
        weights[point] = 1.0/len(training_points)

    return weights


def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""

    error_weights = {}

    for classifier in classifier_to_misclassified:
        classifier_error = 0
        for misclassified in classifier_to_misclassified[classifier]:
            classifier_error += point_to_weight[misclassified]
        error_weights[classifier] = classifier_error

    return error_weights


def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier.  Best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""


    #print max(list, key = lambda entry: entry[1])[0]


    if use_smallest_error:
        list = sorted(classifier_to_error_rate.items(), key = lambda entry: entry[0], reverse = False)
        return min(list, key = lambda entry: fix_roundoff_error(entry[1]))[0]
    else:
        list = sorted(classifier_to_error_rate.items(), key = lambda entry: entry[0], reverse = False)
        new_list = []
        for element in list:
            new_list.append((element[0], fix_roundoff_error(abs( 0.5 - element[1] )) ))
        #print new_list, 'r: ', max(new_list, key = lambda entry: entry[1])[0]

        new_list = sorted(new_list, key = lambda entry: fix_roundoff_error(entry[1]), reverse = True)

        #print new_list, '\n'

    return new_list[0][0]


def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""

    if error_rate == 0:
        return INF
    elif error_rate == 1:
        return -INF
    else :
        return 0.5 * ln((1-error_rate)/(error_rate))


def is_good_enough(H, training_points, classifier_to_misclassified,
                   mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""

    misclassified = 0

    H_dict = dict(H)

    for point in training_points:
        misclassified_mass = 0
        classified_mass = 0
        for classifier in H_dict:
            if point in classifier_to_misclassified[classifier]:
                misclassified_mass += H_dict[classifier]
            else:
                classified_mass += H_dict[classifier]
        if fix_roundoff_error(misclassified_mass) >= fix_roundoff_error(classified_mass):
            misclassified += 1

    if misclassified > mistake_tolerance:
        return False
    else:
        return True


def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""

    for point in point_to_weight:
        if point in misclassified_points:
            point_to_weight[point] = 0.5 * (1.0/(error_rate)) * point_to_weight[point]
        else:
            point_to_weight[point] = 0.5 * (1.0/(1.0 - error_rate)) * point_to_weight[point]

    return point_to_weight

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_num_rounds=INF):
    """Performs the Adaboost algorithm for up to max_num_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""


    H = []

    weights = initialize_weights(training_points)

    while (True):
        error_rates = calculate_error_rates(weights, classifier_to_misclassified)

        if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
            return H
        elif len(H) >= max_num_rounds:
            return H
        elif fix_roundoff_error(error_rates[pick_best_classifier(error_rates, use_smallest_error)]) == 0.5:
            return H

        best_classifier = pick_best_classifier(error_rates, use_smallest_error)

        voting_power = calculate_voting_power(error_rates[best_classifier])

        H.append((best_classifier, voting_power))



        weights = update_weights(weights, classifier_to_misclassified[best_classifier], error_rates[best_classifier])





