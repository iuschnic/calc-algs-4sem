import math as m
def read_data(file_name):
    arr = []
    try:
        file = open(file_name, "r")
    except Exception:
        return None
    file.readline()     # пропуск шапки файла
    while True:
        line = file.readline()
        if not line:
            break
        try:
            x, y = map(float, line.split())     # чтение очередной строки данных и ее преобразование
        except ValueError:
            return -2
        elem = [x, y]
        arr.append(elem)
    return arr

# Функция поиска коэффициентов Ai, Bi, Ci, Fi канонической записи системы
def find_canonic_coefs(data):
    table = [[0, 0, 0, 0], [0, 0, 0, 0]]     #индексация начинается с 2, заполним два буферных элемента для простоты
    # Ai, Bi, Ci, Fi  i = [2....N] делаем буфер чтобы было прорще отслеживать индексацию
    for i in range(2, len(data)):
        hi_1 = data[i - 1][0] - data[i - 2][0]
        hi = data[i][0] - data[i - 1][0]
        yi_2 = data[i - 2][1]
        yi_1 = data[i - 1][1]
        yi = data[i][1]

        Ai = hi_1
        Di = hi
        Bi = -2 * (hi_1 + hi)
        Fi = -3 * ((yi - yi_1) / hi - (yi_1 - yi_2) / hi_1)

        table.append([Ai, Bi, Di, Fi])
    return table

# Функция поиска прогоночных коэффициентов по коэффициентам канонической записи
def find_run_coefs(canonic_table, fir_ksi, fir_nu):
    run_coefs = [[0, 0], [0, 0], [fir_ksi, fir_nu]]     # первый два индекса использоваться не будут, тоже буферные
    # начальные значения, в лекции имеют индекс 2
    ksi = fir_ksi
    nu = fir_nu
    for i in range(2, len(canonic_table)):
        Ai = canonic_table[i][0]
        Bi = canonic_table[i][1]
        Di = canonic_table[i][2]
        Fi = canonic_table[i][3]
        #print(Ai, Bi, Di, Fi)
        temp_ksi = Di / (Bi - Ai * ksi)
        temp_nu = (Fi + Ai * nu) / (Bi - Ai * ksi)
        ksi = temp_ksi
        nu = temp_nu
        '''print(ksi, nu)
        print()'''
        run_coefs.append([ksi, nu])
    '''for elem in run_coefs:
        print(elem)'''
    return run_coefs


def find_ci(run_coefs, canonic_table, c1, cn1):
    C = [0, cn1]     # CN+1 = 0
    c_last = cn1
    for i in range(len(canonic_table) - 1, 1, -1):
        Ai = canonic_table[i][0]
        Bi = canonic_table[i][1]
        Di = canonic_table[i][2]
        Fi = canonic_table[i][3]
        ksi = run_coefs[i][0]
        nu = run_coefs[i][1]
        c = Di * c_last / (Bi - Ai * ksi) + (Fi + Ai * nu) / (Bi - Ai * ksi)
        c_last = c
        C.append(c)
    C.append(c1)
    C = C[::-1]
    C = C[:-1]
    return C

def find_all_coefs(data, c_table):
    coefs = [[0, 0, 0, 0]]     # буферные данные
    for i in range(1, len(c_table)):
        yi = data[i][1]
        yi_1 = data[i - 1][1]
        hi = data[i][0] - data[i - 1][0]
        ci = c_table[i - 1]
        ci_next = c_table[i]

        ai = yi_1
        di = (ci_next - ci) / (3 * hi)
        bi = ((yi - yi_1) / hi) - (hi * (ci_next + 2 * ci) / 3)
        coefs.append([ai, bi, ci, di])
    '''yn = data[len(data) - 1][1]
    yn_1 = data[len(data) - 2][1]
    hn = data[len(data) - 1][0] - data[len(data) - 2][0]
    cn = c_table[len(c_table) - 1]
    an = yn_1
    bn = (yn - yn_1) / hn - 2 * hn * cn / 3
    dn = cn / (3 * hn)
    coefs.append([an, bn, cn, dn])'''
    '''for elem in coefs:
        print(elem)'''
    return coefs

def spline_prepare_data(coefs, x_left, x_right):
    pointsx = []
    pointsy = []
    a = coefs[0]
    b = coefs[1]
    c = coefs[2]
    d = coefs[3]
    step = (x_right - x_left) / 20
    x = x_left
    while x < x_right:
        y = a + b * (x - x_left) + c * (x - x_left) ** 2 + d * (x - x_left) ** 3
        pointsx.append(x)
        pointsy.append(y)
        x += step
    return pointsx, pointsy

def spline_prepare_plot(coefs_arr, intervals):
    graphx = []
    graphy = []
    for i in range(1, len(intervals)):
        pointsx, pointsy = spline_prepare_data(coefs_arr[i], intervals[i - 1], intervals[i])
        for elem in pointsx:
            graphx.append(elem)
        for elem in pointsy:
            graphy.append(elem)
    return graphx, graphy