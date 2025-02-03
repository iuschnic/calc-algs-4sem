import numpy as np


def f_1(x: float, y: float, z: float):
    return x**2 + y**2 + z**2 - 1

def f_2(x: float, y: float, z: float):
    return 2 * x**2 + y**2 - 4*z

def f_3(x: float, y: float, z: float):
    return 3 * x**2 - 4*y + z**2

def j_inverse(x: float, y: float, z: float):
    j = [[2*x, 2*y, 2*z], [4*x, 2*y, -4], [6*x, -4, 2*z]]
    j_inv = np.linalg.inv(np.array(j))
    return j_inv.tolist()

def new_params(x: float, y: float, z: float, j_inv: list[list[float]]):
    f1 = f_1(x, y, z)
    f2 = f_2(x, y, z)
    f3 = f_3(x, y, z)
    newx = x - j_inv[0][0] * f1 - j_inv[0][1] * f2 - j_inv[0][2] * f3
    newy = y - j_inv[1][0] * f1 - j_inv[1][1] * f2 - j_inv[1][2] * f3
    newz = z - j_inv[2][0] * f1 - j_inv[2][1] * f2 - j_inv[2][2] * f3
    return newx, newy, newz


def solve_system(eps: float):
    '''
    Дана система из трех нелинейных уравнений с неизвестными x, y, z
    f1 = x^2 + y^2 + z^2 - 1 = 0
    f2 = 2x^2 + y^2 - 4z = 0
    f3 = 3x^2 - 4y + z^2 = 0
    Требуется найти решение системы методом Ньютона
    Существенную роль в методе играем матрица - Якобиан, состоящая из частных производных fi по xi
    Где fi - одно из уравнений, xi - одна из переменных
    Вспомним формулу метода касательных, чьим обобщением является метод Ньютона
    xk+1 = xk - f(xk)/f(xk)'
    Формула применяется итерационно до получения желаемой точности
    Обобщением этой формулы на систему уравнений является другая формула:
    Xk+1 = Xk - J^(-1)(Xk) * f(Xk)
    X - n-мерный вектор-столбец с компонентами x1...xi...xn
    f - n-мерный вектор-функция (f1, f2, ...)
    k - номер итерации (0, 1, ...)
    J^(-1) - метрица, обратная матрице Якобиана на k-й итерации
    J - матрица Якобиана
    На каждом шаге придется находить матрицу, обратную J при текущих значениях x, y, z
    Для начала найдем формулы частных производных
    Df1/dx = 2x
    Df1/dy = 2y
    Df1/dz = 2z
    Df2/dx = 4x
    Df2/dy = 2y
    Df2/dz = -4
    Df3/dx = 6x
    Df3/dy = -4
    Df3/dz = 2z
    J = [ [2x, 2y, 2z], [4x, 2y, -4], [6x, -4, 2z] ]
    Обратную матрицу будем находить используя numpy
    Сами итерационные формулы:
    xk+1 = xk - A11k * f1(xk, yk, zk) - A12k * f2(xk, yk, zk) - A13k * f3(xk, yk, zk)
    yk+1 = yk - A21k * f1(xk, yk, zk) - A22k * f2(xk, yk, zk) - A23k * f3(xk, yk, zk)
    zk+1 = zk - A31k * f1(xk, yk, zk) - A32k * f2(xk, yk, zk) - A33k * f3(xk, yk, zk)
    Aijk - значение в i-й строке j-го столбца J^(-1) на k-й итерации
    Также придется найти некие начальные значения x0, y0, z0
    eps - точность вычисления
    '''
    max_iter = 1000
    x = 1.0
    y = 1.0
    z = 1.0
    j_inv = j_inverse(x, y, z)
    newx, newy, newz = new_params(x, y, z, j_inv)
    iterations = 1
    while ((abs((newx - x) / x) > eps or abs((newy - y) / y) > eps or abs((newz - z) / z) > eps)
           and iterations < max_iter):
        x, y, z = newx, newy, newz
        j_inv = j_inverse(x, y, z)
        newx, newy, newz = new_params(x, y, z, j_inv)
        iterations += 1
    print("Задание 1:")
    print(f"x = {x}, y = {y}, z = {z}")
    print(f"f1 = {f_1(x, y, z)}")
    print(f"f2 = {f_2(x, y, z)}")
    print(f"f3 = {f_3(x, y, z)}")
    print(f"Произведено {iterations} итераций")
    print()
    return x, y, z
