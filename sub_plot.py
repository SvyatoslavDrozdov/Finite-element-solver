import matplotlib.pyplot as plt
import numpy as np
# from data import nodes_function
from data import nodes_function, create_force_and_boundary
from first_generalization import solution

# number_of_point = 1
point_num = []
nodes = np.array([])
counter_for_nodes = 0

# nodes = np.array([
#     [0, 0],  # first node
#     [1, 1],  # second node
#     [2, 0],  # third node
#     [1, 2],  # fourth node
#     [2, 2],  # fifth node
# ])
# nodes = np.array([])
R = 0.01
E = 2.1E11
A = np.pi * R ** 2
I = np.pi * R ** 4 / 4
# element_properties = np.array([
#     [E, A, I],
#     [E, A, I],
#     [E, A, I],
#     [E, A, I]
# ])

# elements = np.array([
#     [1, 2],  # first element
#     [2, 3],  # second element
#     [2, 4],  # third element
#     [4, 5],  # fourth element
# ])

nodes_restrictions = [
    ["hard seal", None],
    ["movable hinge OY", None],
    ["movable hinge OX", None],
    ["movable hinge Cx", 1],
    ["movable hinge Cx", 4]
]
F_x_1 = 0
F_y_1 = 0
M_1 = 0
F_x_2 = 0
F_y_2 = -250_000_0
M_2 = 0
F_x_3 = 0
F_y_3 = 0
M_3 = 0
F_x_4 = 0
F_y_4 = 0
M_4 = 0
F_x_5 = 0
F_y_5 = 0
M_5 = 0

force_vector = np.array([F_y_2, M_2, F_x_3, M_3, F_x_4, F_y_4, M_4, F_x_5, F_y_5, M_5])


def plot_points_function(X, Y, BC, BC_parameter, line_points, element_number, solve, Forces):
    # global number_of_point
    boundary_condition_matrix = []
    global point_num
    global nodes
    global counter_for_nodes
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
        # point_number = point_num[i]
        boundary_condition = BC[i]
        boundary_condition_parameter = BC_parameter[i]
        boundary_condition = rename_boundary_condition(boundary_condition, boundary_condition_parameter)

        boundary_condition_matrix.append([boundary_condition, boundary_condition_parameter])
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
        if solve:
            node_line_correspondence = []
            nodes = np.array([])
            element_points = set()
            for e in range(0, len(X_nodes)):
                point_1 = line_points[e][0]
                point_2 = line_points[e][1]

                Y_element = Y_nodes[e]
                X_element = X_nodes[e]
                if point_1 not in element_points:
                    nodes = np.append(nodes, [X_element[0], Y_element[0]])
                    node_line_correspondence.append([line_points[e][0], int(len(nodes) / 2)])
                    element_points.add(point_1)
                for i in range(1, len(X_element) - 1):
                    nodes = np.append(nodes, [X_element[i], Y_element[i]])
                if point_2 not in element_points:
                    nodes = np.append(nodes, [X_element[-1], Y_element[-1]])
                    node_line_correspondence.append([line_points[e][1], int(len(nodes) / 2)])
                    element_points.add(point_2)

            nodes = nodes.reshape(int(len(nodes) / 2), 2)

        num = 0
        element_points = set()
        for e in range(0, len(X_nodes)):
            point_1 = line_points[e][0]
            point_2 = line_points[e][1]
            Y_element = Y_nodes[e]
            X_element = X_nodes[e]
            plt.plot(X_element, Y_element, marker="o", color="black")
            if point_1 not in element_points:
                plt.text(X_element[0] + d / 2, Y_element[0] + d / 2, f'{num + 1}', color="black")
                element_points.add(point_1)
                num += 1
            for i in range(1, len(X_element) - 1):
                plt.text(X_element[i] + d / 2, Y_element[i] + d / 2, f'{num + 1}', color="black")
                num += 1
            if point_2 not in element_points:
                plt.text(X_element[-1] + d / 2, Y_element[-1] + d / 2, f'{num + 1}', color="black")
                element_points.add(point_2)
                num += 1

    plt.axis('equal')
    plt.grid()
    plt.savefig('foo.png')

    if solve:
        force = \
            create_force_and_boundary(node_line_correspondence, nodes, line_points, boundary_condition_matrix, Forces)[
                0]
        boundary = \
            create_force_and_boundary(node_line_correspondence, nodes, line_points, boundary_condition_matrix, Forces)[
                1]
        force = force.reshape(3 * len(force))
        # print(node_line_correspondence)
        # print(f"boundary_condition_matrix = {boundary_condition_matrix}")
        # print(f"boundary = f{boundary}")
        element_properties = []
        for i in range(0, len(line_points)):
            element_properties.append([E, A, I])

        elements = []
        e = 0
        print(line_points)
        for line in line_points:
            n_1 = line[0]
            n_2 = line[1]
            for i in range(0, len(node_line_correspondence)):
                if node_line_correspondence[i][0] == n_1:
                    node_1 = node_line_correspondence[i][1]
                if node_line_correspondence[i][0] == n_2:
                    node_2 = node_line_correspondence[i][1]
            print(f"node_1 = {node_1}")
            print(f"node_1 = {node_2}")
            E_N = element_number[e]
            print(f"E_N = {E_N}")
            if node_1 < node_2:
                for j in range(0, E_N-1):
                    elements.append([node_1 + j * E_N, node_1 + (j + 1) * E_N])
                elements.append([node_1 + E_N-1, node_2])
            else:
                for j in range(0, E_N):
                    elements.append([node_1 + j * E_N, node_1 + (j + 1) * E_N])
            e += 1
        print(elements)
        # solution(nodes, line_points, boundary, force, element_properties)
        solution(nodes, elements, boundary, force, element_properties)