import numpy as np

wrong_solution = False
if wrong_solution:
    nodes = np.array([
        [0, 0],  # first node
        [0, 0.5],  # second node
        [-1, 1],
        [1, 1]
    ])

    elements = np.array([
        [1, 2],
        [2, 4],
        [2, 3]

        # first element

    ])

    nodes_restrictions = [
        "hard seal",
        "free",
        "free",
        "free"
    ]
    force_vector = np.array([0, 0, 0, 0, 0, 0, 0, 100, 0])

correct_solution = False
if correct_solution:
    nodes = np.array([
        [0, 0],  # first node
        [0, 0.5],  # second node
        [-1, 1],
        [1, 1]
    ])

    elements = np.array([
        [1, 2],  # first element
        [2, 3],
        [3, 4]

    ])

    nodes_restrictions = [
        "hard seal",
        "free",
        "free",
        "free"
    ]
    force_vector = np.array([0, 0, 0, 0, 100, 0, 0, 0, 0])

third_setting = True
if third_setting:
    nodes = np.array([
        [0, 0],  # first node
        [1, 1],  # second node
        [2, 0],  # third node
        [1, 2],  # fourth node
        [2, 2],  # fifth node
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
        ["movable hinge Cx", 2],
        ["movable hinge Cx", -2]
    ]
    F_x_2 = 0
    F_y_2 = -500_000_0
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
