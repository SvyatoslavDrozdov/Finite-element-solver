import matplotlib.pyplot as plt
from first_generalization import *

plt.figure(figsize=(8, 8))

for e in range(0, elements_number):
    [initial_x_coordinate, initial_y_coordinate] = initial_element_position(e + 1)
    [deformed_x_coordinate, deformed_y_coordinate] = new_element_position(e + 1)
    if e == 0:
        plt.plot(initial_x_coordinate, initial_y_coordinate, 'k--', label="Не деформированное состояние")
        plt.plot(deformed_x_coordinate, deformed_y_coordinate, color="blue", label="Деформированное состояние")
    else:
        plt.plot(initial_x_coordinate, initial_y_coordinate, 'k--')
        plt.plot(deformed_x_coordinate, deformed_y_coordinate, color="blue")
plt.legend()
# plt.title("Расчет балочной конструкции")

Length_max = 0
for e in range(0, elements_number):
    [first_node, second_node] = elements[e]
    [x_i, y_i] = nodes[first_node - 1]
    [x_j, y_j] = nodes[second_node - 1]
    Length = ((x_i - x_j) ** 2 + (y_i - y_j) ** 2) ** 0.5
    if Length_max < Length:
        Length_max = Length

for node in range(0, nodes_number):
    [x_i, y_i] = nodes[node]
    plt.plot(x_i, y_i, marker='o', color="black")
    plt.text(x_i + Length_max / 25, y_i + Length_max / 25, f'узел {node + 1}')
node_num = 1
for nodes_restriction in nodes_restrictions:
    d = 0.1 * Length_max
    if nodes_restriction[0] == "hard seal":
        [x_i, y_i] = nodes[node_num - 1]
        plt.plot(x_i, y_i, 'Dk')
        plt.errorbar(x_i, y_i, xerr=0.1, yerr=0.1, color="black")
    if nodes_restriction[0] == "movable hinge OY":
        [x_i, y_i] = nodes[node_num - 1]
        plt.plot(x_i, y_i, 'or')
        base_x = [x_i, x_i]
        base_y = [y_i - d, y_i + d]
        plt.plot(base_x, base_y, color="red")
    if nodes_restriction[0] == "movable hinge OX":
        [x_i, y_i] = nodes[node_num - 1]
        plt.plot(x_i, y_i, 'or')
        base_x = [x_i - d, x_i + d]
        base_y = [y_i, y_i]
        plt.plot(base_x, base_y, color="red")
    if nodes_restriction[0] == "movable hinge Cx":
        local_d = 2 * d
        k = nodes_restriction[1]
        [x_i, y_i] = nodes[node_num - 1]
        plt.plot(x_i, y_i, 'or')
        x_1 = x_i - (local_d ** 2 / (2 * (k ** 2 + 1))) ** 0.5
        x_2 = x_i + (local_d ** 2 / (2 * (k ** 2 + 1))) ** 0.5
        y_1 = k * (x_1 - x_i) + y_i
        y_2 = k * (x_2 - x_i) + y_i
        base_x = [x_1, x_2]
        base_y = [y_1, y_2]
        plt.plot(base_x, base_y, color="red")

    node_num += 1
plt.axis('equal')
plt.grid()
plt.savefig('foo.png')

plt.show()

# plt.figure(figsize=(6, 6))
# plt.axis('equal')

# plt.grid()
# plt.savefig('empty_foo.png')
# plt.show()
