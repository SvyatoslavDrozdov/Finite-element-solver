import tkinter
import customtkinter as ctk
from PIL import ImageTk, Image
from sub_plot import plot_points_function

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1480x720")
app.resizable(width=False, height=False)


def button_function():
    img = ctk.CTkImage(Image.open("foo.png"), size=(600, 600))
    label = ctk.CTkLabel(master=frame, image=img, text="")
    label.place(relx=0.7, rely=0.5, anchor=ctk.CENTER)


frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

empty_img = ctk.CTkImage(Image.open("empty_foo.png"), size=(600, 600))
empty_label = ctk.CTkLabel(master=frame, image=empty_img, text="")
empty_label.place(relx=0.7, rely=0.45, anchor=ctk.CENTER)

# Добавлю в следующих версиях программы
# button = ctk.CTkButton(master=frame, text="Обновить график", command=button_function)
# button.place(relx=0.1, rely=0.8, anchor=ctk.CENTER)
# button.place(x=3 * 80 - 5, y=60 + 10 * 50)
# My settings: --------------------------------------------------------------------------------------------------------
X1 = 30
X2 = 250
Y1 = 10
Y2 = 60
dY = 50
dX = 25
Y3 = Y2 + 6 * dY
StandardWidth = 80
StandardWidth2 = 120
X3 = X2 + 2 * StandardWidth + 2 * dX
X4 = X3 + 2 * StandardWidth + 2 * dX
X5 = X4 + 2 * StandardWidth + 2 * dX

# My functions: --------------------------------------------------------------------------------------------------------
X = []
Y = []
point_num = []
BC = []
BC_parameter = []
Forces = []


def test(condition, condition_parameter):
    flag = 0
    if condition == "":
        flag = 1
    if condition == "шарнир" and condition_parameter == "":
        flag = 1
    if condition == "шарнир" and condition_parameter == "OX":
        flag = 1
    if condition == "шарнир" and condition_parameter == "OY":
        flag = 1
    if condition == "шарнир" and type(condition_parameter) == float:
        flag = 1
    if condition == "заделка":
        flag = 1
    return flag


def add_point_function():
    global X
    global Y
    global point_num
    global BC
    global BC_parameter
    global line_points
    x = float(entry_x_of_point.get())
    y = float(entry_y_of_point.get())
    boundary_condition = entry_boundary_condition.get()
    try:
        boundary_condition_parameter = float(entry_boundary_condition_parameter.get())
    except:
        boundary_condition_parameter = entry_boundary_condition_parameter.get()
    if test(boundary_condition, boundary_condition_parameter) == 1:
        X.append(x)
        Y.append(y)
        BC.append(boundary_condition)
        BC_parameter.append(boundary_condition_parameter)
        if line_points:
            plot_points_function(X, Y, BC, BC_parameter, line_points, element_number, 0, Forces, E_vector, A_vector,
                                 I_vector, normal_force_functions, tangent_force_functions)
        else:
            plot_points_function(X, Y, BC, BC_parameter, [], [], 0, Forces, [], [], [], [], [])
        button_function()


line_points = []
element_number = []
E_vector = []
A_vector = []
I_vector = []
normal_force_functions = []
tangent_force_functions = []


def add_line_function():
    global line_points
    global element_number
    global E_vector
    global A_vector
    global I_vector
    f_n = entry_f_n.get()
    f_t = entry_f_t.get()
    normal_force_functions.append(f_n)
    tangent_force_functions.append(f_t)

    elem_number = int(entry_elem_number.get())
    element_number.append(elem_number)

    E = float(entry_E.get())
    A = float(entry_A.get())
    I = float(entry_I.get())
    for i in range(0, elem_number):
        E_vector.append(E)
        A_vector.append(A)
        I_vector.append(I)

    num_of_point_1 = int(entry_num_of_point_1.get())
    num_of_point_2 = int(entry_num_of_point_2.get())
    line_points.append([num_of_point_1, num_of_point_2])

    plot_points_function(X, Y, BC, BC_parameter, line_points, element_number, 0, Forces, E_vector, A_vector, I_vector,
                         normal_force_functions, tangent_force_functions)
    button_function()


def solve_function():
    plot_points_function(X, Y, BC, BC_parameter, line_points, element_number, 1, Forces, E_vector, A_vector, I_vector,
                         normal_force_functions, tangent_force_functions)
    button_function()


def add_force_function():
    global Forces
    F_x = float(entry_F_x.get())
    F_y = float(entry_F_y.get())
    M = float(entry_M.get())
    node_force_number = int(entry_num_of_nodes.get())
    for i in range(0, len(Forces)):
        if Forces[i][0] == node_force_number:
            Forces = Forces[:i] + Forces[i + 1:]

    Forces.append([node_force_number, F_x, F_y, M])


# My windows: --------------------------------------------------------------------------------------------------------

# Задание точек: -----------------------------------------------------------------------------------------------------
ctk.CTkLabel(master=frame, text="Задание точек", text_color='white', fg_color="#7F55F2", width=6 * StandardWidth + dX,
             corner_radius=10).place(x=X1, y=Y1)

ctk.CTkLabel(master=frame, text="[ x, y ] =", fg_color="#0066CC", width=2 * StandardWidth - dX, corner_radius=10).place(
    x=X1,
    y=Y2)
entry_x_of_point = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_x_of_point.place(x=X1 + 2 * StandardWidth - dX, y=Y2)
entry_y_of_point = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_y_of_point.place(x=X1 + 3 * StandardWidth - dX, y=Y2)

ctk.CTkLabel(master=frame, text="Закрепление:", fg_color="#0066CC", width=2 * StandardWidth - dX,
             corner_radius=10).place(
    x=X1, y=Y2 + dY)
entry_boundary_condition = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_boundary_condition.place(x=X1 + 2 * StandardWidth - dX, y=Y2 + dY)
entry_boundary_condition_parameter = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_boundary_condition_parameter.place(x=X1 + 3 * StandardWidth - dX, y=Y2 + dY)

add_point_button = ctk.CTkButton(master=frame, text="Добавить", command=add_point_function, fg_color="#418433",
                                 hover_color="#1F4618")
add_point_button.place(x=5 * StandardWidth - 5, y=Y2 + dY)

# Задание линий: -----------------------------------------------------------------------------------------------------
ctk.CTkLabel(master=frame, text="Задание линий", text_color='white', fg_color="#7F55F2", width=6 * StandardWidth + dX,
             corner_radius=10).place(x=X1, y=Y1 + 3 * dY)

ctk.CTkLabel(master=frame, text="[ №1 ,  №2 ] =", fg_color="#0066CC", width=StandardWidth + dX, corner_radius=10).place(
    x=X1, y=Y2 + 3 * dY)
entry_num_of_point_1 = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_num_of_point_1.place(x=X1 + StandardWidth + dX, y=Y2 + 3 * dY)
entry_num_of_point_2 = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_num_of_point_2.place(x=X1 + 2 * StandardWidth + dX, y=Y2 + 3 * dY)

ctk.CTkLabel(master=frame, text="количество элементов:", fg_color="#0066CC", width=StandardWidth + dX,
             corner_radius=10).place(
    x=X1 + 3 * StandardWidth + 2 * dX, y=Y2 + 3 * dY)
entry_elem_number = ctk.CTkEntry(master=frame, width=StandardWidth - dX)
entry_elem_number.place(x=X1 + 5 * StandardWidth + 2 * dX, y=Y2 + 3 * dY)
entry_elem_number.insert(0, 1)

ctk.CTkLabel(master=frame, text="f_n(s) =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1, y=Y2 + 4 * dY)
entry_f_n = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_f_n.place(x=X1 + StandardWidth, y=Y2 + 4 * dY)
entry_f_n.insert(0, 0)

ctk.CTkLabel(master=frame, text="f_t(s) =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1 + 2 * StandardWidth + int(dX / 2), y=Y2 + 4 * dY)
entry_f_t = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_f_t.place(x=X1 + 3 * StandardWidth + int(dX / 2), y=Y2 + 4 * dY)
entry_f_t.insert(0, 0)

ctk.CTkLabel(master=frame, text="E =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1, y=Y2 + 5 * dY)
entry_E = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_E.place(x=X1 + StandardWidth, y=Y2 + 5 * dY)
entry_E.insert(0, "2.1e11")

ctk.CTkLabel(master=frame, text="A =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1 + 2 * StandardWidth + int(dX / 2), y=Y2 + 5 * dY)
entry_A = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_A.place(x=X1 + 3 * StandardWidth + int(dX / 2), y=Y2 + 5 * dY)
entry_A.insert(0, "3.142e-4")

ctk.CTkLabel(master=frame, text="I =", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1 + 4 * StandardWidth + dX, y=Y2 + 5 * dY)
entry_I = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_I.place(x=X1 + 5 * StandardWidth + dX, y=Y2 + 5 * dY)
entry_I.insert(0, "7.8510e-9")

add_line_button = ctk.CTkButton(master=frame, text="Добавить", command=add_line_function, fg_color="#418433",
                                hover_color="#1F4618")
add_line_button.place(x=5 * StandardWidth - 5, y=Y2 + 4 * dY)

# Задание узловых сил: -------------------------------------------------------------------------------------------------
ctk.CTkLabel(master=frame, text="Задание узловых сил", text_color='white', fg_color="#7F55F2",
             width=6 * StandardWidth + dX,
             corner_radius=10).place(x=X1, y=Y1 + 7 * dY)

ctk.CTkLabel(master=frame, text="узел №", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1, y=Y2 + 7 * dY)
entry_num_of_nodes = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_num_of_nodes.place(x=X1 + StandardWidth, y=Y2 + 7 * dY)

ctk.CTkLabel(master=frame, text="F_x", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1, y=Y2 + 8 * dY)
entry_F_x = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_F_x.place(x=X1 + StandardWidth, y=Y2 + 8 * dY)
entry_F_x.insert(0, 0)

ctk.CTkLabel(master=frame, text="F_y", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1 + 2 * StandardWidth + int(dX / 2), y=Y2 + 8 * dY)
entry_F_y = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_F_y.place(x=X1 + 3 * StandardWidth + int(dX / 2), y=Y2 + 8 * dY)
entry_F_y.insert(0, 0)

ctk.CTkLabel(master=frame, text="M", fg_color="#0066CC", width=StandardWidth, corner_radius=10).place(
    x=X1 + 4 * StandardWidth + dX, y=Y2 + 8 * dY)
entry_M = ctk.CTkEntry(master=frame, width=StandardWidth)
entry_M.place(x=X1 + 5 * StandardWidth + dX, y=Y2 + 8 * dY)
entry_M.insert(0, 0)

add_force_button = ctk.CTkButton(master=frame, text="Добавить", command=add_force_function, fg_color="#418433",
                                 hover_color="#1F4618")
add_force_button.place(x=5 * StandardWidth - 5, y=Y2 + 7 * dY)

solve_button = ctk.CTkButton(master=frame, text="Решить", width=4 * StandardWidth + dX, command=solve_function,
                             fg_color="#2310e6",
                             hover_color="#281d96")
solve_button.place(x=X1 + StandardWidth, y=Y2 + 10 * dY)

app.mainloop()
