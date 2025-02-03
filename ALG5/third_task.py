from math import sqrt
import numpy as np
from matplotlib import pyplot as plt

# Параметры задачи
xa = 0.0
xb = 1.0
ya = 1.0
yb = 3.0

N = 20
h = 1 / N
tol = 1e-6
max_iter = 1000


# Первое слагаемое для аппроксимации второй производной разностным аналогом
def term(x, y):
    return (y[x - 1] - 2 * y[x] + y[x + 1]) / (h ** 2)


# Получение свободных коэффициентов СЛАУ
def F(y):
    f = np.zeros(N + 1)

    f[0] = y[0] - ya
    f[N] = y[N] - yb
    for i in range(1, N):
        # (Yn-1 - 2Yn + Yn+1) / h^2 - Yn^3 = Xn^2
        f[i] = term(i, y) - y[i] ** 3 - (i * h) ** 2  # Аппроксимируем вторую производную разностным аналогом
    return f


# Функция для вычисления Якобиана
def J(y):
    jac = np.zeros((N + 1, N + 1))

    jac[0, 0] = 1.0
    jac[N][N] = 1.0

    for i in range(1, N):
        jac[i][i - 1] = 1.0 / (h ** 2)
        jac[i][i] = -2.0 / (h ** 2) - 3.0 * y[i] ** 2
        jac[i][i + 1] = 1.0 / (h ** 2)

    return jac


def gauss(A, B):
    # Прямой ход метода Гаусса
    n = len(B)

    for i in range(n):
        # Поиск максимального элемента в столбце i
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Ставим строку с макс. числом в текущую i-ю строку
        for k in range(i, n):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp
        # меняем местами строки в системе значений B
        tmp = B[maxRow]
        B[maxRow] = B[i]
        B[i] = tmp

        # Приведение к верхнетреугольному виду
        for k in range(i + 1, n):
            c = -A[k][i] / A[i][i]
            for j in range(i, n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]
            B[k] += c * B[i]

    # Обратный ход метода Гаусса
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = B[i]  # == B[maxRow]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]

    return x


def newton(y_init):
    jac = J(y_init)  # Вычисление якобиана СЛАУ

    func_y = F(y_init)  # Получение списка свободных членов

    dy = gauss(jac, -func_y)  # solve for increment from JdX = Y

    return y_init + dy


# Функция для решения системы нелинейных уравнений методом Ньютона
def iter_newton(y_init):
    iter = 0

    y_old = y_init
    y_new = newton(y_old)

    diff = np.linalg.norm(y_old - y_new)

    while diff > tol and iter < max_iter:
        iter += 1
        y_new = newton(y_old)
        diff = np.linalg.norm(y_old - y_new)
        y_old = y_new
    convergent_val = y_new
    return convergent_val


def solve():
    # разностная сетка
    x = np.linspace(xa, xb, N + 1)
    y = np.linspace(ya, yb, N + 1)  # это наше начальное приближение

    # решаем систему нелинейных уравнений методом ньютона
    y = iter_newton(y)

    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
