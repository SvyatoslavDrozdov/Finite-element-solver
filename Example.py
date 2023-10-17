import matplotlib.pyplot as plt
import numpy as np

E = 2.1e11
I = 7.8510e-9

if False:
    l = 2
    k = np.pi
    X = np.linspace(0, l, 1000)
    C = 1 / k ** 3 * (k * l - 2 * np.sin(k * l) + k * l * np.cos(k * l))

    D = 1 / (2 * k ** 4) * (k * l * (k * l + 2 * np.sin(k * l)) + 6 * np.cos(k * l)) - C * l

    x = X
    Y = C * X + D - 1 / (2 * k ** 4) * (k * x * (k * x + 2 * np.sin(k * x)) + 6 * np.cos(k * x))
    Y = 500 * Y / (E * I)

    X = np.linspace(0, l, 1000)
    l = 2
    k = 3.14
    C = 1 / k ** 3 * (k * l - 2 * np.sin(k * l) + k * l * np.cos(k * l))

    D = -C * l + 1 / (2 * k ** 4) * (k * l * (k * l + 2 * np.sin(k * l)) + 6 * np.cos(k * l))

    Y_2 = C * X + D - (1 / (2 * k ** 4)) * (k * X * (k * X + 2 * np.sin(k * X)) + 6 * np.cos(k * X))
    Y_2 = 500 * Y_2 / (E * I)

    plt.plot(X, Y_2, label="second")
    plt.plot(X, Y, label="first")
    plt.legend()
    plt.show()
if False:
    l = 2
    q = 2000
    X = np.linspace(0, l, 1000)
    D = q / 6 * l ** 4 - q / 24 * l ** 4
    Y = q / 24 * X ** 4 - q / 6 * l ** 3 * X + D
    Y = Y / (E * I)
    plt.plot(l - X, Y)
    plt.show()

if False:
    # linear function
    l = 2
    k = 500
    X = np.linspace(0, l, 1000)

    C = -k * l ** 4 / 12
    D = -k * l ** 5 / 60 - C * l
    Y = k * X ** 5 / 60 + C * X + D
    Y = Y / (E * I)
    plt.plot(l - X, Y)
    plt.show()

if False:
    l = 2
    X = np.linspace(0, l, 1000)
    F_0 = 100
    M_0 = 100
    C = -F_0 * l ** 2 / 2 - M_0 * l
    D = -F_0 * l ** 3 / 6 - M_0 * l ** 2 / 2 - C * l
    Y = F_0 * X ** 3 / 6 + M_0 * X ** 2 / 2 + C * X + D
    Y = Y / (E * I)
    plt.plot(l - X, Y)
    plt.show()

if True:
    l = 2
    # q = 2000
    q = 0
    F_0 = 100
    M_0 = 0
    # M_0 = 100

    X = np.linspace(0, l, 1000)
    C = - M_0 * l - F_0 * l ** 2 / 2 - q * l ** 3 / 6
    D = - M_0 * l ** 2 / 2 - F_0 * l ** 3 / 6 - q * l ** 4 / 24 - C * l
    Y = M_0 * X ** 2 / 2 + F_0 * X ** 3 / 6 + q * X ** 4 / 24 + C * X + D

    # Y_2 = F_0 * X ** 3 / 6 - F_0 * l ** 2 / 2 * X + F_0 * l ** 3 / 3
    Y = Y / (E * I)
    # Y_2 = Y_2 / (E * I)
    plt.plot(l - X, Y)
    # plt.plot(l - X, Y_2)

# l = 2
# k = 500
# X = np.linspace(0, l, 1000)
# C = -k * l ** 4 / 12
# D = -k * l ** 5 / 60 - C * l
# Y = k * X ** 5 / 60 + C * X + D
# Y = Y / (E * I)
# plt.plot(l - X, Y)
# plt.show()

# l_1 = 1
# l_2 = 1
# F_1 = 100
# F_2 = 0
#
# C_2 = -F_1 * l_1 * (l_1 + l_2) - F_2 * ((l_1 + l_2) ** 2 / 2 - l_1 * (l_1 + l_2))
# D_2 = - F_1 * l_1 * (l_1 + l_2) ** 2 / 2 - F_2 * ((l_1 + l_2) ** 3 / 6 - l_1 * (l_1 + l_2) ** 2 / 2) - C_2 * (l_1 + l_2)
# C_1 = 1 / 2 * F_1 * l_1 ** 2 - 1 / 2 * F_2 * l_1 ** 2 + C_2
# D_1 = 1 / 3 * F_1 * l_1 ** 3 - 1 / 3 * F_2 * l_1 ** 3 + C_2 * l_1 - C_1 * l_1 + D_2
#
# X = np.linspace(0, l_1 + l_2, 100)
# Y = []
# for x in X:
#     if x <= l_1:
#         y = F_1 * x ** 3 / 6 + C_1 * x + D_1
#     else:
#         y = F_1 * l_1 * x ** 2 / 2 + F_2 * (x ** 3 / 6 - l_1 * x ** 2 / 2) + C_2 * x + D_2
#     y = y / (E * I)
#     Y.append(y)
# plt.plot(l_1 + l_2 - X, Y, label="F_1,F_2 plot")
# plt.title(2)

plt.show()
