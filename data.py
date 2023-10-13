import numpy as np


def nodes_function(X, Y, line_points, element_number, solve):
    X_node = []
    Y_node = []
    for l in range(0, len(line_points)):
        x_1 = X[line_points[l][0] - 1]
        x_2 = X[line_points[l][1] - 1]
        y_1 = Y[line_points[l][0] - 1]
        y_2 = Y[line_points[l][1] - 1]
        X_node.append(np.linspace(x_1, x_2, element_number[l] + 1))
        Y_node.append(np.linspace(y_1, y_2, element_number[l] + 1))

    return [X_node, Y_node]
