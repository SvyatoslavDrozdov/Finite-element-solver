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


def create_force(node_line_correspondence, nodes, boundary_condition_matrix, Forces, node_forces):
    f = np.zeros(3 * len(nodes))

    f = f.reshape(len(nodes), 3)
    for node_num in range(0, len(f)):
        for n in range(0, len(Forces)):
            if node_num + 1 == Forces[n][0]:
                f[node_num][0] = Forces[n][1]
                f[node_num][1] = Forces[n][2]
                f[node_num][2] = Forces[n][3]
        f[node_num][0] += node_forces[node_num][1][0]
        f[node_num][1] += node_forces[node_num][1][1]
        f[node_num][2] += node_forces[node_num][1][2]
    point = 0
    for boundary in boundary_condition_matrix:
        point += 1

        if boundary[0] == "hard seal":
            for l in range(0, len(node_line_correspondence)):
                if node_line_correspondence[l][0] == point:
                    node_number = node_line_correspondence[l][1]
            add_f = f[node_number:]
            f = np.append(f[:node_number - 1], ["*", "*", "*"])

            f = np.append(f, add_f)

            f = f.reshape(int(len(f) / 3), 3)

        if boundary[0] == "hinge":
            for l in range(0, len(node_line_correspondence)):
                if node_line_correspondence[l][0] == point:
                    node_number = node_line_correspondence[l][1]
            add_f = f[node_number:]
            f = np.append(f[:node_number - 1], ["*", "*", f[node_number - 1][2]])

            f = np.append(f, add_f)

            f = f.reshape(int(len(f) / 3), 3)
        if boundary[0] == "movable hinge OX":
            for l in range(0, len(node_line_correspondence)):
                if node_line_correspondence[l][0] == point:
                    node_number = node_line_correspondence[l][1]
            add_f = f[node_number:]
            f = np.append(f[:node_number - 1],
                          [f[node_number - 1][0], "*", f[node_number - 1][2]])
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
    return f


def force_function(func):
    func = func.replace("s^", "s**")
    func = func.replace("sin(", "np.sin(")
    func = func.replace("cos(", "np.cos(")
    func = func.replace("tan(", "np.tan(")
    func = func.replace("log(", "np.log(")

    def y(s):
        f = eval(func)
        return f

    return y
