import matplotlib.pyplot as plt
import numpy as np
from data import nodes_function, create_force, force_function
from first_generalization import solution

point_num = []
nodes = np.array([])
counter_for_nodes = 0

R = 0.01
E = 2.1E11
A = np.pi * R ** 2
I = np.pi * R ** 4 / 4


def plot_points_function(X, Y, BC, BC_parameter, line_points, element_number, solve, Forces, E_vector, A_vector,
                         I_vector, normal_force_functions):
    boundary_condition_matrix = []
    global point_num
    global nodes
    global counter_for_nodes
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

        lines_elements = []
        elements = []
        e = 0

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
                    lines_elements.append([e + 1, [node_1 + j, node_1 + j + 1]])
            elif node_1 in all_node_line_correspondence[e]:
                for j in range(0, E_N - 1):
                    elements.append([node_1 + j, node_1 + j + 1])
                    lines_elements.append([e + 1, [node_1 + j, node_1 + j + 1]])
                elements.append([node_1, all_nodes_on_element_array[e][-1]])
                lines_elements.append([e + 1, [node_1, all_nodes_on_element_array[e][-1]]])
            elif node_2 in all_node_line_correspondence[e]:
                elements.append([node_1, all_nodes_on_element_array[e][0]])
                lines_elements.append([e + 1, [node_1, all_nodes_on_element_array[e][0]]])
                for j in range(0, len(all_nodes_on_element_array[e]) - 1):
                    elements.append([all_nodes_on_element_array[e][j], all_nodes_on_element_array[e][j + 1]])
                    lines_elements.append(
                        [e + 1, [all_nodes_on_element_array[e][j], all_nodes_on_element_array[e][j + 1]]])
            else:
                try:
                    elements.append([node_1, all_nodes_on_element_array[e][0]])
                    lines_elements.append([e + 1, [node_1, all_nodes_on_element_array[e][0]]])
                    for j in range(0, len(all_nodes_on_element_array[e]) - 1):
                        elements.append([all_nodes_on_element_array[e][j], all_nodes_on_element_array[e][j + 1]])
                        lines_elements.append(
                            [e + 1, [all_nodes_on_element_array[e][j], all_nodes_on_element_array[e][j + 1]]])
                    elements.append([all_nodes_on_element_array[e][-1], node_2])
                    lines_elements.append([e + 1, [all_nodes_on_element_array[e][-1], node_2]])
                except:
                    elements.append([node_1, node_2])
                    lines_elements.append([e + 1, [node_1, node_2]])
            e += 1
        element_properties = []

        for i in range(0, len(elements)):
            element_properties.append([E_vector[i], A_vector[i], I_vector[i]])

        # print(f"node_line_correspondence = {node_line_correspondence}")
        # print(f"nodes = {nodes}")
        updated_boundary_condition_matrix = []
        for i in range(0, len(nodes)):
            updated_boundary_condition_matrix.append(["free", ""])

        for points in range(0, len(boundary_condition_matrix)):
            for p in range(0, len(boundary_condition_matrix)):
                if node_line_correspondence[p][0] == points + 1:
                    # print()
                    updated_boundary_condition_matrix[node_line_correspondence[p][1] - 1] = boundary_condition_matrix[
                        points]

        # print(f"lines_elements = {lines_elements}")
        # print(f"line_points = {line_points}")

        # force_density = force_function(func, s)
        # normal_force_functions
        def v(point_coordinate, lgth):
            N = np.array([
                1 - 3 * point_coordinate ** 2 / lgth ** 2 + 2 * point_coordinate ** 3 / lgth ** 3,
                point_coordinate - 2 * point_coordinate ** 2 / lgth + point_coordinate ** 3 / lgth ** 2,
                3 * point_coordinate ** 2 / lgth ** 2 - 2 * point_coordinate ** 3 / lgth ** 3,
                -point_coordinate ** 2 / lgth + point_coordinate ** 3 / lgth ** 2
            ])
            return N

        def Integral(f_1, f_2, L, len_global_element):
            num_for_integral = 2000
            X_integral = np.linspace(0, L, num_for_integral)
            dx = L / num_for_integral
            integral = 0
            for x_loc in X_integral:
                y_loc = f_1(x_loc, L) * f_2(len_global_element + x_loc)
                integral += y_loc * dx
            return integral

        def force_creator(force_func, all_nodes, nod_1, nod_2, len_global_element, counter):
            x_1_fc = nodes[node_1 - 1][0]
            y_1_fc = nodes[node_1 - 1][1]
            x_2_fc = nodes[node_2 - 1][0]
            y_2_fc = nodes[node_2 - 1][1]
            length = ((x_1_fc - x_2_fc) ** 2 + (y_1_fc - y_2_fc) ** 2) ** 0.5
            F_local = Integral(v, force_func, length, len_global_element)

            sin_A = (y_2_fc - y_1_fc) / length
            cos_A = (x_2_fc - x_1_fc) / length
            node_1_force = [-F_local[0] * sin_A, F_local[0] * cos_A, F_local[1]]
            node_2_force = [-F_local[2] * sin_A, F_local[2] * cos_A, F_local[3]]

            counter += 1
            return [node_1_force, node_2_force]

        force_nodes = []
        length_global_element = 0
        counter = 0
        for l in range(0, len(line_points)):
            force_dens = force_function(normal_force_functions[l])
            for i in range(0, len(lines_elements)):
                if lines_elements[i][0] == l + 1:
                    [node_1, node_2] = lines_elements[i][1]
                    x_1_for_creator = nodes[node_1 - 1][0]
                    y_1_for_creator = nodes[node_1 - 1][1]
                    x_2_for_creator = nodes[node_2 - 1][0]
                    y_2_for_creator = nodes[node_2 - 1][1]

                    nod_fo = force_creator(force_dens, nodes, node_1, node_2, length_global_element, counter)
                    counter += 1
                    length_global_element += ((x_1_for_creator - x_2_for_creator) ** 2 + (
                            y_1_for_creator - y_2_for_creator) ** 2) ** 0.5
                    force_nodes.append([node_1, nod_fo[0], [node_1, node_2]])
                    force_nodes.append([node_2, nod_fo[1], [node_1, node_2]])
        print(force_nodes)

        node_forces = []
        for n in range(1, len(nodes) + 1):
            node_forces.append([n])

        # print(f"print(elements) = {elements}")
        print(f"force_nodes = {force_nodes}")
        for n in range(1, len(nodes) + 1):
            sum_Fx = 0
            sum_Fy = 0
            sum_M = 0
            for i in range(0, len(force_nodes)):
                if n == force_nodes[i][0]:
                    sum_Fx += force_nodes[i][1][0]
                    sum_Fy += force_nodes[i][1][1]
                    sum_M += force_nodes[i][1][2]
            node_forces[n - 1].append([sum_Fx, sum_Fy, sum_M])
        # print(f"force_nodes = {force_nodes}")
        # print(f"node_forces = {node_forces}")
        force = create_force(node_line_correspondence, nodes, line_points, boundary_condition_matrix, Forces,
                             node_forces)
        print(f"force = {force}")

        solution(nodes, elements, updated_boundary_condition_matrix, force, element_properties)
