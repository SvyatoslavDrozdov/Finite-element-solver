def write_data(element, local_displacement):
    data = open(rf"C:\Users\xxl20\PycharmProjects\BeamSolver\Finite-element-solver\displacement.txt", mode="a")
    data.write(
        f"element №{element + 1}:{local_displacement[element]}\n")
    data.close()


def delete_data():
    data = open(rf"C:\Users\xxl20\PycharmProjects\BeamSolver\Finite-element-solver\displacement.txt", mode="w")
    data.close()
