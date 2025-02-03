import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Функция считывания данных о кривой из файла
def read_one_dimension(file_name: str):
    data = []
    try:
        file = open(file_name, "r")
    except Exception:
        return None
    # читаем данные из файла до конца
    while True:
        line = file.readline()
        if not line:
            break
        try:
            # x, y - координаты точки, p - ее вес
            x, y, p = map(float, line.split())  # чтение очередной строки данных и ее преобразование
        except ValueError:
            return None
        data.append([x, y, p])
    return data

# Функция считывания данных о поверхности из файла
# Формат - сначала идут координаты узлов квадратной сетки
# Далее идет таблица значений z = f(x, y) в этих точках
# Далее идет таблица весов точек
def read_two_dimension(file_name: str):
    data = []
    try:
        file = open(file_name, "r")
    except Exception:
        return None

    line = file.readline()
    if not line:
        return None
    try:
        coords = list(map(float, line.split()))
    except ValueError:
        return None
    length = len(coords)
    # читаем таблицу значений z = f(x, y)
    for i in range(length):
        line = file.readline()
        if not line:
            break
        try:
            points = list(map(float, line.split()))
            if len(points) != length:
                return None
            pnt_arr = []
            for j in range(length):
                pnt_arr.append([coords[i], coords[j], points[j]])
            data.append(pnt_arr)
        except ValueError:
            return None
    # Читаем таблицу весов точек
    file.readline()
    for i in range(length):
        line = file.readline()
        if not line:
            return None
        try:
            points = list(map(float, line.split()))
            if len(points) != length:
                return None
            for j in range(length):
                data[i][j].append(points[j])
        except ValueError:
            return None
    # data[i][j] = [x, y, z, p]
    return data


# Функция, решающая систему уравнений методом гаусса
def gauss_method(matrix: list[list[float]], vector: list[float]):
    n = len(matrix)
    for i in range(n):
        max_el = abs(matrix[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > max_el:
                max_el = abs(matrix[k][i])
                max_row = k

        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        vector[i], vector[max_row] = vector[max_row], vector[i]

        for k in range(i + 1, n):
            c = -matrix[k][i] / matrix[i][i]
            for j in range(i, n):
                if i == j:
                    matrix[k][j] = 0
                else:
                    matrix[k][j] += c * matrix[i][j]
            vector[k] += c * vector[i]

    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = vector[i] / matrix[i][i]
        for k in range(i - 1, -1, -1):
            vector[k] -= matrix[k][i] * x[i]
    return x


# Функция построения аппроксимирующего многочлена с помощью метода среднеквадратичного отклонения
def linear_apprx_arr(data: list[list[float]], n: int):
    # степень полинома должна быть строго меньше числа узлов
    N = len(data) - 1
    '''if n > N:
        return None'''
    ''' 
    Из степени n получаем n+1 параметр ci, которые нужно определить
    Получаем систему уравнений вида:
    ...
    Ai0 * C0 + Ai1 * C1 ... + Ain * Cn = Bi
    ...
    Где:
    Akj = sum(init: i = 0; i <= N)(PHIk(xi) * PHIj(xi) * pi)
    Bi = sum(init: j = 0; j <= N)(F(xj) * PHIi(xj) * pj)
    pi - вес точки xi заданный в таблице
    PHIj(xi) = xi^j - за базис берем набор степенных функций от x^0 до x^n
    F(xi) = yi заданный в таблице
    Ищем мы сами коэффициенты Ci которые далее подставляем и получаем искомую функцию:
    F(x) = C0 + C1 * x + C2 * x^2 + ... + Ci * x^i + ... + Cn * x^n'''
    # Сначала получим матрицу Akj
    a_matr = []
    for k in range(n + 1):
        line = []
        for j in range(n + 1):
            akj = 0
            for i in range(N + 1):
                xi = data[i][0]
                pi = data[i][2]
                akj += pow(xi, k) * pow(xi, j) * pi
            line.append(akj)
        a_matr.append(line)
    # Получаем массив Bi
    b_arr = []
    for i in range(n + 1):
        bi = 0
        for j in range(N + 1):
            xj = data[j][0]
            yj = data[j][1]
            pj = data[j][2]
            bi += pow(xj, i) * pj * yj
        b_arr.append(bi)
    c_arr = gauss_method(a_matr, b_arr)
    return c_arr


# Функция подготавливает данные для отрисовки графика
# На вход передается массив коэффициентов ci и интервал рассчета
# Функция c0 + c1 * x + c2 * x^2 + ...
def prep_one_dimension(c_arr: list[float], interval: [float, float]) -> list[list[float]]:
    step = (interval[1] - interval[0]) / 200
    coefs = len(c_arr)
    x = interval[0]
    data = []
    while x <= interval[1]:
        y = 0.0
        for i in range(coefs):
            y += c_arr[i] * pow(x, i)
        data.append([x, y])
        x += step
    return data


def plot_one_dimension(labels, plots, xlabel, ylabel):
    if len(plots) != len(labels):
        return
    plt.figure(figsize=(20, 20))
    font = {'weight' : 'bold',
            'size' : 12}
    matplotlib.rc('font', **font)
    plt.plot(plots[0][0], plots[0][1], label=labels[0])
    plt.plot(plots[1][0], plots[1][1], label=labels[1])
    plt.plot(plots[2][0], plots[2][1], 'o', label=labels[2])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend()
    plt.show()


def plot_two_dimensions(labels, plots, xlabel, ylabel, z_label):
    if len(plots) != len(labels):
        return
    plt.figure(figsize=(20, 20))
    ax = plt.axes(projection='3d')
    font = {'weight': 'bold',
            'size': 12}
    matplotlib.rc('font', **font)

    x = plots[1][0]
    y = plots[1][1]
    z = plots[1][2]
    ax.scatter(x, y, z, label=labels[1], color='red')

    x = plots[0][0]
    y = plots[0][1]
    z = plots[0][2]

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax.plot_surface(x, y, z, label=labels[0])

    plt.legend()
    plt.show()


def one_dim_apprx(file_name: str, n: int):
    data = read_one_dimension(file_name)
    if not data:
        return
    # Получаем данные для построения кривой на исходных весах точек
    c_arr = linear_apprx_arr(data, n)
    appx_data = prep_one_dimension(c_arr, [data[0][0], data[-1][0]])
    appx_data_x = [elem[0] for elem in appx_data]
    appx_data_y = [elem[1] for elem in appx_data]
    # Получаем исходные точки, их тоже отобразим на графике
    points_data_x = [elem[0] for elem in data]
    points_data_y = [elem[1] for elem in data]
    # Теперь получаем данные для построения кривой на единичных весах точек
    for elem in data:
        elem[2] = 1
    c_arr = linear_apprx_arr(data, n)
    appx_data = prep_one_dimension(c_arr, [data[0][0], data[-1][0]])
    appx_data_x_1 = [elem[0] for elem in appx_data]
    appx_data_y_1 = [elem[1] for elem in appx_data]
    # Строим графики полученных кривых
    labels = ["График среднеквадратичной интерполяции (табличные веса)",
              "График среднеквадратичной интерполяции (единичные веса)","Точки таблицы"]
    plot_one_dimension(labels, [[appx_data_x, appx_data_y],
                                [appx_data_x_1, appx_data_y_1], [points_data_x, points_data_y]], "x", "y")


# По данной таблице и точке внутри нее получает значение функции z = f(x, y)
def two_dim_point(data: list[list[list[float]]], x0: float, y0: float, n: int):
    # Сначала интерполируем по y с закрепленным x
    # Получаем массив значений функции в f(x, y0)
    f_x_y0 = []
    for elem in data:
        line = [el[1::] for el in elem]
        c_arr = linear_apprx_arr(line, n)
        y = 0.0
        for i in range(len(c_arr)):
            y += c_arr[i] * pow(y0, i)
        f_x_y0.append([elem[0][0], y, n])
    c_arr = linear_apprx_arr(f_x_y0, n)
    y = 0.0
    for i in range(len(c_arr)):
        y += c_arr[i] * pow(x0, i)
    return y



def two_dim_apprx(file_name: str, n: int):
    data = read_two_dimension(file_name)
    if not data:
        return -1
    labels = ["График интерполяции", "Заданные точки"]
    grid_nodes = 40
    x_graph = np.outer(np.linspace(data[0][0][0], data[-1][0][0], grid_nodes), np.ones(grid_nodes))
    y_graph = x_graph.copy().T
    z_graph = []
    for i in range(len(x_graph)):
        line = []
        for j in range(len(y_graph)):
            line.append(two_dim_point(data, float(x_graph[i][j]), float(y_graph[i][j]), n))
        z_graph.append(line)
    z_arr = np.array(z_graph)
    x_points = []
    y_points = []
    z_points = []
    for elem in data:
        for el in elem:
            x_points.append(el[0])
            y_points.append(el[1])
            z_points.append(el[2])
    plot_two_dimensions(labels, [[x_graph, y_graph, z_arr], [x_points, y_points, z_points]],
                        'x', 'y', 'z')


def solve_equation(points: int):
    if points <= 0:
        return -1
    '''
    y + xy + y = 2x - Линейное ДУ
    y(0) = a = 1, y(1) = b = 0 - граничные условия, решение ищем на отрезке [0, 1]
    Решение ищем в виде y(x) = U0(x) + Esum(init: k = 1; k <= n)(Ck * Uk(x))
    U0(x) - функция, удовлетворяющая граничным условиям
    U0(x) = 1 - x
    Ui подбираем любые удобные для счета(m = 2 и m = 3):
    U1(x) = x^2 + x
    U2(x) = x^3 + x^2
    U3(x) = x^4 + x^3
    Для m = 2:
    y(x) = c1 * (x^2 + x) + c2 * (x^3 + x^2)
    y'(x) = c1 * (2x + 1) + c2 * (3x^2 + 2x)
    y''(x) = c1 * 2 + 6 * c2 * x + 2 * c2
    Для m = 3:
    y(x) = c1 * (x^2 + x) + c2 * (x^3 + x^2) + c3 * (x^4 + x^3)
    y'(x) = c1 * (2x + 1) + c2 * (3x^2 + 2x) + c3 * (4x^3 + 3x^2)
    y''(x) = c1 * 2 + c2 * (6x + 2) + c3 * (12x^2 + 6x)
    Подставляем в исходную систему и получаем:
    m = 2: c1 * (3x^2 + 2x + 2) + c2 * (4x^3 + 3x^2 + 6x + 2) = 2x
    m = 3: c1 * (3x^2 + 2x + 2) + c2 * (4x^3 + 3x^2 + 6x + 2) + c3 * (5x^4 + 4x^3 + 12x^2 + 6x) = 2x
    Берем точки с шагом 0.1 и составляем систему'''

    '''
    m = 2:
    a = 3x^2 + 2x + 2
    b = 4x^3 + 3x^2 + 6x + 2
    I = Esum(init: i = 0; i <= N) ((ai * c1 + bi * c2 - 2xi) ^ 2) = (c1 * sum(ai) + c2 * sum(bi) - 2xi) ^ 2
    Берем производные по c1 и c2:
    d/dc1 = 0 = c1 * sum(ai^2) + c2 * sum(ai * bi) - 2xi * ai
    d/dc2 = 0 = c1 * sum(ai * bi) + c2 * sum(bi ^ 2) - 2xi * bi
    Получили два линейных уравнения, считаем 4 суммы и свободные члены, кидаем в алгоритм гаусса
    '''
    #Решение для m = 2
    x = 0
    step = 1.0 / (points - 1)
    matr = [[0, 0], [0, 0]] #массив сумм
    arr = [0, 0]
    while x <= 1:
        ai = (3 * x ** 2 + 2 * x + 2)
        bi = (4 * x ** 3 + 3 * x ** 2 + 6 * x + 2)
        matr[0][0] += ai ** 2
        matr[0][1] += ai * bi
        matr[1][0] += ai * bi
        matr[1][1] += bi ** 2
        arr[0] -= 2 * x * ai
        arr[1] -= 2 * x * bi
        x += step
    c_arr = gauss_method(matr, arr)
    c1 = c_arr[0]
    c2 = c_arr[1]
    x = 0
    data_2_x = []
    data_2_y = []
    while x <= 1:
        # Вычисляем y по найденным ci(множитель из Ui) и U0: y = U0(x) + sum(Ui(x))
        data_2_y.append(c1 * (x ** 2 + x) + c2 * (x ** 3 + x ** 2) + 1 - x)
        data_2_x.append(x)
        x += step

    '''
        m = 3:
        a = 3x^2 + 2x + 2
        b = 4x^3 + 3x^2 + 6x + 2
        c = 5x^4 + 4x^3 + 12x^2 + 6x
        I = Esum(init: i = 0; i <= N) ((ai * c1 + bi * c2 + ci * c3 - 2xi) ^ 2) =
         (c1 * sum(ai) + c2 * sum(bi) + c3 * sum(ci) - 2xi) ^ 2
        Берем производные по c1, c2 и c3:
        d/dc1 = 0 = c1 * sum(ai^2) + c2 * sum(ai * bi) + с3 * sum(ai * ci) + 2xi * ai
        d/dc2 = 0 = c1 * sum(ai * bi) + c2 * sum(bi ^ 2) + c3 * sum(bi * ci) + 2xi * bi
        d/dc3 = 0 = c1 * sum(ai * ci) + c2 * sum(bi * ci) + c3 * sum(ci ^ 2) + 2xi * ci
        Получили три линейных уравнения, считаем 9 сумм и свободные члены, кидаем в алгоритм гаусса
        '''
    x = 0
    step = 1.0 / (points - 1)
    matr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # массив сумм
    arr = [0, 0, 0]
    while x <= 1:
        ai = (3 * x ** 2 + 2 * x + 2)
        bi = (4 * x ** 3 + 3 * x ** 2 + 6 * x + 2)
        ci = (5 * x ** 4 + 4 * x ** 3 + 12 * x ** 2 + 6 * x)
        matr[0][0] += ai ** 2
        matr[0][1] += ai * bi
        matr[0][2] += ai * ci
        matr[1][0] += ai * bi
        matr[1][1] += bi ** 2
        matr[1][2] += bi * ci
        matr[2][0] += ai * ci
        matr[2][1] += bi * ci
        matr[2][2] += ci ** 2
        arr[0] -= 2 * x * ai
        arr[1] -= 2 * x * bi
        arr[2] -= 2 * x * ci
        x += step
    c_arr = gauss_method(matr, arr)
    c1 = c_arr[0]
    c2 = c_arr[1]
    c3 = c_arr[2]
    x = 0
    data_3_x = []
    data_3_y = []
    while x <= 1:
        # Вычисляем y по найденным ci(множитель из Ui) и U0: y = U0(x) + sum(Ui(x))
        data_3_y.append(c1 * (x ** 2 + x) + c2 * (x ** 3 + x ** 2) + c3 * (x ** 4 + x ** 3) + 1 - x)
        data_3_x.append(x)
        x += step


    font = {'weight' : 'bold',
            'size' : 12}
    matplotlib.rc('font', **font)
    plt.plot(data_2_x, data_2_y, label="График функции при m = 2")
    plt.plot(data_3_x, data_3_y, label="График функции при m = 3")

    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()

