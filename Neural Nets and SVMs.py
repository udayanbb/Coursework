# 6.034 Lab 6 2015: Neural Nets & SVMs

from nn_problems import *
from svm_problems import *
from math import e, sqrt

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2, 1]

nn_cross = [2, 2, 1]

nn_stripe = [3, 1]

nn_hexagon = [6, 1]


TEST_NN_GRID = False
nn_grid = []

# Helper functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"

    if x >= threshold:
        return 1
    else:
        return 0

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1/(1+ pow(e, -steepness * (x - midpoint)))

def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -0.5 * pow(desired_output - actual_output, 2)

# Forward propagation
def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""

    neurons = net.topological_sort()

    output_dict = {}


    for neuron in neurons:
        output = 0
        inputs = net.get_incoming_wires(neuron)
        for input in inputs:
            source = input.startNode
            if source in input_values:
                output+= input_values[source]*input.weight
            else:
                if isinstance(source, int):
                    output += source*input.weight
                else:
                    output += output_dict[source]*input.weight
        output_dict[neuron] = threshold_fn(output)

    return (output_dict[neurons[-1]], output_dict)



# Backward propagation
def calculate_deltas(net, input_values, desired_output):
    """Computes the update coefficient (delta_B) for each neuron in the
    neural net.  Uses sigmoid function to compute output.  Returns a dictionary
    mapping neuron names to update coefficient (delta_B values)."""
    outputs = forward_prop(net, input_values, sigmoid)
    outputs = outputs[-1]
    deltas = {}

    neurons = reversed(net.topological_sort())
    for neuron in neurons:
        if net.is_output_neuron(neuron):
            deltas[neuron] = outputs[neuron] * (1- outputs[neuron]) * (desired_output - outputs[neuron])
        else:
            outgoings = 0
            for out in net.get_outgoing_wires(neuron):
                outgoings += out.weight * deltas[out.endNode]
            deltas[neuron] = outputs[neuron] * (1- outputs[neuron]) * outgoings



    return deltas

def update_weights(net, input_values, desired_output, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses
    sigmoid function to compute output.  Returns the modified neural net, with
    updated weights."""

    outputs = forward_prop(net, input_values, sigmoid)
    outputs = outputs[-1]
    deltas = calculate_deltas(net, input_values, desired_output)

    for wire in net.wires:
        if not wire.startNode in outputs:
            if isinstance(wire.startNode, int):
                wire.weight = wire.weight + r * wire.startNode * deltas[wire.endNode]
            else:
                wire.weight = wire.weight + r * input_values[wire.startNode] * deltas[wire.endNode]
        else:
            if not wire.endNode == 'OUT':
                wire.weight = wire.weight + r * outputs[wire.startNode] * deltas[wire.endNode]
    return net

def back_prop(net, input_values, desired_output, r=1, accuracy_threshold=-.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses sigmoid
    function to compute output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""


    iterations = 0
    output = forward_prop(net, input_values, sigmoid)[0]

    while accuracy(desired_output, output) < accuracy_threshold:
        update_weights(net, input_values, desired_output, r)
        output = forward_prop(net, input_values, sigmoid)[0]
        iterations += 1

    return (net, iterations)




#### SUPPORT VECTOR MACHINES ###################################################

# Vector math
def dot_product(u, v):

    output = 0
    for i in range(len(u)):
        output += u[i] * v[i]

    return output

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return sqrt(dot_product(v, v))

# Equation 1
def positiveness(svm, point):
    return dot_product(svm.boundary.w, point.coords) + svm.boundary.b


def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's classification
    is unknown.  Returns +1 or -1, or 0 if point is on boundary"""
    output = dot_product(svm.boundary.w, point.coords) + svm.boundary.b
    if output > 0:
        return 1
    elif output < 0:
        return -1
    else:
        return 0

# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    return 2/norm(svm.boundary.w)

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""

    errors = set()
    for point in svm.training_points:
        if point in svm.support_vectors:
            if not positiveness(svm, point) == point.classification:
                errors.add(point)
        elif abs(positiveness(svm, point)) <= 1:
            errors.add(point)

    return errors

# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""

    errors = set()
    for point in svm.training_points:
        if point in svm.support_vectors:
            if point.alpha <= 0:
                errors.add(point)
        elif not point.alpha == 0:
            errors.add(point)

    return errors

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""

    sum = 0
    vect_sum = None

    for point in svm.support_vectors:
        if point.classification == 1:
            sum += point.alpha
            if vect_sum == None:
                vect_sum = scalar_mult(point.alpha, point.coords)
            else:
                vect_sum = vector_add(vect_sum, scalar_mult(point.alpha, point.coords))
        else:
            sum -= point.alpha
            if vect_sum == None:
                vect_sum = scalar_mult(-point.alpha, point.coords)
            else:
                vect_sum = vector_add(vect_sum, scalar_mult(-point.alpha, point.coords))

    if not sum == 0:
        #print 'sum error:', sum
        return False

    elif not vect_sum == svm.boundary.w:
        #print 'vector error:', vect_sum, '\t', 'should be', svm.boundary.w
        return False

    else:
        return True


# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""

    errors = set()
    for point in svm.training_points:
        if not classify(svm, point) == point.classification:
            errors.add(point)
    return errors

