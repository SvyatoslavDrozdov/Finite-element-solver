import numpy as np


def nodes_function(X, Y, line_points, element_number):
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


def create_force_and_boundary(node_line_correspondence, nodes, line_points, boundary_condition_matrix, Forces):
    f = np.zeros(3 * len(nodes))
    # all_boundary = []
    # for n in range(0, len(nodes)):
    #     all_boundary.append(["free", ""])
    # for nl in range(0, len(node_line_correspondence)):
    #     all_boundary[node_line_correspondence[nl][1] - 1] = boundary_condition_matrix[nl]
    # print(boundary)

    f = f.reshape(len(nodes), 3)
    # print(f)
    for node_num in range(0, len(f)):
        for n in range(0, len(Forces)):
            if node_num + 1 == Forces[n][0]:
                f[node_num][0] = Forces[n][1]
                f[node_num][1] = Forces[n][2]
                f[node_num][2] = Forces[n][3]

    # print(f)
    # f.reshape(len(nodes), 3)
    # print(f)

    point = 0
    for boundary in boundary_condition_matrix:
        point += 1
        # if point >= 2:
        # print(f)

        if boundary[0] == "hard seal":
            for l in range(0, len(node_line_correspondence)):
                if node_line_correspondence[l][0] == point:
                    node_number = node_line_correspondence[l][1]
            # print(f"point = {point}")
            # print(f"deleted = {deleted}")
            add_f = f[node_number :]
            f = np.append(f[:node_number - 1], ["*", "*", "*"])

            f = np.append(f, add_f)

            f = f.reshape(int(len(f) / 3), 3)

        if boundary[0] == "hinge":
            for l in range(0, len(node_line_correspondence)):
                if node_line_correspondence[l][0] == point:
                    node_number = node_line_correspondence[l][1]
            add_f = f[node_number:]
            f = np.append(f[:node_number - 1], ["*", "*", f[node_number - 1 - deleted][2]])

            f = np.append(f, add_f)

            f = f.reshape(int(len(f) / 3), 3)
        # print(boundary[0])
        if boundary[0] == "movable hinge OX":
            for l in range(0, len(node_line_correspondence)):
                if node_line_correspondence[l][0] == point:
                    node_number = node_line_correspondence[l][1]
            add_f = f[node_number:]
            f = np.append(f[:node_number - 1],
                          [f[node_number - 1 ][0], "*", f[node_number - 1][2]])
            f = np.append(f, add_f)
            f = f.reshape(int(len(f) / 3), 3)
        if boundary[0] == "movable hinge OY":
            for l in range(0, len(node_line_correspondence)):
                if node_line_correspondence[l][0] == point:
                    node_number = node_line_correspondence[l][1]
            add_f = f[node_number:]
            f = np.append(f[:node_number - 1],
                          ["*", f[node_number - 1][1], f[node_number - 1][2]])
            f = np.append(f, add_f)
            f = f.reshape(int(len(f) / 3), 3)
    f = f.reshape(3 * len(f))
    f = list(f)

    for i in range(0, len(f)):
        try:
            f.remove("*")
        except:
            pass
    for i in range(0, len(f)):
        f[i] = float(f[i])
    # print(f)
    # print(f)
    # print(f.reshape(3 * len(f)))
    return f
