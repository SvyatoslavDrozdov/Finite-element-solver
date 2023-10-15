import matplotlib.pyplot as plt
import numpy as np
# from data import nodes_function
from data import nodes_function, create_force_and_boundary
from first_generalization import solution

# number_of_point = 1
point_num = []
nodes = np.array([])
counter_for_nodes = 0

R = 0.01
E = 2.1E11
A = np.pi * R ** 2
I = np.pi * R ** 4 / 4


def plot_points_function(X, Y, BC, BC_parameter, line_points, element_number, solve, Forces, E_vector, A_vector,
                         I_vector):
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
            all_node_line_correspondence = []
            all_nodes_on_element_array = []
            nodes = np.array([])
            element_points = set()
            node_counted = 0
            for e in range(0, len(X_nodes)):
                point_1 = line_points[e][0]
                point_2 = line_points[e][1]

                Y_element = Y_nodes[e]
                X_element = X_nodes[e]

                nodes_on_element = set()
                nodes_on_element_array = []
                if point_1 not in element_points:
                    nodes = np.append(nodes, [X_element[0], Y_element[0]])
                    node_counted += 1
                    nodes_on_element.add(node_counted)
                    nodes_on_element_array.append(node_counted)
                    node_line_correspondence.append([line_points[e][0], int(len(nodes) / 2)])
                    element_points.add(point_1)

                for i in range(1, len(X_element) - 1):
                    nodes = np.append(nodes, [X_element[i], Y_element[i]])
                    node_counted += 1
                    nodes_on_element.add(node_counted)
                    nodes_on_element_array.append(node_counted)
                if point_2 not in element_points:
                    nodes = np.append(nodes, [X_element[-1], Y_element[-1]])
                    node_counted += 1
                    nodes_on_element.add(node_counted)
                    nodes_on_element_array.append(node_counted)
                    node_line_correspondence.append([line_points[e][1], int(len(nodes) / 2)])
                    element_points.add(point_2)
                all_node_line_correspondence.append(nodes_on_element)
                all_nodes_on_element_array.append(nodes_on_element_array)
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
            create_force_and_boundary(node_line_correspondence, nodes, line_points, boundary_condition_matrix, Forces)
        # boundary = \
        #     create_force_and_boundary(node_line_correspondence, nodes, line_points, boundary_condition_matrix, Forces)[
        #         1]

        elements = []
        e = 0
        # print(line_points)
        for line in line_points:
            n_1 = line[0]
            n_2 = line[1]
            for i in range(0, len(node_line_correspondence)):
                if node_line_correspondence[i][0] == n_1:
                    node_1 = node_line_correspondence[i][1]
                if node_line_correspondence[i][0] == n_2:
                    node_2 = node_line_correspondence[i][1]
            E_N = element_number[e]
            if node_1 in all_node_line_correspondence[e] and node_2 in all_node_line_correspondence[e]:
                for j in range(0, E_N):
                    elements.append([node_1 + j, node_1 + j + 1])
            elif node_1 in all_node_line_correspondence[e]:
                for j in range(0, E_N - 1):
                    elements.append([node_1 + j, node_1 + j + 1])
                elements.append([node_1, all_nodes_on_element_array[e][-1]])
            elif node_2 in all_node_line_correspondence[e]:
                elements.append([node_1, all_nodes_on_element_array[e][0]])
                for j in range(0, len(all_nodes_on_element_array[e]) - 1):
                    elements.append([all_nodes_on_element_array[e][j], all_nodes_on_element_array[e][j + 1]])
            else:
                try:
                    elements.append([node_1, all_nodes_on_element_array[e][0]])
                    for j in range(0, len(all_nodes_on_element_array[e]) - 1):
                        elements.append([all_nodes_on_element_array[e][j], all_nodes_on_element_array[e][j + 1]])
                    elements.append([all_nodes_on_element_array[e][-1], node_2])
                except:
                    elements.append([node_1, node_2])
            e += 1
        element_properties = []

        for i in range(0, len(elements)):
            # element_properties.append([E, A, I])
            element_properties.append([E_vector[i], A_vector[i], I_vector[i]])
        # print(elements)
        # print(f"all_node_line_correspondence = {all_node_line_correspondence}")
        # print(f"all_nodes_on_element_array = {all_nodes_on_element_array}")
        # solution(nodes, line_points, boundary, force, element_properties)

        updated_boundary_condition_matrix = []
        for i in range(0, len(boundary_condition_matrix)):
            updated_boundary_condition_matrix.append(["free", ""])
        for points in range(0, len(boundary_condition_matrix)):
            for p in range(0, len(boundary_condition_matrix)):
                if node_line_correspondence[p][0] == points + 1:
                    updated_boundary_condition_matrix[node_line_correspondence[p][1] - 1] = boundary_condition_matrix[
                        points]

        # print(f"updated_boundary_condition_matrix = {updated_boundary_condition_matrix}")
        # print(f"boundary_condition_matrix = {boundary_condition_matrix}")
        # print(f"node_line_correspondence = {node_line_correspondence}")
        # print(f"boundary = {boundary}")
        solution(nodes, elements, updated_boundary_condition_matrix, force, element_properties)
