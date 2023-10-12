import numpy as np
import matplotlib.pyplot as plt
from data import nodes, elements, nodes_restrictions, force_vector

R = 0.01
L = 1
P = 100

E = 2.1E11
A = np.pi * R ** 2
I = np.pi * R ** 4 / 4

EAL = E * A / L
EIL3 = 12 * E * I / L ** 3
EIL2 = 6 * E * I / L ** 2
EIL1_2 = 2 * E * I / L
EIL1_4 = 4 * E * I / L

local_stiffness_matrix = np.array([
    [EAL, 0, 0, - EAL, 0, 0],
    [0, EIL3, EIL2, 0, -EIL3, EIL2],
    [0, EIL2, EIL1_4, 0, -EIL2, EIL1_2],
    [-EAL, 0, 0, EAL, 0, 0],
    [0, -EIL3, -EIL2, 0, EIL3, -EIL2],
    [0, EIL2, EIL1_2, 0, -EIL2, EIL1_4]
])

nodes_number = len(nodes)
elements_number = len(elements)


def T(our_element):
    [x_1, y_1] = nodes[our_element[0] - 1]
    [x_2, y_2] = nodes[our_element[1] - 1]
    sin = (y_2 - y_1) / ((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2) ** 0.5
    cos = (x_2 - x_1) / ((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2) ** 0.5
    rotation_matrix = np.array([
        [cos, sin, 0, 0, 0, 0],
        [-sin, cos, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, cos, sin, 0],
        [0, 0, 0, -sin, cos, 0],
        [0, 0, 0, 0, 0, 1]
    ])
    return rotation_matrix


global_element_stiffness_matrix = []
for element in elements:
    stiffness = np.dot(np.dot(T(element).transpose(), local_stiffness_matrix), T(element))
    global_element_stiffness_matrix.append(stiffness)

stiffness_diagonal_matrix = np.zeros((6 * elements_number, 6 * elements_number))
for e in range(0, elements_number):
    for i in range(0, 6):
        for j in range(0, 6):
            stiffness_diagonal_matrix[i + 6 * e][j + 6 * e] = global_element_stiffness_matrix[e][i][j]

H = np.zeros((6 * elements_number, 3 * nodes_number))
k = 0
for i in range(0, elements_number):
    for j in range(0, 2):
        a = elements[i][j]
        H[k][3 * a - 3] = 1
        H[k + 1][3 * a - 2] = 1
        H[k + 2][3 * a - 1] = 1
        k = k + 3

global_stiffness_matrix = np.dot(np.dot(H.transpose(), stiffness_diagonal_matrix), H)
global_len = len(global_stiffness_matrix)


def delete_raw_and_column(matrix, number):
    new_matrix = np.hstack((matrix[:, 0:number], matrix[:, number + 1:]))
    new_matrix = np.vstack((new_matrix[:number], new_matrix[number + 1:]))
    return new_matrix


node_num = 0
for nodes_restriction in nodes_restrictions:
    degree_of_freedom_number = 3 * node_num
    if nodes_restriction[0] == "movable hinge Cx":
        k = nodes_restriction[1]
        column_to_insert = np.array([])
        for node in range(0, nodes_number):
            freedom = 3 * node
            if freedom == degree_of_freedom_number:
                np_string_1 = np.array(
                    [global_stiffness_matrix[freedom][freedom] +
                     k * global_stiffness_matrix[freedom][freedom + 1],
                     global_stiffness_matrix[freedom][freedom + 2], -1])
                np_string_2 = np.array(
                    [global_stiffness_matrix[freedom + 1][freedom] +
                     k * global_stiffness_matrix[freedom + 1][freedom + 1],
                     global_stiffness_matrix[freedom + 1][freedom + 2], 1 / k])
                np_string_3 = np.array(
                    [global_stiffness_matrix[freedom + 2][freedom] +
                     k * global_stiffness_matrix[freedom + 2][freedom + 1],
                     global_stiffness_matrix[freedom + 2][freedom + 2], 0])
            else:
                np_string_1 = np.array(
                    [global_stiffness_matrix[freedom][degree_of_freedom_number] +
                     k * global_stiffness_matrix[freedom][degree_of_freedom_number + 1],
                     global_stiffness_matrix[freedom][degree_of_freedom_number + 2], 0])
                np_string_2 = np.array(
                    [global_stiffness_matrix[freedom + 1][degree_of_freedom_number] +
                     k * global_stiffness_matrix[freedom + 1][degree_of_freedom_number + 1],
                     global_stiffness_matrix[freedom + 1][degree_of_freedom_number + 2], 0])
                np_string_3 = np.array(
                    [global_stiffness_matrix[freedom + 2][degree_of_freedom_number] +
                     k * global_stiffness_matrix[freedom + 2][degree_of_freedom_number + 1],
                     global_stiffness_matrix[freedom + 2][degree_of_freedom_number + 2], 0])
            if node != 0:
                column_to_insert = np.vstack((column_to_insert, np_string_1))
            else:
                column_to_insert = np.append(column_to_insert, np_string_1)
            column_to_insert = np.vstack((column_to_insert, np_string_2))
            column_to_insert = np.vstack((column_to_insert, np_string_3))
        global_stiffness_matrix = np.hstack((np.hstack(
            (global_stiffness_matrix[:, :degree_of_freedom_number], column_to_insert)),
                                             global_stiffness_matrix[:, degree_of_freedom_number + 3:]))
    node_num += 1

degree_of_freedom_number = 0
deleted_number = 0
for nodes_restriction in nodes_restrictions:
    if nodes_restriction[0] == "movable hinge OY":
        global_stiffness_matrix = delete_raw_and_column(global_stiffness_matrix,
                                                        degree_of_freedom_number - deleted_number)
        deleted_number += 1
    if nodes_restriction[0] == "movable hinge OX":
        global_stiffness_matrix = delete_raw_and_column(global_stiffness_matrix,
                                                        degree_of_freedom_number - deleted_number)
        deleted_number += 1

    if nodes_restriction[0] == "hinge":
        global_stiffness_matrix = delete_raw_and_column(global_stiffness_matrix,
                                                        degree_of_freedom_number - deleted_number)
        deleted_number += 1
        global_stiffness_matrix = delete_raw_and_column(global_stiffness_matrix,
                                                        degree_of_freedom_number + 1 - deleted_number)
        deleted_number += 1

    if nodes_restriction[0] == "hard seal":
        global_stiffness_matrix = delete_raw_and_column(global_stiffness_matrix,
                                                        degree_of_freedom_number - deleted_number)
        deleted_number += 1
        global_stiffness_matrix = delete_raw_and_column(global_stiffness_matrix,
                                                        degree_of_freedom_number + 1 - deleted_number)
        deleted_number += 1
        global_stiffness_matrix = delete_raw_and_column(global_stiffness_matrix,
                                                        degree_of_freedom_number + 2 - deleted_number)
        deleted_number += 1
    degree_of_freedom_number += 3
displacement_vector = np.linalg.solve(global_stiffness_matrix, force_vector)

k = 0

displacement = np.array([])
for nodes_restriction in nodes_restrictions:
    if nodes_restriction[0] == "hard seal":
        displacement = np.append(displacement, [0, 0, 0])
    if nodes_restriction[0] == "hinge":
        displacement = np.append(displacement, [0, 0, displacement_vector[k]])
        k += 1
    if nodes_restriction[0] == "movable hinge OY":
        displacement = np.append(displacement, [0, displacement_vector[k], displacement_vector[k + 1]])
        k += 2
    if nodes_restriction[0] == "movable hinge OX":
        displacement = np.append(displacement, [displacement_vector[k], 0, displacement_vector[k + 1]])
        k += 2
    if nodes_restriction[0] == "movable hinge Cx":
        displacement = np.append(displacement,
                                 [displacement_vector[k], nodes_restriction[1] * displacement_vector[k],
                                  displacement_vector[k + 1]])
        k += 3
    if nodes_restriction[0] == "free":
        displacement = np.append(displacement,
                                 [displacement_vector[k], displacement_vector[k + 1], displacement_vector[k + 2]])
        k += 3

displacement = displacement.reshape((nodes_number, 3))

e = 0
local_displacement = np.array([])
for element in elements:
    [i_node, j_node] = elements[e]
    element_displacement = np.append(displacement[i_node - 1], displacement[j_node - 1])
    local_displacement = np.append(local_displacement, np.dot(T(element), element_displacement))
    e += 1
local_displacement = local_displacement.reshape(elements_number, 6)


def v(point_coordinate, element_nodes_displacement, lgth):
    N = np.array([
        1 - 3 * point_coordinate ** 2 / lgth ** 2 + 2 * point_coordinate ** 3 / lgth ** 3,
        point_coordinate - 2 * point_coordinate ** 2 / lgth + point_coordinate ** 3 / lgth ** 2,
        3 * point_coordinate ** 2 / lgth ** 2 - 2 * point_coordinate ** 3 / lgth ** 3,
        -point_coordinate ** 2 / lgth + point_coordinate ** 3 / lgth ** 2
    ])
    return np.dot(N.transpose(), element_nodes_displacement)


def u(point_coordinate, U_1_2, lgth):
    return (U_1_2[1] - U_1_2[0]) * point_coordinate / lgth + U_1_2[0]


def linear_function(variable, r_1, r_2):
    return (r_2[1] - r_1[1]) / (r_2[0] - r_1[0]) * variable + (r_1[1] * r_2[0] - r_2[1] * r_1[0]) / (r_2[0] - r_1[0])


graph_points_number = 21


def initial_element_position(element_number):
    [node_i, node_j] = elements[element_number - 1]
    [x_i, y_i] = nodes[node_i - 1]
    [x_j, y_j] = nodes[node_j - 1]
    if x_i == x_j:
        X = x_i + np.zeros(graph_points_number)
        Y = np.linspace(y_i, y_j, graph_points_number)
    else:
        X = np.linspace(x_i, x_j, graph_points_number)
        Y = linear_function(X, [x_i, y_i], [x_j, y_j])
    return [X, Y]


def new_element_position(element_number):
    [node_i, node_j] = elements[element_number - 1]
    [x_i, y_i] = nodes[node_i - 1]
    [x_j, y_j] = nodes[node_j - 1]
    [X_0, Y_0] = initial_element_position(element_number)
    Length = ((x_i - x_j) ** 2 + (y_i - y_j) ** 2) ** 0.5
    sin_alpha = (y_j - y_i) / Length
    cos_alpha = (x_j - x_i) / Length
    local_variable = np.linspace(0, Length, graph_points_number)
    U_disp = u(local_variable, [local_displacement[element_number - 1][0], local_displacement[element_number - 1][3]],
               Length)
    V_disp = v(local_variable, [local_displacement[element_number - 1][1],
                                local_displacement[element_number - 1][2],
                                local_displacement[element_number - 1][4],
                                local_displacement[element_number - 1][5]], Length)
    delta_X = U_disp * cos_alpha - V_disp * sin_alpha
    delta_Y = U_disp * sin_alpha + V_disp * cos_alpha
    X = X_0 + delta_X
    Y = Y_0 + delta_Y
    return [X, Y]


for e in range(0, elements_number):
    [initial_x_coordinate, initial_y_coordinate] = initial_element_position(e + 1)
    [deformed_x_coordinate, deformed_y_coordinate] = new_element_position(e + 1)
    if e == 0:
        plt.plot(initial_x_coordinate, initial_y_coordinate, color="black", label="Не деформированное состояние")
        plt.plot(deformed_x_coordinate, deformed_y_coordinate, color="green", label="Деформированное состояние")
    else:
        plt.plot(initial_x_coordinate, initial_y_coordinate, color="black")
        plt.plot(deformed_x_coordinate, deformed_y_coordinate, color="green")
plt.legend()
plt.title("Расчет балочной коснтрукции")

plt.show()
