import matplotlib.pyplot as plt
import numpy as np
from data import nodes_function
from first_generalization import solution

# number_of_point = 1
point_num = []

nodes = np.array([])


def plot_points_function(X, Y, BC, BC_parameter, line_points, element_number, solve):
    # global number_of_point
    global point_num
    global nodes
    # if add_point == 1:
    #     point_num.append(number_of_point)
    point_num = np.linspace(1, len(X), len(X))

    def rename_boundary_condition(condition, condition_parameter):
        if condition == "":
            return "free"
        if condition == "шарнир" and condition_parameter == "":
            return "hinge"
        if condition == "шарнир" and condition_parameter == "OX":
            return "movable hinge OX"
        if condition == "шарнир" and condition_parameter == "OY":
            return "movable hinge OY"
        if condition == "шарнир" and type(condition_parameter) == float:
            return "movable hinge Cx"
        if condition == "заделка":
            return "hard seal"

    plt.figure(figsize=(8, 8))
    points_number = len(point_num)
    for i in range(0, points_number):
        if len(X) == 1:
            d = 0.1
        else:
            d = max(max(Y), -min(Y), max(X), -min(X)) / 10
        x = X[i]
        y = Y[i]
        point_number = point_num[i]
        boundary_condition = BC[i]
        boundary_condition_parameter = BC_parameter[i]
        boundary_condition = rename_boundary_condition(boundary_condition, boundary_condition_parameter)

        correct_input = 0

        if boundary_condition == "free":
            plt.plot(x, y, marker='o', color="black")
            correct_input = 1
        if boundary_condition == "hard seal":
            plt.plot(x, y, 'Dk')
            plt.errorbar(x, y, xerr=0.1, yerr=0.1, color="black")
            correct_input = 1
        if boundary_condition == "movable hinge OY":
            plt.plot(x, y, 'or')
            base_x = [x, x]
            base_y = [y - d, y + d]
            plt.plot(base_x, base_y, color="red")
            correct_input = 1
        if boundary_condition == "movable hinge OX":
            plt.plot(x, y, 'or')
            base_x = [x - d, x + d]
            base_y = [y, y]
            correct_input = 1
            plt.plot(base_x, base_y, color="red")
        if boundary_condition == "movable hinge Cx":
            local_d = 2 * d
            plt.plot(x, y, 'or')
            x_1 = x - (local_d ** 2 / (2 * (boundary_condition_parameter ** 2 + 1))) ** 0.5
            x_2 = x + (local_d ** 2 / (2 * (boundary_condition_parameter ** 2 + 1))) ** 0.5
            y_1 = boundary_condition_parameter * (x_1 - x) + y
            y_2 = boundary_condition_parameter * (x_2 - x) + y
            base_x = [x_1, x_2]
            base_y = [y_1, y_2]
            plt.plot(base_x, base_y, color="red")
            correct_input = 1
        if boundary_condition == "hinge":
            plt.plot(x, y, 'or')
            base_x = [x]
            base_y = [y]
            plt.plot(base_x, base_y, color="red", marker="o")
            correct_input = 1
        if correct_input == 1:
            plt.text(x - d / 2, y + d / 2, f'{i + 1}', color="green")
    if line_points:
        [X_nodes, Y_nodes] = nodes_function(X, Y, line_points, element_number)
        num = 0
        for l in range(0, len(line_points)):
            # plt.plot([X[line_points[l][0] - 1], X[line_points[l][1] - 1]],
            #          [Y[line_points[l][0] - 1], Y[line_points[l][1] - 1]])
            plt.plot(X_nodes[l], Y_nodes[l], marker="o", color="black")
            for j in range(0, len(X_nodes[l])):
                if j != 0 or l == 0:
                    print(num)
                    plt.text(X_nodes[l][j] + d / 2, Y_nodes[l][j] + d / 2, f'{num + 1}', color="black")
                    if solve:
                        nodes = np.append(nodes, [X_nodes[l][j], Y_nodes[l][j]])
                    num += 1
    plt.axis('equal')
    plt.grid()
    plt.savefig('foo.png')
    if solve:
        solution()

