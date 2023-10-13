import numpy as np


nodes = np.array([
    [0, 0],  # first node
    [1, 1],  # second node
    [2, 0],  # third node
    [1, 2],  # fourth node
    [2, 2],  # fifth node
])
R = 0.01
E = 2.1E11
A = np.pi * R ** 2
I = np.pi * R ** 4 / 4
element_properties = np.array([
    [E, A, I],
    [E, A, I],
    [E, A, I],
    [E, A, I]
])

elements = np.array([
    [1, 2],  # first element
    [2, 3],  # second element
    [2, 4],  # third element
    [4, 5],  # fourth element
])

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
